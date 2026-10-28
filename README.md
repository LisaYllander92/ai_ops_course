# AI-OPS course 

# Setup: NVIDIA + Pydantic AI

## 1. Initiera projektet

```bash
uv init --no-package --python 3.13
```

## 2. Skapa konto och API-nyckel hos NVIDIA

1. Skapa ett konto på NVIDIA (build.nvidia.com).
2. Skapa en API-nyckel. Du kan döpa om nyckeln när du skapar den, vilket är bra om du har flera nycklar.
3. Kopiera nyckeln till en `.env`-fil i projektets rotmapp:

```env
NVIDIA_API=nvapi-xxxxxxxxxxxxxxxx
```

> Lägg till `.env` i `.gitignore` så att nyckeln inte hamnar på GitHub.

## 3. Installera dependencies

```bash
uv add pandas pydantic-ai ipykernel
```


## Terminology

| glossary               | meaning                                                    |
| ---------------------- | ---------------------------------------------------------- |
| pyroject.toml          | metadata about your project                                |
| uv.lock                | info about projects dependencies - similar to requirements |
| .venv                  | virtual environment isolated from rest of system           |
| .python-version        | contains projects default python version                   |
| uv run <command>       | run command in project e.g. uv run python script.py        |
| uv init                | initialize python project - creates pyrpoject.toml         |
| uv add <package>       | add dependency to project and installs them                |
| uv add --dev <package> | add dev dependency                                         |
| uv remove <package>    | remove dependency from project                             |
| uv sync                | syncs the environment with pyproject.toml                  |
| uv python install      | install python version                                     |
| uv python list         | lists available python versions                            |
|                        |                                                            |