# config/merge.py
def deep_merge(a: dict, b: dict) -> dict:
    """
    Recursive deep merge of dict b into dict a.
    Dict values are merged, scalar values from b overwrite a.
    """
    for k, v in b.items():
        if (
            k in a
            and isinstance(a[k], dict)
            and isinstance(v, dict)
        ):
            deep_merge(a[k], v)
        else:
            a[k] = v
    return a