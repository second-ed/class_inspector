# Read the docs
[class-inspector API docs](https://second-ed.github.io/class_inspector/)

# Custom Validators
Extension of the validators from the attrs library, these allow the use of type checking the constituents of a collection.

### Example attrs validator and the problem this is a solution to*:
```python
possible: list = attr.ib(validator=[instance_of(list)])
not_possible: List[int] = attr.ib(validator=[instance_of(List[int])])
```

This means that we can't validate the members of a collection. However, with the custom validators we can do this:

```python
now_possible: Collection = attr.ib(validator=[validate_generic_of_type(Collection, float)])
```

Meaning we can pass in any object that implements the following dunder methods `[__contains__, __iter__, __len__]` 
AND validate that each member of the collection is a float. This is possible for other types too.

*on closer inspection (ironic given this repo's name) of the attrs API reference this is a solved problem with `deep_iterable()` and `deep_mapping()`. attrs: 2, me: 0

# generated repo map
```
└── class_inspector
    ├── docs
    │   └── source
    │       └── conf.py
    ├── src
    │   └── class_inspector
    │       ├── __init__.py
    │       ├── _logger.py
    │       ├── create_tests.py
    │       ├── cst_walkers.py
    │       ├── custom_validators.py
    │       ├── data_structures.py
    │       ├── guard_conditions.py
    │       ├── transform.py
    │       └── utils.py
    ├── tests
    │   ├── __init__.py
    │   ├── conftest.py
    │   ├── test_create_tests.py
    │   ├── test_custom_validators.py
    │   ├── test_guard_conditions.py
    │   ├── test_transform.py
    │   └── test_utils.py
    ├── README.md
    ├── pyproject.toml
    └── setup.py
::
```