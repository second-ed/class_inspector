from collections import abc
from contextlib import nullcontext as does_not_raise

import attr
import numpy as np
import pytest
from class_inspector.custom_validators import (
    validate_bool_func,
    validate_collection,
    validate_collection_of_type,
    validate_generic,
    validate_generic_bool_func,
    validate_generic_of_type,
    validate_iterable,
    validate_iterable_of_type,
    validate_sequence,
    validate_sequence_of_type,
)


@pytest.mark.parametrize(
    "gen_type, val_func, inputs, expectation",
    [
        (abc.Collection, validate_collection, [1, 2, 3], does_not_raise()),
        (abc.Collection, validate_collection, 0, pytest.raises(TypeError)),
    ],
)
def test_validate_collection(gen_type, val_func, inputs, expectation):
    @attr.define
    class TestClass:
        attrib: gen_type = attr.ib(validator=[val_func])

    with expectation:
        TestClass(inputs)


@pytest.mark.parametrize(
    "gen_type, val_func, inputs, expectation",
    [
        (
            abc.Collection,
            validate_collection_of_type(int),
            [1, 2, 3],
            does_not_raise(),
        ),
        (
            abc.Collection,
            validate_collection_of_type(int),
            0,
            pytest.raises(TypeError),
        ),
        (
            abc.Collection,
            validate_collection_of_type(int),
            [1, 2, "3"],
            pytest.raises(TypeError),
        ),
    ],
)
def test_validate_collection_of_type(gen_type, val_func, inputs, expectation):
    @attr.define
    class TestClass:
        attrib: gen_type = attr.ib(validator=[val_func])

    with expectation:
        TestClass(inputs)


@pytest.mark.parametrize(
    "gen_type, val_func, inputs, expectation",
    [
        (
            abc.Collection,
            validate_generic(abc.Collection),
            [1, 2, 3],
            does_not_raise(),
        ),
        (
            abc.Collection,
            validate_generic(abc.Collection),
            0,
            pytest.raises(TypeError),
        ),
        (
            abc.Iterable,
            validate_generic(abc.Iterable),
            [1, 2, 3],
            does_not_raise(),
        ),
        (
            abc.Iterable,
            validate_generic(abc.Iterable),
            0,
            pytest.raises(TypeError),
        ),
        (
            abc.Sequence,
            validate_generic(abc.Sequence),
            [1, 2, 3],
            does_not_raise(),
        ),
        (
            abc.Sequence,
            validate_generic(abc.Sequence),
            {"test": "case"},
            pytest.raises(TypeError),
        ),
    ],
)
def test_validate_generic(gen_type, val_func, inputs, expectation):
    @attr.define
    class TestClass:
        attrib: gen_type = attr.ib(validator=[val_func])

    with expectation:
        TestClass(inputs)


@pytest.mark.parametrize(
    "gen_type, val_func, inputs, expectation",
    [
        (
            abc.Collection,
            validate_generic_of_type(abc.Collection, int),
            [1, 2, 3],
            does_not_raise(),
        ),
        (
            abc.Collection,
            validate_generic_of_type(abc.Collection, int),
            [1, 2, "3"],
            pytest.raises(TypeError),
        ),
        (
            abc.Iterable,
            validate_generic_of_type(abc.Iterable, float),
            [1.0, 2.0, 3.0],
            does_not_raise(),
        ),
        (
            abc.Iterable,
            validate_generic_of_type(abc.Iterable, float),
            0,
            pytest.raises(TypeError),
        ),
        (
            abc.Iterable,
            validate_generic_of_type(abc.Iterable, float),
            [1, 2, 3],
            pytest.raises(TypeError),
        ),
        (
            abc.Sequence,
            validate_generic_of_type(abc.Sequence, str),
            ["1", "2", "3"],
            does_not_raise(),
        ),
        (
            abc.Sequence,
            validate_generic_of_type(abc.Sequence, str),
            [1, 2, 3],
            pytest.raises(TypeError),
        ),
    ],
)
def test_validate_generic_of_type(gen_type, val_func, inputs, expectation):
    @attr.define
    class TestClass:
        attrib: gen_type = attr.ib(validator=[val_func])

    with expectation:
        TestClass(inputs)


