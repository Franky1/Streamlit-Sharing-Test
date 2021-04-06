# standard libraries
import importlib
import logging
import platform
import socket
import subprocess
import sys

# external libraries
import importlib_metadata
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
        info['processor'] = platform.processor()
        info['ram'] = str(
            round(psutil.virtual_memory().total / (1024.0 ** 3)))+" GB"
        return info
    except Exception as e:
        logging.exception(e)
        return e


# def split_pip_freeze(output):
#     lines = output.splitlines()
#     packages = list([x.split("==", 1)[0].strip() for x in lines])
#     return packages


@st.cache
def get_subprocess_pip_freeze():
    return subprocess.getstatusoutput(r'pip freeze')


@st.cache
def get_subprocess_apt_list():
    # return subprocess.getstatusoutput(r'apt list --installed')
    # return subprocess.getstatusoutput(r'dpkg -l')
    return subprocess.getstatusoutput(r"dpkg-query --show --showformat='${binary:Package}\t${Version}\t${Description}\n'")


@st.cache
def get_packages_distributions():
    packages = importlib_metadata.packages_distributions()
    packages = list(x for x in packages)
    packages = list(filter(lambda x: not x[:1].isdigit(), packages))
    packages = list(filter(lambda x: not x.startswith('_'), packages))
    packages = list(filter(lambda x: not any(e in x for e in r'\/'), packages))
    packages = sorted(packages)
    return packages


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


def st_get_apt_packages():
    st.header("Apt Packages")
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


def st_get_packages_distributions():
    st.header("Pip Packages - packages_distributions")
    packages = get_packages_distributions()
    output = '\n'.join(packages)
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
    packages = st_get_packages_distributions()
    st_test_pip_import(packages)

# TODO: add apt install
# TODO: add pip install
# TODO: add export of report
