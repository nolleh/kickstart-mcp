# kickstart-mcp

[![PyPI - Version](https://img.shields.io/pypi/v/kickstart-mcp.svg)](https://pypi.org/project/kickstart-mcp)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/kickstart-mcp.svg)](https://pypi.org/project/kickstart-mcp)

-----

## Table of Contents

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install kickstart-mcp
```

## License

`kickstart-mcp` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.


---

1. hatch new project
2. in project.toml, add [project.scripts]

```toml
[project.scripts]
weather = weather:main
```

3. add depfor mcp
```toml
dependencies = [
    "mcp"
]
modify requirepython
```
