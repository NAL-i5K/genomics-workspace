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

	// load file into textarea
	$('.query-file').change(function (evt) {
		if (window.File && window.FileReader) {
			var f = evt.target.files[0];
			console.log(f.type);
			if (f && (f.type.match('text.*') || f.type == '')) {
				var r = new FileReader();
				r.onload = function (e) {
					var contents = e.target.result;
					$('#query-textarea').val(contents);
					$('#query-textarea').keyup();
				}
				r.readAsText(f);
			}
		}
	});

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
		var fasta_count = 0;
		for (i = 0; i < lines.length; i++){
			if(i + 1 == lines.length){
				//only one fasta
				if(fasta_count == 1){return 4;}
			}else if(lines[i][0] == '>'){
				lines[i] = '';
				//no content
				if(lines[i+1][0] == '>'){return 4;}
				fasta_count = fasta_count + 1;
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
		if(/^[ATCGUN*\s]+$/i.test(fasta)){return 1;}
		if(/^[ABCDEFGHIKLMNPQRSTVWXYZN*\s]+$/i.test(fasta)){return 2;}
		return 3;
	}

	function setQueryType(qtype) {
		query_type = qtype;
		if($('#texterror').length){
			$('#texterror').remove();
		}
        $('.sequenceType').attr('disabled', false).removeClass('disabled-radio');
		if (qtype == '') {
			$('.enter-query-text').before("<label id='texterror' class=\"error\">No sequence found!</label>");
			$('.enter-query-text').html('Enter sequence below in <a href="http://en.wikipedia.org/wiki/FASTA_format">FASTA</a> format:');
		} else if (qtype == 'invalid') {
			$('.enter-query-text').before("<label id='texterror' class=\"error\">Your sequence is invalid:</label>");
			$('.enter-query-text').html('Enter sequence below in <a href="http://en.wikipedia.org/wiki/FASTA_format">FASTA</a> format:');
		} else if (qtype == 'not_multiple') {
            		$('.enter-query-text').before("<label id='texterror' class=\"error\">You must provide 2+ sequence</label>");
			$('.enter-query-text').html('Enter sequence below in <a href="http://en.wikipedia.org/wiki/FASTA_format">FASTA</a> format:');
		} else if (qtype == 'nucleotide') {
			$('.enter-query-text').html('Your sequence is detected as nucleotide:');
			$('.sequenceType.dna').prop('checked', true);
			$('.sequenceType').change();
		} else if (qtype == 'peptide') {
			$('.enter-query-text').html('Your sequence is detected as peptide:');
			$('.sequenceType.protein').prop('checked', true);
			$('.sequenceType').change();
		}
	}

	function checktxt() {
		if ($('#query-textarea').val() == '') {
			setQueryType('');
			return false;
		}else if(validateFasta($('#query-textarea').val()) == 1) {
			setQueryType('nucleotide');
			return true;
		}else if(validateFasta($('#query-textarea').val()) == 2) {
			setQueryType('peptide');
			return true;
		}else if(validateFasta($('#query-textarea').val()) == 4) {
			setQueryType('not_multiple');
			return true;
		}else{
			setQueryType('invalid');
			return false;
		}
	}

	var parseTextarea = _.debounce(checktxt, 30);
	$('#query-textarea').keyup(parseTextarea);

	$('.sequenceType').change(function (){
		if($('.sequenceType:checked').val() == 'dna'){
			$('#fieldset-protein-multi').css('display','none');
			$('#fieldset-dna-multi').css('display','inline');
			if($('.pairwise:checked').val() == 'full'){
				$('#fieldset-protein-full').css('display','none');
				$('#fieldset-dna-full').css('display','inline');
			}
		}else if($('.sequenceType:checked').val() == 'protein'){
			$('#fieldset-dna-multi').css('display','none');
			$('#fieldset-protein-multi').css('display','inline');
			if($('.pairwise:checked').val() == 'full') {
				$('#fieldset-dna-full').css('display', 'none');
				$('#fieldset-protein-full').css('display', 'inline');
			}
		}
	});

        var ex_nucleotide = ">Test1\n\ATCGATGCTA\n\>Test2\n\ATCGATCGATCGA"

        $('.load-example').click(function() {
                $('#query-textarea').val(ex_nucleotide);
                $('#query-textarea').keyup();
        });


	$('.pairwise').change(function (){
		if($('.pairwise:checked').val() == 'fast'){
			$('#fieldset-protein-full').css('display','none');
			$('#fieldset-dna-full').css('display','none');
			$('#fieldset-fast').css('display','inline');
		}else if($('.pairwise:checked').val() == 'full'){
			$('#fieldset-fast').css('display','none');
			if($('.sequenceType:checked').val() == 'protein'){
				$('#fieldset-protein-full').css('display','inline');
			}else if($('.sequenceType:checked').val() == 'dna'){
				$('#fieldset-dna-full').css('display','inline');
			}
		}
	});



	// Validate MainClustalForm form on keyup and submit
	$("#MainClustalForm").validate({
		rules: {
			'query-sequence': {
				//'textarea_valid':'',
				required: true
			},
			'dna-pwgapopen': {
				number: true
			},
			'dna-pwgapext': {
				number: true
			},
			'protein-pwgapopen': {
				number: true
			},
			'protein-pwgapext': {
				number: true
			},
			'ktuple': {
				number: true
			},
			'window': {
				number: true
			},
			'pairgap': {
				number: true
			},
			'topdiags': {
				number: true
			},
			'dna-gapopen': {
				number: true
			},
			'dna-gapext': {
				number: true
			},
			'dna-gapdist': {
				number: true
			},
			'dna-numiter': {
				number: true
			},
			'protein-gapopen': {
				number: true
			},
			'protein-gapext': {
				number: true
			},
			'protein-gapdist': {
				number: true
			},
			'protein-numiter': {
				number: true
			},
		},
		messages: {
			'query-sequence': {
				required: "No sequence found!"
			},
			'dna-pwgapopen': {
				number: "<br>Please enter a valid number"
			},
			'dna-pwgapext': {
				number: "<br>Please enter a valid number"
			},
			'protein-pwgapopen': {
				number: "<br>Please enter a valid number"
			},
			'protein-pwgapext': {
				number: "<br>Please enter a valid number"
			},
			'ktuple': {
				number: "<br>Please enter a valid number"
			},
			'window': {
				number: "<br>Please enter a valid number"
			},
			'pairgap': {
				number: "<br>Please enter a valid number"
			},
			'topdiags': {
				number: "<br>Please enter a valid number"
			},
			'dna-gapopen': {
				number: "<br>Please enter a valid number"
			},
			'dna-gapext': {
				number: "<br>Please enter a valid number"
			},
			'dna-gapdist': {
				number: "<br>Please enter a valid number"
			},
			'dna-numiter': {
				number: "<br>Please enter a valid number"
			},
			'protein-gapopen': {
				number: "<br>Please enter a valid number"
			},
			'protein-gapext': {
				number: "<br>Please enter a valid number"
			},
			'protein-gapdist': {
				number: "<br>Please enter a valid number"
			},
			'protein-numiter': {
				number: "<br>Please enter a valid number"
			},
		},
		errorPlacement: function (error, element) {
			switch (element.attr('name').toString()) {
				case 'query-sequence':
					error.insertAfter('#legend-sequence');
					break;
				default:
					error.insertAfter(element);
			}
		}
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

	$('#clustalw_submit').click(function() {
		{
			if (checktxt() && $("#MainClustalForm").valid()) {
				$('#program').val('clustalw');
				$('#MainClustalForm').submit();
			}
		}
	});

	$('#clustalo_submit').click(function() {
		{
			if (checktxt() && $("#MainClustalForm").valid()) {
				$('#program').val('clustalo');
				$('#MainClustalForm').submit();
			}
		}
	});

	$('.btn_reset').click(function() {
		{
			$('.sequenceType').attr('disabled', false).removeClass('disabled-radio');
			$('.enter-query-text').html('Enter sequence below in <a href="http://en.wikipedia.org/wiki/FASTA_format">FASTA</a> format:');
			var validator = $( "#MainClustalForm" ).validate();
			validator.resetForm();
            $('.sequenceType.protein').prop('checked', true);
            $('.sequenceType.protein').change();
            $('.pairwise.full').prop('checked', true);
            $('.pairwise.full').change();
		}
	});

        hist_program = $("#hist_program").val();
        if (hist_program == 'clustalo'){
            if ($("#hist_combined_iter").val() == 'True'){
                $("select[name='clustering_guide_tree'][value='yes']").prop('checked', true);
            }else{
                $("select[name='clustering_guide_tree'][value='no']").prop('checked', true);
            }
            $("select[name='omega_output']").val($("#hist_omega_output").val());
            $("select[name='omega_order']").val($("#hist_omega_order").val());
            $("select[name='combined_iter']").val($("#hist_combined_iter").val());
            $("select[name='max_gt_iter']").val($("#hist_max_gt_iter").val());
            $("select[name='max_hmm_iter']").val($("#hist_max_hmm_iter").val());
            $('.nav-tabs a[href="#'+hist_program+'"]').tab('show');     
            $('#query-textarea').val($("#hist_sequence").val());
        } else if (hist_program == 'clustalw'){
            $('.nav-tabs a[href="#'+hist_program+'"]').tab('show');
            $('#query-textarea').val($("#hist_sequence").val());
            $("input[name='sequenceType'][value='"+$('#hist_sequence_type').val()+"']").prop('checked', true);
            $("input[name='pairwise'][value='"+$('#hist_pairwise').val()+"']").prop('checked', true);
            $('.sequenceType').change();
            $('.pairwise').change();
            sequence_type = $('#hist_sequence_type').val();
            pairwise = $('#hist_pairwise').val();
            if ( sequence_type == 'dna' && pairwise == 'full'){
                $("select[name='dnamatrix']").val($('#hist_dnamatrix').val());
                $("input[name='dna_gapopen']").val($('#hist_dna_gapopen').val());
                $("input[name='dna_gapext']").val($('#hist_dna_gapext').val());
                $("input[name='dna_gapdist']").val($('#hist_dna_gapdist').val());
                $("select[name='dna_iteration']").val($('#hist_dna_iteration').val());
                $("input[name='dna_numiter']").val($('#hist_dna_numiter').val());
                $("input[name='dna_clustering'][value='"+$('#hist_dna_clustering').val()+"']").prop('checked', true);
                $("select[name='pwdnamatrix']").val($('#hist_pwdnamatrix').val());
                $("input[name='dna_pwgapopen']").val($('#hist_dna_pwgapopen').val());
                $("input[name='dna_pwgapext']").val($('#hist_dna_pwgapext').val());
            } else if (sequence_type == 'protein' && pairwise == 'full'){
                $("select[name='matrix']").val($('#hist_matrix').val());
                $("input[name='protein_gapopen']").val($('#hist_protein_gapopen').val());
                $("input[name='protein_gapext']").val($('#hist_protein_gapext').val());
                $("input[name='protein_gapdist']").val($('#hist_protein_gapdist').val());
                $("select[name='protein_iteration']").val($('#hist_protein_iteration').val());
                $("input[name='protein_numiter']").val($('#hist_protein_numiter').val());
                $("input[name='protein_clustering'][value='"+$('#hist_protein_clustering').val()+"']").prop('checked', true);
                $("select[name='pwmatrix']").val($('#hist_pwmatrix').val());
                $("input[name='protein_pwgapopen']").val($('#hist_protein_pwgapopen').val());
                $("input[name='protein_pwgapext']").val($('#hist_protein_pwgapext').val());                  
            } 
            if (pairwise == 'fast'){
                $("input[name='ktuple']").val($('#hist_ktuple').val());
                $("input[name='window']").val($('#hist_window').val());
                $("input[name='pairgap']").val($('#hist_pairgap').val());
                $("input[name='topdiags']").val($('#hist_topdiags').val());
                $("input[name='score'][value='"+$('#hist_score').val()+"']").val($('#hist_score').val());
            }



            $("select[name='output']").val($('#hist_output').val());
            $("select[name='outorder']").val($('#hist_outorder').val());
        }

     

});



//prevention of cache pages
$(window).unload(function () { });
