=====
Usage
=====

To use Deep release notes in a project::

    import deep_release_notes_data

To download a list of release notes::

    deep-release-notes-data find-all

List all repository names and the paths to their release notes::

    cat */*/*.json | jq -r '.items[] | "\(.repository.full_name) \(.path)"' | sort | uniq | cat