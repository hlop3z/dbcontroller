import dataclasses as dc
import functools
import re
import typing

try:
    import strawberry

    STRAWBERRY_INPUT = strawberry.input
except ImportError:
    STRAWBERRY_INPUT = False

# Custom Typing
ISNULL = typing.TypeVar("ISNULL", bool, None)


def regex_search(pattern: str, text: str):
    """Search for { Regular Expression } Pattern"""
    _isRegex = lambda x: False if x is None else True
    return _isRegex(re.search(pattern, str(text)))


def regex_replace(items: list[tuple], text: str):
    """Replace Text"""
    for selector, replacement in items:
        text = re.sub(selector, replacement, text)
    return text


@dc.dataclass
class Field:
    type: typing.Any
    name: str = None
    default: typing.Any = ISNULL
    required: bool = False
    regex: dict = dc.field(default_factory=dict)
    rules: list = dc.field(default_factory=list)
    # fixed: bool = False


@dc.dataclass
class Error:
    field: str
    type: str
    text: str = None


@dc.dataclass
class FormResponse:
    data: dc.field(default_factory=dict)
    errors: dc.field(default_factory=list)
    valid: bool = False


def default_value(default):
    """Create Default Value"""
    is_callable = False
    if callable(default):
        is_callable = True
        field = dc.field(default_factory=default)
    else:
        field = dc.field(default=default)
    return is_callable, field


def custom_field_maker(info):
    """Custom Field Maker"""
    if info.default != ISNULL and not info.required:
        is_callable, default = default_value(info.default)
        if is_callable:
            the_type = typing.Optional[info.type]
        else:
            the_type = info.type
        field = tuple([info.name, the_type, default])
    else:
        extra_fields = []
        if not info.required:
            the_type = typing.Optional[info.type]
            extra_fields.extend([the_type, dc.field(default=None)])
        else:
            the_type = info.type
            extra_fields.append(the_type)
        field = tuple([info.name, *extra_fields])
    return field


class Form:
    """(Singleton) Create a Form"""

    def __new__(cls, *args, **kwargs):
        """Class Starter"""
        it_id = "__it__"
        it = cls.__dict__.get(it_id, None)
        if it is not None:
            return it
        it = object.__new__(cls)
        setattr(cls, it_id, it)
        it._init_only_once_for_the_whole_class(cls, *args, **kwargs)
        return it

    def _init_only_once_for_the_whole_class(self, cls, *args, **kwargs):
        """Class __init__ Replacement"""
        builtin_keys = ["_init_only_once_for_the_whole_class", "_validate"]
        fields = [
            x
            for x in self.__dir__()
            if not x.startswith("__") and x not in builtin_keys
        ]
        validate = {}
        annotations = {}
        custom_annotations = []
        for f_name in fields:
            current = getattr(self, f_name)
            current.name = f_name
            validate[f_name] = current
            if current.required:
                annotations[f_name] = current.type
            else:
                annotations[f_name] = typing.Optional[current.type]
            # Custom Type Annotation
            custom_field = custom_field_maker(current)
            custom_annotations.append(custom_field)

        cls.keys = lambda: frozenset(fields)
        cls._config = validate
        cls.__annotations__ = annotations
        cls.__custom_annotations__ = custom_annotations

    def __call__(self, form: dict = None):
        print("Validate Data")
        form = form or {}
        errors = []
        # Check Fields
        for name, setup in self._config.items():
            current_input = form.get(name)
            is_valid_type = isinstance(current_input, setup.type)
            if not is_valid_type:
                the_error = Error(
                    field=name, type="typing", text=f"{ setup.type } is required."
                )
                errors.append(the_error.__dict__)
            # Required Validator
            if setup.required:
                if name not in form.keys():
                    the_error = Error(
                        field=name, type="required", text=f"{ name } is required."
                    )
                    errors.append(the_error.__dict__)
            # Custom Validators
            if current_input:
                # Regex Validator
                for test, error_message in setup.regex.items():
                    # regex_search("[\w\.-]+@[\w\.-]+", demo_text)
                    found_regex = not regex_search("[\w\.-]+@[\w\.-]+", current_input)
                    if found_regex:
                        the_error = Error(field=name, type="regex", text=error_message)
                        errors.append(the_error.__dict__)
                # Custom Rules Validator
                for test in setup.rules:
                    if callable(test):
                        try:
                            found_rule = test(current_input)
                            if found_rule != True:
                                the_error = Error(
                                    field=name, type="rule", text=found_rule
                                )
                                errors.append(the_error.__dict__)
                        except:
                            the_error = Error(
                                field=name, type="except", text="invalid input"
                            )
                            errors.append(the_error.__dict__)
        return FormResponse(data=form, errors=errors, valid=len(errors) == 0)

def make_dataclass(BaseClass, form_name):
    """(Custom) Make Dataclass"""
    validator = BaseClass()
    form_annotations = BaseClass.__custom_annotations__
    OutClass = dc.make_dataclass(
        form_name,
        form_annotations,
        namespace={"__post_init__": lambda self: validator(self.__dict__)},
    )
    return OutClass


def dataclass(
    original_object: object = None,
    *,
    name: str = None,
    suffix: str = "Form",
    graphql: bool = True,
):
    """Form To GQL Input"""

    # Starting Wrapper. . .
    if original_object is None:
        return functools.partial(
            form,
            name=name,
            suffix=suffix,
        )

    # Re-Create Class with Form
    custom_class = type(original_object.__name__, (Form, original_object), {})
    
    # Configure Class
    if name:
        form_name = name
    else:
        form_name = f"{custom_class.__name__}{suffix.title()}"
        
    # Create Data-Class
    OutClass = make_dataclass(custom_class, form_name)
    if STRAWBERRY_INPUT and graphql:
        OutClass = STRAWBERRY_INPUT(OutClass, description=custom_class.__doc__)
    return OutClass


if __name__ == "__main__":

    @dataclass
    class Demo:
        name = Field(
            str,
            required=True,
            regex={"[\w\.-]+@[\w\.-]+": "invalid email address"},
            rules=[(lambda v: v.startswith("demo") or "invalid input")],
        )

    form = Demo()

    # Validate
    form({"name": "demo@google.com"})
