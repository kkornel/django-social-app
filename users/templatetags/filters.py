import datetime
import logging
import re
from datetime import date

from django import template
from django.utils import timezone
from django.utils.safestring import mark_safe  # import function

from social.models import Post
from users.admin import User
from users.models import Profile
"""
https://docs.djangoproject.com/en/2.2/howto/custom-template-tags/

Do not forget to load it:

{% load tag_filter_name %}

{{ post.content|render_content }}
"""

logger = logging.getLogger(__name__)

register = template.Library()


def generate_link(link):
    htpplink = link
    if not link.startswith('http'):
        htpplink = 'http://' + link
    return f'<a class="link" target="_blank" href="{htpplink}">{link}</a>'


def generate_hashtag_link(tag):
    # Free to configure the URL the way adapted your project
    url = "/tags/{}/".format(tag)
    return f'<a class="hashtag" href="{url}">#{tag}</a>'


@register.filter
def render_tags(obj):
    text = re.sub(r"#(\w+)", lambda m: generate_hashtag_link(m.group(1)), obj)
    # If you want Django to mark it as safe content, you can do the following:
    return mark_safe(text)


@register.filter
def render_links(obj):
    logger.debug(obj)
    text = mark_safe(
        re.sub(
            r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*",
            lambda m: generate_link(m.group(0)), obj))
    return mark_safe(text)


@register.filter
def render_tags_and_links(obj):
    text = re.sub(r"#(\w+)", lambda m: generate_hashtag_link(m.group(1)), obj)
    # return re.sub(r"(?P<url>https?://[^\s]+)", lambda m: generate_link(m.group(1)), text)

    # If you want Django to mark it as safe content, you can do the following:
    return mark_safe(
        re.sub(
            r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*",
            lambda m: generate_link(m.group(0)), text))


@register.simple_tag
def has_user_commented(userId, postId):
    try:
        user = User.objects.get(pk=userId)
        profile = user.profile
        post = Post.objects.get(pk=postId)
        has_commented = post.comments.all().filter(author=profile).count() > 0
        return has_commented
    except Exception:
        return False


@register.simple_tag
def is_already_following(followerID, followingID):
    try:
        follower = Profile.objects.get(pk=followerID)
        following = Profile.objects.get(pk=followingID)
        is_following = follower.is_following(following)
        return is_following
    except Exception:
        return False


@register.filter(name='get_class')
def get_class(value):
    return value.__class__.__name__


@register.filter
def time_since_date_posted(obj):
    if obj is not None:
        diff = timezone.now() - obj
        s = diff.seconds
        if diff.days > 30 or diff.days < 0:
            return obj.strftime('Y-m-d H:i')
        elif diff.days == 1:
            return 'One day ago'
        elif diff.days > 1:
            return '{} days ago'.format(diff.days)
        elif s <= 1:
            return 'just now'
        elif s < 60:
            return '{} seconds ago'.format(s)
        elif s < 120:
            return 'one minute ago'
        elif s < 3600:
            return '{} minutes ago'.format(round(s / 60))
        elif s < 7200:
            return 'one hour ago'
        else:
            return '{} hours ago'.format(round(s / 3600))
    else:
        return None
