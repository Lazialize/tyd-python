from __future__ import annotations
from os.path import basename, splitext
from typing import Optional

from .nodes import TydDocument
from .tyd_from_text import parse
from .tyd_to_text import write


def from_document(doc: TydDocument, file_path: Optional[str] = None) -> TydFile:
    """Returns TydFile object created from a TydDocument object.

    Parameters
    ----------
    doc : TydDocument
        A TydDocument object to use to create TydFile.
    file_path : Optional[str]
        A string representing file path, by default None.

    Returns
    -------
    TydFile
        A TydFile created.
    """
    tyd_file = TydFile(doc, file_path)
    return tyd_file


def from_file(file_path: str) -> TydFile:
    """Returns TydFile object created from a file of path passed.

    Parameters
    ----------
    file_path : str
        A string representing filepath.

    Returns
    -------
    TydFile
        A TydFile created.
    """
    try:
        with open(file_path, mode="r", encoding="utf-8") as f:
            read_contents = f.read()

        tyd_node_list = list(parse(read_contents))
        tyd_doc = TydDocument(tyd_node_list)
        return from_document(tyd_doc, file_path)
    except Exception as e:
        raise Exception(f"Exception loading {file_path}: {e}")


class TydFile:
    """This represents tyd file objects.

    **Don't instance!**
    The class is not intended to be created by users.
    You can get instances of the class only via class methods.
    """

    def __init__(self, doc: TydDocument, file_path: Optional[str] = None):
        self._doc: TydDocument = doc
        self._file_path: str = file_path

    @property
    def document(self) -> TydDocument:
        return self._doc

    @document.setter
    def document(self, value: TydDocument) -> None:
        if not isinstance(value, TydDocument):
            # TODO: Will add an error message
            raise TypeError()

        self._doc = value

    @property
    def file_path(self) -> str:
        return self._file_path

    @property
    def file_name(self) -> str:
        return splitext(basename(self._file_path))[0]

    def save(self, file_path=None):
        if file_path is not None:
            self._file_path = file_path
        elif file_path is None:
            raise AttributeError(
                "When didn't set filepath to TydFile, filepath parameter mustn't be None."
            )

        builder = list()

        for node in self._doc:
            builder.append(write(node) + "\n")

        with open(file_path, mode="w", encoding="utf-8") as f:
            f.write("".join(builder))
