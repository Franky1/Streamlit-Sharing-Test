# Streamlit Sharing Test

Public repo for testing with streamlit sharing runtime.

> WORK IN PROGRESS - NOT FINISHED YET

## ToDo

- [x] add requirements.txt
- [x] write simple streamlit app to test the sharing runtime
- [x] add apt packages listing
- [x] single file app
- [x] use st.cache decorator
- [ ] beautify the app
- [ ] download report as txt file with jinja2(?)
- [ ] add try of pip package import (with dropdown?)
- [ ] show import names instead of pip package names
- [ ] add packages.txt
- [ ] interactively install apt packages(?)
- [ ] interactively install pip packages(?)

---

## Checking apt packages

### python-apt

> Not cross-platform, no actual pip repo package?

- <https://apt-team.pages.debian.net/python-apt/contents.html>
- <https://salsa.debian.org/apt-team/python-apt>

### Manually with OS tools

```sh
apt list --installed
```

## Checking pip packages

- <https://docs.python.org/3/library/importlib.html>
- <https://docs.python.org/3/library/importlib.metadata.html>
- <https://importlib-metadata.readthedocs.io/en/latest/>

---

## Status

- WORK IN PROGRESS - not finished yet
- Last changes: 06.04.2021
