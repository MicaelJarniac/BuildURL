<div align="center">

  [![Discord][badge-chat]][chat]
  <br>
  <br>

  | | ![Badges][label-badges] |
  |--|--|
  | ![Build][label-build] | [![Python package][badge-actions]][actions] [![semantic-release][badge-semantic-release]][semantic-release] [![PyPI][badge-pypi]][pypi] [![Read the Docs][badge-docs]][docs] |
  | ![Tests][label-tests] | [![coverage][badge-coverage]][coverage] [![pre-commit][badge-pre-commit]][pre-commit] |
  | ![Standards][label-standards] | [![SemVer 2.0.0][badge-semver]][semver] [![Conventional Commits][badge-conventional-commits]][conventional-commits] |
  | ![Code][label-code] | [![Code style: black][badge-black]][Black] [![Imports: isort][badge-isort]][isort] [![Checked with mypy][badge-mypy]][mypy] |
  | ![Repo][label-repo] | [![GitHub issues][badge-issues]][issues] [![GitHub stars][badge-stars]][stars] [![GitHub license][badge-license]][license] [![All Contributors][badge-all-contributors]][contributors] |
</div>

<!-- Badges -->
[badge-chat]: https://img.shields.io/discord/269146666441900032?label=chat&logo=discord&style=flat-square
[chat]: https://discord.gg/6Q5XW5H

<!-- Labels -->
[label-badges]: https://img.shields.io/badge/%F0%9F%94%96-badges-purple?style=for-the-badge
[label-build]: https://img.shields.io/badge/%F0%9F%94%A7-build-darkblue?style=flat-square
[label-tests]: https://img.shields.io/badge/%F0%9F%A7%AA-tests-darkblue?style=flat-square
[label-standards]: https://img.shields.io/badge/%F0%9F%93%91-standards-darkblue?style=flat-square
[label-code]: https://img.shields.io/badge/%F0%9F%92%BB-code-darkblue?style=flat-square
[label-repo]: https://img.shields.io/badge/%F0%9F%93%81-repo-darkblue?style=flat-square

<!-- Build -->
[badge-actions]: https://img.shields.io/github/workflow/status/MicaelJarniac/BuildURL/Python%20package/main?style=flat-square
[actions]: https://github.com/MicaelJarniac/BuildURL/actions
[badge-semantic-release]: https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079?style=flat-square
[semantic-release]: https://github.com/semantic-release/semantic-release
[badge-pypi]: https://img.shields.io/pypi/v/buildurl?style=flat-square
[pypi]: https://pypi.org/project/buildurl
[badge-docs]: https://img.shields.io/readthedocs/buildurl?style=flat-square
[docs]: https://buildurl.readthedocs.io

<!-- Tests -->
[badge-coverage]: https://img.shields.io/codecov/c/gh/MicaelJarniac/BuildURL?logo=codecov&style=flat-square&token=yqKa1DPwPC
[coverage]: https://codecov.io/gh/MicaelJarniac/BuildURL
[badge-pre-commit]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=flat-square&logo=pre-commit&logoColor=white
[pre-commit]: https://github.com/pre-commit/pre-commit

<!-- Standards -->
[badge-semver]: https://img.shields.io/badge/SemVer-2.0.0-blue?style=flat-square&logo=semver
[semver]: https://semver.org/spec/v2.0.0.html
[badge-conventional-commits]: https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow?style=flat-square
[conventional-commits]: https://conventionalcommits.org

<!-- Code -->
[badge-black]: https://img.shields.io/badge/code%20style-black-black?style=flat-square
[Black]: https://github.com/psf/black
[badge-isort]: https://img.shields.io/badge/imports-isort-%231674b1?style=flat-square&labelColor=ef8336
[isort]: https://pycqa.github.io/isort
[badge-mypy]: https://img.shields.io/badge/mypy-checked-2A6DB2?style=flat-square
[mypy]: http://mypy-lang.org

<!-- Repo -->
[badge-issues]: https://img.shields.io/github/issues/MicaelJarniac/BuildURL?style=flat-square
[issues]: https://github.com/MicaelJarniac/BuildURL/issues
[badge-stars]: https://img.shields.io/github/stars/MicaelJarniac/BuildURL?style=flat-square
[stars]: https://github.com/MicaelJarniac/BuildURL/stargazers
[badge-license]: https://img.shields.io/github/license/MicaelJarniac/BuildURL?style=flat-square
[license]: https://github.com/MicaelJarniac/BuildURL/blob/main/LICENSE
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[badge-all-contributors]: https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square
<!-- ALL-CONTRIBUTORS-BADGE:END -->
[contributors]: #Contributors-✨
<!---->

# BuildURL
Simple URL builder

[Read the Docs][docs]

## Installation

### pip
[*buildurl*][pypi] is available on [pip](https://pip.pypa.io/en/stable/):

```bash
pip install buildurl
```

### GitHub
You can also install the latest version of the code directly from GitHub:
```bash
pip install git+git://github.com/MicaelJarniac/BuildURL
```

## Usage
For more examples, see the [full documentation][docs].

```python
from buildurl import BuildURL

# Use the `/` operator to add a string as a path to the end of the URL, like so:
url = BuildURL("https://pypi.org")
url /= "project"
url /= "buildurl"
print(url.get)  # https://pypi.org/project/buildurl

# Or, using a list:
url = BuildURL("https://pypi.org")
url /= ["project", "buildurl"]
print(url.get)  # https://pypi.org/project/buildurl

# Use the `+` operator to add a dict as a query:
url = BuildURL("https://example.com")
url += {"testing": "true"}
url += {"fruit": "apple"}
print(url.get)  # https://example.com?testing=true&fruit=apple

# Those operations can also be done without modifying the original URL:
url = BuildURL("https://python.org")
print(url.get)  # https://python.org
print((url / "doc").get)  # https://python.org/doc
print(url.get)  # https://python.org

# To get the final URL as a string:
url = BuildURL("https://example.com")
url.get
str(url)
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

More details can be found in [CONTRIBUTING](CONTRIBUTING.md).

## Contributors ✨
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/MicaelJarniac"><img src="https://avatars.githubusercontent.com/u/19514231?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Micael Jarniac</b></sub></a><br /><a href="https://github.com/MicaelJarniac/BuildURL/commits?author=MicaelJarniac" title="Code">💻</a> <a href="https://github.com/MicaelJarniac/BuildURL/commits?author=MicaelJarniac" title="Documentation">📖</a> <a href="#example-MicaelJarniac" title="Examples">💡</a> <a href="#ideas-MicaelJarniac" title="Ideas, Planning, & Feedback">🤔</a> <a href="#maintenance-MicaelJarniac" title="Maintenance">🚧</a> <a href="#platform-MicaelJarniac" title="Packaging/porting to new platform">📦</a> <a href="#projectManagement-MicaelJarniac" title="Project Management">📆</a> <a href="https://github.com/MicaelJarniac/BuildURL/commits?author=MicaelJarniac" title="Tests">⚠️</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

## License
[MIT](LICENSE)
