# scrapets

[![Build Status](https://travis-ci.org/ownport/scrapets.svg?branch=master)](https://travis-ci.org/ownport/scrapets)

scrapets: scraping snippets

## How-to install

Just download `scrapets` file from Releases page https://github.com/ownport/scrapets/releases

## How-to use

```sh
$ ./bin/scrapets fetch
Usage: scrapets fetch [OPTIONS] [URL]...

  Fetch operations

Options:
  --urls FILENAME             fetch files by the list of urls
  --path PATH                 the target directory, default:
                              /media/data1/svc/github/scrapets
  --user-agent TEXT           User agent, default: Mozilla/5.0 (X11; Ubuntu;
                              Linux x86_64; rv:44.0) Gecko/20100101
                              Firefox/44.0
  --pairtree / --no-pairtree  create pairtree structure in the target
                              directory, default: turn off
  --meta TEXT                 format or metadata. Possible values: short,
                              detail. Default: short
  --help                      Show this message and exit.
```

## Included

Python packages:
- click, https://github.com/pallets/click
- reqres, https://github.com/ownport/reqres

## Dependencies

Docker images:
- ownport/scrapy:latest, https://hub.docker.com/r/ownport/scrapy/


## For developers

to compile the project into the binary artifact
``` sh
$ make compile
make compile
[INFO] Cleaning directory: /media/d1/svc/github/scrapets/.local-ci
[INFO] Cleaning directory: /media/d1/svc/github/scrapets/scrapets.egg-info
[INFO] Cleaning directory: /media/d1/svc/github/scrapets/bin
[INFO] Cleaning files: *.pyc
[INFO] Cleaning files: .coverage
[INFO] Compiling to binary, scrapets
```

to run test cases you need to have installed and configured:
- docker, https://www.docker.com/
- local-ci, https://github.com/ownport/local-ci

Docker images:
- ownport/docker-local-repos:latest
- ownport/python-dev:2.7
- ownport/python-dev:3.5

```sh
$  make run-local-ci
...
============================= test session starts ==============================
platform linux2 -- Python 2.7.12, pytest-3.0.2, py-1.4.31, pluggy-0.3.1
rootdir: /repo, inifile:
plugins: cov-2.3.1
collected 15 items

tests/test_fetch.py .....
tests/storage/test_fileobject.py ..........

---------- coverage: platform linux2, python 2.7.12-final-0 ----------
Name                             Stmts   Miss  Cover   Missing
--------------------------------------------------------------
scrapets/__init__.py                 7      2    71%   8-9
scrapets/__main__.py                 2      2     0%   2-4
scrapets/errors.py                   2      0   100%
scrapets/fetch.py                   33      0   100%
scrapets/main.py                    23     23     0%   1-46
scrapets/storage/__init__.py         0      0   100%
scrapets/storage/avroobject.py       0      0   100%
scrapets/storage/common.py           0      0   100%
scrapets/storage/fileobject.py      53      0   100%
scrapets/storage/utils.py           14      1    93%   9
--------------------------------------------------------------
TOTAL                              134     28    79%

========================== 15 passed in 0.47 seconds ===========================
```
