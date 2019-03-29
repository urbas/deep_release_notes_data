# -*- coding: utf-8 -*-

"""Console script for deep_release_notes."""
import click
from datetime import datetime
import logging
from pathlib import Path
import re
import requests
import sys
from time import sleep


@click.group()
def main():
    logging.basicConfig(
        format="[%(levelname)s %(asctime)s|%(filename)s:%(lineno)d] %(message)s",
        level=logging.INFO,
    )


@main.command(name="get-projects")
def get_projects():
    get_projects_since()


@main.command(name="find")
@click.argument("file_name")
def find(file_name):
    http_session = get_github_session()
    downloaded_files = get_files_in_cur_dir()
    next_page = (find_last_page(downloaded_files) or 0) + 1
    while True:
        logging.info("Finding %s file. Page %s...", file_name, next_page)
        response = github_find_file_in_repos(http_session, file_name, next_page)
        if response.status_code == 403 and "Retry-After" in response.headers:
            retry_after = int(response.headers["Retry-After"])
            logging.info("Reached rate limit. Waiting for %s seconds.", retry_after)
            sleep(retry_after)
            logging.info("Retrying now...")
            # It looks like we have to reset the session after we get rate limited
            http_session = get_github_session()
            continue
        else:
            response.raise_for_status()
        write_page_file(file_name, next_page, response.text)
        logging.info(
            "Found %s %s files on page %s.",
            len(response.json()["items"]),
            file_name,
            next_page,
        )
        next_page = get_next_page(response.headers)
        pause = get_request_pause(response.headers)
        if pause:
            pause += 0.5
            logging.info("Sleeping for %s seconds to avoid being rate-limited.", pause)
            sleep(pause)


def github_find_file_in_repos(http_session, file_name, page):
    return http_session.get(
        "https://api.github.com/search/code",
        params={"q": f"{file_name} in:path path:/", "page": page},
    )


def get_projects_since():
    http_session = get_github_session()
    downloaded_files = get_files_in_cur_dir()
    since_id = find_latest_project_id(downloaded_files) or 0
    while True:
        logging.info("Downloading projects since ID %s...", since_id)
        response = http_session.get(
            "https://api.github.com/repositories", params={"since": since_id}
        )
        response.raise_for_status()
        until_id = response.json()[-1]["id"]
        write_projects_file(since_id, until_id, response.text)
        logging.info("Downloaded projects since ID %s until ID %s.", since_id, until_id)
        since_id = until_id
        wait_if_close_to_rate_limit(response, 0.10)


def get_files_in_cur_dir():
    return [str(f) for f in Path().iterdir() if f.is_file()]


def wait_if_close_to_rate_limit(response, closeness_ratio):
    rate_limit = int(response.headers["X-RateLimit-Limit"])
    rate_limit_remaining = int(response.headers["X-RateLimit-Remaining"])
    if rate_limit_remaining / rate_limit < closeness_ratio:
        reset_time = datetime.utcfromtimestamp(
            int(response.headers["X-RateLimit-Reset"])
        )
        wait_seconds = (reset_time - datetime.utcnow()).seconds + 1
        logging.warning(
            "Closing in on the rate limit. Rate limit remaining is %s. "
            "Waiting %s seconds until rate limit reset.",
            rate_limit_remaining,
            wait_seconds,
        )
        sleep(wait_seconds)


def get_github_session():
    session = requests.Session()
    session.auth = tuple(
        Path.home().joinpath(".github", "access_token").read_text().splitlines()
    )
    return session


def write_projects_file(since_id, until_id, project_list_json_str):
    projects_file_name = f"projects-{since_id}-{until_id}.json"
    with open(projects_file_name, "w") as projects_file:
        projects_file.write(project_list_json_str)


def write_page_file(prefix, page, json_str):
    with open(f"{prefix}-{page}.json", "w") as projects_file:
        projects_file.write(json_str)


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


def find_last_page(downloaded_files):
    if not downloaded_files:
        return None
    pattern = re.compile(r"^.*-(?P<page>\d+).json$")
    pages = [
        int(m.group("page"))
        for m in [
            pattern.match(downloaded_file) for downloaded_file in downloaded_files
        ]
        if m is not None
    ]
    return max(pages) if pages else None


def get_next_page(response_headers):
    link_header = response_headers.get("Link")
    if link_header is None:
        return None
    match = re.search(r"&page=(\d+)>; rel=\"next\"", link_header)
    if match is None:
        return None
    return int(match.group(1))


def get_request_pause(response_headers, response_timestamp=None):
    response_timestamp = int(datetime.utcnow().timestamp()) if response_timestamp is None else response_timestamp
    rate_remaining = response_headers.get("X-RateLimit-Remaining")
    rate_reset_timestamp = response_headers.get("X-RateLimit-Reset")
    if not rate_remaining or not rate_reset_timestamp:
        return None
    return (float(rate_reset_timestamp) - float(response_timestamp)) / float(rate_remaining)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
