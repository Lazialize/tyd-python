from os.path import dirname
import pytest

from tyd import TydTable, TydString, TydList

current_dir = dirname(__file__)


@pytest.fixture(params=list(range(3)))
def test_tyd_from_text_params(request):
    if request.param == 0:
        return request.getfixturevalue("test_tyd_from_text_001")
    elif request.param == 1:
        return request.getfixturevalue("test_tyd_from_text_002")
    elif request.param == 2:
        return request.getfixturevalue("test_tyd_from_text_003")


@pytest.fixture
def test_tyd_from_text_001():
    with open(f"{current_dir}/files/testcase_001.tyd", mode="r", encoding="utf-8") as f:
        ans = f.read()
    obj = TydTable("TestCase001", None)
    obj.add(TydString("name", "testcase_001", obj))
    obj.add(TydString("description", "this is a test file for tyd parser", obj))
    obj.add(TydString("content", "test", obj))

    yield (
        obj,
        ans,
    )


@pytest.fixture
def test_tyd_from_text_002():
    with open(f"{current_dir}/files/testcase_002.tyd", mode="r", encoding="utf-8") as f:
        ans = f.read()

    obj = TydTable("TestCase002", None)
    obj.add(TydString("name", "testcase_002", obj))
    obj.add(TydString("description", "This is a test file for tyd parser.", obj))

    content = TydList("content", obj)
    content.add(TydString(None, "testcase_001", obj))
    content.add(TydString(None, "testcase_002", obj))
    content.add(TydString(None, "testcase_003", obj))

    obj.add(content)

    yield (
        obj,
        ans,
    )


@pytest.fixture
def test_tyd_from_text_003():
    with open(f"{current_dir}/files/testcase_003.tyd", mode="r", encoding="utf-8") as f:
        ans = f.read()

    obj = TydTable("TestCase003", None)
    obj.add(TydString("name", "testcase_003", obj))
    obj.add(TydString("description", "This is a test file for tyd parser", obj))

    content = TydTable("content", obj)
    content_1 = TydTable("testcase_001", content)
    content_1.add(TydString("description", "test", content_1))
    content_2 = TydTable("testcase_002", content)
    content_2.add(TydString("content", None, content_2))
    content.add(content_1)
    content.add(content_2)

    obj.add(content)

    yield (
        obj,
        ans,
    )
