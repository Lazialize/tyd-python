from collections import namedtuple
from enum import Enum
from typing import Iterator

from .constants import Constants
from .nodes import TydNode, TydTable, TydList, TydString
from .utils import is_white_space


LineColumn = namedtuple("LineColumn", ["line", "column"])
SymbolAndPointer = namedtuple("SymbolAndPointer", ["pointer", "symbol"])
StringAndPointer = namedtuple("StringAndPointer", ["pointer", "value"])


class SymbolType(Enum):
    RECORD_NAME = 1
    ATTRIBUTE_NAME = 2
    ATTRIBUTE_VALUE = 3


class StringFormat(Enum):
    NAKED = 1
    QUOTED = 2
    VERTICAL = 3


def parse(
    text: str, startIndex: int = 0, parent: TydNode = None, expect_names: bool = True
) -> Iterator[TydNode]:
    p = startIndex

    while True:
        record_name = None
        record_attribute_handle = None
        record_attribute_source = None
        record_attribute_abstract = False
        record_attribute_no_inherit = False

        try:
            p = _next_substance_index(text, p)

            if p == len(text):
                if parent is not None:
                    raise Exception("Missing closing brackets")
                break

            if (
                text[p] == Constants.TABLE_END_CHAR
                or text[p] == Constants.LIST_END_CHAR
            ):
                break

            if expect_names:
                result = _read_symbol(text, SymbolType.RECORD_NAME, p)
                record_name = result.symbol
                p = result.pointer

            p = _next_substance_index(text, p)

            while text[p] == Constants.ATTRIBUTE_START_CHAR:
                p += 1

                result = _read_symbol(text, SymbolType.ATTRIBUTE_NAME, p)
                attribute_name = result.symbol
                p = result.pointer

                if attribute_name == Constants.ABSTRACT_ATTRIBUTE_NAME:
                    record_attribute_abstract = True
                elif attribute_name == Constants.NO_INHERIT_ATTRIBUTE_NAME:
                    record_attribute_no_inherit = True
                else:
                    p = _next_substance_index(text, p)

                    result = _read_symbol(text, SymbolType.ATTRIBUTE_VALUE, p)
                    attribute_value = result.symbol
                    p = result.pointer

                    if attribute_name == Constants.HANDLE_ATTRIBUTE_NAME:
                        record_attribute_handle = attribute_value
                    elif attribute_name == Constants.SOURCE_ATTRIBUTE_NAME:
                        record_attribute_source = attribute_value
                    else:
                        raise Exception(
                            "Unknown attribute name"
                            + attribute_name
                            + " at "
                            + _line_column_string(text, p)
                            + "\n"
                            + _error_section_string(text, p)
                        )

                p = _next_substance_index(text, p)
        except Exception as e:
            raise Exception(
                "Exception parsing Tyd headers at "
                + _line_column_string(text, p)
                + ": "
                + e
                + "\n"
                + _error_section_string(text, p)
            )

        if text[p] == Constants.TABLE_START_CHAR:
            new_table = TydTable(record_name, parent, _index_to_line(text, p))

            p += 1

            p = _next_substance_index(text, p)

            for node in parse(text, p, new_table, True):
                new_table.add(node)
                p = node.docindexend + 1

            p = _next_substance_index(text, p)

            if text[p] != Constants.TABLE_END_CHAR:
                raise Exception(
                    "Expanded '"
                    + Constants.TABLE_END_CHAR
                    + "' at "
                    + _line_column_string(text, p)
                    + "\n"
                    + _error_section_string(text, p)
                )

            new_table.docindexend = p
            new_table.setup_attributes(
                record_attribute_handle,
                record_attribute_source,
                record_attribute_abstract,
                record_attribute_no_inherit,
            )
            yield new_table

            p += 1

        elif text[p] == Constants.LIST_START_CHAR:
            new_list = TydList(record_name, parent, _index_to_line(text, p))

            p += 1

            p = _next_substance_index(text, p)

            for node in parse(text, p, new_list, False):
                new_list.add(node)
                p = node.docindexend + 1

            p = _next_substance_index(text, p)

            if text[p] != Constants.LIST_END_CHAR:
                raise Exception(
                    "Expanded '"
                    + Constants.LIST_END_CHAR
                    + "' at "
                    + _line_column_string(text, p)
                    + "\n"
                    + _error_section_string(text, p)
                )

            new_list.docindexend = p
            new_list.setup_attributes(
                record_attribute_handle,
                record_attribute_source,
                record_attribute_abstract,
                record_attribute_no_inherit,
            )

            yield new_list

            p += 1
        else:
            pstart = p

            result = _parse_string_value(text, pstart)
            p = result.pointer
            val = result.value

            node = TydString(record_name, val, parent, _index_to_line(text, pstart))
            node.docindexend = p - 1
            yield node


