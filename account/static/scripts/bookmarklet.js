(function() {
    var jquery_version = '2.2.4';
    var site_url = 'http://127.0.0.1:8000/';
    var static_url = site_url + 'static/';
    var min_width = 100;
    var min_height = 100;

    function bookmarklet(msg) {
        console.log('bookmarklet init !');
        // load css
        var css = jQuery('<link>');
        css.attr({
            rel: 'stylesheet',
            type: 'text/css',
            href: static_url + 'styles/bookmarklet.css?r=' + Math.floor(Math.random()*99999999999999999999)
        });
        jQuery('head').append(css);

        //load html
        box_html = '<div id="bookmarklet"><a href="#" id="close"><i class="icon ion-close-round"></i></a><h1>Select an image to bookmark:</h1><div class="images"></div></div>';
        jQuery('body').append(box_html);

        //close event
        jQuery('#bookmarklet #close').on('click', function(evt) {
            evt.preventDefault();

            $('#bookmarklet').remove();
        });

        //find images and display
        jQuery.each(jQuery('img[src$="jpg"]'), function(index, image) {
            if (jQuery(image).width() >= min_width && jQuery(image).height() >= min_height) {
                image_url = jQuery(image).attr('src');
                jQuery('#bookmarklet .images').append('<a href="#"><img src="'+ image_url +'" /></a>');
            }
        });

        // when an image is selected open url with it
        jQuery('#bookmarklet .images a').click(function(e) {
            selected_image = jQuery(this).children('img').attr('src');
            jQuery('#bookmarklet').hide();
            window.open(site_url + 'create/?url=' + encodeURIComponent(selected_image) + '&title=' + encodeURIComponent(jQuery('title').text()), '_blank' );
        });
    };

    //check jquery is loaded
    if (typeof window.jQuery != 'undefined') {
        bookmarklet();
    } else {
        var conflict = typeof window.$ != 'undefined';
        // create a script and point to google api
        var script = document.createElement('script');
        script.setAttribute('src', 'http://ajax.googleapis.com/ajax/libs/jquery/' + jquery_version + 'jquery.min.js');
        document.getElementsByTagName('head')[0].appendChild(script);
        var attempts = 15;
        (function() {
            if (typeof window.jQuery == 'undefined') {
                if (--attempts > 0) {
                    window.setTimeout(arguments.callee, 250)
                } else {
                    console.log('an error occured while loading jQuery');
                }
            } else {
                bookmarklet();
            }
        })();
    }
})();
