"""Module to generate random facts.

randfacts provides an interface to a list of facts installed with the module.
You can retrieve facts via the `get_fact` method. randfacts also allows for
execution via the command line. See the examples section for more details.

# Examples:
To use randfacts in your Python code:

```py
>>> import randfacts

# Generate a random SFW (safe for work) fact:
>>> randfacts.get_fact()

# Generate a random NSFW (not safe for work) fact.
>>> randfacts.get_fact(only_unsafe=True)

# Generate a random mixed fact (possibility of both SFW and NSFW facts)
>>> randfacts.get_fact(filter_enabled=False)
```

# CLI Examples:
randfacts can be executed via the command line with the following options:

```sh
$ python3 -m randfacts            # normal execution; only safe facts
$ python3 -m randfacts --unsafe   # only unsafe facts
$ python3 -m randfacts --mixed    # possibility of both SFW and NSFW facts
$ python3 -m randfacts --help     # show CLI help
```
"""

from randfacts.randfacts import (
    __version__,
    all_facts,
    get_fact,
    safe_facts,
    unsafe_facts,
)

__all__ = [
    "__version__",
    "all_facts",
    "get_fact",
    "safe_facts",
    "unsafe_facts",
]
