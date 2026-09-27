"""Template tags for rendering CMS-managed article copy."""
from django import template
from django.utils.html import escape, mark_safe

register = template.Library()

# Lines starting with any of these become bullet list items.
BULLET_PREFIXES = ('- ', '\u2022 ', '* ', '\u2013 ')


@register.filter
def rich_text(value):
    """Render plain CMS text as paragraphs plus bullet lists.

    - A blank line starts a new paragraph.
    - Consecutive plain lines are joined, so editors can wrap text freely.
    - Lines starting with "-", "*", an en dash or a bullet become <li> items.
    - Everything is HTML-escaped, so the output is always safe.
    """
    if not value:
        return ''

    out = []
    paragraph = []
    bullets = []

    def flush_paragraph():
        if paragraph:
            out.append('<p>%s</p>' % escape(' '.join(paragraph)))
            paragraph.clear()

    def flush_bullets():
        if bullets:
            items = ''.join('<li>%s</li>' % escape(item) for item in bullets)
            out.append('<ul>%s</ul>' % items)
            bullets.clear()

    for raw in str(value).splitlines():
        line = raw.strip()
        if not line:
            flush_paragraph()
            flush_bullets()
            continue

        prefix = next((p for p in BULLET_PREFIXES if line.startswith(p)), None)
        if prefix:
            flush_paragraph()
            bullets.append(line[len(prefix):].strip())
            continue

        flush_bullets()
        paragraph.append(line)

    flush_paragraph()
    flush_bullets()
    return mark_safe('\n'.join(out))
