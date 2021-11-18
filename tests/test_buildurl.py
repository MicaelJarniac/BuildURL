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
    with raises(AttributeError):
        url.add_path(["a", "b", 1, 2])

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

    url = BuildURL("https://example.com")
    url.add_path("one", "two", ["three", "four", "five", "six"], "seven//eight")
    assert url.get == "https://example.com/one/two/three/four/five/six/seven/eight"


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

    url = BuildURL("https://example.com")
    url.add_query("a=b&c=d", {"e": "f", "g": "h"}, i="j", k="l")
    assert url.get == "https://example.com?a=b&c=d&e=f&g=h&i=j&k=l"


def test_trailing_slash():
    url = BuildURL("https://example.com/")
    assert url.get == "https://example.com/"

    url = BuildURL("https://example.com/test", force_trailing_slash=True)
    assert url.get == "https://example.com/test/"

    url = BuildURL("https://example.com")
    url /= "test/"
    assert url.get == "https://example.com/test/"

    url = BuildURL("https://example.com")
    url.add_path("test").set_force_trailing_slash().add_query(a="b")
    assert url.get == "https://example.com/test/?a=b"
    url.set_force_trailing_slash(False)
    assert url.get == "https://example.com/test?a=b"
    url.trailing_slash = True
    assert url.get == "https://example.com/test/?a=b"
    url /= "path"
    assert url.get == "https://example.com/test/path?a=b"
    url.force_trailing_slash = True
    url /= "more"
    assert url.get == "https://example.com/test/path/more/?a=b"


def test_copy():
    url = BuildURL("https://example.com")
    url_copy = url.copy()
    url /= "original"
    url_copy /= "copy"
    assert url.get == "https://example.com/original"
    assert url_copy.get == "https://example.com/copy"


def test_repr():
    url = BuildURL("https://example.com")
    assert (
        repr(url) == "BuildURL(base='https://example.com', force_trailing_slash=False)"
    )
    url /= "repr"
    assert (
        repr(url)
        == "BuildURL(base='https://example.com/repr', force_trailing_slash=False)"
    )
    url += {"testing": "it"}
    assert (
        repr(url)
        == "BuildURL(base='https://example.com/repr?testing=it', force_trailing_slash=False)"
    )

    url = BuildURL("https://example.com", force_trailing_slash=True)
    assert (
        repr(url) == "BuildURL(base='https://example.com/', force_trailing_slash=True)"
    )


def test_chaining():
    url = BuildURL("https://example.com")
    url.add_path("one").add_path("two")
    assert url.get == "https://example.com/one/two"
    url.add_query({"test": "more"}).add_path("three").add_query("testing=a_lot")
    assert url.get == "https://example.com/one/two/three?test=more&testing=a_lot"
