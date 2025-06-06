from collections.abc import Generator
from pprint import pprint
from types import EllipsisType

nested_structure = {
    "teachers": {
        "john": {
            "age": ...,
            "full_name": ...,  
        },
        "mary": {
            "age": ...,
            "full_name": ...,  
        },
    },
    "students": {
        "alice": {
            "avg": {
                "math": ...,
                "english": ...,
            },
            "contacts": ...,  
        },
    },
}


def extract_nested(
        data: dict, parents: list[str] | None = None, nested: int = 0
) -> Generator[tuple, None, None]:
    if nested > 100:
        raise NotImplementedError
    
    for key, value in data.items():
        if isinstance(value, EllipsisType):
            if parents:
                yield (*parents, key)
            else:
                yield(key,)
        elif isinstance(value, dict):
            if parents:
                parents.append(key)
                yield tuple(parents)
                yield from extract_nested(data=value, parents=parents, nested=nested+1)
            else:
                yield(key,)
                yield from extract_nested(data=value, parents=[key], nested=nested+1)
        else:
            raise NotImplementedError


results = list(extract_nested(nested_structure))

pprint(results)