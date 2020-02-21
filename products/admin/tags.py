from django.utils.safestring import mark_safe


def get_url_tag(url):
    return mark_safe('<a href="%s" target="_blank">go to</a>' % url)


def get_image_tag(image):
    return mark_safe('<img src="/media/%s" height="50" />' % image)


def get_spec_list_tag(spec_list):
    tags = ""

    for specs in spec_list:
        tags += "<ul>"
        for spec in specs:
            tags += "<li><p style='font-weight: bold;'>%s</p> %s</li>" % spec
        tags += "</ul>"

    return mark_safe(tags)
