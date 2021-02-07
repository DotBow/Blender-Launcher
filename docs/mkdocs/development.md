# Development

## Requirements

- Linux or Windows x64
- Python 3.8
- Pipenv

## Using Pipenv

!!! info

    All actions should be performed under repository root folder (i.e. ``/Blender-Launcher``)

### Preparing virtual environment

1. Install pipenv package

    ```
    pip install pipenv
    ```

1. Install dependencies

    ```
    pipenv install --dev
    ```

1. Enter the virtual environment

    ```
    pipenv shell
    ```

### Running Blender Launcher as Python script (i.e. executing ``main.py``)

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

    1. Look for bundled app under ``Blender-Launcher\dist`` folder

=== "Linux"

    1. Run shell script file

        ```
        . build_linux.sh
        ```

    1. Look for bundled app under ``Blender-Launcher\dist`` folder
