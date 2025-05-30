# submariner

[![PyPI - Version](https://img.shields.io/pypi/v/submarine.svg)](https://pypi.org/project/submariner)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/submarine.svg)](https://pypi.org/project/submariner)

-----
# Intro
Submariner is a tool that lets you explore python packages, submodules, functions and classes, giving you quick visibility on what types are available for import.
The AI feature provide code examples that fit common usecases of the explored packages.

## Table of Contents

- [Installation](#installation)
- [License](#license)

## Setup
Proper use of submariner requires that you have a gemini api key in your environment.
```
GOOGLE_API_KEY=YOUR_API_KEY
```
New options will be added in the future.

## Installation

```console
pip install submariner
```

## Usage
```console
submarine deepdive {python_package} --use-ai
```
Where python package can be any package of your choice.
Although the package is called submariner, right now invoking the package requires that you type `submarine`

```console
submarine --help
```

## License

`submariner` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