def _parse_string_value(text: str, p: int) -> StringAndPointer:
    if text[p] == '"':
        fmt = StringFormat.QUOTED
    elif text[p] == "|":
        fmt = StringFormat.VERTICAL
    else:
        fmt = StringFormat.NAKED

    if fmt == StringFormat.QUOTED:
        p += 1

        pstart = p

        while p < len(text) and not (text[p] == '"' and text[p - 1] != "\\"):
            p += 1

        val = text[pstart:p]

        val = _resolve_escape_chars(val)

        p += 1

        return StringAndPointer(p, val)
    elif fmt == StringFormat.VERTICAL:
        builder = list()

        while True:
            p += 1
            line_content_start = p

            while p < len(text) and not _is_new_line(text, p):
                p += 1

            builder.append(text[line_content_start:p])
            p = _next_substance_index(text, p)

            if p < len(text) and text[p] == "|":
                builder.append("\n")
                continue

            else:
                val = "".join(builder)
                return StringAndPointer(p, val)

    elif fmt == StringFormat.NAKED:
        pstart = p

        while (
            p < len(text)
            and not _is_new_line(text, p)
            and not (
                (
                    text[p] == Constants.RECORD_END_CHAR
                    or text[p] == Constants.COMMENT_CHAR
                    or text[p] == Constants.TABLE_END_CHAR
                    or text[p] == Constants.LIST_END_CHAR
                )
                and text[p - 1] != "\\"
            )
        ):
            p += 1

        q = p - 1
        while is_white_space(text[q]):
            q -= 1

        val = text[pstart : q + 1]

        if val == Constants.NULL_VALUE_STRING:
            val = None

        else:
            val = _resolve_escape_chars(val)

        return StringAndPointer(p, val)
    else:
        raise Exception()


def _resolve_escape_chars(input_value: str):
    i = 0
    while i < len(input_value):
        if input_value[i] == "\\":
            if len(input_value) <= i + 1:
                raise Exception(
                    "Tyd string value ends with single backslash: " + input_value
                )

            resolved_char = _escaped_char_of(input_value[i + 1])
            input_value = input_value[:i] + resolved_char + input_value[i + 2 :]
        i += 1
    return input_value


def _escaped_char_of(char: str):
    if char == "\\":
        return "\\"
    elif char == '"':
        return '"'
    elif char == "#":
        return "#"
    elif char == ";":
        return ";"
    elif char == "]":
        return "]"
    elif char == "}":
        return "}"
    elif char == "\r":
        return "\u000D"
    elif char == "n":
        return "\u000A"
    elif char == "t":
        return "\u0009"
    else:
        raise Exception("Cannot escape char: \\" + char)


def _read_symbol(text: str, st: SymbolType, p: int) -> SymbolAndPointer:
    pstart = p
    while True:
        c = text[p]

        if is_white_space(c):
            break

        if not _is_symbol_char(c):
            break

        p += 1

    if p == pstart:
        raise Exception(
            "Expected "
            + _symbol_type_name(st)
            + " at "
            + _line_column_string(text, p)
            + "\n"
            + _error_section_string(text, p)
        )

    return SymbolAndPointer(p, text[pstart:p])


def _symbol_type_name(st: SymbolType):
    if st == SymbolType.RECORD_NAME:
        return "record name"
    elif st == SymbolType.ATTRIBUTE_NAME:
        return "attribute name"
    elif st == SymbolType.ATTRIBUTE_VALUE:
        return "attribute value"
    else:
        raise Exception("Passed value isn't SymbolType")


def _is_symbol_char(c: str) -> bool:
    return c in Constants.SYMBOL_CHARS


def _is_new_line(text: str, p: int) -> bool:
    return _is_new_line_lf(text, p) or _is_new_line_crlf(text, p)


def _is_new_line_lf(text: str, p: int) -> bool:
    return text[p] == "\n"


def _is_new_line_crlf(text: str, p: int) -> bool:
    return text[p] == "\r" and p < len(text) - 1 and text[p + 1] == "\n"


def _line_column_string(text: str, index: int):
    result = _index_to_line_column(text, index)
    return f"line {result.line}, col {result.column}"


def _insert_string(index: int, base: str, insert: str) -> str:
    head = base[:index]
    tail = base[index:]
    return f"{head}{insert}{tail}"


def _error_section_string(text: str, index: int):
    CHAR_RANGE_WIDTH = 500

    modtext = text
    modtext = _insert_string(min(index, len(text) - 1), modtext, "[ERROR]")

    if index > CHAR_RANGE_WIDTH or len(text) > index + CHAR_RANGE_WIDTH:
        start = min(index - CHAR_RANGE_WIDTH, 0)
        length = min(CHAR_RANGE_WIDTH * 2, len(text) - index)
        text = text[start : start + length]

    return modtext


def _index_to_line(text: str, index: int) -> int:
    result = _index_to_line_column(text, index)
    return result.line


def _index_to_line_column(text: str, index: int) -> LineColumn:
    line = 1
    column = 1

    p = 0
    while p < index:
        if _is_new_line_lf(text, p):
            line += 1
            column = 0
        elif _is_new_line_crlf(text, p):
            line += 1
            column = 0
            p += 1
        column += 1
        p += 1

    return LineColumn(line, column)


def _next_substance_index(text: str, p: int) -> int:
    while True:
        if p >= len(text):
            return len(text)

        if is_white_space(text[p]):
            p += 1
            continue

        if text[p] == Constants.RECORD_END_CHAR:
            p += 1
            continue

        if text[p] == Constants.COMMENT_CHAR:
            while p < len(text) and _is_new_line(text, p):
                p += 1

            if _is_new_line_lf(text, p):
                p += 1
            elif _is_new_line_crlf(text, p):
                p += 2
            else:
                raise Exception()

            continue

        return p
