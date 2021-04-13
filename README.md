# Streamlit Sharing Test

Public repo for playing and testing with the **Streamlit sharing** runtime.

As long as the app will be available on Streamlit Sharing, it can be found at this URL:

<https://share.streamlit.io/franky1/streamlit-sharing-test/main>

> WORK IN PROGRESS

## Features

This app is designed to explore the Streamlit Sharing runtime a bit.

- Show Python version of runtime
- Show basic system information
- List all installed apt packages
- List all installed pip packages
- List all installed pip trees
- List all available python modules
- Manually run shell commands in the runtime
- Export runtime informations to file

---

## ToDo

- [x] try tabulate instead of plotly tables
- [x] remove plotly at all
- [ ] add more documentation in README

---

## Printing Pretty Tables with Python

- tabulate <https://github.com/astanin/python-tabulate>
- beautifultable <https://github.com/pri22296/beautifultable>
- prettytable <https://github.com/jazzband/prettytable>

### Tutorials

- <https://www.youtube.com/watch?v=zfZuM3TmYS4>
  - <https://pythonprogramming.altervista.org/create-a-beautiful-html-table-with-python/>

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

> Not cross-platform?
> No actual pip repo package available?
> No success yet to install this package under Debian

- <https://apt-team.pages.debian.net/python-apt/contents.html>
- <https://salsa.debian.org/apt-team/python-apt>

## Checking pip packages

### Checking pip packages manually with pip

```sh
pip freeze
pip list --format columns
pip list --format freeze
pip list --format json
```

### piptree

- <https://github.com/naiquevin/pipdeptree>

### importlib

- <https://docs.python.org/3/library/importlib.html>
- <https://docs.python.org/3/library/importlib.metadata.html>
- <https://importlib-metadata.readthedocs.io/en/latest/>

---

## Plotly Tables in Streamlit

- Plotly in Streamlit <https://docs.streamlit.io/en/0.79.0/api.html#streamlit.plotly_chart>
- Plotly Table <https://plotly.com/python/table/#styled-table>
- Plotly Layout <https://plotly.com/python/reference/layout/>

### Plotly Table example

```python
import plotly.graph_objects as go

fig = go.Figure(data=[go.Table(
    header=dict(values=['A', 'B']),
    cells=dict(values=[[10, 20, 30, 40],
                       [40, 20, 10, 50]]))
    ])
fig.show()
```

---

### Lokal Docker Streamlit runtime

A Dockerfile is also provided for local testing of the Streamlit app.

```sh
docker build -t franky1/streamlit:latest .
docker run -ti -p 8501:8501 --rm franky1/streamlit:latest
docker run -ti -p 8501:8501 -v $(pwd):/app --rm franky1/streamlit:latest  # linux
docker run -ti -p 8501:8501 -v ${pwd}:/app --rm franky1/streamlit:latest  # powershell
docker run -ti -p 8501:8501 -v %cd%:/app --rm franky1/streamlit:latest  # cmd.exe
docker run -ti --rm python:3.7.10-slim /bin/bash # testing python container
```

Open local docker streamlit app site: <http://localhost:8501/>

Port `8501` is the default port for Streamlit.

---

## Status

- WORK IN PROGRESS - not finished yet
- Last changes: 13.04.2021
