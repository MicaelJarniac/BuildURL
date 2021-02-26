from buildurl import BuildURL


def test_base():
    url = BuildURL("https://example.com")
    assert url.get == "https://example.com"
    assert str(url) == "https://example.com"
    assert len(url) == 19


def test_path():
    url = BuildURL("https://example.com")
    url /= "test"
    assert url.get == "https://example.com/test"
    url /= "more"
    assert url.get == "https://example.com/test/more"
    assert str(url / "again") == "https://example.com/test/more/again"
    assert url.get == "https://example.com/test/more"


def test_query():
    url = BuildURL("https://example.com")
    url += {"test": "well"}
    assert url.get == "https://example.com?test=well"
    url += {"and": "again"}
    assert url.get == "https://example.com?test=well&and=again"
    assert (
        str(url + {"once": "more"})
        == "https://example.com?test=well&and=again&once=more"
    )
    assert url.get == "https://example.com?test=well&and=again"


def test_copy():
    url = BuildURL("https://example.com")
    url_copy = url.copy()
    url /= "original"
    url_copy /= "copy"
    assert url.get == "https://example.com/original"
    assert url_copy.get == "https://example.com/copy"


def test_repr():
    url = BuildURL("https://example.com")
    assert repr(url) == "BuildURL(base='https://example.com')"
    url /= "repr"
    assert repr(url) == "BuildURL(base='https://example.com/repr')"
    url += {"testing": "it"}
    assert repr(url) == "BuildURL(base='https://example.com/repr?testing=it')"