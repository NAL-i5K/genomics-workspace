from __future__ import absolute_import

"""Refactored BLAST task pipeline with explicit helper boundaries.

This module preserves the behavior of blast/tasks.py while making the data flow
easier to read and maintain.

Common data shapes used throughout the BLAST post-processing pipeline:

1. hsp_list
   A list of typed BLAST TSV rows. Each row is still a positional list whose
   column order matches blast_info['col_names'].

2. hsp_dict
   A normalized dictionary representation of one HSP row. Example shape:
   {
       'qseqid': 'query_1',
       'sseqid': 'gnl|db|scaffold_42',
       'evalue': 1e-20,
       'bitscore': 200.0,
       'qlen': 450,
       'qstart': 10,
       'qend': 220,
       'sstart': 5000,
       'send': 5210,
       'qstrand': '+',
       'sstrand': '+'
   }

3. database_hsp_dict_list
   The old tasks.py variable name db_hsp_dict_list refers to a list of HSP
   dictionaries that all belong to the same BLAST database title after the
   Sequence table lookup has mapped sseqid -> blast_db title.

4. grouped_hsps
   HSP dictionaries that share the same qseqid, sseqid, qstrand, and sstrand.
   These are the candidate subfeatures that may be merged into one GFF3 match.

5. match_hsps
   A contiguous subset of grouped_hsps that survived the overlap split logic and
   should be emitted as one GFF3 match feature with one or more match_part
   features beneath it.
"""

from celery import shared_task
from celery.decorators import periodic_task
from celery.signals import task_failure, task_sent, task_success
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger
from datetime import datetime, timedelta
from django.conf import settings
from django.core.cache import cache
from itertools import groupby
from os import path, stat
from pytz import utc
from shutil import rmtree
from subprocess import PIPE, Popen

from blast.models import BlastDb, BlastQueryRecord, JbrowseSetting, Sequence

import csv
import json
import time


logger = get_task_logger(__name__)

OVERLAP_CUTOFF = 5
GFF_VERSION_HEADER = '##gff-version 3\n'
GFF_COLUMN_NAMES = [
    'seqid',
    'source',
    'type',
    'start',
    'end',
    'score',
    'strand',
    'phase',
    'attributes',
]

if settings.USE_CACHE:
    LOCK_EXPIRE = 30
    LOCK_ID = 'task_list_cache_lock'
    CACHE_ID = 'task_list_cache'
    acquire_lock = lambda: cache.add(LOCK_ID, 'true', LOCK_EXPIRE)
    release_lock = lambda: cache.delete(LOCK_ID)


def update_task_status(status_file_path, status):
    """Update status.json so the frontend can continue polling progress."""
    with open(status_file_path, 'rt') as status_file:
        status_data = json.load(status_file)
        status_data['status'] = status

    with open(status_file_path, 'wt') as status_file:
        json.dump(status_data, status_file)


def update_database_record(task_id, **fields_to_update):
    """Persist selected fields on the BlastQueryRecord for this task."""
    record = BlastQueryRecord.objects.get(task_id__exact=task_id)
    for field_name, field_value in fields_to_update.items():
        setattr(record, field_name, field_value)
    record.save()
    return record


def execute_blast_commands(args_list):
    """Run the prepared BLAST and blast_formatter commands in order."""
    for args in args_list:
        Popen(args, stdin=PIPE, stdout=PIPE).wait()


def validate_blast_results(file_prefix):
    """Return the original status codes for missing or empty BLAST outputs."""
    asn_file = file_prefix + '.asn'
    tsv_file = file_prefix + '.tsv'

    if not path.isfile(asn_file):
        return 'NO_ASN'
    if stat(asn_file)[6] == 0:
        return 'ASN_EMPTY'
    if not path.isfile(tsv_file):
        return 'NO_TSV'
    if stat(tsv_file)[6] == 0:
        return 'TSV_EMPTY'
    return 'VALID'


def parse_report_file(report_path):
    """Collect line numbers in the BLAST text report that start with ' Score ='."""
    line_num_list = []
    target_string = ' Score ='

    with open(report_path, 'rt') as report_file:
        for line_num, line in enumerate(report_file):
            if line.startswith(target_string):
                line_num_list.append(line_num)

    return line_num_list


