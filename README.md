# <div style="text-align: center">DGCastle<br/>[![Build Status](https://travis-ci.org/eprouty/dgcastle.svg?branch=master)](https://travis-ci.org/eprouty/dgcastle)  [![Coverage Status](https://coveralls.io/repos/github/eprouty/dgcastle/badge.svg?branch=master)](https://coveralls.io/github/eprouty/dgcastle?branch=master)</div>

A statistics tracking tool for disc golf, with a focus on team challenge.

Supported Python Versions:
* 3.6.x

## Getting Started

This project is configured using virtualenv and python3, to get started make sure both of those are installed on your system and run:

`make init`

To reactivate your virtualenv run:

`source .venv/bin/activate`

You can leave the virtualenv using:

`deactivate`

## Running Tests

Tests use the python3 unittest library and can be run using:

`make test`

## Importing Data
Format for match play input follows these rules for validating results.

Matchplay results can have 1 of 3 different types of values...
1. A victory that ended before all 18 holes were played
    * "X&Y where X > 1 and X > Y >= 1 and X - Y <= 2
2. A victory that ended at 18 holes
    * "Xup" where 0 < X < 3
3. A tie or "all square"
    * "tie" or "as"
