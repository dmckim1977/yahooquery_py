# Default Package

## Getting Started

### Update these parameters in `project.__init__.py`

```python
__version__ = "0.1.0"
__description__ = "Project description"
__author__ = "David McKim"
__author_email__ = "davidmckim@gmail.com"
__copyright__ = "Copyright David McKim"
```

### Update these parameters in `pyproject.toml`

```toml
[project]
name = "project_name"
...

dependencies = [
    ...
]

[project.optional-dependencies]
test = [
    "pytest >=2.7.3",
    "pytest-cov",
    ...
]
```


## Components

### SQLAlchemy

To setup:
- Add database environment variables to `.env`

To remove:
- Remove `project.database` directory.  
- Remove imports in `src.project.__init__.py`
- Remove from `requirements.txt`
- Remove from `.env`

### Sentry

To setup:

- Get new DSN from the portal. 
- Add DSN to `.env` variable `SENTRY_DSN`

To remove:
- Remove from `requirements.txt`
- Remove from `project.__init__.py`
- 