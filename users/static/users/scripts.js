function send_like(event, postPk, userPk, postId, csrf) {
    const aHrefLike = $('#' + postId);
    const isLiked = aHrefLike.hasClass('liked');
    const smallTextLikesCount = $('#' + postId).find("#post-likes-count");
    aHrefLike.toggleClass("liked");
    aHrefLike.toggleClass("heart");
    $.ajax({
        url: '/like/',
        type: 'POST',
        data: {
            'postId': postPk,
            'userId': userPk,
            csrfmiddlewaretoken: csrf,
        },
        success: function (data) {
            let likesCount = parseInt(data);
            smallTextLikesCount.text(likesCount);
        },
        error: function (data) {
            console.log(data);
        },
    });
    event.stopImmediatePropagation();
}

function openInNewTab(event, url) {
    var win = window.open(url, '_blank');
    win.focus();
    event.stopImmediatePropagation();
}

$('.dropdown-arrow').click(function (event) {
    // It solves problem of not opening the dropdown at first click.
    event.stopPropagation();
});

function stopPropagationForGivenPost(event, postId) {
    // It's used to show dropdown without trigerring 
    // onlick of whole post.
    $('#' + postId).dropdown();
    event.stopPropagation();
}

function stopPropagation(event) {
    event.stopPropagation();
}

// function stopImmediatePropagation(event) {
//     event.stopImmediatePropagation();
// }