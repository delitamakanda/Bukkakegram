(function() {
    if (window.myBookmarklet !== undefined) {
        myBookmarklet();
    } else {
        document.body.appendChild(document.createElement('script')).src='https://bukkakegram-static.s3.amazonaws.com/static/scripts/bookmarklet.js?r='+Math.floor(Math.random()*99999999999999999999);
    }
})();
