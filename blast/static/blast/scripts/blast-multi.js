/// <reference path="../../../templates/blast/main.html" />
/////////////////////
// DATA PROCESSING //
/////////////////////
// Sort dataset_list by organism
function preprocess(dataset_list) {
    var dataset_dict = {};
    var organism_list = [];
    var alphabet_list = [];
    var dataset_list_count = dataset_list.length;
    for (var i = 0; i < dataset_list_count; i++) {
        var entry = dataset_list[i];
        var data_type = entry[0];
        var alphabet = entry[1];
        var file_name = entry[2];
        var organism_name = entry[3];
        var description = entry[4];
        if (!(organism_name in dataset_dict)) {
            dataset_dict[organism_name] = {};
            organism_list.push(organism_name);
            //console.log(organism_name);
        }
        if (!(alphabet in dataset_dict[organism_name])) {
            dataset_dict[organism_name][alphabet] = [];
        }
        if ($.inArray(alphabet, alphabet_list) < 0) {
            alphabet_list.push(alphabet);
        }
        dataset_dict[organism_name][alphabet].push([file_name, data_type, description]); // add info
    }
    return [dataset_dict, organism_list, alphabet_list];
}

[dataset_dict, organism_list, alphabet_list] = preprocess(dataset_list);

// for IE6,7,8
if (!Array.prototype.indexOf) {
  Array.prototype.indexOf = function (obj, fromIndex) {
    if (fromIndex == null) {
        fromIndex = 0;
    } else if (fromIndex < 0) {
        fromIndex = Math.max(0, this.length + fromIndex);
    }
    for (var i = fromIndex, j = this.length; i < j; i++) {
        if (this[i] === obj)
            return i;
    }
    return -1;
  };
}
$(function() { // document ready
	///////////////////////////////
	// HTML STRUCTURE GENERATION //
	///////////////////////////////

	var organism_list_count = organism_list.length;
	var alphabet_list_count = alphabet_list.length;
	for (var i = 0; i < organism_list_count; i++) {
		var organism_id = organism_list[i].toLowerCase().replace(' ', '-');
		// organism-checkbox
		var $organism_checkbox = $('<input>', {
			'organism': organism_id,
                        'id': organism_id,
			'type': 'checkbox',
			'class': 'organism-checkbox ' + organism_id,
                        'name': 'organism-checkbox[]',
		});
		var $organism_div = $('<div/>', {
			'organism': organism_id,
			'class': 'organism-div italic',
		}).append($organism_checkbox).append(organism_list[i]);
		$('<label/>').append($organism_div).appendTo('#box-organism');
		var $organism_datasets_div = $('<div/>', {
			'class': organism_id + ' datasets-div',
			'style': 'display: none',
		}).appendTo('#box-datasets');
		$('<div class="dataset-title">' + organism_list[i] + '</div>').appendTo($organism_datasets_div);
		for (var j = 0; j < alphabet_list_count; j++) {
			if (alphabet_list[j] in dataset_dict[organism_list[i]]) {
				var alphabet_class = alphabet_list[j].toLowerCase();
				var alphabet_fieldset_id = organism_id + '-' + alphabet_class + '-fieldset'
				var $alphabet_fieldset = $('<fieldset class="' + alphabet_class + '"><legend>' + alphabet_list[j] + '</legend></fieldset>').appendTo($organism_datasets_div);
				var entry_count = dataset_dict[organism_list[i]][alphabet_list[j]].length;
				for (var k = 0; k < entry_count; k++) {
					var file_name = dataset_dict[organism_list[i]][alphabet_list[j]][k][0];
					var data_type = dataset_dict[organism_list[i]][alphabet_list[j]][k][1];
					var description = dataset_dict[organism_list[i]][alphabet_list[j]][k][2];
					var data_type_class = data_type.toLowerCase().replace(' ', '-');
					// dataset checkbox
					var $organism_datasets_checkbox = $('<input>', {
						'type': 'checkbox',
						'name': 'db-name',
						'value': file_name,
            'id': file_name,
						'organism': organism_id,
						'dataset-type': data_type_class,
						'class': 'dataset-checkbox ' + organism_id + ' ' + data_type_class + ' ' + alphabet_class,
					});
					var $organism_datasets_checkbox_div = $('<div/>').append($organism_datasets_checkbox).append(data_type + ' - ' + description);
					var $organism_datasets_label = $('<label/>').append($organism_datasets_checkbox_div);
					$alphabet_fieldset.append($organism_datasets_label);
				}
			}
		}
	}

  hist_checkbox = $("#hist_checkbox").val();
  hist_check_array = hist_checkbox.split(',');
  for(var i = 0; i < hist_check_array.length; i++) {
      c = '#' + hist_check_array[i].split(".")[0]
      $(c).prop("checked", true);
      $('#'+$(c).attr('organism')).prop("checked", true);
  };

	////////////////////
	// EVENT HANDLING //
  ////////////////////

	var default_data_type = $('.all-dataset-checkbox').attr('dataset-type') || 'genome-assembly';
	$('.organism-div').hoverIntent(function() {
		// show and hide right panel
		$('.datasets-div').hide();
		$('.' + $(this).attr('organism') + '.datasets-div').show();
		// background toggle
		$('.organism-div').removeClass('organism-active-background');
		$(this).addClass('organism-active-background');
		//console.log('.' + $(this).attr('organism') + '.datasets-div');
	});
	$('.organism-checkbox').change(function(e) {
		if ($(this).is(':checked')) {
			$('.dataset-checkbox.' + $(this).attr('organism') + '.' + default_data_type).prop('checked', true).change();
			//console.log('.datasets-checkbox.' + $(this).attr('organism') + '.' + default_data_type);
		} else {
			// uncheck all dataset checkboxes of the organism
			$('.dataset-checkbox.' + $(this).attr('organism')).prop('checked', false).change();
		}
	});
	$('.dataset-checkbox').change(function() {
		if ($(this).is(':checked')) {
			// check organism checkbox
			$('.organism-checkbox.' + $(this).attr('organism')).prop('checked', true);
			default_data_type = $(this).attr('dataset-type');
		} else {
			//console.log($('.dataset-checkbox.' + $(this).attr('organism')).is(':checked'));
			// if none of the dataset checkboxes are checked
			if (!$('.dataset-checkbox.' + $(this).attr('organism')).is(':checked')) {
				// uncheck the organism checkbox
				$('.organism-checkbox.' + $(this).attr('organism')).prop('checked', false);
			}
		}
		setDatabaseType();
	});
	$('.all-organism-checkbox').change(function() {
		if ($(this).is(':checked')) {
			$('.all-dataset-checkbox.' + default_data_type).prop('checked', true);
			// check all dataset checkboxes with the dataset type
			$('.dataset-checkbox.' + default_data_type).prop('checked', true).change();
		} else {
			// uncheck all dataset checkboxes of the organism
			$('.all-dataset-checkbox').prop('checked', false).change();
		}
	});
	$('.all-dataset-checkbox').change(function() {
		if ($(this).is(':checked')) {
			// check organism checkbox
			$('.all-organism-checkbox').prop('checked', true);
			// check all dataset checkboxes with the dataset type
			$('.dataset-checkbox.' + $(this).attr('dataset-type')).prop('checked', true).change();
		} else {
			// uncheck all dataset checkboxes with the dataset type
			$('.dataset-checkbox.' + $(this).attr('dataset-type')).prop('checked', false).change();
			// if none of the dataset checkboxes are checked
			if (!$('.all-dataset-checkbox').is(':checked')) {
				// uncheck the organism checkbox
				$('.all-organism-checkbox').prop('checked', false);
			}
		}
	});

	var db_type = '';
	function setDatabaseType() {
		if (db_type == '') {
			// check what has been checked
			if ($('.nucleotide').is(':checked')) {
				db_type = 'nucleotide';
				$('.peptide').prop('disabled', true).addClass('disabled-fieldset');
			} else if ($('.peptide').is(':checked')) {
				db_type = 'peptide';
				$('.nucleotide').prop('disabled', true).addClass('disabled-fieldset');
			}
		} else {
			if (!$('.dataset-checkbox').is(':checked')) {
				db_type = '';
        $('.peptide').prop('disabled', false).removeClass('disabled-fieldset');
        $('.nucleotide').prop('disabled', false).removeClass('disabled-fieldset');
			}
		}
		chooseProgram();
	}

	var query_type = '';
	function setQueryType(qtype) {
		query_type = qtype;
		if (qtype == '') {
			$('.enter-query-text').html('Enter sequence below in <a href="docs/fasta.html">FASTA</a> format:');
		} else if (qtype == 'invalid') {
			$('.enter-query-text').html('Your sequence is invalid:');
		} else if (qtype == 'nucleotide') {
			$('.enter-query-text').html('Your sequence is detected as nucleotide:');
		} else if (qtype == 'peptide') {
			$('.enter-query-text').html('Your sequence is detected as peptide:');
		}
		chooseProgram();
	}


  function disableProgram(){
		$('.program').prop('disabled', false).removeClass('disabled-radio');
		if (db_type == 'nucleotide') {
			$('.blastp').prop('disabled', true).addClass('disabled-radio');
      $('.blastx').prop('disabled', true).addClass('disabled-radio');
		} else if (db_type == 'peptide') {
			$('.blastn').prop('disabled', true).addClass('disabled-radio');
      $('.tblastn').prop('disabled', true).addClass('disabled-radio');
      $('.tblastx').prop('disabled', true).addClass('disabled-radio');
		}
		if (query_type == 'nucleotide') {
			$('.blastp').prop('disabled', true).addClass('disabled-radio');
      $('.tblastn').prop('disabled', true).addClass('disabled-radio');
		} else if (query_type == 'peptide') {
			$('.blastn').prop('disabled', true).addClass('disabled-radio');
      $('.blastx').prop('disabled', true).addClass('disabled-radio');
      $('.tblastx').prop('disabled', true).addClass('disabled-radio');
		}
  }

	var program_selected = 'blastn';
	var chooseProgram = _.debounce(function () {
    disableProgram();
		query_type = '';
		// select first non disabled option
		$('input.program:not([disabled])').first().prop('checked', true);
		program_selected = $('input.program:not([disabled])').first().val();
		$('.' + program_selected).mouseover();
        add_blast_options(program_selected.toUpperCase());
    }, 30);


    //Reset all element if reload of previous page when back button is pressed
    if ($('#click_submit_hidden').val() == 'true') {
        $('#click_submit_hidden').val('false');
        $('#query-textarea').val('');
        $(".query-file").replaceWith('<input type="file" name="query-file" class="query-file">');
        $('.all-organism-checkbox').prop("checked", false);
        $('.all-organism-checkbox').change();
        $('.program').prop('disabled', false).removeClass('disabled-radio');
        chooseProgram();
    }

    function sum(obj) {
        var sum = 0;
        for(var el in obj) {
            if(obj.hasOwnProperty(el)) {
                sum += parseFloat(obj[el]);
            }
        }
        return sum;
    }

    function filter_key(obj, test) {
        var result = {}, key;
        for (key in obj) {
            if (obj.hasOwnProperty(key) && test(key)) {
                result[key] = obj[key];
            }
        }
        return result;
    }

    var parseTextarea = _.debounce(function () {
        // parse only the first 100 chars for speed
        //console.log($('#query-textarea').val());
        var lines = $('#query-textarea').val().substring(0, 1000).match(/[^\r\n]+/g);
        if (lines == null) {
            setQueryType('');
            return;
        }
        var line_count = lines.length;
        var seq_count = 0;
        var alphabets = {};
        // http://www.ncbi.nlm.nih.gov/BLAST/blastcgihelp.shtml
        var normal_nucleic_codes = 'ATCGN';
        var valid_amino_codes = 'ABCDEFGHIKLMNPQRSTUVWXYZ*';
        var amino_only_codes = 'EFILPQZX*';
        for (var i = 0; i < line_count; i++) {
            //console.log(i + ' ' + lines[i]);
            var line = $.trim(lines[i]).toUpperCase();
            if (line[0] == '>') {
                seq_count++;
            } else {
                // check_alphabet(line);
                for (var j = 0; j < line.length; j++) {
                    if (!(line[j] in alphabets)) {
                        alphabets[line[j]] = 1;
                    } else {
                        alphabets[line[j]]++;
                    }
                }
            }
        }
        //console.log(alphabets);
        var valid_amino_count = sum(filter_key(alphabets, function (key) {
            return valid_amino_codes.indexOf(key) != -1;
        }));
        var amino_only_count = sum(filter_key(alphabets, function (key) {
            return amino_only_codes.indexOf(key) != -1;
        }));
        var normal_nucleic_count = sum(filter_key(alphabets, function (key) {
            return normal_nucleic_codes.indexOf(key) != -1;
        }));
        var total_count = sum(alphabets);
        // Too many degenerate codes within an input nucleotide query will cause blast.cgi to
        // reject the input. For protein queries, too many nucleotide-like code (A,C,G,T,N) may also
        // cause similar rejection.
        if (total_count == 0) {
            setQueryType('');
        } else if ((normal_nucleic_count / total_count) > 0.6 && amino_only_count == 0) {
            setQueryType('nucleotide');
        } else if (valid_amino_count == total_count) {
            setQueryType('peptide');
        } else {
            setQueryType('invalid');
        }
        //console.log(query_type, normal_nucleic_count, total_count);
    }, 30);
    $('#query-textarea').keyup(parseTextarea);

     // blast program descriptions for labels and their radio buttons
    $('.blastn').mouseover(function() {
        $('#blastProgramDescription').text('blastn - Nucleotide vs. Nucleotide');
    });
    $('.tblastn').mouseover(function() {
        $('#blastProgramDescription').text('tblastn - Peptide vs. Translated Nucleotide');
    });
    $('.tblastx').mouseover(function() {
        $('#blastProgramDescription').text('tblastx - Translated Nucleotide vs. Translated Nucleotide');
    });
    $('.blastp').mouseover(function() {
        $('#blastProgramDescription').text('blastp - Peptide vs. Peptide');
    });
    $('.blastx').mouseover(function() {
        $('#blastProgramDescription').text('blastx - Translated Nucleotide vs. Peptide');
    });
    $('#fieldset-program').mouseleave(function() {
        $('.' + $('input.program:checked').val()).mouseover();
    });

    // example sequences for testing
    var ex_nucleotide = ">CLEC010822-RA:cDNA , Heat shock protein 70-2\n" +
                        "TGGAAATTTAAATATTTTCGATTTGGCGCGCCTTTAAGCCGGCGCCC" +
                        "AATCGCGTTTCGGAACGTATTGTCAGTCAGCCGGACCAATCAACGCC" +
                        "GTCCACGATTCCCGACTTCTCCCCGTCACCCAACCCCATTCTTATTC" +
                        "CACAGCCGCGGCCGTTCGTCCGTTCAGTCGAACCTAGGACTTGATTC" +
                        "GAGTACAAAGCGGACGAAAAAACGCGAATTAAACATAGTGTCTTATT" +
                        "CTTAATTTTGATCTAGTTGAAAACAAAAAAAGAGAGAAGGGTATATT" +
                        "TTTTTATATTTTCGAGTCAGTTGTATCAAAAATCAAACCGGAATAAT" +
                        "TCAGAGATTTTCACAATAATGATTTTACATTTTCTCGTTTTGCTTTT" +
                        "CGCTTCGGCCTTAGCAGCCGACGAGAAGAATAAGGACGTCGGAACCG" +
                        "TCGTGGGCATTGACCTCGGCACGACTTACTCTTGTGTGGGAGTGTAC" +
                        "AAGAATGGAAGAGTTGAAATCATCGCCAACGATCAAGGAAACAGGAT" +
                        "TACACCTTCATACGTCGCTTTCACCAGTGAAGGCGAGCGTCTTATCG" +
                        "GAGATGCCGCCAAGAATCAGTTGACGACCAACCCTGAAAACACCGTC" +
                        "TTCGACGCTAAGCGTCTTATCGGACGAGAATGGACGGACAGCACTGT" +
                        "TCAAGACGATATCAAGTTCTTCCCATTCAAAGTCTTGGAGAAAAATA" +
                        "GCAAGCCTCACATTCAAGTCTCCACGTCCCAGGGCAACAAAATGTTC" +
                        "GCACCCGAAGAAATCTCCGCTATGGTATTGGGTAAAATGAAAGAGAC" +
                        "GGCAGAGGCATATTTGGGAAAGAAGGTCACCCACGCCGTAGTCACAG" +
                        "TACCCGCATACTTCAACGATGCCCAGAGGCAGGCAACAAAAGATGCT" +
                        "GGAACGATTTCAGGACTCAACGTCATGAGGATCATCAACGAACCGAC" +
                        "CGCAGCAGCTATTGCTTACGGACTGGACAAGAAAGAAGGAGAAAAGA" +
                        "ACGTACTCGTTTTTGATCTCGGCGGTGGTACTTTTGATGTATCTCTT" +
                        "CTCACCATCGACAACGGAGTTTTCGAAGTCGTTTCTACAAACGGTGA" +
                        "TACTCACTTAGGAGGAGAGGACTTTGATCAAAGGGTTATGGACCACT" +
                        "TTATTAAACTGTACAAGAAGAAGAAGGGCAAGGATATCAGGAAAGAC" +
                        "AACAGGGCTGTTCAGAAACTCAGGAGGGAAGTCGAAAAAGCAAAGAG" +
                        "GGCTCTGTCTTCTAGCCACCAGGTCAGGATAGAAATTGAAAGCTTCT" +
                        "ATGACGGTGAAGACTTCTCTGAGACTCTCACTAGGGCAAAATTCGAA" +
                        "GAGCTCAACATGGACCTCTTCCGTTCCACCATGAAACCCGTTCAGAA" +
                        "GGTCCTCGAAGATGCTGACATGAACAAGAAAGACGTCGATGAAATTG" +
                        "TTTTAGTAGGAGGCAGCACCAGGATTCCAAAAGTTCAGGCCCTCGTC" +
                        "AAAGAGTTTTTCAACGGAAAAGAACCATCCCGAGGTATCAACCCCGA" +
                        "TGAAGCTGTCGCTTATGGAGCAGCAGTTCAAGCTGGAGTTTTATCTG" +
                        "GTGAACAAGACACCGATTCAATCGTCCTCCTTGATGTCAACCCTCTG" +
                        "ACCCTCGGAATCGAAACAGTCGGTGGTGTCATGACCAAACTCATCCC" +
                        "AAGGAACACAGTCATCCCGACGAAAAAATCTCAGATCTTCTCGACAG" +
                        "CTTCAGACAACCAACACACTGTCACCATTCAGGTTTATGAGGGAGAA" +
                        "AGGCCAATGACCAAAGATAATCATTTGCTCGGAAAATTCGATTTGAC" +
                        "AGGAATACCGCCTGCACCAAGGGGAGTGCCACAGATTGAAGTCACTT" +
                        "TTGAGATCGATGCCAACGGTATCCTTCAGGTGTCCGCCGAGGACAAG" +
                        "GGAACGGGCAACAGAGAGAAAATAGTCATCACAAACGACCAGAACAG" +
                        "GTTGACTCCAGACGACATCGATAGGATGATCAAGGACGCCGAGAAGT" +
                        "TCGCTGATGACGACAAGAAGCTCAAGGAGCGCGTCGAGGCCAGGAAC" +
                        "GAACTGGAGTCGTACGCCTATTCTCTCAAGAACCAGCTCGCCGACAA" +
                        "GGACAAGTTCGGATCGAAGGTGACGGATTCTGACAAGGCCAAGATGG" +
                        "AAAAAGCCATCGAAGAGAAAATCAAGTGGCTTGACGAGAACCAAGAC" +
                        "GCCGACAGTGAAGCCTTCAAGAAGCAAAAGAAAGAACTCGAAGATGT" +
                        "CGTACAGCCCATCATCTCAAAATTATACCAAGGAGGTGCTCCGCCGC" +
                        "CACCTGGAGCCGGTCCTCAATCGGAGGACGATCTTAAAGATGAGTTA" +
                        "TAAGACTGCAAAACCTTTGTGTAAATCTGTGGAACATTTCTTTGACT" +
                        "GGTGATACTTAATTTTTAAGTCAGTATTTATATATTTAAAAACAAAA" +
                        "AACCTATACATCTGAGAAGGAAATTTGTTCCTTTTTTTCAATTTAAA" +
                        "ATTTGAGTTTTTTCTTGTTTCATAAAATGTTCATTCCGCAGTTTATA" +
                        "AAGTTAATTTAAAAAACAAAAACAAAAATAAAAGACTTTGTTAACTA" +
                        "AGAAATTTATAATTTATTTGTTACTTTTTTATTTAATAATTTTTTTA" +
                        "GTGAATTGGGAATTGATGAATTACATTCAGCATTGAAAATTTATTGG" +
                        "TACCGTGTATTATAATTAATGTTGTCTGTAATTTATATAATTTCGTT" +
                        "TCATTAGGTTTTTGTTTGTCAGTTGGGCTCAATCCCAAAATTTGAGA" +
                        "ACATTCTGAAGGTGTGATAATAAAAGTTTCTTTATTTAAA";

    var ex_peptide = ">CLEC010822-PA:polypeptide ,Heat shock protein 70-2\n" +
                     "MILHFLVLLFASALAADEKNKDVGTVVGIDLGTTYSCVGVYKNGRVEIIANDQ" +
                     "GNRITPSYVAFTSEGERLIGDAAKNQLTTNPENTVFDAKRLIGREWTDSTVQD" +
                     "DIKFFPFKVLEKNSKPHIQVSTSQGNKMFAPEEISAMVLGKMKETAEAYLGKK" +
                     "VTHAVVTVPAYFNDAQRQATKDAGTISGLNVMRIINEPTAAAIAYGLDKKEGE" +
                     "KNVLVFDLGGGTFDVSLLTIDNGVFEVVSTNGDTHLGGEDFDQRVMDHFIKLY" +
                     "KKKKGKDIRKDNRAVQKLRREVEKAKRALSSSHQVRIEIESFYDGEDFSETLT" +
                     "RAKFEELNMDLFRSTMKPVQKVLEDADMNKKDVDEIVLVGGSTRIPKVQALVK" +
                     "EFFNGKEPSRGINPDEAVAYGAAVQAGVLSGEQDTDSIVLLDVNPLTLGIETV" +
                     "GGVMTKLIPRNTVIPTKKSQIFSTASDNQHTVTIQVYEGERPMTKDNHLLGKF" +
                     "DLTGIPPAPRGVPQIEVTFEIDANGILQVSAEDKGTGNREKIVITNDQNRLTP" +
                     "DDIDRMIKDAEKFADDDKKLKERVEARNELESYAYSLKNQLADKDKFGSKVTD" +
                     "SDKAKMEKAIEEKIKWLDENQDADSEAFKKQKKELEDVVQPIISKLYQGGAPP" +
                     "PPGAGPQSEDDLKDEL*\n" +
                     ">OFAS004830-PA:polypeptide ,Heat shock protein 70-2\n" +
                     "MAAGGSRPTRPAVGIDLGTTYSCVGYFDKGRVEIIANDQGNRVTPSYVAFTET" +
                     "DRIVGDAARGQAIMNPSNTVYDAKRLIGRKFDDPSVQADRKMWPFKVASKEGK" +
                     "PMIEVTYKGETRQFFPEEISSMVLSKMRETAESYIGKKVSNAVVTVPAYFNDS" +
                     "QRQATKDSGTIAGLNVLRIINEPTAAAVAYGLDKKGSGEINVLIFDLGGGTFD" +
                     "VSVLTIADGLFEVKATAGDTHLGGADFDNRMVQYFLEEFKRKTKKEVNDNKRA" +
                     "LRRLQAACERAKRVLSTATQATVEIDSFVDGIDLYSAVSRAKFEEINSDLFRG" +
                     "TLGPVEKAIRDSKIPKNRIDEIVLVGGSTRIPKIQSLLVEYFNGKELNKTINP" +
                     "DEAVAYGAAVQAAIIVGDTSDEVKDVLLLDVTPLSLGIETAGGIMTNLIPRNT" +
                     "TIPVKHSQIFSTYSDNQPGVLIQVYEGERAMTKDNNLLGTFELRGFPPAPRGV" +
                     "PQIEVAFDVDANGILNVTAQEMSTKKTSKITITNDKGRLTKAQIEKMVKEAER" +
                     "YKSEDTAARETAEAKNGLESYCYAMKNSVEEAANLGRVTEDEMKSVVRKCNET" +
                     "IMWIEANRSATKMEFEKKMRETESVCKPIATKILSRGTQQNNAGGGTPTNERG" +
                     "PVIEEAD\n" +
                     ">OFAS004738-PA:polypeptide ,Heat shock protein 70-1\n" +
                     "MPAIGIDLGTTYSCVGVWQHGKVEIIANDQGNRTTPSYVAFSDTERLIGDAAK" +
                     "NQVAMNPQNTVFDAKRLIGRKYDDPKIQDDLKHWPFRVVDCSSKPKIQVEYKG" +
                     "ETKTFAPEEISSMVLVKMKETAEAYLGGTVRDAVITVPAYFNDSQRQATKDAG" +
                     "AIAGLNVLRIINEPTAAALAYGLDKNLKGERNVLIFDLGGGTFDGPREQDHSL" +
                     "KGERNVLIFDLGGGTFDVSILTIDEGSLFEVKSTAGDTHLGGEDFDNRLVNHL" +
                     "AEEFKRKYRKDLKTNPRALRRLRTAAERAKRTLSSSTEASIEIDALFEGVDFY" +
                     "TKITRARFEELCSDLFRSTLQPVEKALQDAKLDKGLIHDVVLVGGSTRIPKIQ" +
                     "NLLQNFFNGKSLNMSINPDEAVAYGAAVQAAILSGDQSSKIQDVLLVDVAPLS" +
                     "LGIETAGGVMTKIIERNTRI";

    $('.load-nucleotide').click(function() {
        $('#query-textarea').val(ex_nucleotide);
        $('#query-textarea').keyup();
    });

    $('.load-peptide').click(function() {
        $('#query-textarea').val(ex_peptide);
        $('#query-textarea').keyup();
    });

    // load file into textarea
    $('.query-file').change(function(evt) {
        if (window.File && window.FileReader) {
            var f = evt.target.files[0];
            console.log(f.type);
            if (f && (f.type.match('text.*') || f.type == '')) {
                var r = new FileReader();
                r.onload = function(e) {
                    var contents = e.target.result;
                    $('#query-textarea').val(contents);
                    $('#query-textarea').keyup();
                }
                r.readAsText(f);
            }
        }
    });

    function add_blast_options(blast_program) {
        var html_content='';

        $('#fieldset-options-blast legend:first').html(blast_program+' Options');   //Show the option title
        $('#fieldset-options-blast label.error').remove();
        $('.parms').hide().addClass('unselected_parms');
        $('.' + blast_program.toLowerCase() + '-parms').show();
        $('.' + blast_program.toLowerCase() + '-parms').removeClass('unselected_parms');

        $('.chk_low_complexity').change();
        $('.chk_soft_masking').change();

        }

        // Validate MainBlastForm form on keyup and submit
        $("#MainBlastForm").validate({
            rules: {
                'query-sequence': {
                    required: true
                },
                'organism-checkbox[]': {
                    required: true
                },
                'db-name': {
                    required: true
                },
                evalue: {
                    required: true,
                    number: true
                },
                word_size: {
                    required: true,
                    number: true
                },
                reward: {
                    required: true,
                    number: true
                },
                penalty: {
                    required: true,
                    number: true
                },
                gapopen: {
                    required: true,
                    number: true
                },
                gapextend: {
                    required: true,
                    number: true
                },
                threshold: {
                    required: true,
                    number: true
                }
            },
            messages: {
                'query-sequence': {
                    required: "No sequence found!"
                },
                'organism-checkbox[]': {
                    required: "Please choose at least one organism"
                },
                'db-name': {
                    required: "Please choose the type of databases"
                },
                evalue: {
                    required: "Please provide an E-value",
                    number: "Please enter a valid number"
                },
                word_size: {
                    required: "Please provide word size value",
                    number: "Please enter a valid number"
                },
                reward: {
                    required: "Please provide match score value",
                    number: "Please enter a valid number"
                },
                penalty: {
                    required: "Please provide mismatch score value",
                    number: "Please enter a valid number"
                },
                gapopen: {
                    required: "Please provide a value for gap opening penalty",
                    number: "Please enter a valid number"
                },
                gapextend: {
                    required: "Please provide a value for gap extension penalty",
                    number: "Please enter a valid number"
                },
                threshold: {
                    required: "Please provide a threshold",
                    number: "Please enter a valid number"
                }
            },
            errorPlacement: function (error, element){
                switch (element.attr('name').toString()) {
                    case 'query-sequence':
                        error.insertAfter('#legend-sequence');
                        break;
                    case 'organism-checkbox[]':
                        error.insertAfter('#legend-Organisms');
                        break;
                    case 'db-name':
                        error.insertAfter('.dataset-title');
                        break;
                    default:
                        error.insertAfter(element);
                }
        }
    });

    $('input.program:radio').click(function() {
        add_blast_options($('input.program:checked').val().toUpperCase());
    });

    $('.btn_reset').click(function() {
        $('#query-textarea').val('');
        $('#query-textarea').keyup();
        $('.all-organism-checkbox').prop("checked", false);
        $('.all-organism-checkbox').change();
        $('.program').prop('disabled', false).removeClass('disabled-radio');
        add_blast_options('BLASTN');
        //$(".query-file").replaceWith('<input type="file" name="query-file" class="query-file">');

        $('label.error').remove();
        $('#MainBlastForm')[0].reset();
    });

    $('.chk_low_complexity').change(function() {
        if ($('#'+$('input.program:checked').val()+'_chk_low_complexity').is(':checked')) {
            $('#low_complexity_hidden').val('yes');
        }else {
            $('#low_complexity_hidden').val('no');
        }
    });

    $('.chk_soft_masking').change(function() {
        if ($('#'+$('input.program:checked').val()+'_chk_soft_masking').is(':checked')) {
            $('#soft_masking_hidden').val('true');
        }else {
            $('#soft_masking_hidden').val('false');
        }
    });

    add_blast_options('BLASTN'); //show initially

    $('#queries-tab').click(function() {
        user_id = $('table[id^="queries-"]')[0].id.split('-')[1];
        if ( $.fn.dataTable.isDataTable('#queries-' + user_id) ) {
            var table = $('#queries-' + user_id).DataTable();
            table.ajax.reload();
        }
        else {
            $('#queries-' + user_id).dataTable( {
                "ajax": {
                    "url": window.location.pathname + "user-tasks/" + user_id,
                    "dataSrc": ""
                },
                "columns": [
                    { "data": "enqueue_date" },
                    { "data": "result_status" },
                    { "data": "task_id" },

                ],
                "aoColumnDefs": [{
                    "aTargets": [2], // Column to target
                    "mRender": function ( data, type, full ) {
                        // 'full' is the row's data object, and 'data' is this column's data
                        // e.g. 'full[0]' is the comic id, and 'data' is the comic title
                        return '<a href="' + data  + '" target="_blank">' + data + '</a>';
                    }},
                    {
                    "aTargets": [0], // Column to target
                    "mRender": function ( data, type, full ) {
                        return new Date(data).toUTCString();
                    }}
                ],
                "order": [[ 0, "desc" ]],
            });
        }
    });

    $('.blast_submit').click(function(){
      On_Submit();
    });

    function On_Submit(){
      if($("#MainBlastForm").valid()) {
          $('.unselected_parms').remove();
          $('#click_submit_hidden').val('true');	//Use for a back button is pressed. See line 52.
          $('#MainBlastForm').submit();
      }
    }

    hist_program = $("#hist_program").val();
    if (hist_program == ''){
    }
    if ( hist_program == 'blastn' ){
        $(".blastn-parms #word_size").val($("#hist_word_size").val());
        $(".blastn-parms #evalue").val($("#hist_evalue").val());
        $(".blastn-parms #reward").val($("#hist_reward").val());
        $(".blastn-parms #penalty").val($("#hist_penalty").val());
        $(".blastn-parms #gapopen").val($("#hist_gapopen").val());
        $(".blastn-parms #gapextend").val($("#hist_gapextend").val());
        check_low_complexity = $("#hist_low_complexity").val();
        check_soft_masking = $("#hist_soft_masking").val();
        if ( check_low_complexity === 'False'){
            $('#blastn_chk_low_complexity').prop("checked", false).attr("checked", false);
            $('#low_complexity_hidden').val('no');
        }
        if ( check_soft_masking === 'False'){
            $('#blastn_chk_soft_masking').prop("checked", false).attr("checked", false);
            $('#soft_masking_hidden').val('no');
        }
        //$('#query-textarea').val($("#hist_sequence1").val());
        $(".blastn-parms #strand").val($("#hist_strand").val());
        $(".blastn-parms #max_target_seqs").val($("#hist_max_target_seqs").val());
        db_type = 'nucleotide';
        query_type = 'nucleotide';
        disableProgram();
        $('#blastn').prop("checked", true);
    } else if (hist_program == 'tblastn' ){
        $(".tblastn-parms #word_size").val($("#hist_word_size").val());
        $(".tblastn-parms #evalue").val($("#hist_evalue").val());
        $(".tblastn-parms #gapopen").val($("#hist_gapopen").val());
        $(".tblastn-parms #gapextend").val($("#hist_gapextend").val());
        $(".tblastn-parms #threshold").val($("#hist_threshold").val());
        check_low_complexity = $("#hist_low_complexity").val();
        check_soft_masking = $("#hist_soft_masking").val();
        if ( check_low_complexity === 'False'){
            $('#tblastn_chk_low_complexity').prop("checked", false).attr("checked", false);
            $('#low_complexity_hidden').val('no');
        }
        if ( check_soft_masking === 'False'){
            $('#tblastn_chk_soft_masking').prop("checked", false).attr("checked", false);
            $('#soft_masking_hidden').val('no');
        }
        //$('#query-textarea').val($("#hist_sequence1").val());
        $(".tblastn-parms #max_target_seqs").val($("#hist_max_target_seqs").val());
        $(".tblastn-parms #matrix").val($("#hist_matrix").val());
        db_type = 'nucleotide';
        query_type = 'peptide';
        disableProgram();
        $('#tblastn').prop("checked", true);
        //add_blast_options($('input.program:checked').val().toUpperCase());
    } else if (hist_program == 'tblastx' ){
        $(".tblastx-parms #word_size").val($("#hist_word_size").val());
        $(".tblastx-parms #evalue").val($("#hist_evalue").val());
        $(".tblastx-parms #threshold").val($("#hist_threshold").val());
        check_low_complexity = $("#hist_low_complexity").val();
        check_soft_masking = $("#hist_soft_masking").val();
        if ( check_low_complexity === 'False'){
            $('#tblastx_chk_low_complexity').prop("checked", false).attr("checked", false);
            $('#low_complexity_hidden').val('no');
        }
        if ( check_soft_masking === 'False'){
            $('#tblastx_chk_soft_masking').prop("checked", false).attr("checked", false);
            $('#soft_masking_hidden').val('no');
        }
        //$('#query-textarea').val($("#hist_sequence1").val());
        $(".tblastx-parms #max_target_seqs").val($("#hist_max_target_seqs").val());
        $(".tblastx-parms #matrix").val($("#hist_matrix").val());
        $(".tblastx-parms #strand").val($("#hist_strand").val());
        db_type = 'nucleotide';
        query_type = 'nucleotide';
        disableProgram();
        $('#tblastx').prop("checked", true);
        //add_blast_options($('input.program:checked').val().toUpperCase());
    } else if (hist_program == 'blastp' ){
        $(".blastp-parms #word_size").val($("#hist_word_size").val());
        $(".blastp-parms #evalue").val($("#hist_evalue").val());
        $(".blastp-parms #gapopen").val($("#hist_gapopen").val());
        $(".blastp-parms #gapextend").val($("#hist_gapextend").val());
        $(".blastp-parms #threshold").val($("#hist_threshold").val());
        check_low_complexity = $("#hist_low_complexity").val();
        check_soft_masking = $("#hist_soft_masking").val();
        if ( check_low_complexity === 'False'){
            $('#blastp_chk_low_complexity').prop("checked", false).attr("checked", false);
            $('#low_complexity_hidden').val('no');
        }
        if ( check_soft_masking === 'False'){
            $('#blastp_chk_soft_masking').prop("checked", false).attr("checked", false);
            $('#soft_masking_hidden').val('no');
        }
        //$('#query-textarea').val($("#hist_sequence1").val());
        $(".blastp-parms #max_target_seqs").val($("#hist_max_target_seqs").val());
        $(".blastp-parms #matrix").val($("#hist_matrix").val());
        db_type = 'peptide';
        query_type = 'peptide';
        disableProgram();
        $('#blastp').prop("checked", true);
        //add_blast_options($('input.program:checked').val().toUpperCase());
    } else if (hist_program == 'blastx' ){
        $(".blastx-parms #word_size").val($("#hist_word_size").val());
        $(".blastx-parms #evalue").val($("#hist_evalue").val());
        $(".blastx-parms #gapopen").val($("#hist_gapopen").val());
        $(".blastx-parms #gapextend").val($("#hist_gapextend").val());
        $(".blastx-parms #threshold").val($("#hist_threshold").val());
        check_low_complexity = $("#hist_low_complexity").val();
        check_soft_masking = $("#hist_soft_masking").val();
        if ( check_low_complexity === 'False'){
            $('#blastx_chk_low_complexity').prop("checked", false).attr("checked", false);
            $('#low_complexity_hidden').val('no');
        }
        if ( check_soft_masking === 'False'){
            $('#blastx_chk_soft_masking').prop("checked", false).attr("checked", false);
            $('#soft_masking_hidden').val('no');
        }
        //$('#query-textarea').val($("#hist_sequence1").val());
        $(".blastx-parms #max_target_seqs").val($("#hist_max_target_seqs").val());
        $(".blastx-parms #matrix").val($("#hist_matrix").val());
        $(".blastx-parms #strand").val($("#hist_strand").val());
        db_type = 'peptide';
        query_type = 'nucleotide';
        disableProgram();
        $('#blastp').prop("checked", true);
        //add_blast_options($('input.program:checked').val().toUpperCase());
    }

    if (hist_program != ''){
	hist_checkbox = $("#hist_checkbox").val();
	hist_check_array = hist_checkbox.split(',');
	for(var i = 0; i < hist_check_array.length; i++){
	    c = '#' + hist_check_array[i].split(".")[0]
	    $(c).prop("checked", true);
	    $('#'+$(c).attr('organism')).prop("checked", true);
	};
        $('#query-textarea').val($("#hist_sequence1").val());
        add_blast_options($('input.program:checked').val().toUpperCase());
    }


});

//prevention of cache pages
$(window).unload(function () { });
