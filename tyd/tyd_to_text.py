from typing import List

from .nodes import TydNode, TydString, TydTable, TydCollection, TydList, TydDocument
from .constants import Constants


def write(node: TydNode, indent: int = 0) -> str:

    if isinstance(node, TydString):
        return (
            _indent_string(indent)
            + ((node.name + " ") if node.name is not None else "")
            + _string_content_writable(node.value)
        )

    if isinstance(node, (TydTable, TydDocument)):
        sb = []

        if _append_node_intro(node, sb, indent) and len(node) > 0:
            sb.append("\n")

        if len(node) == 0:
            sb.append(Constants.TABLE_START_CHAR + Constants.TABLE_END_CHAR + "\n")
        else:
            sb.append(_indent_string(indent) + Constants.TABLE_START_CHAR + "\n")
            for i in node:
                sb.append(write(i, indent + 1) + "\n")
            sb.append(_indent_string(indent) + Constants.TABLE_END_CHAR + "\n")

        return "".join(sb)

    if isinstance(node, TydList):
        sb = []

        if _append_node_intro(node, sb, indent) and len(node) > 0:
            sb.append("\n")

        if len(node) == 0:
            sb.append(Constants.LIST_START_CHAR + Constants.LIST_END_CHAR + "\n")
        else:
            sb.append(_indent_string(indent) + Constants.LIST_START_CHAR + "\n")
            for i in node:
                sb.append(write(i, indent + 1) + "\n")
            sb.append(_indent_string(indent) + Constants.LIST_END_CHAR + "\n")

        return "".join(sb)

    raise Exception()


def _string_content_writable(value: str) -> str:
    if value == "":
        return '""'

    if value is None:
        return Constants.NULL_VALUE_STRING

    return (
        '"' + _escape_chars_escaped_for_quoted_string(value) + '"'
        if _should_write_with_quotes(value)
        else value
    )


def _should_write_with_quotes(value: str) -> bool:
    if len(value) > 40:
        return True

    if value[len(value) - 1] == ".":
        return True

    for char in value:
        if (
            char == ""
            or char == "\n"
            or char == "\t"
            or char == '"'
            or char == Constants.COMMENT_CHAR
            or char == Constants.RECORD_END_CHAR
            or char == Constants.ATTRIBUTE_START_CHAR
            or char == Constants.TABLE_START_CHAR
            or char == Constants.TABLE_END_CHAR
            or char == Constants.LIST_START_CHAR
            or char == Constants.LIST_END_CHAR
        ):
            return True

    return False


def _escape_chars_escaped_for_quoted_string(value: str) -> str:
    return value.replace('"', '\\"').replace(
        Constants.COMMENT_CHAR, "\\" + Constants.COMMENT_CHAR
    )


def _append_node_intro(node: TydCollection, sb: List[str], indent: int) -> bool:
    appended_something = False

    if node.name is not None:
        _append_with_whitespace(node.name, sb, indent, appended_something)
        appended_something = True

    if node.attribute_abstract:
        _append_with_whitespace(
            Constants.ATTRIBUTE_START_CHAR + Constants.ABSTRACT_ATTRIBUTE_NAME,
            sb,
            indent,
            appended_something,
        )
        appended_something = True

    if node.attribute_no_inherit:
        _append_with_whitespace(
            Constants.ATTRIBUTE_START_CHAR + Constants.NO_INHERIT_ATTRIBUTE_NAME,
            sb,
            indent,
            appended_something,
        )
        appended_something = True

    if node.attribute_handle is not None:
        _append_with_whitespace(
            Constants.ATTRIBUTE_START_CHAR
            + Constants.HANDLE_ATTRIBUTE_NAME
            + " "
            + node.attribute_handle,
            sb,
            indent,
            appended_something,
        )
        appended_something = True

    if node.attribute_source is not None:
        _append_with_whitespace(
            Constants.ATTRIBUTE_START_CHAR
            + Constants.SOURCE_ATTRIBUTE_NAME
            + " "
            + node.attribute_source,
            sb,
            indent,
            appended_something,
        )

    return appended_something


def _append_with_whitespace(
    s: str, sb: List[str], indent: int, appended_something: bool
) -> None:
    sb.append((" " if appended_something else _indent_string(indent)) + s)


def _indent_string(indent: int):
    s = ""

    for i in range(indent):
        s += "    "

    return s
