/// <reference path="../../../templates/hmmer/main.html" />
/////////////////////
// DATA PROCESSING //
/////////////////////
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
	//alert("hello");
	//alert(alphabet_list[0]);
	//alert(dataset_dict[organism_list[0]][alphabet_list[0]]);
	for (var i = 0; i < organism_list_count; i++) {

		var organism_id = organism_list[i].toLowerCase().replace(' ', '-');
		// organism-checkbox
		var $organism_checkbox = $('<input>', {
			'organism': organism_id,
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
				//var alphabet_fieldset_id = organism_id + '-' + alphabet_class + '-fieldset'
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
	////////////////////
	// EVENT HANDLING //
	////////////////////
	var default_data_type = $('.all-dataset-checkbox').attr('dataset-type') || 'genome-assembly';
	//alert($('.all-dataset-checkbox').attr('dataset-type'));
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
			//alert($(this).attr('name'));
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
		//alert('.all-dataset-checkbox.' + default_data_type);
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
				$('.peptide').attr('disabled', 'disabled').addClass('disabled-fieldset');
			} else if ($('.peptide').is(':checked')) {
				db_type = 'peptide';
				$('.nucleotide').attr('disabled', 'disabled').addClass('disabled-fieldset');
			}
		} else {
			if (!$('.dataset-checkbox').is(':checked')) {
				db_type = '';
				$('.peptide').attr('disabled', false).removeClass('disabled-fieldset');
				$('.nucleotide').attr('disabled', false).removeClass('disabled-fieldset');
			}
		}
		chooseProgram();
	}
	
	var query_type = '';
	function setQueryType(qtype) {
		query_type = qtype;
		if (qtype == '') {
			$('.enter-query-text').html('Enter sequence below in <a target="_blank" href="http://en.wikipedia.org/wiki/FASTA_format">FASTA</a> / IN <a target="_blank" href="http://toolkit.tuebingen.mpg.de/reformat/help_params#format">MSA (format descriptions)</a>:');
		} else if (qtype == 'invalid') {
			$('.enter-query-text').html('Your sequence is invalid:');
		} else if (qtype == 'fasta') {
			$('.enter-query-text').html('Your sequence is detected as fasta:');
		} else if (qtype == 'msa'){
			$('.enter-query-text').html('Your sequence is not detected as fasta (phmmer disabled):');
		}
		chooseProgram();
	}
	
	//var program_selected = 'phmmer';
	var chooseProgram = _.debounce(function () {
		$('.program').attr('disabled', false).removeClass('disabled-radio');
		if (query_type == 'fasta') {

		} else if (query_type == 'msa') {
			$('.phmmer').attr('disabled', 'disabled').addClass('disabled-radio');
		} else if (query_type == 'invalid'){
			$('.hmmsearch').attr('disabled', 'disabled').addClass('disabled-radio');
			$('.phmmer').attr('disabled', 'disabled').addClass('disabled-radio');
		}
		//query_type = '';
		// select first non disabled option
		$('input.program:not([disabled])').first().prop('checked', true);
		program_selected = $('input.program:not([disabled])').first().val();
		$('.' + program_selected).mouseover();
	}, 30);

    //Reset all element if reload of previous page when back button is pressed
	if ($('#click_submit_hidden').val() == 'true') {
        $('#click_submit_hidden').val('false');
	    $('#query-textarea').val('');
	    $(".query-file").replaceWith('<input type="file" name="query-file" class="query-file">');
	    $('.all-organism-checkbox').prop("checked", false).attr("checked", false);
	    $('.all-organism-checkbox').change();
	    $('.program').attr('disabled', false).removeClass('disabled-radio');
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

	function validateFasta(fasta) {

		if (!fasta) { // check there is something first of all
			return false;
		}

		// immediately remove trailing spaces
		fasta = fasta.trim();

		// split on newlines...
		var lines = fasta.split('\n');

		// check for header
		for (i = 0; i < lines.length; i++){
			if(lines[i][0] == '>'){
				// remove one line, starting at the first position
				lines[i] = '';
			}
		}

		// join the array back into a single string without newlines and
		// trailing or leading spaces
		fasta = lines.join('').trim();

		if (!fasta) { // is it empty whatever we collected ? re-check not efficient
			return false;
		}

		// note that the empty string is caught above
		// allow for Selenocysteine (U)
		return /^[ABCDEFGHIKLMNPQRSTVWXYZ*\s]+$/i.test(fasta);
	}

	function validateSTO(sto){
		if(!sto){
			return false;
		}
		sto = sto.trim();
		var row_len = 0;
		var not_empty = false;
		var lines = sto.split('\n');
		for(var i = 0; i < lines.length; i++){
			if(lines[i] == ''){
				row_len = 0;
			} else if(lines[i] == '//'){
				return true;
			} else if(lines[i].slice(0,1) != "#"){

				if(row_len == 0){
					row_len = lines[i].length;

				}else{
					//at least two sequences
					not_empty = true
					if(row_len != lines[i].length){
						return false;
					}
				}
			}
		}
		if(not_empty)
			return true;
	}

	function checktxt() {
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
		var normal_nucleic_codes = 'ATCGN';
		var valid_amino_codes = 'ABCDEFGHIKLMNPQRSTVWXYZ*';
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
		// Too many degenerate codes within an input nucleotide query will cause hmmer.cgi to
		// reject the input. For protein queries, too many nucleotide-like code (A,C,G,T,N) may also
		// cause similar rejection.
		if (total_count == 0) {
			setQueryType('');
		} else if(!validateFasta($('#query-textarea').val())){
			setQueryType('msa');
		} else if(validateFasta($('#query-textarea').val())){
			setQueryType('fasta');
		}
		//console.log(query_type, normal_nucleic_count, total_count);
	}

	var parseTextarea = _.debounce(checktxt, 30);
	$('#query-textarea').keyup(parseTextarea);

	 // hmmer program descriptions for labels and their radio buttons
	$('.program.phmmer').mouseover(function() {
		$('#hmmerProgramDescription').text('phmmer - Protein sequence vs. Protein sequence database');
	});
	$('.program.hmmsearch').mouseover(function() {
		$('#hmmerProgramDescription').text('hmmsearch - MSA vs. Protein sequence database');
	});
	$('#fieldset-program').mouseleave(function() {
		$('.' + $('input.program:checked').val()).mouseover();
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


        var ex_nucleotide = ">Test1\n\ATCGATGCTA\n\>Test2\n\ATCGATCGATCGA"

        $('.load-example').click(function() {
                $('#query-textarea').val(ex_nucleotide);
                $('#query-textarea').keyup();
        });


        var ex_sample_seq = ">CLEC010822-PA:polypeptide, Heat shock protein 70-2\n\
MILHFLVLLFASALAADEKNKDVGTVVGIDLGTTYSCVGVYKNGRVEIIANDQGNRITPSYVAFTSEGERLIGDAAKNQLTTNPENTVFDAKRLIGREWTDSTVQDDIKFFPFKVLEKNSKPHIQVSTSQGNKMFAPEEISAMVLGKMKETAEAYLGKKVTHAVVTVPAYFNDAQRQATKDAGTISGLNVMRIINEPTAAAIAYGLDKKEGEKNVLVFDLGGGTFDVSLLTIDNGVFEVVSTNGDTHLGGEDFDQRVMDHFIKLYKKKKGKDIRKDNRAVQKLRREVEKAKRALSSSHQVRIEIESFYDGEDFSETLTRAKFEELNMDLFRSTMKPVQKVLEDADMNKKDVDEIVLVGGSTRIPKVQALVKEFFNGKEPSRGINPDEAVAYGAAVQAGVLSGEQDTDSIVLLDVNPLTLGIETVGGVMTKLIPRNTVIPTKKSQIFSTASDNQHTVTIQVYEGERPMTKDNHLLGKFDLTGIPPAPRGVPQIEVTFEIDANGILQVSAEDKGTGNREKIVITNDQNRLTPDDIDRMIKDAEKFADDDKKLKERVEARNELESYAYSLKNQLADKDKFGSKVTDSDKAKMEKAIEEKIKWLDENQDADSEAFKKQKKELEDVVQPIISKLYQGGAPPPPGAGPQSEDDLKDEL*\n\
>OFAS004830-PA:polypeptide, Heat shock protein 70-2\n\
MAAGGSRPTRPAVGIDLGTTYSCVGYFDKGRVEIIANDQGNRVTPSYVAFTETDRIVGDAARGQAIMNPSNTVYDAKRLIGRKFDDPSVQADRKMWPFKVASKEGKPMIEVTYKGETRQFFPEEISSMVLSKMRETAESYIGKKVSNAVVTVPAYFNDSQRQATKDSGTIAGLNVLRIINEPTAAAVAYGLDKKGSGEINVLIFDLGGGTFDVSVLTIADGLFEVKATAGDTHLGGADFDNRMVQYFLEEFKRKTKKEVNDNKRALRRLQAACERAKRVLSTATQATVEIDSFVDGIDLYSAVSRAKFEEINSDLFRGTLGPVEKAIRDSKIPKNRIDEIVLVGGSTRIPKIQSLLVEYFNGKELNKTINPDEAVAYGAAVQAAIIVGDTSDEVKDVLLLDVTPLSLGIETAGGIMTNLIPRNTTIPVKHSQIFSTYSDNQPGVLIQVYEGERAMTKDNNLLGTFELRGFPPAPRGVPQIEVAFDVDANGILNVTAQEMSTKKTSKITITNDKGRLTKAQIEKMVKEAERYKSEDTAARETAEAKNGLESYCYAMKNSVEEAANLGRVTEDEMKSVVRKCNETIMWIEANRSATKMEFEKKMRETESVCKPIATKILSRGTQQNNAGGGTPTNERGPVIEEAD\n\
>OFAS004738-PA:polypeptide, Heat shock protein 70-1\n\
MPAIGIDLGTTYSCVGVWQHGKVEIIANDQGNRTTPSYVAFSDTERLIGDAAKNQVAMNPQNTVFDAKRLIGRKYDDPKIQDDLKHWPFRVVDCSSKPKIQVEYKGETKTFAPEEISSMVLVKMKETAEAYLGGTVRDAVITVPAYFNDSQRQATKDAGAIAGLNVLRIINEPTAAALAYGLDKNLKGERNVLIFDLGGGTFDGPREQDHSLKGERNVLIFDLGGGTFDVSILTIDEGSLFEVKSTAGDTHLGGEDFDNRLVNHLAEEFKRKYRKDLKTNPRALRRLRTAAERAKRTLSSSTEASIEIDALFEGVDFYTKITRARFEELCSDLFRSTLQPVEKALQDAKLDKGLIHDVVLVGGSTRIPKIQNLLQNFFNGKSLNMSINPDEAVAYGAAVQAAILSGDQSSKIQDVLLVDVAPLSLGIETAGGVMTKIIERNTRI";

        $('.load-example-seq').click(function() {
                $('#query-textarea').val(ex_sample_seq);
                $('#query-textarea').keyup();
        });

        var ex_sample_aln = "CLUSTAL O(1.2.3) multiple sequence alignment\n\n\n\
CLEC010822-PA:polypeptide,      MILHFLVLLFASALAADEKNKDVGTVVGIDLGTTYSCVGVYKNGRVEIIANDQGNRITPS\n\
OFAS004830-PA:polypeptide,      --------------MAAGGSRPTRPAVGIDLGTTYSCVGYFDKGRVEIIANDQGNRVTPS\n\
OFAS004738-PA:polypeptide,      -----------------------MPAIGIDLGTTYSCVGVWQHGKVEIIANDQGNRTTPS\n\
                                                         .:************ :.:*:*********** ***\n\
\n\
CLEC010822-PA:polypeptide,      YVAFTSEGERLIGDAAKNQLTTNPENTVFDAKRLIGREWTDSTVQDDIKFFPFKVLEKNS\n\
OFAS004830-PA:polypeptide,      YVAFT-ETDRIVGDAARGQAIMNPSNTVYDAKRLIGRKFDDPSVQADRKMWPFKVASKEG\n\
OFAS004738-PA:polypeptide,      YVAFS-DTERLIGDAAKNQVAMNPQNTVFDAKRLIGRKYDDPKIQDDLKHWPFRVVDCSS\n\
                                ****: : :*::****:.*   **.***:********:: * .:* * * :**:* . ..\n\
\n\
CLEC010822-PA:polypeptide,      KPHIQVSTSQGNKMFAPEEISAMVLGKMKETAEAYLGKKVTHAVVTVPAYFNDAQRQATK\n\
OFAS004830-PA:polypeptide,      KPMIEVTYKGETRQFFPEEISSMVLSKMRETAESYIGKKVSNAVVTVPAYFNDSQRQATK\n\
OFAS004738-PA:polypeptide,      KPKIQVEYKGETKTFAPEEISSMVLVKMKETAEAYLGGTVRDAVITVPAYFNDSQRQATK\n\
                                ** *:*  .  .: * *****:*** **:****:*:* .* .**:********:******\n\
\n\
CLEC010822-PA:polypeptide,      DAGTISGLNVMRIINEPTAAAIAYGLDKKE---------------------------GEK\n\
OFAS004830-PA:polypeptide,      DSGTIAGLNVLRIINEPTAAAVAYGLDKKGSGEINV------------------------\n\
OFAS004738-PA:polypeptide,      DAGAIAGLNVLRIINEPTAAALAYGLDKNLKGERNVLIFDLGGGTFDGPREQDHSLKGER\n\
                                *:*:*:****:**********:******:                               \n\
\n\
CLEC010822-PA:polypeptide,      NVLVFDLGGGTFDVSLLTIDNG-VFEVVSTNGDTHLGGEDFDQRVMDHFIKLYKKKKGKD\n\
OFAS004830-PA:polypeptide,      --LIFDLGGGTFDVSVLTIADG-LFEVKATAGDTHLGGADFDNRMVQYFLEEFKRKTKKE\n\
OFAS004738-PA:polypeptide,      NVLIFDLGGGTFDVSILTIDEGSLFEVKSTAGDTHLGGEDFDNRLVNHLAEEFKRKYRKD\n\
                                  *:***********:*** :* :*** :* ******* ***:*::::: : :*:*  *:\n\
\n\
CLEC010822-PA:polypeptide,      IRKDNRAVQKLRREVEKAKRALSSSHQVRIEIESFYDGEDFSETLTRAKFEELNMDLFRS\n\
OFAS004830-PA:polypeptide,      VNDNKRALRRLQAACERAKRVLSTATQATVEIDSFVDGIDLYSAVSRAKFEEINSDLFRG\n\
OFAS004738-PA:polypeptide,      LKTNPRALRRLRTAAERAKRTLSSSTEASIEIDALFEGVDFYTKITRARFEELCSDLFRS\n\
                                :. : **:::*:   *:***.**:: :. :**::: :* *:   ::**:***:  ****.\n\
\n\
CLEC010822-PA:polypeptide,      TMKPVQKVLEDADMNKKDVDEIVLVGGSTRIPKVQALVKEFFNGKEPSRGINPDEAVAYG\n\
OFAS004830-PA:polypeptide,      TLGPVEKAIRDSKIPKNRIDEIVLVGGSTRIPKIQSLLVEYFNGKELNKTINPDEAVAYG\n\
OFAS004738-PA:polypeptide,      TLQPVEKALQDAKLDKGLIHDVVLVGGSTRIPKIQNLLQNFFNGKSLNMSINPDEAVAYG\n\
                                *: **:*.:.*:.: *  :.::***********:* *: ::****. .  **********\n\
\n\
CLEC010822-PA:polypeptide,      AAVQAGVLSGEQDT--DSIVLLDVNPLTLGIETVGGVMTKLIPRNTVIPTKKSQIFSTAS\n\
OFAS004830-PA:polypeptide,      AAVQAAIIVGDTSDEVKDVLLLDVTPLSLGIETAGGIMTNLIPRNTTIPVKHSQIFSTYS\n\
OFAS004738-PA:polypeptide,      AAVQAAILSGDQSSKIQDVLLVDVAPLSLGIETAGGVMTKIIERNTRIPCKQTQTFTTYS\n\
                                *****.:: *: .   ..::*:** **:*****.**:**::* *** ** *::* *:* *\n\
\n\
CLEC010822-PA:polypeptide,      DNQHTVTIQVYEGERPMTKDNHLLGKFDLTGIPPAPRGVPQIEVTFEIDANGILQVSAED\n\
OFAS004830-PA:polypeptide,      DNQPGVLIQVYEGERAMTKDNNLLGTFELRGFPPAPRGVPQIEVAFDVDANGILNVTAQE\n\
OFAS004738-PA:polypeptide,      DNQPAVTVQVYEGERVMTKDNNLLGTFDLTGIPPAPRGVPKIDVTFDMDANGILNVSAKD\n\
                                ***  * :******* *****:***.*:* *:********:*:*:*::******:*:*::\n\
\n\
CLEC010822-PA:polypeptide,      KGTGNREKIVITNDQNRLTPDDIDRMIKDAEKFADDDKKLKERVEARNELESYAYSLKNQ\n\
OFAS004830-PA:polypeptide,      MSTKKTSKITITNDKGRLTKAQIEKMVKEAERYKSEDTAARETAEAKNGLESYCYAMKNS\n\
OFAS004738-PA:polypeptide,      NSSGKSKNIRIENNKGRLSKEEIDRMINEAERYKEEDDKERERIAAKNKLETYIFSIKQA\n\
                                 .: : .:* * *::.**:  :*::*:::**:: .:*   :*   *:* **:* :::*: \n\
\n\
CLEC010822-PA:polypeptide,      LADKDKFGSKVTDSDKAKMEKAIEEKIKWLDENQDADSEAFKKQKKELEDVVQPIISKLY\n\
OFAS004830-PA:polypeptide,      VEEAANLGRV-TEDEMKSVVRKCNETIMWIEANRSATKMEFEKKMRETESVCKPIATKIL\n\
OFAS004738-PA:polypeptide,      VDDAGD--KL-SEEDKNTARAKCDEAMRWLDNNSLAAKDEYEHKYEELQRDCTNFMTKMY\n\
                                : :  .     ::.:  .     :* : *:: *  * .  :::: .* :     : :*: \n\
\n\
CLEC010822-PA:polypeptide,      QGGAPPPP----------GAGPQSEDDLKDEL*\n\
OFAS004830-PA:polypeptide,      SRGTQQN--NAGGGTPTNERGPVIEEAD-----\n\
OFAS004738-PA:polypeptide,      AGGAGSCGQQNGNNFSQQSRGPTVEEVD-----\n\
                                  *:                **  *:       ";

        $('.load-example-aln').click(function() {
                $('#query-textarea').val(ex_sample_aln);
                $('#query-textarea').keyup();
        });


	// Validate MainHmmerForm form on keyup and submit
	$("#MainHmmerForm").validate({
		rules: {
			'query-sequence': {
				//'textarea_valid':'',
				required: true
			},
			'organism-checkbox[]': {
				required: true
			},
			'db-name': {
				required: true
			},
			s_sequence: {
				required: true,
				number: true
			},
			s_hit: {
				required: true,
				number: true
			},
			r_sequence: {
				required: true,
				number: true
			},
			r_hit: {
				required: true,
				number: true
			},
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
			s_sequence: {
				required: "Please provide a value for significance sequence",
				number: "Please enter a valid number"
			},
			s_hit: {
				required: "Please provide a value for significance hit",
				number: "Please enter a valid number"
			},
			r_sequence: {
				required: "Please provide a value for report sequence",
				number: "Please enter a valid number"
			},
			r_hit: {
				required: "Please provide a value for report hit",
				number: "Please enter a valid number"
			},
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

    $('.cutoff').change(function(){
        if($('.cutoff:checked').val() == 'bitscore'){
            $('#s_sequence').val('25');
            $('#s_hit').val('22');
            $('#r_sequence').val('7');
            $('#r_hit').val('5');
        }

        if($('.cutoff:checked').val() == 'evalue'){
            $('#s_sequence').val('0.01');
            $('#s_hit').val('0.03');
            $('#r_sequence').val('0.01');
            $('#r_hit').val('0.03');
        }
    });

    $('.btn_reset').click(function() {
        query_type = '';
        $('.program').attr('disabled', false).removeClass('disabled-radio');
        $('#query-textarea').val('');
        $('.all-organism-checkbox').prop("checked", false).attr("checked", false);
        $('.all-organism-checkbox').change();
        $(".query-file").val('');
        $('label.error').remove();
		$('.cutoff').change();
    });

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
	checktxt();
});

function On_Submit(){
	if($("#MainHmmerForm").valid()) {
		$('#click_submit_hidden').val('true');
		if($('input[name=program]:checked', '#MainHmmerForm').val() == 'hmmsearch'){
            $('#MainHmmerForm').submit();
		}else if($('input[name=program]:checked', '#MainHmmerForm').val() == 'phmmer'){
			$('#click_submit_hidden').val('true');
			$('#MainHmmerForm').submit();
		};
	}
}

//prevention of cache pages
$(window).unload(function () { });
