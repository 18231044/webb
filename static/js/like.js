/*Like.js*/
document.querySelector('.like').addEventListener (
    'click', 
    function() {
        var btn = $(this)
        var spn = $(this).find('span')
        if (btn.hasClass("dislike")) {
            btn.removeClass("dislike")
            btn.addClass("active-like")
            spn.removeClass("glyphicon-heart-empty")
            spn.addClass("glyphicon-heart")
        }
        else if (btn.hasClass("active-like")) {
            btn.removeClass("active-like")
            btn.addClass("dislike")
            spn.removeClass("glyphicon-heart")
            spn.addClass("glyphicon-heart-empty")
        }
    }
)
$('.post-btn button').click (
    function() {
        var btn = $(this)
        if (btn.hasClass("light"))
            btn.removeClass("light")
        else
            btn.addClass("light")
    }
)