def parse_tsv_to_typed_list(tsv_path, blast_info):
    """Parse the BLAST TSV output using the column types from blast_info."""
    type_func = {'str': str, 'float': float, 'int': int}
    hsp_list = []

    with open(tsv_path, 'rt') as tsv_file:
        for row in csv.reader(tsv_file, delimiter='\t'):
            typed_row = [
                type_func[column_type](value)
                for column_type, value in zip(blast_info['col_types'], row)
            ]
            hsp_list.append(typed_row)

    return hsp_list


def build_column_index(blast_info):
    """Map each BLAST column name to its positional index in hsp_list rows."""
    return {column_name: index for index, column_name in enumerate(blast_info['col_names'])}


def determine_strand(start, end):
    """Return '+' when coordinates are ascending, otherwise '-' for reverse order."""
    return '-' if end < start else '+'


def build_hsp_dict(row, column_index):
    """Convert one typed HSP row into a named dictionary with explicit strands."""
    return {
        'qseqid': row[column_index['qseqid']],
        'sseqid': row[column_index['sseqid']],
        'evalue': row[column_index['evalue']],
        'bitscore': row[column_index['bitscore']],
        'qlen': row[column_index['qlen']],
        'qstart': row[column_index['qstart']],
        'qend': row[column_index['qend']],
        'sstart': row[column_index['sstart']],
        'send': row[column_index['send']],
        'qstrand': determine_strand(
            row[column_index['qstart']],
            row[column_index['qend']],
        ),
        'sstrand': determine_strand(
            row[column_index['sstart']],
            row[column_index['send']],
        ),
    }


def build_hsp_dict_list(hsp_list, blast_info):
    """Build the named HSP dictionaries used by later lookup and GFF3 steps."""
    column_index = build_column_index(blast_info)
    return [build_hsp_dict(row, column_index) for row in hsp_list]


def collect_subject_sequence_ids(hsp_dict_list):
    """Extract the distinct Sequence.id values referenced by the BLAST results."""
    return set(hsp_dict['sseqid'] for hsp_dict in hsp_dict_list)


def fetch_sequence_to_database_map(subject_sequence_ids):
    """Return a mapping of Sequence.id -> BlastDb.title.

    This is the Sequence table query the original code performed inline. It
    answers the question: given a BLAST subject sequence id, which BLAST
    database title does that sequence belong to?
    """
    return dict(
        Sequence.objects.select_related('blast_db')
        .filter(id__in=subject_sequence_ids)
        .values_list('id', 'blast_db__title')
    )


def fetch_database_to_organism_map(database_titles):
    """Return a mapping of BlastDb.title -> Organism.short_name."""
    return dict(
        BlastDb.objects.select_related('organism')
        .filter(title__in=database_titles)
        .values_list('title', 'organism__short_name')
    )


def fetch_database_to_jbrowse_url_map(database_titles):
    """Return the JBrowse link-out mapping used by the BLAST results page.

    When JBrowse integration is disabled, the original tasks.py code stored an
    empty list in info.json instead of an empty object. This helper preserves
    that behavior so downstream consumers see the same payload shape.
    """
    if not settings.ENABLE_JBROWSE_INTEGRATION:
        return []

    return dict(
        JbrowseSetting.objects.select_related('blast_db')
        .filter(blast_db__title__in=database_titles)
        .values_list('blast_db__title', 'url')
    )


def fetch_database_lookups(hsp_dict_list):
    """Run the database lookup phase used by info.json, results JSON, and GFF3.

    Returns a tuple of:
    - sseqid_db: Sequence.id -> BlastDb.title
    - db_organism: BlastDb.title -> organism short name
    - db_url: BlastDb.title -> JBrowse URL, or [] when disabled
    """
    subject_sequence_ids = collect_subject_sequence_ids(hsp_dict_list)
    sseqid_db = fetch_sequence_to_database_map(subject_sequence_ids)
    database_titles = set(sseqid_db.values())
    db_organism = fetch_database_to_organism_map(database_titles)
    db_url = fetch_database_to_jbrowse_url_map(database_titles)
    return sseqid_db, db_organism, db_url


def write_info_json(basedir, sseqid_db, db_organism, db_url, line_num_list):
    """Persist the metadata payload consumed by the BLAST results frontend."""
    info_path = path.join(basedir, 'info.json')
    info_data = {
        'sseqid_db': sseqid_db,
        'db_organism': db_organism,
        'db_url': db_url,
        'line_num_list': line_num_list,
    }
    with open(info_path, 'wt') as info_file:
        json.dump(info_data, info_file)


