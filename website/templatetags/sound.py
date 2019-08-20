from django import template
register=template.Library()

@register.filter
def sounds(data):
    data =data.replace('&lt;','<')
    data =data.replace('&gt;','>')
    data =data.replace('&#39;','\'')
    data =data.replace('&quot;','"')
    data =data.replace('&amp;','&')
    return data