# How to contribute

## Git and GitHub Flow

> Git is a version control system for tracking changes in computer files and coordinating work on those files among multiple people. It is primarily used for source code management in software development.
> - [wikipedia](https://en.wikipedia.org/wiki/Git)

In genomics-workspace, we use git and GitHub flow. If you didn't know git or GitHub before, check following resources:

- [Try Git: Git Tutorial](https://try.github.io/) provided by GitHub
- [Understanding the GitHub Flow](https://guides.github.com/introduction/flow/) within 5 minutes
- [Git and GitHub learning resources](https://help.github.com/articles/git-and-github-learning-resources/)

## Django

Genomics-workspace is a django website project, so you need to know django before any contribusion. There are many useful resoures available. If you didn't know django before, check the [official tutorial](https://docs.djangoproject.com/en/1.11/intro/) and [tutorials by django girls](https://tutorial.djangogirls.org/en/) first. One thing you need to note when you read any resource related to django is that currently, we use django 1.11.

## Coding Style

This section describes our coding style guide. Our main rule is straightforward:

> All code in any code-base should look like a single person typed it, no matter how many people contributed.
> —[idiomatic.js](https://github.com/rwaldron/idiomatic.js/)

To make things easier, we adopt linters and code formatters together. Therefore, you only need to make sure code you contribute pass all the checks of linters, and run the code formatters for files you modify before commit the changes. Because most of the code base of this project are written in Python and JavaScript, currently we only restrict the code style of these two programming language, but we will exapand this ideas to other part of this project. For Python code, we use [yapf](https://github.com/google/yapf) as code formatter. For JavaScript code, we use [JSHint](http://jshint.com/) as linter and [prettier](https://github.com/prettier/prettier) as code formatter. Detailed usages are summarized below:

- Use `yapf path_to_py_file_you_want_format.py` to format a Python file. You may want to use option `-i` to write the formatted file in-place.
- Use `npx jshint --show-non-errors path_to_js_file_you_want_check.js` to lint the JavaScript file.
- Use `npx prettier path_to_js_file_you_want_check.js` to format a js file. You may want to use option `--write` to write the formatted file in-place.
