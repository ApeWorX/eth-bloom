# eth-bloom

[![Join the conversation on Discord](https://img.shields.io/discord/809793915578089484?color=blue&label=chat&logo=discord&logoColor=white)](https://discord.gg/GHryRvPB84)
[![Build Status](https://github.com/ApeWorX/eth-bloom/actions/workflows/test.yaml/badge.svg)](https://github.com/ApeWorX/eth-bloom/actions/workflows/test.yaml)
[![PyPI version](https://badge.fury.io/py/eth-bloom.svg)](https://badge.fury.io/py/eth-bloom)
[![Python versions](https://img.shields.io/pypi/pyversions/eth-bloom.svg)](https://pypi.python.org/pypi/eth-bloom)

A python implementation of the bloom filter used by Ethereum.

> This library and repository was previously located at https://github.com/pipermerriam/ethereum-bloom. It was transferred to the Ethereum foundation github in November 2017 and renamed to `eth-bloom`. The PyPI package was also renamed from `ethereum-bloom` to `eth-bloom`.

Read more in the documentation below. [View the change log](https://github.com/ApeWorX/eth-bloom/blob/main/CHANGELOG.rst).

For more information on what Bloom Filters are, see [Wikipedia](https://en.wikipedia.org/wiki/Bloom_filter).

## Installation

```sh
python -m pip install eth-bloom
```

## Usage

The `BloomFilter` object

```python
>>> from eth_bloom import BloomFilter
>>> b = BloomFilter()
>>> b'a value' in b  # check whether a value is present
False
>>> b.add(b'a value')  # add a single value
>>> b'a value' in b
True
>>> int(b)  # cast to an integer
3458628712844765018311492773359360516229024449585949240367644166080576879632652362184119765613545163153674691520749911733485693171622325900647078772681584616740134230153806267998022370194756399579977294154062696916779055028045657302214591620589415314367270329881298073237757853875497241510733954508399863880080986777555986663988492288946856978031023631618215522505971170427986911575695114157059398791122395379400594948096
>>> bin(b)  # cast to a binary string
'0b100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
```

You can also add an iterable of items to a bloom filter.

```python
>>> b = BloomFilter()
>>> b'value-a' in b
False
>>> b'value-b' in b
False
>>> b.extend([b'value-a', b'value-b'])
>>> b'value-a' in b
True
>>> b'value-b' in b
True
```

You can initialize a bloom filter from an iterable of byte strings.

```python
>>> b = BloomFilter.from_iterable([b'value-a', b'value-b'])  # initialize from an iterable of values.
>>> b'value-a' in b
True
>>> b'value-b' in b
True
```

You can initialize a bloom filter from the integer representation of the bloom bits.

```python
>>> b = BloomFilter(3458628712844765018311492773359360516229024449585949240367644166080576879632652362184119765613545163153674691520749911733485693171622325900647078772681584616740134230153806267998022370194756399579977294154062696916779055028045657302214591620589415314367270329881298073237757853875497241510733954508399863880080986777555986663988492288946856978031023631618215522505971170427986911575695114157059398791122395379400594948096)
>>> b'a value' in b
True
```

You can also merge bloom filters

```python
>>> from eth_bloom import BloomFilter
>>> b1 = BloomFilter()
>>> b2 = BloomFilter()
>>> b1.add(b'a')
>>> b1.add(b'common')
>>> b2.add(b'b')
>>> b2.add(b'common')
>>> b'a' in b1
True
>>> b'b' in b1
False
>>> b'common' in b1
True
>>> b'a' in b2
False
>>> b'b' in b2
True
>>> b'common' in b2
True
>>> b3 = b1 + b2  # using addition
>>> b'a' in b3
True
>>> b'b' in b3
True
>>> b'common' in b3
True
>>> b4 = b1 | b2  # or using bitwise or
>>> b'a' in b4
True
>>> b'b' in b4
True
>>> b'common' in b4
True
>>> b1 |= b2  # or using in-place operations (works with += too)
>>> b'a' in b1
True
>>> b'b' in b1
True
>>> b'common' in b1
True
```

## Developer Setup

If you would like to hack on eth-bloom, please check out the [Snake Charmers
Tactical Manual](https://github.com/ethereum/snake-charmers-tactical-manual)
for information on how we do:

- Testing
- Pull Requests
- Documentation

We use [prek](https://prek.j178.dev) to maintain consistent code style. Once
installed, it will run automatically with every commit. You can also run it manually
with `uv run prek run --all-files`. If you need to make a commit that skips the
`prek` checks, you can do so with `git commit --no-verify`.

### Development Environment Setup

You can set up your dev environment with the `dev` dependency group, which is
installed by default when you run `uv sync`.

```sh
git clone git@github.com:ApeWorX/eth-bloom.git
cd eth-bloom
uv sync
uv run prek install
```

### Checks

Run the standard local checks with:

```sh
uv build
uv run --group lint ruff check .
uv run --group lint ruff format --check .
uv run --group lint --group test mypy -p eth_bloom
uv run --group test pytest tests
```

### Release setup

To release a new version, create a GitHub Release. The release tag is used by
`setuptools-scm` to derive the package version, and GitHub Actions publishes the built
package to PyPI using trusted publishing.
