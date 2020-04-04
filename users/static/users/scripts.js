function send_like(event, post_pk, user_pk, a_id, csrf) {
    const aHrefLike = $('#' + a_id);
    const isLiked = aHrefLike.hasClass('liked');
    const smallTextLikesCount = $('#' + a_id).find("#post-likes-count");
    aHrefLike.toggleClass("liked");
    aHrefLike.toggleClass("heart");
    $.ajax({
        url: '/like/',
        type: 'POST',
        data: {
            'post_pk': post_pk,
            'user_pk': user_pk,
            csrfmiddlewaretoken: csrf,
        },
        success: function (data) {
            console.log(data);
            let likes_count = JSON.parse(data)["likes_count"];
            let likesCount = parseInt(likes_count);
            smallTextLikesCount.text(likesCount);
        },
        error: function (data) {
            console.log(data);
        },
    });
    event.stopImmediatePropagation();
}

function follow_user(event, follower_id, followed_id, is_from_modal, a_id, csrf) {
    const aHrefFollow = $('#' + a_id);
    if (is_from_modal) {
        aHrefFollow.toggleClass("purple-btn-outline-modal");
    } else {
        aHrefFollow.toggleClass("purple-btn-outline");
    }
    aHrefFollow.toggleClass("purple-btn");
    aHrefFollow.text((aHrefFollow.text() == 'Follow') ? 'Following' : 'Follow');
    $.ajax({
        url: '/follow/',
        type: 'POST',
        data: {
            'follower_id': follower_id,
            'followed_id': followed_id,
            csrfmiddlewaretoken: csrf,
        },
        success: function (data) {
            console.log(data);
            if (is_from_modal) {
                return
            }
            data = JSON.parse(data);
            followers = data["followers"];
            following = data["following"];
            console.log(data["following"]);
            $('#followers-count').text(followers);
            $('#following-count').text(following);
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

function stopImmediatePropagation(event) {
    event.stopImmediatePropagation();
}