.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/urbas/deep_release_notes_data/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/urbas/deep_release_notes_data/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `deep_release_notes_data` for local development.

1. Fork the `deep_release_notes_data` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/deep_release_notes_data.git

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development::

    $ mkvirtualenv deep_release_notes_data
    $ cd deep_release_notes_data/
    $ python setup.py develop

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and the
   tests, including testing other Python versions with tox::

    $ flake8 deep_release_notes_data tests
    $ python setup.py test or py.test
    $ tox

   To get flake8 and tox, just pip install them into your virtualenv.

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Tips
----

To run a subset of tests::

$ py.test tests.test_deep_release_notes_data


Repeatable development environment
----------------------------------

You can start a repeatable development environment with docker. Simply invoke this::

$ docker build -t deep_release_notes_data --build-arg=PYTHON_VERSION=$(< .python-version) .

Now you can search for release notes on GitHub::

$ docker run -v "/tmp/deep_release_notes_data:/data" -v "$HOME/.github:/github_conf" -it deep_release_notes_data -v find-all --size=10000

And then clone repositories that contain release notes::

$ docker run -v "/tmp/deep_release_notes_data:/data" -it deep_release_notes_data -v clone-found-repos


Deploying
---------

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed (including an entry in HISTORY.rst).
Then run::

$ bumpversion patch # possible: major / minor / patch
$ git push
$ git push --tags

Travis will then deploy to PyPI if tests pass.
