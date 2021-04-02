from pytest import raises

from buildurl import BuildURL


def test_base():
    url = BuildURL("https://example.com")
    assert url.get == "https://example.com"
    assert str(url) == "https://example.com"
    assert len(url) == 19


def test_split():
    url = BuildURL("scheme://netloc/path;params?query=value#fragment")
    assert url.get == "scheme://netloc/path;params?query=value#fragment"
    assert url.scheme == "scheme"
    assert url.netloc == "netloc"
    assert url.path == "path;params"
    assert url.query == "query=value"
    assert url.fragment == "fragment"


def test_fresh():
    url = BuildURL()
    assert url.get == ""
    url.scheme = "scheme"
    url.netloc = "netloc"
    url.path = "path;params"
    url.query = "query=value"
    url.fragment = "fragment"
    assert url.get == "scheme://netloc/path;params?query=value#fragment"


def test_path():
    url = BuildURL("https://example.com")
    url /= "test"
    assert url.get == "https://example.com/test"
    url /= "more"
    assert url.get == "https://example.com/test/more"
    assert str(url / "again") == "https://example.com/test/more/again"
    assert url.get == "https://example.com/test/more"
    url /= ["paths", "added"]
    assert url.get == "https://example.com/test/more/paths/added"
    assert url.path == "test/more/paths/added"

    with raises(AttributeError):
        url /= 0
    with raises(AttributeError):
        url /= 0.1
    with raises(AttributeError):
        url /= True

    assert url.get == "https://example.com/test/more/paths/added"

    url = BuildURL("https://example.com/why")
    assert url.get == "https://example.com/why"
    url.path = ["still", "testing"]
    assert url.get == "https://example.com/still/testing"
    url.path = "/once/more/"
    assert url.get == "https://example.com/once/more/"
    url.path = ["again", "and", "again"]
    assert url.get == "https://example.com/again/and/again"
    url.path = None
    assert url.get == "https://example.com"

    url = BuildURL("https://example.com/")
    assert url.get == "https://example.com/"
    url /= "path"
    assert url.get == "https://example.com/path"
    url /= "another//path"
    assert url.get == "https://example.com/path/another/path"
    url /= "/again/"
    assert url.get == "https://example.com/path/another/path/again/"

    url = BuildURL("https://example.com/folder/")
    assert url.get == "https://example.com/folder/"


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

    with raises(AttributeError):
        url += 0
    with raises(AttributeError):
        url += 0.1
    with raises(AttributeError):
        url += True

    assert url.get == "https://example.com?test=well&and=again"

    url = BuildURL("https://example.com?testing=true")
    assert url.get == "https://example.com?testing=true"
    url.query = {"still": "testing"}
    assert url.get == "https://example.com?still=testing"
    url.query = "once=more"
    assert url.get == "https://example.com?once=more"
    url.query_dict = {"again": "and-again"}
    assert url.get == "https://example.com?again=and-again"
    url.query = None
    assert url.get == "https://example.com"


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
