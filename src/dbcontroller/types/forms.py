"""
    Form Creator
        Modules:
            * dataclass: Create a Custom DataClass.
            * Field: Create a Field for the dataclass.
"""
import dataclasses as dc
import functools
import re
import typing
from types import SimpleNamespace

try:
    import strawberry

    STRAWBERRY_INPUT = strawberry.input
except ImportError:
    STRAWBERRY_INPUT = False

# Custom Typing
ISNULL = typing.TypeVar("ISNULL", bool, None)


@dc.dataclass
class FormField:
    """DataClass -> Field"""

    type: typing.Any
    name: str = None
    default: typing.Any = ISNULL
    required: bool = False
    regex: dict = dc.field(default_factory=dict)
    rules: list = dc.field(default_factory=list)
    filters: dict = dc.field(default_factory=dict)
    # fixed: bool = False


@dc.dataclass
class FormError:
    """DataClass -> Form Error"""

    field: str
    type: str
    text: str = None


@dc.dataclass
class FormResponse:
    """DataClass -> Form Response"""

    data: dc.field(default_factory=dict)
    errors: dc.field(default_factory=list)
    is_valid: bool = False


@dc.dataclass
class FormCRUD:
    """DataClass -> Form Error"""

    create: typing.Any = None
    read: typing.Any = None
    update: typing.Any = None
    delete: typing.Any = None


def regex_search(pattern: str, text: str):
    """Search for { Regular Expression } Pattern"""

    # regex_search("[\w\.-]+@[\w\.-]+", "admin@example.com")
    def is_regex(x):
        "Real Regex"
        return x is not None

    return is_regex(re.search(pattern, str(text)))


def regex_replace(items: list[tuple], text: str):
    """Replace Text"""
    for selector, replacement in items:
        text = re.sub(selector, replacement, text)
    return text


def default_value(default):
    """Create Default Value"""
    is_callable = False
    if callable(default):
        is_callable = True
        field = dc.field(default_factory=default)
    else:
        field = dc.field(default=default)
    return is_callable, field


def custom_field_maker(info: FormField):
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


