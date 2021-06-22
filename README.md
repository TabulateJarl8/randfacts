[![PyPI version](https://badge.fury.io/py/randfacts.svg)](https://badge.fury.io/py/randfacts)
[![Downloads](https://pepy.tech/badge/randfacts)](https://pepy.tech/project/randfacts)
[![PyPI license](https://img.shields.io/pypi/l/randfacts.svg)](https://pypi.python.org/pypi/randfacts/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/TabulateJarl8/randfacts/graphs/commit-activity)
[![GitHub issues](https://img.shields.io/github/issues/TabulateJarl8/randfacts.svg)](https://GitHub.com/TabulateJarl8/randfacts/issues/)


Randfacts is a python library that generates random facts. You can use `randfacts.getFact()` to return a random fun fact. Disclaimer: Facts are not guaranteed to be true.

Example:
```python
import randfacts
x = randfacts.getFact()
print(x)
```
will print a random fact like:
`Penguins can't taste sweet or savory flavors, only sour and salty ones`

This package has a filter option to filter out potentially inappropriate facts. The filter is on by default. To disable the filter, you can just set the `filter_enabled` parameter to `False`.
```python
from randfacts import getFact
print(getFact(False))
```

`getFact` also has a parameter that will make the function only return unsafe facts. This argument takes precedence over the `filter_enabled` argument. For example:

```py
print(getFact(only_unsafe=True))
```

If you want to access the list of facts directly, you can just import the `safeFacts`, `unsafeFacts`, or `allFacts` lists from the randfacts module.

randfacts can be executed via the command line with the following commands:

Normal execution; only safe facts

```sh
$ python3 -m randfacts
```

The unsafe argument can be supplied to provide only unsafe facts

```sh
$ python3 -m randfacts --unsafe
```

The mixed argument can be provided to provide both safe and unsafe facts.

```sh
$ python3 -m randfacts --mixed
```