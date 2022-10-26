# Getting Started with the EDK

The Meltano Extension Developer Kit (EDK) is the fastest way to build custom Meltano extensions. Extensions allow you to integrate any existing data tool into your existing Meltano projects - or build your own.

## What can I build with the EDK?

For examples of types of tools you can build or wrap with the EDK, see the list of [EDK Preview Utilities](https://hub.meltano.com/utilities/) on Meltano Hub.

If you're looking to build a custom data extractor or loader (aka "taps" and "targets"), then the [*Meltano Singer SDK*](https://github.com/meltano/singer-sdk) is actually what you're looking for.

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
copier gh:meltano/edk-template my-new-extension
```

Install the project dependencies:

```bash
cd my-new-extension
poetry install
```

## Developing extensions using the EDK

For detailed instructions on developing Meltano EDK extensions, see the [Meltano EDK documentation](https://edk.meltano.com) and review the [Work-In-Progress Specification](https://github.com/meltano/edk/blob/main/README.md).

For working examples of Meltano EDK extensions, see:

- [dbt-ext](https://github.com/meltano/dbt-ext)
- [cron-ext](https://github.com/meltano/cron-ext)
