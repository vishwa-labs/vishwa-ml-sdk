from typing import Dict, Any


def get_safe_dict_value(dictionary: Dict[Any, Any], key: str, default=None) -> Any:
    if key in dictionary:
        return dictionary[key]
    return default


def find_key_in_nested_json(json_data, target_key):
    """
    Recursively search for a key in a nested JSON structure.

    Args:
    json_data (dict): The JSON data to search through.
    target_key (str): The key to search for.

    Returns:
    The value of the found key, or None if the key is not found.
    """
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if key == target_key:
                return value
            else:
                result = find_key_in_nested_json(value, target_key)
                if result is not None:
                    return result
    elif isinstance(json_data, list):
        for item in json_data:
            result = find_key_in_nested_json(item, target_key)
            if result is not None:
                return result
    return None
