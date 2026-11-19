"""Follow the public support journey in Chromium, locally or on GitHub Pages."""
from argparse import ArgumentParser
from contextlib import contextmanager, nullcontext
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.parse import urlsplit

from playwright.sync_api import expect, sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PAGES = "https://peytoncchen.github.io"


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


@contextmanager
def local_site():
    handler = partial(QuietHandler, directory=str(ROOT))
    with ThreadingHTTPServer(("127.0.0.1", 0), handler) as server:
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            yield f"http://127.0.0.1:{server.server_port}"
        finally:
            server.shutdown()
            thread.join()


def smoke(origin):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        live = origin == PAGES
        if not live:
            def local_request(route):
                if urlsplit(route.request.url).netloc == urlsplit(origin).netloc:
                    route.continue_()
                else:
                    route.abort()
            page.route("**/*", local_request)
        start = origin if live else origin + "/support/"
        response = page.goto(start, wait_until="domcontentloaded")
        if response is None or not response.ok:
            raise RuntimeError(f"Could not load {start}")
        if live:
            page.get_by_role("link", name="Support & privacy →", exact=True).click()
        expect(page).to_have_url(origin + "/support/")
        expect(page.get_by_role("heading", level=1, name="Support & privacy")).to_be_visible()
        for link, path, heading in [
            ("Glovebox help →", "/support/glovebox/", "A little help for the logbook."),
            ("Read the privacy policy →", "/support/glovebox/privacy/", "Privacy policy"),
        ]:
            page.get_by_role("link", name=link, exact=True).click()
            expect(page).to_have_url(origin + path)
            expect(page.get_by_role("heading", level=1, name=heading, exact=True)).to_be_visible()
        browser.close()
    print(f"Passed support journey from {start} through {path}")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="read the published GitHub Pages site")
    with (nullcontext(PAGES) if parser.parse_args().live else local_site()) as base_url:
        smoke(base_url)
