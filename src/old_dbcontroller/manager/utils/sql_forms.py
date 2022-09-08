from typing import Any


def clean_form(base: Any, cols: list, form: dict):
    """Clean User's Input

    Args:
        form (dict): User's Input.

    Returns:
        dict: Clean User's Input.
    """
    inputs = {}
    base_form = base(**form)
    for key, val in base_form.__dict__.items():
        if key in cols and key != "_id":
            inputs[key] = val
    return inputs


def clean_update_form(base: Any, cols: list, form: dict):
    """Clean User's Input (Update-Form)"""
    clean = clean_form(base, cols, form)
    return {key: val for key, val in clean.items() if val and key in form.keys()}
