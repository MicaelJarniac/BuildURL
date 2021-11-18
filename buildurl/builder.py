"""BuildURL's core."""

from copy import deepcopy
from typing import Any, Dict, List, Optional, Tuple, Union
from urllib.parse import parse_qs, urlencode, urlsplit, urlunsplit

# Type aliases
PathList = List[str]
Path = Union[str, PathList]
QueryDict = Dict[str, Any]
Query = Union[str, QueryDict]


class BuildURL:
    """Tool to simplify the creation of URLs with query parameters.

    Args:
        base:
            The base URL to build upon.
        force_trailing_slash:
            Whether or not to forcefully include a trailing slash at the end
            of `path`, `False` by default.

    Examples:
        >>> from buildurl import BuildURL
        >>> url = BuildURL("https://pypi.org")
        >>> print(url.get)
        https://pypi.org
        >>> url = BuildURL("https://example.com/test",
        ... force_trailing_slash=True)
        >>> print(url.get)
        https://example.com/test/
    """

    def __init__(self, base: str = "", force_trailing_slash: bool = False):
        """Initialize a new instance of BuildURL."""
        purl = urlsplit(base)

        # scheme://netloc/path;params?query#fragment
        # There can be one `params` per `path` element, so it's included as
        # part of `path`, and not isolated
        self.scheme: str = purl.scheme
        self.netloc: str = purl.netloc
        self._path_list: PathList = list()
        self.query_dict: QueryDict = dict()
        self.fragment: str = purl.fragment

        self.trailing_slash: bool = False
        self.force_trailing_slash: bool = force_trailing_slash

        path_str: str = purl.path
        if path_str:
            self.path = path_str

        query_str: str = purl.query
        if query_str:
            self.query = query_str

    def copy(self) -> "BuildURL":
        """Create a deep copy of itself.

        Examples:
            >>> url = BuildURL("https://example.com")
            >>> url_copy = url.copy()
            >>> url /= "test"
            >>> print(url.get)
            https://example.com/test
            >>> print(url_copy.get)
            https://example.com
        """
        return deepcopy(self)

    def set_force_trailing_slash(self, enabled: bool = True) -> "BuildURL":
        """Set the `force_trailing_slash` attribute.

        Args:
            enabled:
                The new value for `force_trailing_slash`, default `True`.

        Returns:
            Reference to self.

        Examples:
            >>> url = BuildURL("https://example.com")
            >>> url.set_force_trailing_slash().add_path("test")
            BuildURL(base='https://example.com/test/', force_trailing_slash=True)
            >>> url.set_force_trailing_slash(False)
            BuildURL(base='https://example.com/test', force_trailing_slash=False)
        """
        self.force_trailing_slash = enabled
        return self

    def add_path(self, *args: Path) -> "BuildURL":
        """Add to the path.

        Args:
            *args:
                The paths to add.
                Can be a string containing a single path, multiple paths
                separated by `/`, or a list of single path strings.

        Returns:
            Reference to self.

        Examples:
            >>> url = BuildURL("https://example.com")
            >>> url.add_path("test")
            BuildURL(...)
            >>> print(url.get)
            https://example.com/test
            >>> url.add_path(["more", "paths"]).add_path("/again/and/again/")
            BuildURL(...)
            >>> print(url.get)
            https://example.com/test/more/paths/again/and/again/
            >>> url = BuildURL("https://example.com")
            >>> url.add_path("never", "stopping", "to/play", ["with", "paths"])
            BuildURL(...)
            >>> print(url.get)
            https://example.com/never/stopping/to/play/with/paths
        """
        path_list = list()
        for path in args:
            if isinstance(path, str):
                path_list.extend(path.split("/"))
            elif isinstance(path, list):
                # TODO Convert some types to `str`, like `int` and `float`
                if not all((isinstance(p, str) for p in path)):
                    raise AttributeError
                path_list.extend(path)
            else:
                raise AttributeError

        if len(path_list):
            self.trailing_slash = path_list[-1] == ""
        path_list = [p for p in path_list if p]  # Remove empty strings

        self._path_list.extend(path_list)

        return self

    def add_query(self, *args: Query, **kwargs) -> "BuildURL":
        """Add a query argument.

        Args:
            *args:
                The query keys and values to add.
                Can be a string containing the keys and values, like
                `"key1=value1&key2=value2"`, or a dict, like
                `{"key1": "value1", "key2": "value2"}`.
            **kwargs:
                Keyword arguments corresponding to key-value pairs.

        Returns:
            Reference to self.

        Examples:
            >>> url = BuildURL("https://example.com")
            >>> url.add_query({"key": "value"})
            BuildURL(...)
            >>> print(url.get)
            https://example.com?key=value
            >>> url.add_query("another=query&more=stuff")
            BuildURL(...)
            >>> print(url.get)
            https://example.com?key=value&another=query&more=stuff
            >>> url.add_query(a="b").add_query("c=d", "e=f")
            BuildURL(...)
            >>> print(url.get)
            https://example.com?key=value&another=query&more=stuff&a=b&c=d&e=f
        """
        query_dict = dict()
        for query in args:
            if isinstance(query, str):
                query_dict.update(parse_qs(query))
            elif isinstance(query, dict):
                query_dict.update(query)
            else:
                raise AttributeError

        if kwargs:
            query_dict.update(kwargs)

        self.query_dict.update(query_dict)

        return self

    @property
    def path(self) -> str:
        """Path string."""
        path = "/".join(self._path_list)
        if self.trailing_slash or self.force_trailing_slash:
            path += "/"
        return path

    @path.setter
    def path(self, path: Optional[Path]):
        """Replace current path."""
        self._path_list = list()
        if path is not None:
            self.add_path(path)

    @property
    def query(self) -> str:
        """Query string."""
        return urlencode(self.query_dict, doseq=True)

    @query.setter
    def query(self, query: Optional[Query]):
        """Replace current query."""
        self.query_dict = dict()
        if query is not None:
            self.add_query(query)

    @property
    def parts(self) -> Tuple[str, ...]:
        """Tuple of necessary parts to construct the URL."""
        return (
            self.scheme,
            self.netloc,
            self.path,
            self.query,
            self.fragment,
        )

    @property
    def get(self) -> str:
        """Get the generated URL."""
        return urlunsplit(self.parts)

    def __itruediv__(self, path: Path) -> "BuildURL":
        """Add new path part to the URL inplace.

        Essentially a shortcut to ``add_path``.

        Args:
            path:
                New path to add.

        Returns:
            Reference to self.

        Examples:
            >>> url = BuildURL("https://example.com")
            >>> url /= "test"
            >>> print(url.get)
            https://example.com/test
            >>> url /= ["more", "paths"]
            >>> print(url.get)
            https://example.com/test/more/paths
            >>> url /= "/again/and/again/"
            >>> print(url.get)
            https://example.com/test/more/paths/again/and/again/
        """
        self.add_path(path)
        return self

    def __truediv__(self, path: Path) -> "BuildURL":
        """Generate new URL with added path.

        Equivalent to first copying the URL, then using ``add_path``.

        Args:
            path:
                New path to add.

        Returns:
            New BuildURL instance.

        Examples:
            >>> url = BuildURL("https://example.com")
            >>> new_url = url / "testing"
            >>> print(url.get)
            https://example.com
            >>> print(new_url.get)
            https://example.com/testing
        """
        out = self.copy()
        out /= path
        return out

    def __iadd__(self, query: Query) -> "BuildURL":
        """Add query arguments inplace.

        Essentially a shortcut to ``add_query``.

        Args:
            query:
                The query key and value to add.

        Returns:
            Reference to self.

        Examples:
            >>> url = BuildURL("https://example.com")
            >>> url += {"key": "value"}
            >>> print(url.get)
            https://example.com?key=value
            >>> url += "another=query&more=stuff"
            >>> print(url.get)
            https://example.com?key=value&another=query&more=stuff
        """
        self.add_query(query)
        return self

    def __add__(self, query: Query) -> "BuildURL":
        """Generate new URL with added query.

        Equivalent to first copying the URL, then using ``add_query``.

        Args:
            query:
                The query key and value to add.

        Returns:
            New BuildURL instance.

        Examples:
            >>> url = BuildURL("https://example.com")
            >>> new_url = url + {"test": "it"}
            >>> print(url.get)
            https://example.com
            >>> print(new_url.get)
            https://example.com?test=it
        """
        out = self.copy()
        out += query
        return out

    def __repr__(self) -> str:
        """Representation of the current instance.

        Returns:
            String representation of self.

        Examples:
            >>> url = BuildURL("https://example.com/test?now=true")
            >>> print(repr(url))
            BuildURL(base='https://example.com/test?now=true', force_trailing_slash=False)
        """
        return f"{self.__class__.__name__}(base='{self.get}', force_trailing_slash={self.force_trailing_slash})"

    def __str__(self) -> str:
        """Shortcut for getting the URL.

        Can be obtained by printing the instance of the class.

        Returns:
            Generated URL.

        Examples:
            >>> url = BuildURL("https://example.com")
            >>> url /= "test"
            >>> print(str(url))
            https://example.com/test
            >>> print(url)
            https://example.com/test
        """
        return self.get

    def __len__(self) -> int:
        """Length of the generated URL."""
        return len(self.get)
