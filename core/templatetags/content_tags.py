"""Template tags for rendering CMS-managed article copy."""
import re

from django import template
from django.utils.html import escape, mark_safe

register = template.Library()

# Gold gradient used for the accented words in the homepage headline.
HERO_GRADIENT = (
    'text-transparent bg-clip-text bg-gradient-to-r '
    'from-lacd-gold via-amber-300 to-amber-400'
)
# ``**words**`` is emphasised: gold gradient in the hero headline, bold in articles.
BOLD = re.compile(r'\*\*(.+?)\*\*')
HERO_ACCENT = BOLD

# Lines starting with any of these become bullet list items.
BULLET_PREFIXES = ('- ', '\u2022 ', '* ', '\u2013 ')


def _inline(text):
    """Escape HTML, then turn ``**bold**`` markers into <strong> tags."""
    return BOLD.sub(lambda match: '<strong>%s</strong>' % match.group(1), escape(text))


@register.filter
def rich_text(value):
    """Render plain CMS text as paragraphs plus bullet lists.

    - A blank line starts a new paragraph.
    - Consecutive plain lines are joined, so editors can wrap text freely.
    - Lines starting with "-", "*", an en dash or a bullet become <li> items.
    - Words wrapped in ``**`` become bold, so section headings stand out.
    - Everything is HTML-escaped first, so the output is always safe.
    """
    if not value:
        return ''

    out = []
    paragraph = []
    bullets = []

    def flush_paragraph():
        if paragraph:
            out.append('<p>%s</p>' % _inline(' '.join(paragraph)))
            paragraph.clear()

    def flush_bullets():
        if bullets:
            items = ''.join('<li>%s</li>' % _inline(item) for item in bullets)
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


@register.filter
def hero_headline(value):
    """Render the CMS 'Hero Text' homepage headline.

    - A new line becomes a line break that is hidden on phones, matching the
      markup the section used before it was editable.
    - Words wrapped in ``**`` are shown in the gold gradient.
    - Everything is HTML-escaped first, so the output is always safe.
    """
    if not value:
        return ''

    lines = []
    for raw in str(value).splitlines():
        line = raw.strip()
        if not line:
            continue
        safe = escape(line)
        safe = HERO_ACCENT.sub(
            lambda match: '<span class="%s">%s</span>' % (HERO_GRADIENT, match.group(1)),
            safe,
        )
        lines.append(safe)

    if not lines:
        return ''
    return mark_safe(' <br class="hidden sm:inline">\n'.join(lines))
