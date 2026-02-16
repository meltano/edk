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
uv tool install copier
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

For detailed instructions on developing Meltano EDK extensions, see the [Meltano EDK documentation](https://edk.meltano.com) and review the [Work-In-Progress Specification](https://github.com/meltano/edk/blob/main/README.md).

For working examples of Meltano EDK extensions, see:

- [dbt-ext](https://github.com/meltano/dbt-ext)
- [cron-ext](https://github.com/meltano/cron-ext)

## Basic steps to get started

First generate an initial projecting using the edk template:

```shell
$ copier gh:meltano/edk my-new-extension
No git tags found in template; using HEAD as ref
🎤 The name of your extension i.e. `MyExtensionName`
   MyExtensionThing
🎤 The name of the admin to use for the pyproject.toml entry e.g. `Bob Loblaw`

🎤 The name of your extension in lowercase e.g. `myextensionname`
   myextensionthing
🎤 The ID of the wrapper to use e.g. `myextensionname-ext`
   myextensionthing-ext
🎤 The name of the library to use e.g. `myextensionname_ext`
   myextensionthing_ext
🎤 The prefix to use for the CLI e.g. `myextensionname`
   myextensionthing
🎤 The path/name of the cli command you are wrapping e.g. `dbt`
   uname
🎤 A short description of what this extension does. Will be used for the generated README.md.
   A meltano utility extension for MyExtensionThing that wraps the `uname` command.

Copying from template version 0.0.0.post20.dev0+01ba53c
    create  .
    create  README.md
    create  myextensionthing_ext
    create  myextensionthing_ext/extension.py
    create  myextensionthing_ext/__init__.py
    create  myextensionthing_ext/main.py
    create  myextensionthing_ext/pass_through.py
    create  .copier-answers.yml
    create  pyproject.toml
```

The file structure of the resulting project should look as follows:

```shell
my-new-extension
├── README.md
├── myextensionthing_ext
│   ├── __init__.py
│   ├── extension.py    # <--- Where you do things like setup your env, load configs, create initialization tasks, etc. This is where you'll spend most of your time.
│   ├── main.py         # <--- If needed, this is where you would define custom cli commands that would be invoked with `myextensionthing_extension`
│   └── pass_through.py # <--- The cli entry point for `myextensionthing_invoker` you'll probably not need to modify this.
├── poetry.lock
└── pyproject.toml
```

To start using this extension, `cd` into the created directory, and install the project:

```shell
$ cd my-new-extension
$ my-new-extension poetry install
Updating dependencies
Resolving dependencies... (3.7s)

Writing lock file

Package operations: 9 installs, 1 update, 0 removals

  • Installing click (8.1.3)
  • Installing mccabe (0.6.1)
  • Installing mypy-extensions (0.4.3)
  • Installing pycodestyle (2.7.0)
  • Installing pyflakes (2.3.1)
  • Installing black (22.10.0)
  • Installing flake8 (3.9.2)
  • Installing isort (5.10.1)
  • Updating meltano-edk (0.1.0 4933305 -> 0.1.0 01ba53c)
  • Installing typer (0.6.1)

Installing the current project: myextensionthing-ext (0.0.1)
```

This `pyproject.toml` exposes two commands accessible via `poetry`:

- `myextensionthing_extension`: the extension cli itself, used for when you want interact with the extension directly
- `myextensionthing_invoker`: the wrapper for the `uname` command, used for when you want to invoke the wrapped command

For example to run `uname -a` you could run:

```shell
$ poetry run myextensionthing_invoker -a
Darwin MacBook-Pro.localdomain 21.6.0 Darwin Kernel Version 21.6.0: Mon Aug 22 20:19:52 PDT 2022; root:xnu-8020.140.49~2/RELEASE_ARM64_T6000 arm64
```

But you can also interact with the extension itself:

```shell
$ poetry run myextensionthing_extension --help
Usage: myextensionthing_extension [OPTIONS] COMMAND [ARGS]...

  Simple Meltano extension that wraps the uname CLI.

Options:
  --log-level TEXT                [env var: LOG_LEVEL; default: INFO]
  --log-timestamps / --no-log-timestamps
                                  Show timestamp in logs  [env var:
                                  LOG_TIMESTAMPS; default: no-log-timestamps]
  --log-levels                    Show log levels  [env var: LOG_LEVELS]
  --meltano-log-json              Log in the meltano JSON log format  [env
                                  var: MELTANO_LOG_JSON]
  --install-completion            Install completion for the current shell.
  --show-completion               Show completion for the current shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.

Commands:
  describe    Describe the available commands of this extension.
  initialize  Initialize the MyExtensionThing plugin.
  invoke      Invoke the plugin.

$ poetry run myextensionthing_extension initialize
<outputs nothing, because this extension currently has no initialization tasks>
```

From here you can start adding your own functionality to the extension. For example, if you wanted to run something prior to invoking the wrapped command, you could add a `pre_invoke` method to the `extension.py` file:

```diff
diff --git a/myextensionthing_ext/extension.py b/myextensionthing_ext/extension.py
index 877977b..b9d77c3 100644
--- a/myextensionthing_ext/extension.py
+++ b/myextensionthing_ext/extension.py
@@ -57,3 +57,5 @@ class MyExtensionThing(ExtensionBase):
             ]
         )

+    def pre_invoke(self, invoke_name: str | None, *invoke_args: Any) -> None:
+        log.info("Howdy. I am a pre-invoke task being called by the extension")
```

The line `Howdy. I am a pre-invoke task being called by the extension` will now be printed to the console everytime you run the `myextensionthing_invoker` command:

```shell
$ poetry run myextensionthing_invoker -a
Howdy. I am a pre-invoke task being called by the extension
Darwin MacBook-Pro.localdomain 21.6.0 Darwin Kernel Version 21.6.0: Mon Aug 22 20:19:52 PDT 2022; root:xnu-8020.140.49~2/RELEASE_ARM64_T6000 arm64
```

The extension base class also provides a `post_invoke` method that can be used to run tasks after the wrapped command is invoked, head over to the [EDK reference docs](https://edk.meltano.com/en/latest/classes/meltano.edk.extension.ExtensionBase.html#meltano.edk.extension.ExtensionBase) for more information on what the interface consists of and what else is available out of the box.
