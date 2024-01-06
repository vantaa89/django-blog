from django import template
from django.template.defaultfilters import stringfilter

import markdown as md
import re

register = template.Library()


@register.filter()
@stringfilter
def markdown(content):
    content = re.sub(r'\$(.*)\$', lambda match: match.group(0).replace('_', '<mathsubscript>'), content)    
    html_content = md.markdown(content, extensions=[
        'markdown.extensions.fenced_code',
        'markdown.extensions.codehilite',
        'markdown.extensions.nl2br',
        ])
    html_content = html_content.replace('<mathsubscript>', '_')
    return html_content
