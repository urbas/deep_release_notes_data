#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `deep_release_notes_data` package."""
from datetime import datetime

from deep_release_notes_data.cli import (
    get_next_page,
    find_last_downloaded_page,
    get_request_pause,
)


def test_get_next_page_none():
    next_page = get_next_page({})
    assert next_page is None


def test_get_next_page():
    next_page = get_next_page(
        {
            "Link": '<https://api.github.com/search/code?q=releasenotes.md+in%3Apath+path%3A%2F&page=2>; rel="next", '
            '<https://api.github.com/search/code?q=releasenotes.md+in%3Apath+path%3A%2F&page=34>; rel="last"'
        }
    )
    assert next_page == 2


def test_get_next_page_first_not_next():
    next_page = get_next_page(
        {
            "Link": '<https://api.github.com/search/code?q=releasenotes.md+in%3Apath+path%3A%2F&page=2>; rel="blah", '
            '<https://api.github.com/search/code?q=releasenotes.md+in%3Apath+path%3A%2F&page=34>; rel="next"'
        }
    )
    assert next_page == 34


def test_get_next_page_params():
    next_page = get_next_page(
        {
            "Link": "<https://api.github.com/search/code?q=CHANGELOG.rst+in%3Apath+path%3A%2F+size%3A%3E6000&page=2&"
            'sort=indexed>; rel="prev", <https://api.github.com/search/code?q=CHANGELOG.rst+in%3Apath+path%3A%2F+'
            'size%3A%3E6000&page=4&sort=indexed>; rel="next", <https://api.github.com/search/code?q=CHANGELOG.rst+'
            'in%3Apath+path%3A%2F+size%3A%3E6000&page=34&sort=indexed>; rel="last", '
            "<https://api.github.com/search/code?q=CHANGELOG.rst+in%3Apath+path%3A%2F+size%3A%3E6000&page=1&"
            'sort=indexed>; rel="first"'
        }
    )
    assert next_page == 4


def test_get_next_page_wrong():
    next_page = get_next_page({"Link": "wrong!"})
    assert next_page is None


def test_find_last_page_none():
    assert find_last_downloaded_page(()) is None


def test_find_last_incorrect():
    assert find_last_downloaded_page(["dfhdj"]) is None


def test_find_last_page_one():
    assert find_last_downloaded_page(["foo-123.json"]) == 123


def test_find_last_page():
    assert (
        find_last_downloaded_page(["foo-123.json", "mar-872.json", "boo-8.json"]) == 872
    )


def test_get_request_pause_none():
    assert get_request_pause({}) is None


def test_get_request_pause():
    utc_epoch_now = int(datetime.utcnow().timestamp())
    reset_timestamp = utc_epoch_now + 60
    assert (
        get_request_pause(
            {"X-RateLimit-Remaining": "30", "X-RateLimit-Reset": str(reset_timestamp)},
            utc_epoch_now,
        )
        == 2
    )


def test_get_request_pause_some_remaining():
    utc_epoch_now = int(datetime.utcnow().timestamp())
    reset_timestamp = utc_epoch_now + 60
    assert (
        get_request_pause(
            {"X-RateLimit-Remaining": "10", "X-RateLimit-Reset": str(reset_timestamp)},
            utc_epoch_now,
        )
        == 6
    )
