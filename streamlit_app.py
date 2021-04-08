# standard libraries
import importlib
# import json
import logging
import platform
import socket
import subprocess
import sys

# external libraries
import importlib_metadata
# import pandas as pd
import psutil
import streamlit as st
# import streamlit.components.v1 as components
# from tabulate import tabulate


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
        info['processor'] = platform.processor()
        info['ram'] = str(
            round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB"
        return info
    except Exception as e:
        logging.exception(e)
        return e


def split_pip_freeze(output):
    lines = output.splitlines()
    packages = dict()
    for line in lines:
        if "==" in line:
            pkg, vers = line.split("==", 1)
        elif "@" in line:
            pkg, vers = line.split("@", 1)
        else:
            continue
        pkg = pkg.strip()
        vers = vers.strip()
        packages[pkg] = vers
    return packages


def run_subprocess(command):
    return subprocess.getstatusoutput(command)


@st.cache
def get_subprocess_pip_freeze():
    return subprocess.getstatusoutput(r'pip freeze')


@st.cache
def get_subprocess_pip_list():
    return subprocess.getstatusoutput(r'pip list --format=columns')


@st.cache
def get_subprocess_apt_list():
    # return subprocess.getstatusoutput(r'apt list --installed')
    # return subprocess.getstatusoutput(r'dpkg -l')
    return subprocess.getstatusoutput(r"dpkg-query --show --showformat='${Package;-26} ${Version;-24} \t${binary:Synopsis}\n'")


@st.cache
def get_packages_distributions():
    packages = importlib_metadata.packages_distributions()
    packages = list(x for x in packages)
    packages = list(filter(lambda x: not x[:1].isdigit(), packages))
    packages = list(filter(lambda x: not x.startswith('_'), packages))
    packages = list(filter(lambda x: not any(e in x for e in r'\/'), packages))
    packages = sorted(packages, key=lambda x: x.lower())
    return packages


def st_get_python_version():
    st.header("Python Version")
    st.markdown(
        "Show the currently used Python version in the runtime")
    st.code(sys.version.replace('\n', ' '), language='logging')
    # st.markdown(sys.version.replace('\n', ' '))


def st_get_system_version():
    st.header("System Information")
    st.markdown(
        "Show some basic system informations about the runtime")
    codeblock = str()
    sysinfos = getSystemInfoDict()
    if isinstance(sysinfos, dict):
        for key, value in sysinfos.items():
            codeblock += f"{key: <17}: {value}\n"
        st.code(codeblock, language='logging')
    else:
        st.error('Acquisition of system infos failed')
        st.code(sysinfos, language='logging')


def st_get_apt_packages():
    st.header("Apt Packages")
    st.markdown(
        "List all installed `apt` packages of the runtime - acquired with `dpkg-query`")
    exitcode, output = get_subprocess_apt_list()
    if exitcode:
        st.warning('FAILED: dpkg-query --show --showformat')
        # st.warning('FAILED: apt list --installed')
        st.code(output, language='logging')
    else:
        st.code(output, language='logging')


def st_get_pip_freeze():
    st.header("Pip Packages - pip freeze")
    exitcode, output = get_subprocess_pip_freeze()
    if exitcode:
        st.error('FAILED: pip freeze')
        st.code(output, language='logging')
    else:
        st.code(output, language='logging')
    return exitcode, output


def st_get_pip_list():
    st.header("Pip Packages")
    st.markdown(
        "List all installed `pip` packages of the runtime - acquired with `pip list`")
    exitcode, output = get_subprocess_pip_list()
    if exitcode:
        st.error('FAILED: pip list')
        st.code(output, language='logging')
    else:
        st.code(output, language='logging')
        # pip_list = json.loads(output)
        # pip_list = list(dict({item['name'] : item['version']}) for item in pip_list)
        # pip_list = tabulate(pip_list, headers=['Package', 'Version'], tablefmt="grid")
        # pip_list = tabulate(pip_list, tablefmt="html")
        # components.html(pip_list)
        # st.json(pip_list)
        # st.table(pd.DataFrame.from_dict(pip_list, orient='index', dtype='str', columns=['Version']))
    return exitcode, output


def st_get_packages_distributions():
    st.header("Pip Modules")
    st.markdown(
        "List all importable python modules of the runtime - acquired with `importlib_metadata.packages_distributions`")
    packages = get_packages_distributions()
    output = '\n'.join(packages)
    # st.markdown(output)
    st.code(output, language='logging')
    return packages


def st_test_pip_import(packages):
    st.header("Test pip package import")
    option = st.selectbox(label='Select pip module:', options=packages)
    st.write('You selected module:', option)
    if st.button('Import selected pip module'):
        try:
            importlib.import_module(option)
        except ImportError as e:
            logging.exception(e)
            st.error(e)
        else:
            st.info(f'sucessfully imported {option}')


def st_run_shell_commands():
    st.header("Run shell command")
    st.markdown(
        "Here you can run any shell command in the runtime. Enter the command and press enter to start execution.")
    command = st.text_input(label="Input of shell command - Press Enter to run command")
    # if st.button('Run command'):
    if command:
        exitcode, output = run_subprocess(command)
        if exitcode:
            st.error(f'FAILED: {command}')
            st.code(output, language='logging')
        else:
            st.info(f'Success: {command}')
            st.code(output, language='logging')


if __name__ == "__main__":
    st.set_page_config(page_title="Streamlit Sharing", page_icon='✅',
                    layout='wide', initial_sidebar_state='collapsed')
    st.title('Streamlit Sharing Test')
    st.markdown(
        "This app is designed to explore the Streamlit Sharing runtime a bit.")
    st_get_python_version()
    st_get_system_version()
    st_get_apt_packages()
    # exitcode, output = st_get_pip_freeze()
    exitcode, output = st_get_pip_list()
    packages = st_get_packages_distributions()
    st_run_shell_commands()
    st_test_pip_import(packages)

# TODO: add pip install element
# TODO: add export of report
