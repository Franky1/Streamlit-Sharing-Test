# standard libraries
import importlib
import logging
import platform
import re
import socket
import subprocess
import sys
import uuid

# external libraries
import psutil
import streamlit as st


@st.cache
def getSystemInfoDict():
    try:
        info = dict()
        info['platform'] = platform.system()
        info['platform-release'] = platform.release()
        info['platform-version'] = platform.version()
        info['architecture'] = platform.machine()
        info['hostname'] = socket.gethostname()
        info['ip-address'] = socket.gethostbyname(socket.gethostname())
        info['mac-address'] = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        info['processor'] = platform.processor()
        info['ram'] = str(
            round(psutil.virtual_memory().total / (1024.0 ** 3)))+" GB"
        return info
    except Exception as e:
        logging.exception(e)
        return e

@st.cache
def split_pip_freeze(output):
    lines = output.splitlines()
    packages = list([x.split("==", 1)[0].strip() for x in lines])
    return packages


@st.cache
def get_subprocess_pip_freeze():
    return subprocess.getstatusoutput(r'pip freeze')


@st.cache
def get_subprocess_apt_list():
    return subprocess.getstatusoutput(r'apt list --installed')


def st_get_python_version():
    st.header("Python Version")
    st.code(sys.version, language='logging')


def st_get_system_version():
    st.header("System Information")
    codeblock = str()
    sysinfos = getSystemInfoDict()
    if isinstance(sysinfos, dict):
        for key, value in sysinfos.items():
            codeblock += f"{key} : {value}\n"
        st.code(codeblock, language='logging')
    else:
        st.error('Acquisition of system infos failed')
        st.code(sysinfos, language='logging')


def st_get_pip_freeze():
    st.header("Pip Packages - pip freeze")
    exitcode, output = get_subprocess_pip_freeze()
    if exitcode:
        st.error('FAILED: pip freeze')
        st.code(output, language='logging')
    else:
        st.code(output, language='logging')
    return exitcode, output


def st_get_apt_packages():
    st.header("Apt Packages")
    exitcode, output = get_subprocess_apt_list()
    if exitcode:
        st.warning('FAILED: apt list --installed')
        st.code(output, language='logging')
    else:
        st.code(output, language='logging')


def st_test_pip_import(output):
    st.header("Test pip package import")
    option = st.selectbox(label='Select pip package:', options=split_pip_freeze(output))
    st.write('You selected:', option)
    try:
        importlib.import_module(option)
    except ImportError as e:
        logging.exception(e)
        st.error(e)


if __name__ == "__main__":
    st.set_page_config(page_title="Streamlit Sharing", page_icon='✅',
                    layout='wide', initial_sidebar_state='collapsed')
    st.title('Streamlit Sharing Test')
    st.text(
        "Purpose is to show all the installed packages in the streamlit sharing runtime.")
    st_get_python_version()
    st_get_system_version()
    st_get_apt_packages()
    exitcode, output = st_get_pip_freeze()
    # if not exitcode:
    #     st_test_pip_import(output)

# TODO: add apt install
# TODO: add pip install
# TODO: add pip import
# TODO: add export of report
