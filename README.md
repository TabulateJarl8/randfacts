<p align="center">
<img src="https://raw.githubusercontent.com/TabulateJarl8/randfacts/master/imgs/logo-embedded-font.svg" />
</p>
<p align="center">
	<a href="https://badge.fury.io/py/randfacts"><img alt="PyPI" src="https://img.shields.io/pypi/v/randfacts" /></a>
	<a href="https://aur.archlinux.org/packages/python-randfacts/"><img alt="AUR version" src="https://img.shields.io/aur/version/python-randfacts"></a>
	<a href="https://pepy.tech/project/randfacts"><img alt="Downloads" src="https://pepy.tech/badge/randfacts" /></a>
	<a href="https://pypi.python.org/pypi/randfacts/"><img alt="PyPI license" src="https://img.shields.io/pypi/l/randfacts.svg" /></a>
	<a href="https://GitHub.com/TabulateJarl8/randfacts/graphs/commit-activity"><img alt="Maintenance" src="https://img.shields.io/badge/Maintained%3F-yes-green.svg" /></a>
	<a href="https://GitHub.com/TabulateJarl8/randfacts/issues/"><img alt="GitHub Issues" src="https://img.shields.io/github/issues/TabulateJarl8/randfacts.svg" /></a>
	<a href="https://github.com/TabulateJarl8/randfacts/actions/workflows/main.yml"><img alt="GitHub Workflow Status" src="https://img.shields.io/github/actions/workflow/status/TabulateJarl8/randfacts/main.yml?branch=master&label=Duplicate%20Facts%20Test" /></a>
	<a href="https://github.com/TabulateJarl8"><img alt="GitHub followers" src="https://img.shields.io/github/followers/TabulateJarl8?style=social" /></a>
	<a href="https://github.com/TabulateJarl8/randfacts"><img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/TabulateJarl8/randfacts?style=social" /></a>
	<br>
	<a href="https://ko-fi.com/L4L3L7IO2"><img alt="Kofi Badge" src="https://ko-fi.com/img/githubbutton_sm.svg" /></a>
</p>

Randfacts is a Python module that generates random facts. You can use `randfacts.get_fact()` to return a random fun fact. Disclaimer: Facts are not guaranteed to be true.

# Installation

randfacts can either be installed via pip or via the AUR, whichever way you prefer.

### Installation via pip:

```sh
$ pip3 install randfacts
```

### Installation via AUR:

Via your AUR helper, like paru:
```sh
$ paru -S python-randfacts
```

Or manually
```sh
$ git clone https://aur.archlinux.org/python-randfacts.git && cd python-randfacts
$ makepkg -si
```

# Usage and examples

```python
import randfacts
x = randfacts.get_fact()
print(x)
```
The above example will print a random fact like:
`Penguins can't taste sweet or savory flavors, only sour and salty ones`

This package has a filter option to filter out potentially inappropriate facts. The filter is on by default. To disable the filter, you can just set the `filter_enabled` parameter to `False`.
```python
from randfacts import get_fact
print(get_fact(False))
# or
print(get_fact(filter_enabled=False))
```

`get_fact` also has a parameter that will make the function only return unsafe facts. This argument takes precedence over the `filter_enabled` argument. For example:

```py
print(get_fact(only_unsafe=True))
```

If you want to access the list of facts directly, you can just import the `safe_facts`, `unsafe_facts`, or `all_facts` lists from the randfacts module.


## Command line usage

randfacts can be executed via the command line with the following commands:

Normal execution; only SFW (safe for work) facts

```sh
$ python3 -m randfacts
```

The unsafe argument can be supplied to provide only NSFW (not safe for work) facts

```sh
$ python3 -m randfacts --unsafe
```

The mixed argument can be provided to provide both SFW and NSFW facts.

```sh
$ python3 -m randfacts --mixed
```

More help.

```sh
$ python3 -m randfacts --help
```
