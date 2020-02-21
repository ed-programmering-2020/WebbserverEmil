from django.utils.safestring import mark_safe


def get_url_tag(url):
    return mark_safe('<a href="%s" target="_blank">go to</a>' % url)


def get_image_tag(image, complete=False):
    if complete is False:
        image = "/media/" + image.url

    return mark_safe('<img src="%s" height="50" />' % image)
