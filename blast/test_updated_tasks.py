from __future__ import print_function

import importlib
import sys
import types
import unittest
import tempfile

from django.conf import settings


def install_test_stubs():
    if not settings.configured:
        settings.configure(
            USE_CACHE=False,
            ENABLE_JBROWSE_INTEGRATION=False,
            CACHES={
                'default': {
                    'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                },
            },
        )

    fake_models = types.ModuleType('blast.models')
    fake_models.BlastDb = type('BlastDb', (), {})
    fake_models.BlastQueryRecord = type('BlastQueryRecord', (), {})
    fake_models.JbrowseSetting = type('JbrowseSetting', (), {})
    fake_models.Sequence = type('Sequence', (), {})
    sys.modules['blast.models'] = fake_models

    if 'celery' not in sys.modules:
        fake_celery = types.ModuleType('celery')
        fake_celery.shared_task = lambda *args, **kwargs: (lambda func: func)
        sys.modules['celery'] = fake_celery

    fake_celery_decorators = types.ModuleType('celery.decorators')
    fake_celery_decorators.periodic_task = lambda *args, **kwargs: (lambda func: func)
    sys.modules['celery.decorators'] = fake_celery_decorators

    fake_celery_task_schedules = types.ModuleType('celery.task.schedules')
    fake_celery_task_schedules.crontab = lambda *args, **kwargs: ('crontab', args, kwargs)
    sys.modules['celery.task.schedules'] = fake_celery_task_schedules

    fake_celery_utils_log = types.ModuleType('celery.utils.log')

    class FakeLogger(object):
        def info(self, *args, **kwargs):
            return None

        def exception(self, *args, **kwargs):
            return None

    fake_celery_utils_log.get_task_logger = lambda *args, **kwargs: FakeLogger()
    sys.modules['celery.utils.log'] = fake_celery_utils_log

    fake_celery_signals = types.ModuleType('celery.signals')

    class FakeSignal(object):
        def connect(self, func):
            return func

    fake_celery_signals.task_failure = FakeSignal()
    fake_celery_signals.task_sent = FakeSignal()
    fake_celery_signals.task_success = FakeSignal()
    sys.modules['celery.signals'] = fake_celery_signals

    fake_celery_contrib = types.ModuleType('celery.contrib')
    fake_celery_contrib.rdb = object()
    sys.modules['celery.contrib'] = fake_celery_contrib


install_test_stubs()

updated_tasks = importlib.import_module('blast.updated_tasks')
legacy_tasks = importlib.import_module('blast.tasks')
build_match_feature = updated_tasks.build_match_feature
build_match_part_feature = updated_tasks.build_match_part_feature
split_matches_by_overlap = updated_tasks.split_matches_by_overlap


def make_hsp(**overrides):
    hsp = {
        'qseqid': 'query_1',
        'sseqid': 'subject_1',
        'evalue': 1e-20,
        'bitscore': 250.0,
        'qlen': 500,
        'qstart': 10,
        'qend': 60,
        'sstart': 100,
        'send': 150,
        'qstrand': '+',
        'sstrand': '+',
    }
    hsp.update(overrides)
    return hsp


class SplitMatchesByOverlapTestCase(unittest.TestCase):
    def test_keeps_contiguous_forward_hsps_in_one_match(self):
        grouped_hsps = [
            make_hsp(qstart=10, qend=60, sstart=100, send=150),
            make_hsp(qstart=64, qend=114, sstart=154, send=204),
        ]

        match_groups = split_matches_by_overlap(grouped_hsps, overlap_cutoff=5)

        self.assertEqual(len(match_groups), 1)
        self.assertEqual(match_groups[0], grouped_hsps)

    def test_keeps_forward_subject_reverse_query_hsps_in_one_match(self):
        grouped_hsps = [
            make_hsp(qstart=210, qend=160, sstart=100, send=150, qstrand='-', sstrand='+'),
            make_hsp(qstart=155, qend=105, sstart=154, send=204, qstrand='-', sstrand='+'),
        ]

        match_groups = split_matches_by_overlap(grouped_hsps, overlap_cutoff=5)

        self.assertEqual(len(match_groups), 1)
        self.assertEqual(match_groups[0], grouped_hsps)

    def test_splits_forward_hsps_when_overlap_exceeds_cutoff(self):
        grouped_hsps = [
            make_hsp(qstart=10, qend=60, sstart=100, send=150),
            make_hsp(qstart=50, qend=100, sstart=140, send=190),
        ]

        match_groups = split_matches_by_overlap(grouped_hsps, overlap_cutoff=5)

        self.assertEqual(len(match_groups), 2)
        self.assertEqual(match_groups[0], [grouped_hsps[0]])
        self.assertEqual(match_groups[1], [grouped_hsps[1]])

    def test_keeps_reverse_subject_forward_query_hsps_in_one_match(self):
        grouped_hsps = [
            make_hsp(qstart=200, qend=250, sstart=900, send=850, qstrand='+', sstrand='-'),
            make_hsp(qstart=145, qend=205, sstart=845, send=895, qstrand='+', sstrand='-'),
        ]

        match_groups = split_matches_by_overlap(grouped_hsps, overlap_cutoff=5)

        self.assertEqual(len(match_groups), 1)
        self.assertEqual(match_groups[0], grouped_hsps)

    def test_keeps_reverse_subject_reverse_query_hsps_in_one_match(self):
        grouped_hsps = [
            make_hsp(qstart=310, qend=250, sstart=900, send=840, qstrand='-', sstrand='-'),
            make_hsp(qstart=365, qend=305, sstart=965, send=905, qstrand='-', sstrand='-'),
        ]

        match_groups = split_matches_by_overlap(grouped_hsps, overlap_cutoff=5)

        self.assertEqual(len(match_groups), 1)
        self.assertEqual(match_groups[0], grouped_hsps)


class Gff3FeatureBuilderTestCase(unittest.TestCase):
    def test_build_match_feature_for_single_hsp_uses_evalue_score(self):
        match_hsps = [
            make_hsp(
                qseqid='query_alpha',
                evalue=1e-12,
                qstart=15,
                qend=85,
                sstart=1000,
                send=1070,
                qstrand='+',
                sstrand='+',
            ),
        ]

        feature = build_match_feature('chr1', 'blastx', match_hsps, match_id=7)

        self.assertEqual(feature['seqid'], 'chr1')
        self.assertEqual(feature['source'], 'blastx')
        self.assertEqual(feature['type'], 'match')
        self.assertEqual(feature['start'], '1000')
        self.assertEqual(feature['end'], '1070')
        self.assertEqual(feature['score'], str(1e-12))
        self.assertEqual(feature['strand'], '+')
        self.assertEqual(feature['phase'], '0')
        self.assertEqual(
            feature['attributes'],
            'ID=match00007;Name=query_alpha;Target=query_alpha 15 85 +'
        )

    def test_build_match_feature_for_multiple_hsps_uses_range_and_dot_score(self):
        match_hsps = [
            make_hsp(qseqid='query_beta', qstart=80, qend=30, sstart=500, send=450, qstrand='-', sstrand='-'),
            make_hsp(qseqid='query_beta', qstart=25, qend=5, sstart=440, send=390, qstrand='-', sstrand='-'),
        ]

        feature = build_match_feature('scaffold_9', 'tblastn', match_hsps, match_id=12)

        self.assertEqual(feature['start'], '450')
        self.assertEqual(feature['end'], '440')
        self.assertEqual(feature['score'], '.')
        self.assertEqual(feature['strand'], '-')
        self.assertEqual(
            feature['attributes'],
            'ID=match00012;Name=query_beta;Target=query_beta 5 80 -'
        )

    def test_build_match_part_feature_uses_parent_target_and_bitscore(self):
        match_part_hsp = make_hsp(
            qseqid='query_gamma',
            evalue=2.5e-30,
            bitscore=123.456789,
            qstart=90,
            qend=20,
            sstart=700,
            send=630,
            qstrand='-',
            sstrand='-',
        )

        feature = build_match_part_feature(
            'contig42',
            'blastn',
            match_part_hsp,
            match_id=3,
            match_part_id=8,
        )

        self.assertEqual(feature['seqid'], 'contig42')
        self.assertEqual(feature['source'], 'blastn')
        self.assertEqual(feature['type'], 'match_part')
        self.assertEqual(feature['start'], '630')
        self.assertEqual(feature['end'], '700')
        self.assertEqual(feature['score'], str(2.5e-30))
        self.assertEqual(feature['strand'], '-')
        self.assertEqual(feature['phase'], '0')
        self.assertEqual(
            feature['attributes'],
            'ID=match_part00008;Parent=match00003;Target=query_gamma 20 90 -;Bitscore=123.457'
        )


def build_legacy_gff_text(db_hsp_dict_list, blast_program, overlap_cutoff):
    gff_col_names = 'seqid source type start end score strand phase attributes'.split()
    output_lines = ['##gff-version 3']
    match_id = 1
    match_part_id = 1

    for key_db_hsp_dict_list in legacy_tasks._sorted_group_hsps(db_hsp_dict_list):
        seqid = legacy_tasks._parse_seqid_for_gff(key_db_hsp_dict_list[0]['sseqid'])
        gff_item = {'seqid': seqid, 'source': blast_program}
        matches_list = legacy_tasks._split_matches_by_overlap(key_db_hsp_dict_list, overlap_cutoff)
        for matches in matches_list:
            gff_item['type'] = 'match'
            gff_item['start'] = str(matches[0]['sstart'] if matches[0]['sstrand'] == '+' else matches[0]['send'])
            gff_item['end'] = str(matches[-1]['send'] if matches[0]['sstrand'] == '+' else matches[-1]['sstart'])
            gff_item['score'] = '.'
            gff_item['strand'] = matches[0]['sstrand']
            gff_item['phase'] = '0'
            gff_item['attributes'] = 'ID=match%05d;Name=%s;Target=%s %d %d %s' % (
                match_id,
                matches[0]['qseqid'],
                matches[0]['qseqid'],
                min(matches[0]['qstart'], matches[0]['qend'], matches[-1]['qstart'], matches[-1]['qend']),
                max(matches[0]['qstart'], matches[0]['qend'], matches[-1]['qstart'], matches[-1]['qend']),
                matches[0]['qstrand'],
            )
            if len(matches) == 1:
                gff_item['score'] = str(matches[0]['evalue'])
            output_lines.append('\t'.join([gff_item[col] for col in gff_col_names]))

            gff_item['type'] = 'match_part'
            for match_part in matches:
                gff_item['start'] = str(match_part['sstart'] if match_part['sstrand'] == '+' else match_part['send'])
                gff_item['end'] = str(match_part['send'] if match_part['sstrand'] == '+' else match_part['sstart'])
                gff_item['score'] = str(match_part['evalue'])
                gff_item['attributes'] = (
                    'ID=match_part%05d;Parent=match%05d;Target=%s %d %d %s;Bitscore=%g' % (
                        match_part_id,
                        match_id,
                        match_part['qseqid'],
                        min(match_part['qstart'], match_part['qend']),
                        max(match_part['qstart'], match_part['qend']),
                        match_part['qstrand'],
                        match_part['bitscore'],
                    )
                )
                output_lines.append('\t'.join([gff_item[col] for col in gff_col_names]))
                match_part_id += 1
            match_id += 1

    return '\n'.join(output_lines) + '\n'


class Gff3ParityWithLegacyTasksTestCase(unittest.TestCase):
    def test_generated_gff_matches_legacy_output(self):
        db_hsp_dict_list = [
            make_hsp(
                qseqid='queryA',
                sseqid='gnl|db|scaffold_1',
                qstart=10,
                qend=60,
                sstart=100,
                send=150,
                qstrand='+',
                sstrand='+',
                evalue=1e-20,
                bitscore=210.0,
            ),
            make_hsp(
                qseqid='queryA',
                sseqid='gnl|db|scaffold_1',
                qstart=64,
                qend=114,
                sstart=154,
                send=204,
                qstrand='+',
                sstrand='+',
                evalue=2e-20,
                bitscore=205.0,
            ),
            make_hsp(
                qseqid='queryA',
                sseqid='gnl|db|scaffold_1',
                qstart=90,
                qend=140,
                sstart=130,
                send=180,
                qstrand='+',
                sstrand='+',
                evalue=3e-20,
                bitscore=198.0,
            ),
            make_hsp(
                qseqid='queryB',
                sseqid='gnl|db|scaffold_2',
                qstart=220,
                qend=160,
                sstart=900,
                send=840,
                qstrand='-',
                sstrand='-',
                evalue=4e-30,
                bitscore=250.0,
            ),
            make_hsp(
                qseqid='queryB',
                sseqid='gnl|db|scaffold_2',
                qstart=280,
                qend=220,
                sstart=960,
                send=900,
                qstrand='-',
                sstrand='-',
                evalue=5e-30,
                bitscore=240.0,
            ),
        ]

        expected_text = build_legacy_gff_text(db_hsp_dict_list, 'blastn', overlap_cutoff=5)

        with tempfile.TemporaryDirectory() as tempdir:
            updated_tasks.write_gff3_for_database(
                'fixture_db',
                db_hsp_dict_list,
                tempdir,
                'blastn',
                overlap_cutoff=5,
            )
            output_path = tempdir + '/fixture_db.gff'
            with open(output_path, 'rt') as generated_file:
                generated_text = generated_file.read()

        self.assertEqual(generated_text, expected_text)