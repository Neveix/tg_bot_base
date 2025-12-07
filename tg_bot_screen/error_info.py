from typing import Any, Callable, Type

def get_value_error(arg_value: Any, expected_type: Type | Callable, 
                    obj: Any, arg_name: str):
    return ValueError(f"У {type(obj).__name__} аргумент "
            f"{arg_name}={arg_value!r} неправильного типа "
            f"{type(arg_value).__name__} "
            f"(Ожидался {expected_type.__name__})")

def check_callable(arg_value: Any, obj: Any, arg_name: str):
    if not callable(arg_value):
        raise get_value_error(arg_value, Callable, obj, arg_name)

def check_bad_value(arg_value: Any, expected_type: Type, 
                    obj: Any, arg_name: str): 
    if not isinstance(arg_value, expected_type):
        raise get_value_error(arg_value, expected_type, obj, arg_name)

def check_bad_text(arg_value: str, obj: Any, arg_name: str):
    check_bad_value(arg_value, str, obj, arg_name)
        
def check_bad_text_and_len(arg_value: str, obj: Any, arg_name: str):
    check_bad_text(arg_value, obj, arg_name)
    if len(arg_value) == 0:
        raise ValueError(f"У {obj!r} аргумент {arg_name}={arg_value!r} "
                         f"не может быть {""!r}")

