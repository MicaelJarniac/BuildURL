from copy import deepcopy
from typing import Any, Dict, List, Optional, Tuple, Union
from urllib.parse import parse_qs, urlencode, urlsplit, urlunsplit

# Type aliases
PathList = List[str]
Path = Union[str, PathList]
QueryDict = Dict[str, Any]
Query = Union[str, QueryDict]


class BuildURL:
    """Tool to simplify the creation of URLs with query parameters"""

    def __init__(self, base: str = ""):
        """Start the creation of an URL.

        Args:
            base:
                The base URL to build upon.
        """

        # self.base = base

        purl = urlsplit(base)

        # scheme://netloc/path;params?query#fragment
        # There can be one `params` per `path` element, so it's included as
        # part of `path`, and not isolated
        self.scheme: str = purl.scheme
        self.netloc: str = purl.netloc
        self.path_list: PathList = list()
        self.query_dict: QueryDict = dict()
        self.fragment: str = purl.fragment

        path_str: str = purl.path
        if path_str:
            self.path = path_str

        query_str: str = purl.query
        if query_str:
            self.query = query_str

    def copy(self) -> "BuildURL":
        """Create a deep copy of itself."""
        return deepcopy(self)

    def add_path(self, path: Path) -> None:
        """Add to the path.

        Args:
            path:
                The path to add.
        """

        path_list = list()
        if isinstance(path, str):
            path_list = path.split("/")
        elif isinstance(path, list):
            path_list = path
        else:
            raise AttributeError

        path_list = [p for p in path_list if p]  # Remove empty strings

        self.path_list.extend(path_list)

    def add_query(self, query: Query) -> None:
        """Add a query argument.

        Args:
            query:
                The query keys and arguments to add.
        """

        query_dict = dict()
        if isinstance(query, str):
            query_dict = parse_qs(query)
        elif isinstance(query, dict):
            query_dict = query
        else:
            raise AttributeError

        self.query_dict.update(query_dict)

    @property
    def path(self) -> str:
        """Path string."""
        return "/".join(self.path_list)

    @path.setter
    def path(self, path: Optional[Path]):
        """Replace current path."""
        self.path_list = list()
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

        Args:
            path:
                New path to add.

        Returns:
            Reference to self.
        """

        self.add_path(path)
        return self

    def __truediv__(self, path: Path) -> "BuildURL":
        """Generate new URL with added path.

        Args:
            path:
                New path to add.

        Returns:
            New BuildURL instance.
        """

        out = self.copy()
        out /= path
        return out

    def __iadd__(self, query: Query) -> "BuildURL":
        """Add query arguments inplace.

        Args:
            query:
                The query key and value to add.

        Returns:
            Reference to self.
        """

        self.add_query(query)
        return self

    def __add__(self, query: Query) -> "BuildURL":
        """Generate new URL with added query.

        Args:
            query:
                The query key and value to add.

        Returns:
            New BuildURL instance.
        """

        out = self.copy()
        out += query
        return out

    def __repr__(self) -> str:
        """Representation of the current instance.

        Returns:
            String representation of self.
        """

        return f"{self.__class__.__name__}(base='{self.get}')"

    def __str__(self) -> str:
        """Shortcut for getting the URL.

        Can be obtained by printing the instance of the class.

        Returns:
            Generated URL.
        """

        return self.get

    def __len__(self) -> int:
        """Length of the generated URL."""
        return len(self.get)
