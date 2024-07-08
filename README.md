# Meltano extension developer kit

[![Documentation Status](https://readthedocs.org/projects/meltano-edk/badge/?version=latest)](https://edk.meltano.com/en/latest/?badge=latest) |
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/meltano/edk/main.svg)](https://results.pre-commit.ci/latest/github/meltano/edk/main)

The Meltano extension developer kit is the fastest way to build custom Meltano extensions. If you're looking to build a custom extractor, loader, or tap then the [*SDK*](https://github.com/meltano/singer-sdk) is actually what you're looking for.

## Creating a new extension using the EDK

This repo ships with a [copier](https://copier.readthedocs.io/en/stable/) based template to help developers get and new extension using the [Meltano EDK](https://edk.meltano.com) up and running quickly.

### Prerequisites for using the template

Install copier:

```bash
pipx install copier
```

### Use copier to initialize a new extension

Start a new EDK project using the supplied template (directly from Github):

```bash
copier copy gh:meltano/edk my-new-extension
```

Install the project dependencies:

```bash
cd my-new-extension
poetry install
```

## Developing extensions using the EDK

For detailed instructions on developing Meltano EDK extensions, see the [Meltano EDK documentation](https://edk.meltano.com) and review the [Work-In-Progress Specification](https://meltano-edk--28.org.readthedocs.build/en/28/specification.html).

For working examples of Meltano EDK extensions, see:

- [dbt-ext](https://github.com/meltano/dbt-ext)
- [cron-ext](https://github.com/meltano/cron-ext)
