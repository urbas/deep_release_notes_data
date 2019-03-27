#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `deep_release_notes` package."""

from click.testing import CliRunner
from deep_release_notes import cli
from deep_release_notes.cli import find_latest_project_id


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
    latest_project_id = find_latest_project_id(["projects-0-123.json", "projects-234-345.json", "projects-123-234.json"])
    assert latest_project_id == 345


def test_find_latest_project_id_incorrect():
    latest_project_id = find_latest_project_id(["projects--123.json"])
    assert latest_project_id is None
