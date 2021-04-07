# Streamlit Sharing Test

Public repo for testing with streamlit sharing runtime.

> WORK IN PROGRESS - NOT FINISHED YET

## ToDo

- [x] add requirements.txt
- [x] write simple streamlit app to test the sharing runtime
- [x] add apt packages listing
- [x] single file app
- [x] use st.cache decorator
- [ ] make the frontend more beautiful
- [ ] change from `pip freeze` to `pip list`
- [ ] use st.table instead of codeblocks
- [x] add try of pip package import (with dropdown)
- [x] show import names instead of pip package names
- [ ] add packages.txt
- [ ] interactively install apt packages - if possible
- [ ] interactively install pip packages - if possible
- [ ] add more documentation in README
- [ ] add direct link to app in README

---

## Checking apt packages

### Manually with OS tools

<https://man7.org/linux/man-pages/man1/dpkg-query.1.html>

```sh
apt list --installed
dpkg --list
dpkg --show --showformat=format
```

### python-apt

> No cross-platform
> No actual pip repo package?

- <https://apt-team.pages.debian.net/python-apt/contents.html>
- <https://salsa.debian.org/apt-team/python-apt>

## Checking pip packages

### Manually with OS tools

```sh
pip freeze
```

### importlib

- <https://docs.python.org/3/library/importlib.html>
- <https://docs.python.org/3/library/importlib.metadata.html>
- <https://importlib-metadata.readthedocs.io/en/latest/>

---

## Status

- WORK IN PROGRESS - not finished yet
- Last changes: 07.04.2021
