# ----------------------------------------------------------------------------
# Some code snippets not used in the app itself
# ----------------------------------------------------------------------------
import collections
import pkg_resources  # part of setuptools
import streamlit as st

def st_get_pip_packages():
    st.header("Pip Packages")
    codeblock = str()
    piplist = dict()
    for p in pkg_resources.working_set:
        piplist[p.project_name] = p.version
    piplistordered = collections.OrderedDict(sorted(piplist.items()))
    for key, value in piplistordered.items():
        codeblock += f"{key} : {value}\n"
    st.code(codeblock, language='logging')

# ----------------------------------------------------------------------------

