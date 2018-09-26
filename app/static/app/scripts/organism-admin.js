$(function () { // document ready
    // Suggest short name from display name
    // text change event
    $('#id_display_name').keyup(function () {
        var name = $('#id_display_name').val().toLowerCase().replace(/^\s+|\s+$/g, '');
        if (name.length == 0)
            return;
        var tokens = name.split(/\s+/);
        var token_count = tokens.length;
        var short_name = '';
        if (token_count == 1) {
            short_name = tokens[0].substr(0, 6);
        } else if (token_count > 1) {
            short_name = tokens[0].substr(0, 3) + tokens.pop().substr(0, 3);
        }
        if (!$('#id_short_name').data('userModified'))
            $('#id_short_name').val(short_name);
    });

    // don't overwrite user input
    $('#id_short_name').keyup(function () {
        if ($('#id_short_name').val().length > 0) {
            $('#id_short_name').data('userModified', true);
        } else {
            $('#id_short_name').data('userModified', false);
        }
    });

    //Get NCBI taxonomy id
    $('#id_display_name').change(function () {
        var name = $('#id_display_name').val().toLowerCase().replace(/^\s+|\s+$/g, '');
        $.getJSON('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=taxonomy&retmode=json&term=' + name, function (data) {
            $('#id_tax_id').val(data['esearchresult']['idlist'][0]);
        });
    });

    // Get description from wikipedia
    $('#id_display_name').change(function () {
        var name = $('#id_display_name').val().toLowerCase().replace(/^\s+|\s+$/g, '');
        $.getJSON('https://en.wikipedia.org/w/api.php?action=query&list=search&srprop=snippet&srlimit=1&format=json&callback=?&srsearch=' + name, function (data) {
            // example name can be used: 'Anoplophora%20glabripennis'
            if (data['query']['search'].length > 0) {
                $.getJSON('https://en.wikipedia.org/w/api.php?action=query&prop=extracts&format=json&exintro=true&callback=?&titles=' + data['query']['search'][0]['title'], function (data) {
                    var keys = Object.keys(data['query']['pages']);
                    if (keys.length > 0) {
                        $('#id_description').val($(data['query']['pages'][keys[0]]['extract']).text()).trigger('autosize.resize');;
                    }
                });
            }
        });
    });
});
