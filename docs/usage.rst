=====
Usage
=====

To use Deep release notes in a project::

    import deep_release_notes

To download a list of release notes::

    deep-release-notes find-all

List all repository names and the paths to their release notes::

    cat */*/*.json | jq -r '.items[] | "\(.repository.full_name) \(.path)"' | sort | uniq | cat