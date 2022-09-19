## Dev environment

### Virtual environment pipenv

Define virtual environment 

**(YOU MUST BE IN src directory)**

```
python3 -m venv env
```

Use the environment

```
source env/bin/activate
```

quit environment

```
deactivate
```

### Set environnement into vs code 

```
mkdir .vscode && touch .vscode/settings.json
```

```
{
    "python.defaultInterpreterPath": "env/bin/python",    
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "editor.rulers": [
        79
    ]
}
```
### Save dependencies to requirements
```
pip install package && pip freeze > requirements.txt
```

### Install dependencies

```
pip install -r requirements.txt
```

