import itksn
from itksn.core import EnumStr
from construct import Bytes


def test_enumstr():
    myenum = EnumStr(Bytes(2), itsaa=b"aa", itsbb=b"bb", itsyy=b"yy")
    assert myenum.parse(b"yy").intvalue == b"yy"
    assert myenum.parse(b"yy") == "itsyy"
    assert myenum.parse(b"xx").intvalue == b"xx"
    assert myenum.parse(b"xx") == ""


def test_parse_example1():
    parsed = itksn.parse(b"20Uxxyynnnnnnn")
    assert parsed.atlas_project == "atlas_detector"
    assert parsed.system_code == "phaseII_upgrade"
    assert parsed.project_code == ""
    assert parsed.subproject_code == b"yy"
    assert parsed.identifier == b"nnnnnnn"


def test_parse_example2():
    parsed = itksn.parse(b"20UPIyynnnnnnn")
    assert parsed.atlas_project == "atlas_detector"
    assert parsed.system_code == "phaseII_upgrade"
    assert parsed.project_code == "inner_pixel"
    assert parsed.subproject_code == b"yy"
    assert parsed.identifier == b"nnnnnnn"
