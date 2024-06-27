# Tetris RL

## Installation

Setup `conda` environment:

```shell
conda env create -f environment.yml
```

Install `poetry`: [poetry installation instructions](https://python-poetry.org/docs/#installation)

Install dependencies:

```shell
poetry install
```

## Development

### Linting and Formatting

### Ruff

The project uses [Ruff](https://docs.astral.sh/ruff/) as the linter and formatter, replacing Black, Pylint, etc.

Configuration options for Ruff can be found in `ruff.toml` and configuration documentation can be found on their main website.

**_Note_**: Ruff is not a language server and you should still have one installed in your editor of choice.

---

If you are using VSCode, then I recommend the following settings in your `settings.json` file at a minimum:

```json
"python.languageServer": "Pylance",
"[python]": {
"editor.defaultFormatter": "charliermarsh.ruff",
"editor.formatOnSave": true,
"editor.codeActionsOnSave": {
        "source.organizeImports": "explicit"
    }
}
```

#### Docstrings

The recommended docstring format is numpy, examples can be found here:

https://numpydoc.readthedocs.io/en/latest/example.html

If you are using VSCode, then I recommend using autoDocstring

---

https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring

To setup the extension for numpy go to the extension settings and change the format to numpy.
