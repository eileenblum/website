Source Files for the Outdex Blog
================================

This repository holds the source files for the Outdex blog.
They are simple markdown files that are automatically converted to HTML via [Pelican](http://docs.getpelican.com/), a static website generator implemented in Python.
We use the `pandoc_reader` plugin to get access to the [pandoc dialect](https://pandoc.org/MANUAL.html#pandocs-markdown) instead of basic markdown.
Whenever a new commit is pushed to the repository, the source files are automatically converted and deployed by [Netlify](https://www.netlify.com).

Branches
--------

The repository uses the following standardized branches:

- `master` holds the source files from which the public-facing part of outdex is built.
  Only administrators may push to `master`.
- `staging` is used for testing new features before they are rolled out.
  The staging branch is automatically deployed at `https://staging.outdex.xyz`.

New posts should be submitted as pull requests from a forked repository.

Cloning the repository
----------------------

1. Create a fork
1. Use `git clone` to clone your fork.
1. Work in your local repository as usual and sync changes to your fork.
1. When you're done, file a pull request so that we can merge in your contribution.

The themes folder contains our [custom fork](https://github.com/outde-xyz/Flex) of the [flex theme](https://github.com/alexandrevicenzi/Flex).
The fork is not incorporated as a submodule, as this proved too much of a headache to manage correctly.
Yes, that's against best practices, but our fork of the theme changes so rarely that this isn't an issue in practice.

File Structure
--------------

Once you've cloned the repository, you'll see a couple of files and folders.
The most important ones are:

- `content`: the markdown files for the website
- `output`: the actual website generated by Pelican
- `pelicanconf.py`: contains various settings for site creation; do not change unless you know what you're doing
- `publishconf.py`: allows you to override certain settings in the final creation phase; do not change unless you know what you're doing
- `Makefile`: set of instructions for building the website

As an author, only `content` is of interest to you.

Workflow
--------

Creating a new post is easy if you're already familiar with the usual Github workflow.

1.  In the local clone of your forked repo, go to the folder `content` and then the folder for the appropriate category (`Discussions`, `News`, or `Tutorials`).
1.  Create a new markdown file.
1.  Make sure the markdown file starts with a well-formed YAML header of the following form:
    ```
    ---
    title: >-
        Title of post, with normal capitalization
    series: >-
        only for use with multipart posts
    authors:
        - author1
        - author2
    date: YYYY-MM-DD
    modified: YYYY-MM-DD (only used when updating an existing post)
    bibliography: some_bib_file.bib (if you use citations)
    toc: true (if you want a table of contents)
    tags:
        - tag1
        - tag2
    ---
    ```
1.  Look at other posts in the repo for concrete examples.
1.  Once you are done writing, make a commit in the usual fashion:
    ```
    git add .
    git commit -m "some description"
    git push origin master
    ```
1.  File a pull request against our repo.
    Netlify will automatically deploy your commit.
    It also adds a message to your pull request with a link to the deployed commit.
    Follow the link to check that your submission compiled correctly.
1.  If anything is wrong, make the appropriate changes in your fork and sync.
    The pull request will be updated automatically.
1.  Once you're happy, add an approval message to the pull request (e.g. *ready for publication*).
    At this point, we will merge it into the `master` branch.
    Netlify will then deploy the `master` branch and your post will be visible at `https://outde.xyz`.

It may sound complicated, but you'll quickly get the hang of it.

System Requirements
-------------------

Outdex is now hosted on [Netlify](https://www.netlify.com), which offers better build tools with automatic deployment.
So there is no longer any need for a local build environment, commits are automatically deployed by Netlify and each pull request comes with a live preview.

The list below is largely for future reference in case the build environment needs to be recreated from scratch.

1.  Python 3.6 or higher.

1.  Pelican 4.0 or higher.
    
    - Linux users might already have it their repository.
    - On OSX and Windows (and Linux, if necessary) you can install Pelican via Python's package manager `pip` (but see the next section on how to use `pip` in a smarter way).

    ~~~~~
    pip install pelican
    ~~~~~

1.  The `ghp-import` script is no longer needed. 
    GitHub pages has been abandoned in favor of Netlify.
    If desired, you can install `gph-import` via pip

    ~~~~~
    pip install ghp-import
    ~~~~~

    or use your package manager if you're on Linux.

1.  A number of Python3 libraries:
    - `markdown`, version 3.0 or higher
    - `pygments`, version 2.3 or higher
    - `typogrify` library, version 2.0.7 or higher
    - *beautifulsoup4*, version 4.7 or higher; in Debian, the library is called `python3-bs4`

    As before, use pip or your package manager to install these dependencies.

1.  At least version 2.2 of `pandoc` and 0.14 of `pandoc-citeproc`.
    Linux users should definitely install those from their repositories.
    Everybody else is referred to [pandoc's install guide](https://pandoc.org/installing.html).

1.  A recent-ish version of the `make` tool.
    This is usually already installed on Linux and OSX.
    If it isn't, make sure you have the basic tools for compiling software installed.
    On Debian and Ubuntu, the following should work:

    ~~~~
    sudo aptitutde install build-essential
    ~~~~

    On Windows, install [GnuWin32](http://gnuwin32.sourceforge.net/packages/make.htm) or [MinGW](http://www.mingw.org/).
    The `make` binary also has to be in your PATH, which happens automatically on Linux and OSX but not Windows.
    

A Note on `pip` Installations
------------------------------

Python's `pip` has the nasty habit of scattering the install files across various system folders.
A better solution is to create a *virtual environment* in your home directory that holds all the files related to working with pelican:

~~~~~
mkdir ~/.outdex_env
python3 -m venv ~/.outdex_env
~/.outdex_env/bin/pip3 install pelican ghp-import markdown pygments typogrify beautifulsoup4
~~~~~

You then have to make the pelican script accessible through your shell, either by adding `~/.outdex_env` to your PATH or by symlinking it to a folder in your PATH (e.g. `/usr/local/bin` or `~/.local/bin`).


Technical issues
----------------

Our version of the `pandoc_reader` plugin contains several fixes and extensions.

1.  The default version breaks Pelican's `{filename}`-hooks because of how pandoc versions after 1.15.0 mangle curly braces.
    The version in our repo has a minor workaround to fix this.
    In `pandoc_reader.py`, 

    ```python
    return output, metadata
    ```

    has been expanded to

    ```python
    output = output.replace('%7Bfilename%7D','{filename}')
    return output, metadata
    ```

1.  The plugin now uses Python's `frontmatter` package to extract YAML headers.
    It then preprocesses them and passes them on to Pelican.
    This makes it easy to pass parameters to pandoc (e.g. CLS and bib-files), and we'll also be able to create PDFs from the same source files.

1.  We also process custom edge markers to auto-extract the summary.

To Do
-----

- [x] set up email for submissions (hosted by Zoho)
- [ ] fix summary breaking math; should always end immediately after first paragraph
- [x] ~~maybe switch commenting system to `staticman`?~~ We're now using [talkyard](https://www.talkyard.io/)
- [x] expand pandoc reader to handle Pelican's `{filename}`-hooks
- [ ] adapt filter for pandoc to automatically include tikz and forest code as svgs; this will be tricky because Netlify has no official Latex support
- [ ] design pandoc filter for converting glossed examples to HTML tables
- [ ] Categories should not be treated as tags
- [ ] automatically convert posts to PDF and embed download link
- [x] create favicon from logo
