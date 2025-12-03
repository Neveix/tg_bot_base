from typing import Any, Type, TYPE_CHECKING

def check_bad_value(arg_value: Any, expected_type: Type[Any], obj: Any, arg_name: str):
    if not isinstance(arg_value, expected_type):
        raise ValueError(f"У {type(obj).__name__} аргумент {arg_name}={arg_value!r} \
неправильного типа {type(arg_value).__name__} (Ожидался {expected_type.__name__})")

def check_bad_text(arg_value: str, obj: Any, arg_name: str):
    check_bad_value(arg_value, str, obj, arg_name)
        
def check_bad_text_and_len(arg_value: str, obj: Any, arg_name: str):
    check_bad_text(arg_value, obj, arg_name)
    if len(arg_value) == 0:
        raise ValueError(f"У {obj!r} аргумент {arg_name}={arg_value!r} не может быть {""!r}")

