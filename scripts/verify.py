#!/usr/bin/env python3
"""Validate published HTML and local references without network or runtime edits."""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids, self.links, self.errors = set(), [], []
        self.dynamic = False
        self.title = self.lang = False
        self.feed(text)
        self.close()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.dynamic |= tag == 'x-dc'
        self.title |= tag == 'title'
        self.lang |= tag == 'html' and bool(attrs.get('lang'))
        if attrs.get('id'):
            if attrs['id'] in self.ids and not self.dynamic:
                self.errors.append('duplicate id: ' + attrs['id'])
            self.ids.add(attrs['id'])
        for name in ('src', 'href'):
            if attrs.get(name):
                self.links.append(attrs[name])

    handle_startendtag = handle_starttag


def target(root, source, value):
    url = urlsplit(value)
    if url.scheme or url.netloc:
        return None
    path = unquote(url.path)
    resolved = ((root / path.lstrip('/')) if path.startswith('/') else source.parent / path).resolve() if path else source.resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise ValueError('reference escapes the site: ' + value)
    if resolved.is_dir():
        resolved /= 'index.html'
    if not resolved.is_file():
        raise ValueError('missing local reference: ' + value)
    return resolved, unquote(url.fragment)


def verify(root):
    root = Path(root).resolve()
    files = [root / 'index.html', *sorted((root / 'support').rglob('*.html'))]
    pages, errors = {}, []
    for path in files:
        if not path.is_file():
            errors.append(f'{path.relative_to(root)}: required page missing')
            continue
        page = pages[path] = Page(path.read_text())
        if not page.title or not page.lang:
            page.errors.append('page needs a title and document language')
        errors.extend(f'{path.relative_to(root)}: {error}' for error in page.errors)
    for path, page in pages.items():
        for value in page.links:
            try:
                resolved = target(root, path, value)
                if resolved and resolved[1] and resolved[0].suffix == '.html':
                    destination = pages.get(resolved[0]) or Page(resolved[0].read_text())
                    # Conditional x-dc routes/IDs are materialized by the generated
                    # runtime; source IDs are not a rendered navigation contract.
                    if not destination.dynamic and resolved[1] not in destination.ids:
                        raise ValueError('missing local fragment: ' + value)
            except ValueError as error:
                errors.append(f'{path.relative_to(root)}: {error}')
    for path in (root / 'support').rglob('*.css'):
        for value in re.findall(r'url\(\s*[\'\"]?([^\)\'\"]+)[\'\"]?\s*\)', path.read_text()):
            try:
                target(root, path, value.strip())
            except ValueError as error:
                errors.append(f'{path.relative_to(root)}: {error}')
    return len(pages), errors


if __name__ == '__main__':
    count, errors = verify(ROOT)
    for error in errors:
        print(error, file=sys.stderr)
    print(f'Static verification: {count} published pages, {len(errors)} errors; external URLs, dynamic route fragments and browser rendering are separate checks.')
    raise SystemExit(bool(errors))
