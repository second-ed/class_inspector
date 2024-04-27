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
func_insp.get_guards()
```
output:
```python
    if not all([isinstance(param1, float), isinstance(param2, int), isinstance(param3, bool)]):
        raise TypeError(
            f"test_function expects arg types: [float, int, bool], "
            f"received: [{type(param1).__name__}, {type(param2)__name__}, {type(param3).__name__}]"
        )
```


### Returned parametrized tests:
usage:
```python
func_insp.analyse(test_function)
func_insp.get_tests()
```
output:
```python
@pytest.mark.parametrize(
    "param1, param2, param3, expected_result",
    [
        (param1, param2, param3, expected_result),
    ]
)
def test_values_test_function(param1, param2, param3, expected_result) -> None:
    test_function(param1, param2, param3) == expected_result


@pytest.mark.parametrize(
    "param1, param2, param3",
    [
        (float, int, bool),
        (float, int, bool),
        (float, int, bool),
    ]
)
def test_types_test_function(param1, param2, param3) -> None:
    with pytest.raises(TypeError):
        test_function(param1, param2, param3) 
```
The test values are for the user to fill in with values that are appropriate for the function.

The test types shows what types the parameters expect and it is up to the user to fill in those cases with types that are
not specified, there is one test case per parameter to test each parameter's guard condition while the others are correct.

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