def build_results_json_rows(hsp_list, hsp_dict_list, sseqid_db):
    """Prefix each TSV row with its BLAST database title for the results table."""
    return [
        [sseqid_db[hsp_dict['sseqid']]] + hsp_row
        for hsp_row, hsp_dict in zip(hsp_list, hsp_dict_list)
    ]


def write_results_json(json_path, hsp_list, hsp_dict_list, sseqid_db):
    """Write the JSON array used by blast/results.html."""
    with open(json_path, 'wt') as json_file:
        json.dump(build_results_json_rows(hsp_list, hsp_dict_list, sseqid_db), json_file)


def hsp_group_key(hsp_dict):
    """Return the legacy grouping key used by the original tasks.py implementation."""
    return ''.join([
        hsp_dict['qseqid'],
        hsp_dict['sseqid'],
        hsp_dict['qstrand'],
        hsp_dict['sstrand'],
    ])


def sort_hsps_within_group(grouped_hsps):
    """Sort one grouped HSP list by subject coordinates in strand-aware order."""
    return sorted(
        grouped_hsps,
        key=lambda hsp_dict: (
            (hsp_dict['sstart'], hsp_dict['send'])
            if hsp_dict['sstrand'] == '+'
            else (hsp_dict['send'], hsp_dict['sstart'])
        ),
    )


def iter_sorted_hsp_groups(database_hsp_dict_list):
    """Yield grouped, subject-sorted HSPs for one database.

    The older name db_hsp_dict_list was unclear. It is simply "all HSP dicts for
    one BLAST database" after filtering by sseqid_db.
    """
    sorted_database_hsps = sorted(database_hsp_dict_list, key=hsp_group_key)
    for _, grouped_hsps in groupby(sorted_database_hsps, key=hsp_group_key):
        yield sort_hsps_within_group(list(grouped_hsps))


def parse_seqid_for_gff(original_seqid):
    """Apply the existing i5k-specific seqid normalization for GFF3 output."""
    seqid_tokens = original_seqid.split('|')
    if len(seqid_tokens) < 2 or original_seqid.startswith('gi|'):
        return original_seqid
    if original_seqid.startswith('gnl'):
        return seqid_tokens[-1].split('_', 1)[-1]
    return seqid_tokens[1]


def cut_compare_and_next_pos(hsp_dict):
    """Compute overlap comparison coordinates and next cursor positions.

    The return value is:
    - compare_s: subject coordinate used to test overlap with the previous HSP
    - compare_q: query coordinate used to test overlap with the previous HSP
    - next_s: subject cursor to remember after accepting this HSP
    - next_q: query cursor to remember after accepting this HSP
    """
    if hsp_dict['sstrand'] == '+':
        if hsp_dict['qstrand'] == '+':
            return hsp_dict['sstart'], hsp_dict['qstart'], hsp_dict['send'], hsp_dict['qend']
        return (
            hsp_dict['sstart'],
            hsp_dict['qlen'] - hsp_dict['qstart'],
            hsp_dict['send'],
            hsp_dict['qlen'] - hsp_dict['qend'],
        )

    if hsp_dict['qstrand'] == '+':
        return (
            hsp_dict['send'],
            hsp_dict['qlen'] - hsp_dict['qend'],
            hsp_dict['sstart'],
            hsp_dict['qlen'] - hsp_dict['qstart'],
        )

    return hsp_dict['send'], hsp_dict['qend'], hsp_dict['sstart'], hsp_dict['qstart']


def split_matches_by_overlap(grouped_hsps, overlap_cutoff):
    """Split one grouped HSP list into one or more GFF3 match feature groups.

    Each output list represents the match_part subfeatures that should be merged
    into a single parent match feature.
    """
    subject_cursor = 0
    query_cursor = 0
    current_match_hsps = []
    match_groups = []

    for hsp_dict in grouped_hsps:
        compare_s, compare_q, next_s, next_q = cut_compare_and_next_pos(hsp_dict)
        should_cut = (
            subject_cursor - compare_s > overlap_cutoff or
            query_cursor - compare_q > overlap_cutoff
        )
        if should_cut:
            match_groups.append(current_match_hsps)
            current_match_hsps = []

        current_match_hsps.append(hsp_dict)
        subject_cursor, query_cursor = next_s, next_q

    match_groups.append(current_match_hsps)
    return match_groups


