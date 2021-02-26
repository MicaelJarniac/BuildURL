from copy import deepcopy
from typing import Any, Dict, Union
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse


class BuildURL:
    """Tool to simplify the creation of URLs with query parameters"""

    def __init__(self, base: str):
        """Start the creation of an URL.

        Args:
            base:
                The base URL to build upon.
        """

        # self.base = base

        purl = urlparse(base)

        # scheme://netloc/path;params?query#fragment
        self.scheme: str = purl.scheme
        self.netloc: str = purl.netloc
        self._path_list: list = list()
        self.params: str = purl.params
        self._query_dict: dict = dict()
        self.fragment: str = purl.fragment

        path_str: str = purl.path
        query_str: str = purl.query

        if path_str:
            self.add_path(path_str.split("/"))
        if query_str:
            self.add_query(parse_qs(query_str))

    def copy(self) -> "BuildURL":
        """Create a deep copy of itself."""
        return deepcopy(self)

    def add_query(self, query: Dict[str, Any]) -> None:
        """Add a query argument.

        Args:
            query:
                The query keys and arguments to add.
        """

        self._query_dict.update(query)

    def add_path(self, path: Union[str, list]) -> None:
        """Add to the path.

        Args:
            path:
                The path to add.
        """

        if isinstance(path, str):
            self._path_list.append(path)
        elif isinstance(path, list):
            self._path_list.extend(path)
        else:
            raise AttributeError

    @property
    def path(self) -> str:
        """Path string."""
        return "/".join(self._path_list)

    @property
    def query(self) -> str:
        """Query string."""
        return urlencode(self._query_dict, doseq=True)

    @property
    def parts(self) -> tuple:
        """Tuple of necessary parts to construct the URL."""
        return (
            self.scheme,
            self.netloc,
            self.path,
            self.params,
            self.query,
            self.fragment,
        )

    @property
    def get(self) -> str:
        """Get the generated URL."""
        return urlunparse(self.parts)

    def __itruediv__(self, path: str) -> "BuildURL":
        """Add new path part to the URL inplace.

        Args:
            path:
                New path to add.

        Returns:
            Reference to self.
        """

        self.add_path(path)
        return self

    def __truediv__(self, path: str) -> "BuildURL":
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

    def __iadd__(self, query: Dict[str, Any]) -> "BuildURL":
        """Add query arguments inplace.

        Args:
            query:
                The query key and value to add.

        Returns:
            Reference to self.
        """

        self.add_query(query)
        return self

    def __add__(self, query: Dict[str, Any]) -> "BuildURL":
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
