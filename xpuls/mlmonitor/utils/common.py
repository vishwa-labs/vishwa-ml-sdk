from typing import Dict, Any


def get_safe_dict_value(dictionary: Dict[Any, Any], key: str, default=None) -> Any:
    if key in dictionary:
        return dictionary[key]
    return default
