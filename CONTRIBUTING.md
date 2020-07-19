Contributing to bettingtool
=======================

Thanks for taking the time to contribute! :)

The following is a set of guidelines for contributing to bettingtool project, which is hosted in the [bettingtool repository](https://github.com/soote1/bettingtool) on GitHub. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

Table of Contents
=======================

* [What should I know before I get started?](#what-should-i-know-before-i-get-started)
* [How can I contribute?](#how-can-i-contribute)
* [Styleguides](#styleguides)


 What should I know before I get started?
=======================
Before you start contributing to bettingtool project, we encourage you to review the bettingtool wiki so that you can understand the architecture behind the system and the logic running each  component.

* [bettingtool wiki](https://github.com/soote1/bettingtool/wiki)

 How can I contribute?
=======================
* Suggesting enhancements.
* Developing new features.
* Providing support for new online sports betting sites.
* Reporting bugs.

## Pull Requests.

Currently, there are 6 active branches in the repository:

* master
* dev
* feature/extractor
* feature/processor
* feature/pythontools
* feature/server
* feature/dashboard

Contributions for each component should be started from the corresponding branch. For example:
* If you want to add support for a new online sports betting site, then you will need to create a new branch from the latest version of feature/extractor. 
* If you want to improve the algorithm to analyze the odds, then you will need to create a new branch from feature/pythontools. 
* If you want to create a new feature for bettingtool, then you will need to create a new branch from dev.

dev is the main branch right now, it has the latest version of all the other branches. We will do a backmerge from dev to master once we are ready for the first release.

We are trying to follow a Test Driven Development methodology, so make sure the unit tests are passing before pushing your changes to the repo you. If you are adding or updating logic, then make sure to provide new unit tests or update the existing ones to provide test coverage.

Styleguides
=======================
* [Python Style Guide](https://www.python.org/dev/peps/pep-0008/)
* [Javascript Stype Guide](https://standardjs.com/)