def build_match_feature(seqid, blast_program, match_hsps, match_id):
    """Build the parent GFF3 match feature for one merged set of HSPs."""
    first_hsp = match_hsps[0]
    last_hsp = match_hsps[-1]
    target_start = min(
        first_hsp['qstart'],
        first_hsp['qend'],
        last_hsp['qstart'],
        last_hsp['qend'],
    )
    target_end = max(
        first_hsp['qstart'],
        first_hsp['qend'],
        last_hsp['qstart'],
        last_hsp['qend'],
    )

    feature = {
        'seqid': seqid,
        'source': blast_program,
        'type': 'match',
        'start': str(first_hsp['sstart'] if first_hsp['sstrand'] == '+' else first_hsp['send']),
        'end': str(last_hsp['send'] if first_hsp['sstrand'] == '+' else last_hsp['sstart']),
        'score': '.',
        'strand': first_hsp['sstrand'],
        'phase': '0',
        'attributes': (
            'ID=match%05d;Name=%s;Target=%s %d %d %s' % (
                match_id,
                first_hsp['qseqid'],
                first_hsp['qseqid'],
                target_start,
                target_end,
                first_hsp['qstrand'],
            )
        ),
    }
    if len(match_hsps) == 1:
        feature['score'] = str(first_hsp['evalue'])
    return feature


def build_match_part_feature(seqid, blast_program, match_part_hsp, match_id, match_part_id):
    """Build one GFF3 match_part feature from a single HSP dictionary."""
    return {
        'seqid': seqid,
        'source': blast_program,
        'type': 'match_part',
        'start': str(match_part_hsp['sstart'] if match_part_hsp['sstrand'] == '+' else match_part_hsp['send']),
        'end': str(match_part_hsp['send'] if match_part_hsp['sstrand'] == '+' else match_part_hsp['sstart']),
        'score': str(match_part_hsp['evalue']),
        'strand': match_part_hsp['sstrand'],
        'phase': '0',
        'attributes': (
            'ID=match_part%05d;Parent=match%05d;Target=%s %d %d %s;Bitscore=%g' % (
                match_part_id,
                match_id,
                match_part_hsp['qseqid'],
                min(match_part_hsp['qstart'], match_part_hsp['qend']),
                max(match_part_hsp['qstart'], match_part_hsp['qend']),
                match_part_hsp['qstrand'],
                match_part_hsp['bitscore'],
            )
        ),
    }


def write_gff3_feature(gff_handle, feature):
    """Write one GFF3 feature dictionary in canonical column order."""
    gff_handle.write('\t'.join(feature[column_name] for column_name in GFF_COLUMN_NAMES) + '\n')


def write_gff3_for_database(database_name, database_hsp_dict_list, basedir, blast_program, overlap_cutoff):
    """Write one <database>.gff file for the HSPs belonging to that database."""
    gff_path = path.join(basedir, database_name + '.gff')
    match_id = 1
    match_part_id = 1

    with open(gff_path, 'wt') as gff_handle:
        gff_handle.write(GFF_VERSION_HEADER)

        for grouped_hsps in iter_sorted_hsp_groups(database_hsp_dict_list):
            seqid = parse_seqid_for_gff(grouped_hsps[0]['sseqid'])
            match_groups = split_matches_by_overlap(grouped_hsps, overlap_cutoff)

            for match_hsps in match_groups:
                write_gff3_feature(
                    gff_handle,
                    build_match_feature(seqid, blast_program, match_hsps, match_id),
                )

                for match_part_hsp in match_hsps:
                    write_gff3_feature(
                        gff_handle,
                        build_match_part_feature(
                            seqid,
                            blast_program,
                            match_part_hsp,
                            match_id,
                            match_part_id,
                        ),
                    )
                    match_part_id += 1

                match_id += 1


def generate_gff3_files(hsp_dict_list, sseqid_db, db_url, basedir, blast_program, overlap_cutoff):
    """Generate all database-specific GFF3 files for databases with JBrowse URLs."""
    eligible_hsps = sorted(
        [
            hsp_dict
            for hsp_dict in hsp_dict_list
            if sseqid_db[hsp_dict['sseqid']] in db_url
        ],
        key=lambda hsp_dict: sseqid_db[hsp_dict['sseqid']],
    )

    for database_name, grouped_database_hsps in groupby(
        eligible_hsps,
        key=lambda hsp_dict: sseqid_db[hsp_dict['sseqid']],
    ):
        write_gff3_for_database(
            database_name,
            list(grouped_database_hsps),
            basedir,
            blast_program,
            overlap_cutoff,
        )


