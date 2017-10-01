var showAddBukkake = function() {
    var $popin = $('body').find('.popin-box'),
        $overlay = $('body').find('.overlay');

    $('.btn-add').on('click', function(e) {
        e.preventDefault();
        e.stopPropagation();

        if ( !$popin.hasClass('active') ) {
            $popin.addClass('active');
            $overlay.addClass('active');
        } else {
            $popin.removeClass('active');
            $overlay.removeClass('active');
        }
    });

    $('body').on('click', '.btn-close' , function() {
        if ($overlay.hasClass('active') ) {
            $overlay.removeClass('active');
            $popin.removeClass('active');
        }
    })
};

var likeBukkake = function() {
    $('.button-like').on('click', function(e){
        e.preventDefault();
        var element = $(this);

        $.get({
            url: '/like_bukkake/',
            type: 'GET',
            data: { bukkake_id : element.attr("data-id") },
            success: function(response) {
                element.html(' ' + response);
            }
        });
    });
}

$(function() {
    showAddBukkake();
    likeBukkake();
});