class FormBase:
    """(Singleton) Create a Form"""

    def __new__(cls):
        """Class Starter"""
        it_id = "__it__"
        it = cls.__dict__.get(it_id, None)
        if it is not None:
            return it
        it = object.__new__(cls)
        setattr(cls, it_id, it)
        it._init_only_once_for_the_whole_class(cls)
        return it

    def _init_only_once_for_the_whole_class(self, cls):
        """Class __init__ Replacement"""
        builtin_keys = ["_init_only_once_for_the_whole_class", "_validate"]
        fields = [
            x for x in dir(self) if not x.startswith("__") and x not in builtin_keys
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

        self._config = validate
        cls.__annotations__ = annotations
        cls.__custom_annotations__ = custom_annotations

    def __call__(self, form: dict = None):
        form = form or {}
        errors = []
        output_form = {**form}
        # Check Fields
        for name, setup in self._config.items():
            current_input = form.get(name)
            is_valid_type = isinstance(current_input, setup.type)
            if not is_valid_type and current_input:
                the_error = FormError(
                    field=name, type="typing", text=f"{ setup.type } is required."
                )
                errors.append(the_error.__dict__)
            # Required Validator
            if setup.required:
                if name not in form.keys():
                    the_error = FormError(
                        field=name, type="required", text=f"{ name } is required."
                    )
                    errors.append(the_error.__dict__)
            # Custom Validators
            if current_input:
                # Regex Validator
                for test, error_message in setup.regex.items():
                    found_regex = not regex_search(test, current_input)
                    if found_regex:
                        the_error = FormError(
                            field=name, type="regex", text=error_message
                        )
                        errors.append(the_error.__dict__)
                # Custom Rules Validator
                for test in setup.rules:
                    if callable(test):
                        try:
                            found_rule = test(current_input)
                            if found_rule is not True:
                                the_error = FormError(
                                    field=name, type="rule", text=found_rule
                                )
                                errors.append(the_error.__dict__)
                        except:
                            the_error = FormError(
                                field=name, type="except", text="invalid input"
                            )
                            errors.append(the_error.__dict__)
                # Custom Filters
                if len(errors) == 0:
                    regex_methods = []
                    new_input = current_input
                    if setup.filters:
                        for test in setup.filters.get("regex"):
                            if isinstance(test, list | tuple):
                                regex_methods.append(test)
                            if (
                                isinstance(current_input, str)
                                and len(regex_methods) > 0
                            ):
                                new_input = regex_replace(regex_methods, current_input)
                        for test in setup.filters.get("rules"):
                            if callable(test):
                                try:
                                    new_input = test(new_input)
                                except:
                                    pass
                    # Add Field To Form
                    output_form[name] = new_input
        if "input" in output_form:
            del output_form["input"]
        return FormResponse(
            data=SimpleNamespace(**output_form),
            errors=errors,
            is_valid=len(errors) == 0,
        )


def run_validator(form, validator):
    """Return Custom Response to the Dataclass"""
    form.input = validator(form.__dict__)


def make_dataclass(BaseClass, form_name):
    """(Custom) Make Dataclass"""
    validator = BaseClass()
    form_annotations = BaseClass.__custom_annotations__
    cleaned_data = custom_field_maker(
        SimpleNamespace(name="input", type=typing.Any, default=None, required=False)
    )
    form_annotations.append(cleaned_data)
    OutClass = dc.make_dataclass(
        form_name,
        form_annotations,
        namespace={"__post_init__": lambda self: run_validator(self, validator)},
    )
    del OutClass.__annotations__["input"]
    return OutClass


def dataclass(
    original_object: object = None,
    *,
    name: str = None,
    prefix: str = None,
    suffix: str | list = None,
    graphql: bool = True,
):
    """Form To GQL Input"""

    # Starting Wrapper. . .
    if original_object is None:
        return functools.partial(
            dataclass,
            name=name,
            prefix=prefix,
            suffix=suffix,
            graphql=graphql,
        )

    # Configure Class
    if name:
        form_name = name
    else:
        form_name = ""
        # Class Prefix
        if prefix:
            if isinstance(prefix, list):
                for fix in prefix:
                    form_name += fix.title()
            else:
                form_name += prefix.title()
        # Class Name
        form_name += f"{original_object.__name__}"
        # Class Suffix
        if suffix:
            if isinstance(suffix, list):
                for fix in suffix:
                    form_name += fix.title()
            else:
                form_name += suffix.title()
    # Re-Create Class with Form
    custom_class = type(original_object.__name__, (FormBase, original_object), {})

    # Create Data-Class
    OutClass = make_dataclass(custom_class, form_name)
    if STRAWBERRY_INPUT and graphql:
        OutClass = STRAWBERRY_INPUT(OutClass, description=original_object.__doc__)
    return OutClass


def form_filters(regex: list = None, rules: list = None) -> dict:
    """Form Filters"""
    regex = regex or []
    rules = rules or []
    return {
        "regex": regex,
        "rules": rules,
    }


def form_crud(model: str = None) -> FormCRUD:
    """Form CRUD"""
    if not model:
        raise ValueError("Model must be specified.")

    def form_crud_read(search_name: str = None):
        """Form CRUD: <Read>"""
        name = model.title()
        if search_name:
            name += search_name.title()
        return functools.partial(dataclass, name=f"{name}ReadCRUD")

    return FormCRUD(
        create=functools.partial(dataclass, name=f"{model.title()}CreateCRUD"),
        read=form_crud_read,
        update=functools.partial(dataclass, name=f"{model.title()}UpdateCRUD"),
        delete=functools.partial(dataclass, name=f"{model.title()}DeleteCRUD"),
    )


class Form:
    """Form Wrapper"""

    field = FormField
    filters = form_filters

    # Custom DataClasses
    input = functools.partial(dataclass, suffix="input")
    search = functools.partial(dataclass, suffix="search")
    form = functools.partial(dataclass, suffix="form", graphql=False)
    crud = form_crud


if __name__ == "__main__":

    @Form.form
    class Demo:
        """Demo"""

        name = Form.field(
            str,
            required=True,
            regex={r"[\w\.-]+@[\w\.-]+": "invalid email address"},
            rules=[(lambda v: v.startswith("demo") or "invalid input")],
        )

    # Validate
    Demo({"name": "demo@google.com"})
