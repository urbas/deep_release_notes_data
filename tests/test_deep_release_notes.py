#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `deep_release_notes` package."""
from datetime import datetime

from click.testing import CliRunner
from deep_release_notes import cli
from deep_release_notes.cli import (
    find_latest_project_id,
    get_next_page,
    find_last_page,
    get_request_pause,
)


def test_help():
    runner = CliRunner()
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "--help  Show this message and exit." in help_result.output


def test_find_latest_project_id_none():
    latest_project_id = find_latest_project_id(())
    assert latest_project_id is None


def test_find_latest_project_id_one():
    latest_project_id = find_latest_project_id(["projects-0-123.json"])
    assert latest_project_id == 123


def test_find_latest_project_id():
    latest_project_id = find_latest_project_id(
        ["projects-0-123.json", "projects-234-345.json", "projects-123-234.json"]
    )
    assert latest_project_id == 345


def test_find_latest_project_id_incorrect():
    latest_project_id = find_latest_project_id(["projects--123.json"])
    assert latest_project_id is None


def test_get_next_page_none():
    next_page = get_next_page({})
    assert next_page is None


def test_get_next_page():
    next_page = get_next_page(
        {
            "Link": '<https://api.github.com/search/code?q=releasenotes.md+in%3Apath+path%3A%2F&page=2>; rel="next", <https://api.github.com/search/code?q=releasenotes.md+in%3Apath+path%3A%2F&page=34>; rel="last"'
        }
    )
    assert next_page == 2


def test_get_next_page_first_not_next():
    next_page = get_next_page(
        {
            "Link": '<https://api.github.com/search/code?q=releasenotes.md+in%3Apath+path%3A%2F&page=2>; rel="blah", <https://api.github.com/search/code?q=releasenotes.md+in%3Apath+path%3A%2F&page=34>; rel="next"'
        }
    )
    assert next_page == 34


def test_get_next_page_wrong():
    next_page = get_next_page({"Link": "wrong!"})
    assert next_page is None


def test_find_last_page_none():
    assert find_last_page(()) is None


def test_find_last_incorrect():
    assert find_last_page(["dfhdj"]) is None


def test_find_last_page_one():
    assert find_last_page(["foo-123.json"]) == 123


def test_find_last_page():
    assert find_last_page(["foo-123.json", "mar-872.json", "boo-8.json"]) == 872


def test_get_request_pause_none():
    assert get_request_pause({}) is None


def test_get_request_pause():
    utc_epoch_now = int(datetime.utcnow().timestamp())
    reset_timestamp = utc_epoch_now + 60
    assert (
        get_request_pause(
            {
                "X-RateLimit-Remaining": "30",
                "X-RateLimit-Reset": str(reset_timestamp),
            },
            utc_epoch_now,
        )
        == 2
    )


def test_get_request_pause_some_remaining():
    utc_epoch_now = int(datetime.utcnow().timestamp())
    reset_timestamp = utc_epoch_now + 60
    assert (
        get_request_pause(
            {
                "X-RateLimit-Remaining": "10",
                "X-RateLimit-Reset": str(reset_timestamp),
            },
            utc_epoch_now,
        )
        == 6
    )
