# Building the Package

NetBox package artifacts can be built and verified locally. The hardened fork keeps the documentation sources in the repository for reference, but documentation is not a runtime dependency and is not rendered or bundled as part of the package build.

## Prerequisites

Install the package build tooling:

```no-highlight
python -m pip install --upgrade build packaging twine
```

## Building

Build both the source distribution and wheel from a clean checkout:

```no-highlight
python -m build
```

To build only the wheel:

```no-highlight
python -m build --wheel
```

## Verifying

Check the built artifacts and their metadata:

```no-highlight
twine check dist/*
python scripts/verify_wheel_metadata.py dist/*.whl
python scripts/verify_wheel_contents.py dist/*.whl
python scripts/verify_sdist_contents.py dist/*.tar.gz
python scripts/verify_dependencies.py
```

The wheel and sdist include runtime-critical package data, configuration templates, static assets, translations, and deployment examples. The documentation source tree is intentionally not included in the installed runtime.
