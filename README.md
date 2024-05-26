# FunctionInspector


This class is used for inspecting a function, it stores the parameters and any type hints as well as the return annotation. 
This is then used to generate parametrized test stubs to be filled out and guard conditions for the types as derived from 
the input type hints.

It can be used to inspect functions that aren't your own or used to aid development.

## Example
### Example function:
```python
def test_function(param1: float, param2: int, param3: bool) -> float:
    if param3:
        return param1 - param2
    else:
        return param1 + param2
```

### Returned guard conditions:
usage:
```python
func_insp.analyse(test_function)
func_insp.add_guards()
```
output:
```python
def test_function(param1: float, param2: int, param3: bool) -> float:
    if not all([isinstance(param1, float), isinstance(param2, int), isinstance(param3, bool)]):
        raise TypeError(
            "test_function expects arg types: [float, int, bool], "
            f"received: [{type(param1).__name__}, {type(param2).__name__}, {type(param3).__name__}]"
        )
    if param3:
        return param1 - param2
    else:
        return param1 + param2
```


### Returned parametrized tests:
usage:
```python
func_insp.analyse(test_function)
func_insp.get_test(check_types=True)
```
output:
```python
@pytest.mark.parametrize(
    "param1, param2, param3, expected_result, expected_context",
    [
        (param1, param2, param3, expected_result, expected_context),
        (param1, param2, param3, None, pytest.raises(TypeError)),
        (param1, param2, param3, None, pytest.raises(TypeError)),
        (param1, param2, param3, None, pytest.raises(TypeError)),
    ]
)
def test_test_function(param1, param2, param3, expected_result, expected_context) -> None:
    with expected_context:
        assert test_function(param1, param2, param3) == expected_result
```
Compared to previous versions the tests are now combined to pass in the expected context, this could be whatever error a parameter set could raise or a successful assertion with the null_context passed as `does_not_raise()`. 
A type error raise test is created for each of the parameters if the `check_types` argument is `True`. The `match` argument can also be used to check the error message is what is expected too.

##### An example is below:
```python
@pytest.mark.parametrize(
    "param1, param2, param3, expected_result, expected_context",
    [
        (3, 2, True, 1, does_not_raise()),
        ("3", 2, False, 0, pytest.raises(TypeError))
    ]
)
def test_test_function(param1, param2, param3, expected_result, expected_context) -> None:
    with expected_context:
        assert test_function(param1, param2, param3) == expected_result
```

There is potential for the type testing to use hypothesis `@given` parameters however that's on the TODO list.


# ModuleInspector

A wrapper around FunctionInspector that can be given a module and perform FunctionInspector actions on the group of functions or classes.


# ClassInspector

Slightly out of date, this is used to help write getters and setters. However, I recommend using the attrs library instead as it's safer.


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


# AttrGenerator
This is an intermediate step between the ultimate goal of a standard class to attrs convertor, this converts a list of attributes into an attr class with type based validators

### Example
```python
from class_inspector.attr_generator import AttrGenerator, AttrMap

attributes = [
        AttrMap("test1", "int", True),
        AttrMap("test2", "float", False),
        AttrMap("test3", "bool", True),
        AttrMap("test4", "str", False),
        AttrMap("test5", "List[int]", True),
        AttrMap("test6", "Dict[str, float]", False),
    ]

at_gen = AttrGenerator("TestClass", attributes)
at_gen.get_attr_class()
```

#### output
```python
import attr
from attr.validators import instance_of, deep_iterable, deep_mapping


@attr.define
class TestClass:
    test1: int = attr.ib(validator=[instance_of(int)])
    test2: float = attr.ib(validator=[instance_of(float)], init=False)
    test3: bool = attr.ib(validator=[instance_of(bool)])
    test4: str = attr.ib(validator=[instance_of(str)], init=False)
    test5: list = attr.ib(validator=[deep_iterable(member_validator=instance_of(int), iterable_validator=instance_of(list))])
    test6: dict = attr.ib(validator=[deep_mapping(key_validator=instance_of(str), value_validator=instance_of(float), mapping_validator=instance_of(dict))], init=False)
```

AttrMap class is a wrapper to avoid a lot of duplicated dictionaries, however this is also valid input:
```python
attributes = [
    {'attr_name': 'test1', 'attr_type': 'int', 'attr_init': True},
    {'attr_name': 'test2', 'attr_type': 'float', 'attr_init': False},
    {'attr_name': 'test3', 'attr_type': 'bool', 'attr_init': True},
    {'attr_name': 'test4', 'attr_type': 'str', 'attr_init': False},
    {'attr_name': 'test5', 'attr_type': 'List[int]', 'attr_init': True},
    {'attr_name': 'test6', 'attr_type': 'Dict[str, float]', 'attr_init': False}
]
```