# Installation

## Requirements

- Python 3.10+
- Anthropic API key

## Install

```python
pip install pyuds
```

## Set Your API Key

### Environment variable

```python
export ANTHROPIC_API_KEY="sk-ant-..."
```

### .env file (optional)

If you prefer a `.env` file, install `python-dotenv` and load it in your app:

```python
pip install python-dotenv
```

```python
from dotenv import load_dotenv
load_dotenv()
```

## Optional Extras

```python
pip install pyuds[can]
```

```python
pip install pyuds[doip]
```

## Verify Installation

```python
python -c "from pyuds import UDS; print(UDS().ask('Hello'))"
```

## Troubleshooting

!!! warning "Common Issues"
    - `ModuleNotFoundError: No module named 'pyuds'` — confirm you installed into the active environment.
    - `ANTHROPIC_API_KEY not set` — export the environment variable before running.
    - SSL or proxy errors — configure your proxy or verify network access.

!!! note "Apple Silicon"
    If you use a system Python with restricted site-packages, prefer a virtual environment.
