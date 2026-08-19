import itertools

from hypothesis import (
    given,
    settings,
)
from hypothesis import (
    strategies as st,
)

from eth_bloom import (
    BloomFilter,
)

address = st.binary(min_size=20, max_size=20)
topic = st.binary(min_size=32, max_size=32)
topics = st.lists(topic, min_size=0, max_size=4)


log_entry = st.tuples(address, topics)
log_entries = st.lists(log_entry, min_size=0, max_size=30)


def check_bloom(bloom, log_entries):
    for address, topics in log_entries:
        assert address in bloom
        for topic in topics:
            assert topic in bloom


@given(log_entries)
@settings(
    max_examples=20000,
    # consider setting `deadline` to `None` or raising it if timeout issues persist
    deadline=400,
)
def test_bloom_filter_add_method(log_entries):
    bloom = BloomFilter()

    for address, topics in log_entries:
        bloom.add(address)
        for topic in topics:
            bloom.add(topic)

    check_bloom(bloom, log_entries)


@given(log_entries)
@settings(max_examples=20000)
def test_bloom_filter_extend_method(log_entries):
    bloom = BloomFilter()

    for address, topics in log_entries:
        bloom.extend([address])
        bloom.extend(topics)

    check_bloom(bloom, log_entries)


@given(log_entries)
@settings(max_examples=20000)
def test_bloom_filter_from_iterable_method(log_entries):
    bloomables = itertools.chain.from_iterable(
        itertools.chain([address], topics) for address, topics in log_entries
    )
    bloom = BloomFilter.from_iterable(bloomables)
    check_bloom(bloom, log_entries)


def test_casting_to_integer():
    bloom = BloomFilter()

    assert int(bloom) == 0

    bloom.add(b"value 1")
    bloom.add(b"value 2")

    assert (
        int(bloom)
        == 1090215279796298345343057319992441901006450066263950115824040002588950485497113027143927523755823134941133023716890165043342811041924870874305880232180990464248298835944719578227183672673286106858273952584661686762419935928160959430409028732374024192153399763277382459194254234587232383494962731940352290891816707697788111127980409605093135659121120897102645250001200507634146244124778321795865777525978540960830042468420173693965828992647991129039043403835835590424035347457188427354145120006479590726476620907513681178254852999008485376  # noqa: E501
    )


def test_casting_to_binary():
    bloom = BloomFilter()

    assert bin(bloom) == "0b0"

    bloom.add(b"value 1")
    bloom.add(b"value 2")

    assert bin(bloom) == (
        "0b1000000000000000000000000000000000000000000000000000000000000"
        "000000000000000000000000000000000000000000000000000100000000000"
        "000000000000000000000000000000000000000000000000000000000000000"
        "000000000000000000000000000000000000000000000000000000000000000"
        "000000000000000000000000000000000000000000000000000000000000000"
        "000000000000000000000000000000000000000000000000000000000000000"
        "010000000000000000000000000000000000000000000000000000000000000"
        "000000000000000000000000000000000000000000000000000000000000000"
        "000000000000000000000000000000000000000000000000000000000000000"
        "000000000000000000000000000000000000000000000000000000000000000"
        "000000000000000000000000000000000000000000000000000000000000000"
        "000000000000000000000000000000000000000000000000000000000000000"
        "000000000000000000000000000000000000000000000000000000000000000"
        "000000000000000000000000000000000000000000000000000000000000000"
        "000000000000000000010000000000000000000000000001000000000000000"
        "000000000000000000000000000000000000000000000000000000000000000"
        "000000000000000000000000000000000000000000000000000000000000000"
        "000000000000000000000000000000000000000000000000000000000000000"
        "000000000000000000000000000000000000000000000000000000000000000"
        "000000000000000000000000000000000000000000000000000000000000000"
        "000000000000000000000000000000000000000000000000000000000000000"
        "000000000000000000000000000000000000000000000000000000000000000"
        "000000000000000000000000000000000000000000000000000000000000000"
        "000000000000000000000000000000000000000000000000000000000000000"
        "000000000100000000000000000000000000000000000000000000000000000"
        "000000000000000000000000000000000000000000000000000000000000000"
        "000000000000000000000000000000000000000000000000000000000000000"
        "000000000000000000000000000000000000000000000000000000000000000"
        "00000000000000000000000"
    )


def test_combining_filters():
    b1 = BloomFilter()
    b2 = BloomFilter()

    b1.add(b"a")
    b1.add(b"b")
    b1.add(b"c")

    b2.add(b"d")
    b2.add(b"e")
    b2.add(b"f")

    b1.add(b"common")
    b2.add(b"common")

    assert b"a" in b1
    assert b"b" in b1
    assert b"c" in b1

    assert b"a" not in b2
    assert b"b" not in b2
    assert b"c" not in b2

    assert b"d" in b2
    assert b"e" in b2
    assert b"f" in b2

    assert b"d" not in b1
    assert b"e" not in b1
    assert b"f" not in b1

    assert b"common" in b1
    assert b"common" in b2

    b3 = b1 | b2

    assert b"a" in b3
    assert b"b" in b3
    assert b"c" in b3
    assert b"d" in b3
    assert b"e" in b3
    assert b"f" in b3
    assert b"common" in b3

    b4 = b1 + b2

    assert b"a" in b4
    assert b"b" in b4
    assert b"c" in b4
    assert b"d" in b4
    assert b"e" in b4
    assert b"f" in b4
    assert b"common" in b4

    b5 = BloomFilter(int(b1))
    b5 |= b2

    assert b"a" in b5
    assert b"b" in b5
    assert b"c" in b5
    assert b"d" in b5
    assert b"e" in b5
    assert b"f" in b5
    assert b"common" in b5

    b6 = BloomFilter(int(b1))
    b6 += b2

    assert b"a" in b6
    assert b"b" in b6
    assert b"c" in b6
    assert b"d" in b6
    assert b"e" in b6
    assert b"f" in b6
    assert b"common" in b6
