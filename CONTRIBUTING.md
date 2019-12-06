## Contributing to Briar GTK

Thank you for looking in this file!

When contributing to the development of Briar GTK, please first discuss the change you wish to make via issue, email, or any other method with the maintainers before making a change.

If you have any questions regarding the use or development of Briar GTK,
want to discuss design or simply hang out, please join us in [Briar's Mattermost chat](https://chat.briarproject.org/), [#briar on freenode.net](irc://freenode.net/#briar) or [the bridge to the Matrix network](https://matrix.to/#/#freenode_#briar:matrix.org).

Please note we have a [code of conduct](/code-of-conduct.md), please follow it in all your interactions with the project.

## Source repository

Briar GTK's main source repository is at [code.briarproject.org/nicoalt/briar-gtk](https://code.briarproject.org/nicoalt/briar-gtk).

Development happens in the master branch.

If you need to publish a branch, feel free to do it at any
publically-accessible Git hosting service, although code.briarproject.org
makes things easier for the maintainers.

## Style

We use pycodestyle and pylint for code formatting and we enforce it on the GitLab CI server.

## Running the test suite

You can run the tests with the script at [tools/run-tests.sh](tools/run-tests.sh).

# Issues, issues and more issues!

There are many ways you can contribute to Briar GTK, and all of them involve creating issues
in [Briar GTK's issue tracker](https://code.briarproject.org/nicoalt/briar-gtk/issues). This is the entry point for your contribution.

To create an effective and high quality ticket, try to put the following information on your
ticket:

 1. A detailed description of the issue or feature request
     - For issues, please add the necessary steps to reproduce the issue.
     - For feature requests, add a detailed description of your proposal.
 2. A checklist of Development tasks
 3. A checklist of Design tasks
 4. A checklist of QA tasks

## Issue template
```
[Title of the issue or feature request]

Detailed description of the issue. Put as much information as you can, potentially
with images showing the issue or mockups of the proposed feature.

If it's an issue, add the steps to reproduce like this:

Steps to reproduce:

1. Open Briar GTK
2. Do an Action
3. ...

## Design Tasks

* [ ]  design tasks

## Development Tasks

* [ ]  development tasks

## QA Tasks

* [ ]  qa (quality assurance) tasks
```

## Merge Request Process

1. Ensure your code compiles.
2. Ensure the test suit passes. Run `tools/run-tests.sh`.
3. If you're adding new API, it must be properly documented.
4. The commit message has to be formatted as follows:
   ```
   component: <summary>

   A paragraph explaining the problem and its context.

   Another one explaining how you solved that.

   <link to the bug ticket>
   ```
5. You may merge the merge request once you have the sign-off of the maintainers, or if you
   do not have permission to do that, you may request the second reviewer to merge it for you.

## Code of Conduct

We follow the [GNOME Foundation Code of Conduct](/code-of-conduct.md).
