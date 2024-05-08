def validate_category_name(name: str | None) -> str:
    if not isinstance(name, str):
        return

    name = name.strip()
    if len(name) == 0:
        return

    return name
