$(function() {
    $('.button-like').on('click', function(e){
        e.preventDefault();
        var element = $(this);

        $.ajax({
            url: '/like_bukkake/',
            type: 'GET',
            data: { bukkake_id : element.attr("data-id") },
            success: function(response) {
                element.html(' ' + response);
            }
        });
    });

    $.material.init()
});
