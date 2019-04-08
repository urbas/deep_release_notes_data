ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}-slim

ENV SRC_DIR=/sources
WORKDIR ${SRC_DIR}

RUN apt-get update && apt-get install --no-install-recommends -y \
    git \
 && rm -rf /var/lib/apt/lists/*

ADD setup.py README.rst HISTORY.rst ${SRC_DIR}/
RUN pip install --no-cache-dir -e ${SRC_DIR}

ADD . ${SRC_DIR}

# NB: Prevents docker from creating __pycache__ directories that are owned by root
ENV PYTHONDONTWRITEBYTECODE=true

VOLUME [ "/data", "/github_conf" ]

ENV GITHUB_CONF_DIR=/github_conf
ENV DRN_SEARCH_OUTPUT_DIR=/data/search
ENV DRN_REPOS_OUTPUT_DIR=/data/repos

ENTRYPOINT [ "deep-release-notes-data" ]
CMD deep-release-notes-data --help