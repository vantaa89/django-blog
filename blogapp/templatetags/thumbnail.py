from django import template
import re

register = template.Library()


def get_thumbnail(content):
    match = re.search(r'!\[\]\(\S*\)', content)
    # find the first image link that appears in the content
    if match is not None:
        st = match.group()
        start_idx = st.find('(')
        return str(st[start_idx+1:-1])
    else:
        return '/static/placeholder.jpeg'

register.filter('thumbnail', get_thumbnail)