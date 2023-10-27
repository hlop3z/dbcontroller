"""
    Database - Table Config
"""
import dataclasses as dc

from ..tools import get_module_name


@dc.dataclass(frozen=True)
class TableConfig:
    """Table Setup"""

    table_uri: str = None
    table_name: str = None
    required: list = None
    primary_key: list = None
    index: list = None
    unique: list = None
    unique_together: list = None
    many_to_many: dict = None
    ignore: list = None
    engine: str = None
    database: str = None
    many_to_many: list = None
    auto: list = None


def table_info(original_object, table_name, config):
    """Table Info"""
    class_name = original_object.__name__
    class_module_name = get_module_name(original_object)
    if not class_module_name:
        class_module_name = "main"
    class_table_name = f"{class_module_name.lower()}_{class_name.lower()}"
    info_class_table_uri = f"{class_module_name.lower()}.{class_name.lower()}"
    if table_name:
        class_table_name = table_name
    # Set Name
    config["table_name"] = class_table_name
    config["table_uri"] = info_class_table_uri
    out_config = dict(config.items())
    del out_config["controller"]
    return TableConfig(**out_config)
