# cache2q

Two queue (2Q) cache implementation in Python

Original paper: https://www.vldb.org/conf/1994/P439.PDF

[![CI](https://github.com/DimaProskurin/cache2q/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/DimaProskurin/cache2q/actions/workflows/ci.yml)
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![pypi](https://img.shields.io/pypi/v/cache2q)](https://pypi.org/project/cache2q/)
---------------------------------------------

## Installation
```bash
pip install cache2q
```

## Usage
```python
from cache2q import Cache2Q

cache = Cache2Q(512)

# set value by key
cache.set("hello", "world")

# get value by key
cache.get("hello")  # "world"

# if key not exists
cache.get("key")  # None

# remove key
cache.remove("hello")
cache.get("hello")  # None

# clear cache
cache.clear()
```