@shared_task()
def run_blast_task(task_id, args_list, file_prefix, blast_info):
    """Run BLAST, parse its outputs, and write JSON plus optional GFF3 files."""
    import django
    django.setup()

    logger.info('blast_task_id: %s' % (task_id,))

    status_file_path = path.join(path.dirname(file_prefix), 'status.json')
    tsv_path = file_prefix + '.tsv'
    json_path = file_prefix + '.json'
    report_path = file_prefix + '.0'
    basedir = path.dirname(tsv_path)

    update_database_record(
        task_id,
        dequeue_date=datetime.utcnow().replace(tzinfo=utc),
    )
    update_task_status(status_file_path, 'running')

    execute_blast_commands(args_list)

    result_status = validate_blast_results(file_prefix)
    if result_status == 'VALID':
        try:
            line_num_list = parse_report_file(report_path)
            hsp_list = parse_tsv_to_typed_list(tsv_path, blast_info)
            hsp_dict_list = build_hsp_dict_list(hsp_list, blast_info)

            sseqid_db, db_organism, db_url = fetch_database_lookups(hsp_dict_list)
            write_info_json(basedir, sseqid_db, db_organism, db_url, line_num_list)
            write_results_json(json_path, hsp_list, hsp_dict_list, sseqid_db)

            blast_program = path.basename(args_list[0][0])
            generate_gff3_files(
                hsp_dict_list,
                sseqid_db,
                db_url,
                basedir,
                blast_program,
                OVERLAP_CUTOFF,
            )
            result_status = 'SUCCESS'
        except Exception:
            logger.exception('Failed to generate GFF3 or JSON output for task %s', task_id)
            result_status = 'NO_GFF'

    update_database_record(
        task_id,
        result_status=result_status,
        result_date=datetime.utcnow().replace(tzinfo=utc),
    )
    update_task_status(status_file_path, 'done')

    return task_id


@periodic_task(run_every=(crontab(hour='0', minute='10')))
def remove_files():
    """Delete BLAST task output directories older than seven days."""
    logger.info('removing expired files (under test, not working actually)')
    expiry_cutoff = datetime.utcnow().replace(tzinfo=utc) + timedelta(days=-7)
    for expired_task in BlastQueryRecord.objects.filter(result_date__lt=expiry_cutoff):
        task_path = path.join(settings.MEDIA_ROOT, 'blast', 'task', expired_task.task_id)
        if path.exists(task_path):
            rmtree(task_path)
            logger.info('removed directory %s' % (task_path))


@task_sent.connect
def task_sent_handler(sender=None, task_id=None, task=None, args=None, kwargs=None, **kwds):
    """Track queued tasks in cache when queue tracking is enabled."""
    if settings.USE_CACHE:
        while not acquire_lock():
            time.sleep(0.1)
        try:
            task_list = cache.get(CACHE_ID, [])
            if args:
                blast_task_id = args[0]
                task_list.append((task_id, blast_task_id))
                logger.info('[task_sent] task sent: %s. queue length: %s' % (blast_task_id, len(task_list)))
                cache.set(CACHE_ID, task_list)
            else:
                logger.info('[task_sent] no args. rabbit task_id: %s' % (task_id))
        finally:
            release_lock()
    else:
        logger.info('[task_sent] task sent. rabbit task_id: %s' % (task_id))


@task_success.connect
def task_success_handler(sender=None, result=None, **kwds):
    """Remove completed tasks from the cached queue list."""
    if settings.USE_CACHE:
        while not acquire_lock():
            time.sleep(0.1)
        try:
            blast_task_id = result
            task_list = cache.get(CACHE_ID, [])
            if task_list and blast_task_id:
                for queued_task in task_list:
                    if blast_task_id in queued_task:
                        task_list.remove(queued_task)
                        logger.info('[task_success] task removed from queue: %s' % (blast_task_id))
                        break
                logger.info('[task_success] task done: %s. queue length: %s' % (blast_task_id, len(task_list)))
                cache.set(CACHE_ID, task_list)
            else:
                logger.info('[task_success] no queue list or blast task id.')
        finally:
            release_lock()
    else:
        logger.info('[task_success] task done. rabbit task_id: %s.' % (result))


@task_failure.connect
def task_failure_handler(sender=None, task_id=None, exception=None,
                         args=None, kwargs=None, traceback=None, einfo=None, **kwds):
    """Mirror the original queue cleanup behavior when a task fails."""
    logger.info('[task_failure] task failed. rabbit task_id: %s' % (task_id))
    if settings.USE_CACHE:
        task_success_handler(sender, task_id)