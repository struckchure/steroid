def formatPath(text: str) -> str:
    if len(text) == 0:
        return text
    return f"/{text}" if not text.startswith("/") else text


def removeLeadingOrTrailingSlash(text: str) -> str:
    if text.startswith("/"):
        text = text[1:]
    if text.endswith("/"):
        text = text[:-1]

    return text
