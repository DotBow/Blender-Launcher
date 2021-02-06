# Development

## Requirements

- Linux or Windows x64
- Python 3.8
- Pipenv

## Using Pipenv

All actions should be performed under repository root folder.

### Preparing virtual environment

1. Install pipenv package

```
pip install pipenv --dev
```

2. Install dependencies

```
pipenv install
```

3. Enter the virtual environment

```
pipenv shell
```

### Running Blender Launcher as Python script (i.e. executing main.py)

```
pipenv run start
```

### Building Blender Launcher executable

=== "Windows"

    1. Run batch file

    ```
    .\build_win.bat
    ```

    2. Look for bundled app under _"Blender-Launcher\dist"_ folder

=== "Linux"

    1. Run shell script file

    ```
    . build_linux.sh
    ```

    2. Look for bundled app under _"Blender-Launcher\dist"_ folder