@pytest.mark.parametrize(
    "gen_type, val_func, inputs, expectation",
    [
        (abc.Iterable, validate_iterable, {1, 2, 3}, does_not_raise()),
        (abc.Iterable, validate_iterable, 0, pytest.raises(TypeError)),
    ],
)
def test_validate_iterable(gen_type, val_func, inputs, expectation):
    @attr.define
    class TestClass:
        attrib: gen_type = attr.ib(validator=[val_func])

    with expectation:
        TestClass(inputs)


@pytest.mark.parametrize(
    "gen_type, val_func, inputs, expectation",
    [
        (
            abc.Iterable,
            validate_iterable_of_type(int),
            [1, 2, 3],
            does_not_raise(),
        ),
        (
            abc.Iterable,
            validate_iterable_of_type(int),
            0,
            pytest.raises(TypeError),
        ),
        (
            abc.Iterable,
            validate_iterable_of_type(int),
            [1, 2, "3"],
            pytest.raises(TypeError),
        ),
    ],
)
def test_validate_iterable_of_type(gen_type, val_func, inputs, expectation):
    @attr.define
    class TestClass:
        attrib: gen_type = attr.ib(validator=[val_func])

    with expectation:
        TestClass(inputs)


@pytest.mark.parametrize(
    "gen_type, val_func, inputs, expectation",
    [
        (abc.Sequence, validate_sequence, [1, 2, 3], does_not_raise()),
        (abc.Sequence, validate_sequence, 0, pytest.raises(TypeError)),
    ],
)
def test_validate_sequence(gen_type, val_func, inputs, expectation):
    @attr.define
    class TestClass:
        attrib: gen_type = attr.ib(validator=[val_func])

    with expectation:
        TestClass(inputs)


@pytest.mark.parametrize(
    "gen_type, val_func, inputs, expectation",
    [
        (
            abc.Sequence,
            validate_sequence_of_type(int),
            [1, 2, 3],
            does_not_raise(),
        ),
        (
            abc.Sequence,
            validate_sequence_of_type(int),
            0,
            pytest.raises(TypeError),
        ),
        (
            abc.Sequence,
            validate_sequence_of_type(int),
            [1, 2, "3"],
            pytest.raises(TypeError),
        ),
    ],
)
def test_validate_sequence_of_type(gen_type, val_func, inputs, expectation):
    @attr.define
    class TestClass:
        attrib: gen_type = attr.ib(validator=[val_func])

    with expectation:
        TestClass(inputs)


@pytest.mark.parametrize(
    "val_func, inputs, expectation",
    [
        (
            validate_bool_func(np.isnan),
            np.nan,
            does_not_raise(),
        ),
        (
            validate_bool_func(np.isnan),
            1,
            pytest.raises(ValueError),
        ),
        # TODO: this raises a TypeError at the moment that interrupts collection
        #  need to work out why the raises isn't catching the TypeError
        # (
        #     validate_bool_func(np.nan),
        #     np.nan,
        #     pytest.raises(TypeError),
        # ),
    ],
)
def test_validate_bool_func(val_func, inputs, expectation):
    @attr.define
    class TestClass:
        attrib: list = attr.ib(validator=[val_func])

    with expectation:
        TestClass(inputs)


@pytest.mark.parametrize(
    "gen_type, val_func, inputs, expectation",
    [
        (
            abc.Collection,
            validate_generic_bool_func(abc.Collection, np.isnan),
            [np.nan, np.nan, np.nan],
            does_not_raise(),
        ),
        (
            abc.Collection,
            validate_generic_bool_func(abc.Collection, np.isnan),
            [np.nan, np.nan, 1, 2, 3],
            pytest.raises(ValueError),
        ),
        (
            abc.Collection,
            validate_generic_bool_func(abc.Collection, np.isnan),
            1,
            pytest.raises(TypeError),
        ),
    ],
)
def test_validate_generic_bool_func(gen_type, val_func, inputs, expectation):
    @attr.define
    class TestClass:
        attrib: gen_type = attr.ib(validator=[val_func])

    with expectation:
        TestClass(inputs)
