# -*- coding: utf-8 -*-

"""Console script for deep_release_notes."""
import click
import logging
from pathlib import Path
import re
import requests
import sys


@click.group()
def main():
    logging.basicConfig(
        format="[%(levelname)s %(asctime)s|%(filename)s:%(lineno)d] %(message)s",
        level=logging.INFO,
    )


@main.command(name="get-projects")
def get_projects():
    get_projects_since()


def get_projects_since():
    http_session = requests.session()
    downloaded_files = [str(f) for f in Path().iterdir() if f.is_file()]
    since_id = find_latest_project_id(downloaded_files) or 0
    while True:
        response = http_session.get(
            "https://api.github.com/repositories", params={"since": since_id}
        )
        response.raise_for_status()
        until_id = response.json()[-1]["id"]
        write_projects_file(since_id, until_id, response.text)
        logging.info("Downloaded projects since %s until %s.", since_id, until_id)
        since_id = until_id


def write_projects_file(since_id, until_id, project_list_json_str):
    projects_file_name = f"projects-{since_id}-{until_id}.json"
    with open(projects_file_name, "w") as projects_file:
        projects_file.write(project_list_json_str)


def find_latest_project_id(projects_files):
    if not projects_files:
        return None
    pattern = re.compile(r"projects-\d+-(?P<until_id>\d+).json")
    until_ids = [
        int(m.group("until_id"))
        for m in [pattern.match(projects_file) for projects_file in projects_files]
        if m is not None
    ]
    return max(until_ids) if until_ids else None


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
