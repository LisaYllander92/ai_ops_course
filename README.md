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

# Web scraping with Firecrawl

## Setup

### 1. Create an account and get an API key

Sign up at [firecrawl.dev](https://www.firecrawl.dev), copy your API key and add it to your `.env` file:

```env
FIRECRAWL_API_KEY=your_key_here
```

> **Note:** Never commit `.env` to Git. Make sure it is listed in `.gitignore`.

## Try it out

### 2. Search the web

1. Open the **Search** playground in the Firecrawl dashboard.
2. Run a query and click **Get code**.
3. Copy the generated code into your project.
4. Replace the hardcoded API key with the one from `.env`:

```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("FIRECRAWL_API_KEY")
```

### 3. Scrape a web page

1. Open the **Scrape** playground.
2. Paste the URL of the page you want to scrape.
3. Run it and click **Get code**.
4. Copy the code and use the same `.env` approach for the API key.

## Before you scrape

Check that you are allowed to scrape the site by looking at its `robots.txt`:

```
https://example.com/robots.txt
```

Look for `Disallow` rules that cover the pages you want to scrape, and also check the site's terms of service.