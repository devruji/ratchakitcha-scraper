#!/usr/bin/env python3
"""
Download a monthly report from ratchakitcha.soc.go.th using Playwright.
"""

import argparse
import logging

from typing import cast
from datetime import date
from pathlib import Path
from typing import Optional

from playwright.sync_api import (
    sync_playwright,
    Browser,
    Page,
    TimeoutError as PlaywrightTimeoutError,
    ViewportSize,
)

# ─── Configuration ──────────────────────────────────────────────────────────────

REPORT_URL = "https://ratchakitcha.soc.go.th"
SELECTORS = {
    "cookie_btn": "button:has-text('ยอมรับ')",
    "old_filter": "text=คัดกรองแบบเดิม",
    "month_dropdown": "#monthlyreport_month",
    "download_btn": ".btn-monthly-report",
}
VIEWPORT: ViewportSize = cast(
    ViewportSize,
    {"width": 1280, "height": 1024},
)
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/115.0.0.0 Safari/537.36"
)
PLAYWRIGHT_ARGS = [
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--disable-dev-shm-usage",
]


# ─── Helpers ────────────────────────────────────────────────────────────────────


def calculate_month_index(target_month: int) -> str:
    """
    Convert a calendar month (1–12) into dropdown index:
      0 = this month, 1 = last month, …, 11 = 11 months ago.
    Raises ValueError if month is out of range.
    """
    if not 1 <= target_month <= 12:
        raise ValueError("`target_month` must be between 1 and 12")
    today = date.today().month
    return str((today - target_month) % 12)


def configure_logging():
    """Set up the root logger with a basic format."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def _accept_cookies(page: Page):
    """Click the cookie banner if it appears."""
    if page.locator(SELECTORS["cookie_btn"]).count():
        logging.info("Accepting cookie banner")
        page.click(SELECTORS["cookie_btn"])


def _switch_to_old_filter(page: Page):
    """Toggle to the legacy filter UI if available."""
    if page.locator(SELECTORS["old_filter"]).count():
        logging.info("Switching to old filter UI")
        page.click(SELECTORS["old_filter"])


# ─── Core ───────────────────────────────────────────────────────────────────────


def download_month_report(
    target_month: int, download_dir: Path, headless: bool = True
) -> Path:
    """
    Download the monthly report for `target_month` into `download_dir`.

    Returns:
        Path to the saved report file.
    """
    download_dir.mkdir(parents=True, exist_ok=True)
    month_index = calculate_month_index(target_month)
    logging.info("Month %d → dropdown index %s", target_month, month_index)

    playwright = sync_playwright().start()
    browser: Optional[Browser] = None

    try:
        browser = playwright.chromium.launch(headless=headless, args=PLAYWRIGHT_ARGS)
        context = browser.new_context(
            accept_downloads=True,
            viewport=VIEWPORT,
            user_agent=USER_AGENT,
        )
        page = context.new_page()
        page.set_default_navigation_timeout(60000)
        page.set_default_timeout(60000)

        logging.info("Navigating to %s", REPORT_URL)
        page.goto(REPORT_URL, wait_until="networkidle")

        _accept_cookies(page)
        _switch_to_old_filter(page)

        logging.info("Waiting for month selector")
        try:
            page.wait_for_selector(
                SELECTORS["month_dropdown"], state="visible", timeout=20000
            )
        except PlaywrightTimeoutError:
            raise RuntimeError(f"Could not find {SELECTORS['month_dropdown']} on page")

        logging.info("Selecting month index %s", month_index)
        page.select_option(SELECTORS["month_dropdown"], value=month_index)

        logging.info("Triggering download")
        with page.expect_download() as dl_info:
            page.click(SELECTORS["download_btn"])
        download = dl_info.value

        dest = download_dir / download.suggested_filename
        download.save_as(str(dest))
        logging.info("Report saved to %s", dest)
        return dest

    finally:
        if browser:
            browser.close()
        playwright.stop()


# ─── CLI ────────────────────────────────────────────────────────────────────────


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-m",
        "--month",
        type=int,
        required=True,
        help="Target month number (1=Jan … 12=Dec)",
    )
    parser.add_argument(
        "-o",
        "--out-dir",
        type=Path,
        default=Path.cwd() / "downloads",
        help="Directory to save the report",
    )
    parser.add_argument(
        "-hl",
        "--headless",
        action="store_true",
        help="Run browser in headless mode (default: False)",
    )
    return parser.parse_args()


def main():
    configure_logging()
    args = parse_args()
    download_month_report(args.month, args.out_dir, headless=args.headless)


if __name__ == "__main__":
    main()
