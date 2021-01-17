from django import template

register = template.Library()

@register.simple_tag
def url(value, field_name, urlencode=None):
    u = '?{}={}'.format(field_name,value)

    if  urlencode:
        qs=urlencode.split('&')
        searched_qs= filter(lambda p: p.split('=')[0]!=field_name, qs)
        encoded_qs= '&'.join(searched_qs)
        u= '{}&{}'.format(u, encoded_qs)

    return u
