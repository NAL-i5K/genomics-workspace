$(function() { // document ready

    $.fn.dataTable.moment('MMM D YYYY');
    $('#table-pendings').DataTable( {
        'dom': 'Tlftip',
        "order": [[ 2, "asc" ]],
        'tableTools': {
            "sRowSelect": "multi",
            "aButtons": [],
        },
    });
    
    
    $('#table-users').DataTable( {
        'dom': 'lftip',
    });
    
    
    $('#table-species').DataTable( {
        'dom': 'lftip',
    });

    
    $('#table-pendings tbody').on('click', 'tr', function () {
        $('#remind-count').text(TableTools.fnGetInstance('table-pendings').fnGetSelected().length);
    });


    $('#btn-admin-remind').click(function(event) {
        event.preventDefault();
        var species_set = new Set();
        $.each(TableTools.fnGetInstance('table-pendings').fnGetSelectedData(), function(idx, val) {
            species_set.add(val[1]);
        });
        var species = [];
        species_set.forEach(function(value) {
            species.push(value);
        });
        console.log(species);
        $('#alert').html(
            '<div class="alert alert-success alert-dismissible" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button><strong>Done!</strong> Emails were sent to the coordinators.</div>'
        );
        //$('#alert').html(
        //'<div class="alert alert-danger alert-dismissible" role="alert" style='display:none;' id='alert-remind-fail'><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button><strong>Oh no!</strong> Email sending failed. Please contact sysadmin.</div>'}
        //);
        TableTools.fnGetInstance('table-pendings').fnSelectNone();
        $('#remind-count').text('0');
    });
});

