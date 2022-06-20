<style>body {text-align: justify}</style>

# Development

## Requirements

- Linux or Windows x64
- Python 3.9
- Pipenv

!!! warning

    To use different Python version change requirements inside `Pipfile` and use following command to apply changes:

    ```
    pipenv lock
    ```

## Using Pipenv

!!! info "Note"

    All actions should be performed under repository root folder i.e. `/Blender-Launcher`!

### Preparing virtual environment

1. Install pipenv package

    ```
    pip install pipenv
    ```

1. Install dependencies

    === "Minimum set of packages for building executable"

        ```
        pipenv install
        ```

    === "All set of packages including development tools"

        ```
        pipenv install --dev
        ```

1. Enter the virtual environment

    ```
    pipenv shell
    ```

### Running Blender Launcher as Python script (i.e. executing `main.py`)

```
pipenv run start
```

### Building Blender Launcher executable

!!! warning

    Executable for target platform must be built under this exclusive platform!

=== "Windows"

    1. Run batch file

        ```
        .\build_win.bat
        ```

    1. Look for bundled app under `Blender-Launcher\dist\release` folder

=== "Linux"

    1. Run shell script file

        ```
        . build_linux.sh
        ```

    1. Look for bundled app under `Blender-Launcher\dist\release` folder
