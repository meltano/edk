## Extension types

### Plain extensions

Plain extensions are extensions that do work directly, they may call other applications (including meltano) but serve a specific purprose (e.g. managing local cronjobs) rather than wrapping another application.

Plain extensions should supply a single cli that is the entrypoint for the extension. This cli should be named `extensionname_extension` (e.g. `cron_extension`).

### Wrapper extensions

Wrapper extensions are extensions that wrap other applications to make them more accessible to a meltano user. They may also provide additional functionality on top of the application or provide a more user friendly interface.

For example the dbt extension wraps the dbt cli and provides additional functionality to manage dbt projects and simplifies the process of running dbt with meltano.

Wrapper extension should supply two cli commands, one for interacting with the extension itself, and one for interacting with the wrapped application. The extension cli should be named `extensionname_extension` (e.g. `superset_extension`) and the wrapped application cli should be named `extensionname_invoker` (e.g. `superset_invoker`).

## Initial required commands and syntax

## `_extension` commands:

```shell
extension_extension invoke <specific-command> # for wrapper extensions
extension_extension invoke <:splat>           # for wrapper extensions
extension_extension describe --format=[default=json, yaml?]
extension_extension initialize
extension_extension --help
```

### `invoke`

Analogous to a `meltano invoke <command> [flags...]`, the `extension invoke <command>` call is expected to behave similarly and invoke the requested command. i.e.

```shell
extension invoke sync-ui # may sync with some dashboard ui
extension invoke deploy # may perform some other action
```



### `describe`

> **Note** - Evolving status. "best practice" recommendation, not *yet* a requirement

The describe command allows for auto discovery/configuration and generally describes the execution requirements of the extension itself (not necissarily the wrapper). In v1 the payload is limited. Consisting only of `commands` which describes what the commands the extension command itself (e.g. `_ext`), supports and whether the command is a wrapper command or not.

Expected `describe` output, jsonspec pending:

```shell
$ poetry run superset_extension describe
Describe(
    commands=[
        ExtensionCommand(
            name='superset_extension',
            description='extension commands',
            commands=[
                'describe',
                'invoke',
                'pre_invoke',
                'post_invoke',
                'initialize',
                'create_admin',
            ],
            pass_through_cli=False,
        ),
        InvokerCommand(
            name='superset_invoker',
            description='pass through invoker',
            commands=[':splat'],
            pass_through_cli=True,
        ),
    ],
)
```

### `initialize` / `init`

> **Note** - Evolving "best practice" recommendation, not *yet* a requirement

The `init` command is a convenience command that allows for a user to initialize an extension. Performing one time setup tasks. i.e. creating a config file, or configuring scaffolding.

### Special/reserved command keywords

> **Warning** - Evolving status

While a service pattern is not yet supported, future additional top-level commands are likely, and so extension developers not using the SDK may want to keep that in mind. i.e.

```shell
# possible future patterns
extension service ui start
extension service scheduler start
extension service all stop
```

Some future commands may trigger special handling behavior upstream within Meltano. Currently, limited to:

- `test*` (test, test_a_thing, test-other-thing, testAllThings) which maybe triggered during `meltano test`.

If a extension exposes multiple matching commands, they're invoked in the order they're encountered.

### exit codes

- `0` in all success cases
- All non 0 indicate unsuccessful invocation and in most cases will halt the execution chain

## `_invoker` commands:

`_invoker` commands should accept the same arguments, in the same format, as the wrapped application. This includes bare invocations and help commands. The `_invoker` should effectively transparently pass all arguments to the wrapped application.

### exit codes

For `_invoker` commands, the exit code should typically be the same as the exit code of the wrapped application. In cases the where the `_invoker` itself is responsible for the exit code standard unix exit codes should be used.

- `0` in all success cases
- All non 0 indicate unsuccessful invocation and in most cases will halt the execution chain

## Stdio behavior (Errors, Logging, and Output)

### IO

- stdin is currently unused but reserved.  It's unused at this time, but maybe used for message passing in the future.
- stdout is currently unused but reserved. It's unused at this time, but might be used for message passing in the future. extensions should avoid needlessly writing to stdout.
- stderr is available for structured extension output intended for end users and operators.

### Errors & Output

Extensions should emit plain (uncolored) structured log's to stderr. In the first version of this spec the structure isn't yet set, but developers are advised to follow the KISS principle and use a basic format. In the future, extensions may be required to support an optional JSON output format.

The following 3 fields should be present, with limited other ad hoc key/value pairs to supply context where needed:

- ISO formatted timestamp (off by default)
- log level (off by default)
- event (which should encapsulate any forwarded log lines from underlying calls the extension has made. e.g. airflow output)
- limited KV pairs for additional context as deemed useful

A small note on log level usage:

`Debug` and `Info` are generally the two most used and abused levels, but in the future, meltano will likely optimize around `Warn` and `Error` for passing on messaging to end users. With that in mind, it's important to call errors out explicitly via messages at the `Error` level on stderr. You should assume that an end user will be the primary consumer of a such a message - and so you should co-locate important context in the same log line or concisely explain what went wrong in the message if possible.

"Good" example:

```shell
$ extension invoke scheduler
2022-07-26 17:30.32 [INFO] message="Starting scheduler" important=context key=variable
<lots of airflow logs>
2022-07-26 17:30.32 [ERROR] message="Failed to start airflow: couldn't create db" error="/some/path doesn't exist" important=context
```

"bad" example:

```shell
$ extension invoke scheduler
2022-07-26 17:30.32 [INFO] message="Starting airflow"
<lots of airflow logs>
<bare exceptions/trace backs>
2022-07-26 17:30.32 [ERROR] message=Failed to start airflow
```

In the future, the spec will likely evolve to report errors in an explicitly structured form.

### Logging controls

> **Note** - Evolving "best practice" recommendation, not *yet* a requirement

The following enviornment variables or cli flags should be supported by extensions to control logging behavior:

- `LOG_LEVEL` - set the log level for the extension. Defaults to `INFO` if not set.
- `LOG_TIMESTAMPS` - set to strig `true` to enable logging of timestamp field. Defaults to `false` if not set.
- `LOG_LEVELS` - set to string `true` to enable logging of log level field. Defaults to `false` if not set.
- `MELTANO_LOG_JSON` - set to string `true` to enable JSON logging. Defaults to `false` if not set.
