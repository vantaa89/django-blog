from django import template
from django.template.defaultfilters import stringfilter

import markdown as md
import re

from blogapp.views import render_markdown

register = template.Library()


@register.filter()
@stringfilter
def markdown(content):
    return render_markdown(content)
