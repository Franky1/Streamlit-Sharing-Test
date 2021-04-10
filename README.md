# Streamlit Sharing Test

Public repo for playing and testing with streamlit sharing runtime.

> WORK IN PROGRESS - NOT FINISHED YET

As long as the app will be available on Streamlit Sharing, it can be found at this URL:

<https://share.streamlit.io/franky1/streamlit-sharing-test/main>

## Features

This app is designed to explore the Streamlit Sharing runtime a bit.

- Show Python version of runtime
- Show basic system information
- List all installed apt packages
- List all installed pip packages
- List all importable python modules
- Manually run shell commands in the runtime

---

## ToDo

- [ ] make the frontend more beautiful
- [ ] try tabulate
- [x] add try of pip package import (with dropdown)
- [x] show import names instead of pip package names
- [ ] interactively install apt packages - if possible
- [ ] interactively install pip packages - if possible
- [ ] add more documentation in README
- [ ] try `st.experimental_rerun()`

---

## Checking apt packages

### Checking apt packages manually with OS tools

```sh
apt list --installed
dpkg --list
dpkg-query --show --showformat=format
```

#### dpkg-query

<https://man7.org/linux/man-pages/man1/dpkg-query.1.html>

### python-apt

> No cross-platform
> No actual pip repo package?

- <https://apt-team.pages.debian.net/python-apt/contents.html>
- <https://salsa.debian.org/apt-team/python-apt>

## Checking pip packages

### Checking pip packages manually with OS tools

```sh
pip freeze
pip list --format=columns
```

### piptree

- <https://github.com/naiquevin/pipdeptree>

### importlib

- <https://docs.python.org/3/library/importlib.html>
- <https://docs.python.org/3/library/importlib.metadata.html>
- <https://importlib-metadata.readthedocs.io/en/latest/>

---

## Status

- WORK IN PROGRESS - not finished yet
- Last changes: 10.04.2021
