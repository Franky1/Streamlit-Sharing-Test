# standard libraries
import base64
import importlib
import json
import logging
import platform
import shutil
import socket
import subprocess
import sys
from typing import Dict, List, Tuple, Union

# external libraries
import importlib_metadata
import psutil
import streamlit as st
# import streamlit.components.v1 as components
from tabulate import tabulate

# Type Hint Definitions:
TypeDictStr = Dict[str, str]
TypeListStr = List[str]
TypeListListStr = List[List[str]]
TypeTupleOut = Tuple[int, str]

# Output Text collector:
output_text: TypeDictStr = dict()


@st.cache
def getSystemInfoDict() -> Union[TypeDictStr, Exception]:
    try:
        info = dict()
        info['platform.system'] = platform.system()
        info['platform.release'] = platform.release()
        info['platform.version'] = platform.version()
        info['platform.machine'] = platform.machine()
        info['socket.gethostname'] = socket.gethostname()
        info['ip-address'] = socket.gethostbyname(socket.gethostname())
        info['platform.processor'] = platform.processor()
        info['ram'] = str(
            round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB"
        return info
    except Exception as e:
        logging.exception(e)
        return e


def split_pip_freeze(output: str) -> TypeDictStr:
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


def run_subprocess(command: str) -> TypeTupleOut:
    return subprocess.getstatusoutput(command)


@st.cache
def get_subprocess_pip_freeze() -> TypeTupleOut:
    return subprocess.getstatusoutput(r'pip freeze')


@st.cache
def get_subprocess_pip_list() -> TypeTupleOut:
    return subprocess.getstatusoutput(r'pip list --format json')


@st.cache
def get_subprocess_pipdeptree(fullpath=None) -> TypeTupleOut:
    if fullpath:
        return subprocess.getstatusoutput(rf'{fullpath} --json')
    else:
        return subprocess.getstatusoutput(r'pipdeptree --json')


@st.cache
def get_subprocess_apt_list() -> TypeTupleOut:
    return subprocess.getstatusoutput(r"dpkg-query --show --showformat='${Package} ${Version} ${binary:Synopsis}\n'")


@st.cache
def get_subprocess_apt_sources() -> TypeTupleOut:
    return subprocess.getstatusoutput(r'cat /etc/apt/sources.list')


@st.cache
def get_packages_distributions() -> TypeListStr:
    metadata = importlib_metadata.packages_distributions()
    packages = list(x for x in metadata)
    packages = list(filter(lambda x: not x[:1].isdigit(), packages))
    packages = list(filter(lambda x: not x.startswith('_'), packages))
    packages = list(filter(lambda x: not any(e in x for e in r'\/'), packages))
    packages = sorted(packages, key=lambda x: x.lower())
    return packages


def st_get_python_version() -> str:
    st.markdown("---")
    st.header("🐍 Python Version")
    st.markdown(
        "Show the currently used Python version in the runtime - acquired with **`sys.version`**")
    output = sys.version.replace('\n', '')
    st.code(output, language='logging')
    return output


def tabulate_table_factory(headers: TypeListStr, cells: TypeListListStr, showindex: bool=False, tablefmt="github") -> str:
    tabular_data = [*zip(*cells)]  # Transpose the 2D array of cells
    tab = tabulate(tabular_data=tabular_data, headers=headers, showindex=showindex, tablefmt=tablefmt)
    return tab


def st_get_system_version() -> str:
    st.markdown("---")
    st.header("ℹ️ System Information")
    st.markdown(
        "Show some basic system informations about the runtime")
    stringblock = str()
    sysinfos = getSystemInfoDict()
    if isinstance(sysinfos, dict):
        headers = ['Parameter', 'Value']
        cells = [list(sysinfos.keys()), list(sysinfos.values())]
        st.markdown(tabulate_table_factory(headers, cells, showindex=False))
        stringblock = tabulate_table_factory(headers, cells, showindex=False, tablefmt="fancy_grid")
    else:
        st.error('Acquisition of system infos failed')
        st.code(sysinfos, language='logging')
    return stringblock


def get_apt_package_list(output: str) -> List:
    out = list()
    lines = output.splitlines()
    for line in lines:
        a, b, c = line.split(maxsplit=2)
        out.append([a, b, c])
    ret = [*zip(*out)]  # Transpose the 2D array of cells
    return ret


def st_get_apt_packages() -> str:
    st.markdown("---")
    st.header("🐧 Apt Packages")
    st.markdown(
        "List all installed **`apt`** packages of the runtime - acquired with **`dpkg-query --show --showformat`**")
    exitcode, output = get_subprocess_apt_list()
    stringblock = str()
    if exitcode:
        st.warning('FAILED: dpkg-query --show --showformat')
        st.code(output, language='logging')
    else:
        headers = ['Package', 'Version', 'Description']
        cells = get_apt_package_list(output)
        st.markdown(tabulate_table_factory(headers, cells, showindex=True))
        stringblock = tabulate_table_factory(headers, cells, showindex=True, tablefmt="fancy_grid")
    return stringblock


def st_get_apt_sources() -> str:
    st.markdown("---")
    st.header("🔗 Apt Sources")
    st.markdown(
        "List all installed **`apt`** sources of the runtime - acquired with **`cat /etc/apt/sources.list`**")
    exitcode, output = get_subprocess_apt_sources()
    if exitcode:
        st.warning('FAILED: cat /etc/apt/sources.list')
        st.code(output, language='logging')
    else:
        st.code(output, language='logging')
    return output


def st_get_pip_freeze() -> str:
    st.markdown("---")
    st.header("🐍 Pip Packages - pip freeze")
    exitcode, output = get_subprocess_pip_freeze()
    if exitcode:
        st.error('FAILED: pip freeze')
        st.code(output, language='logging')
    else:
        st.code(output, language='logging')
    return output


def get_dict_from_piplist(jsonified: Dict) -> TypeDictStr:
    packages = dict()
    for elem in jsonified:
        pkg = elem.get('name')
        ver = elem.get('version')
        packages[pkg] = ver
    return dict(sorted(packages.items()))


def st_get_pip_list() -> str:
    st.markdown("---")
    st.header("🐍 Pip Packages")
    st.markdown(
        "List all installed **`pip`** packages of the runtime - acquired with **`pip list`**")
    exitcode, output = get_subprocess_pip_list()
    stringblock = str()
    if exitcode:
        st.error('FAILED: pip list')
        st.code(output, language='logging')
    else:
        jsonified = json.loads(output)
        jsonified = get_dict_from_piplist(jsonified)
        if isinstance(jsonified, dict):
            headers = ["Package", "Version"]
            cells = [list(jsonified.keys()), list(jsonified.values())]
            st.info(f'Number of Python packages: {len(jsonified)}')
            st.markdown(tabulate_table_factory(headers, cells, showindex=True))
            stringblock = tabulate_table_factory(headers, cells, showindex=True, tablefmt="fancy_grid")
    return stringblock


def get_dependencies(jsonified: Dict) -> str:
    dependencies = str()
    if jsonified:
        for pkg in jsonified:
            pkg_str = f"{pkg['key']} : {pkg['package_name']} : {pkg['installed_version']} : {pkg['required_version']}"
            dependencies += f"{pkg_str}\n"
    return dependencies.strip()


def get_dict_from_pipdeptree(jsonified: Dict) -> TypeDictStr:
    packages = dict()
    for elem in jsonified:
        pkg = elem.get('package')
        pkg_str = f"{pkg['key']} : {pkg['package_name']} : {pkg['installed_version']}"
        dep = get_dependencies(elem.get('dependencies'))
        packages[pkg_str] = dep
    return dict(sorted(packages.items()))


def st_get_pipdeptree() -> str:
    st.markdown("---")
    st.header("🐍 Pipdeptree Output")
    st.markdown(
        "List all installed python packages of the runtime - acquired with **`pipdeptree`**")
    # which = shutil.which("pipdeptree")  # workaround on streamlit sharing
    which = "pipdeptree"
    exitcode, output = get_subprocess_pipdeptree(which)
    stringblock = str()
    if exitcode:
        st.error(rf'FAILED: {which} --json')
        st.code(output, language='logging')
    else:
        jsonified = json.loads(output)
        jsonified = get_dict_from_pipdeptree(jsonified)
        if isinstance(jsonified, dict):
            headers = ["Package (key : package_name : installed_version)", "Dependencies (key : package_name : installed_version : required_version)"]
            cells = [list(jsonified.keys()), list(jsonified.values())]
            table = tabulate_table_factory(headers, cells, showindex=True, tablefmt="pipe")
            st.info(f'Number of Python packages: {len(jsonified)}')
            st.markdown(table)
            stringblock = tabulate_table_factory(headers, cells, showindex=True, tablefmt="fancy_grid")
    return stringblock


def chunkify(lst: List, n: int) -> TypeListListStr:
    return [lst[i::n] for i in range(n)]


def fill_chunks_equally_with_empty_values(cells: List) -> List:
    output = list()
    maxlength = max(list(len(col) for col in cells))
    for col in cells:
        length = len(col)
        if length < maxlength:
            for _ in range(maxlength - length):
                col.append('')
        output.append(col)
    return output


def st_get_packages_distributions() -> str:
    st.markdown("---")
    st.header("🐍 Pip Modules")
    st.markdown(
        "List all importable python modules of the runtime - acquired with **`importlib_metadata.packages_distributions`**")
    packages = get_packages_distributions()
    stringblock = str()
    if isinstance(packages, list):
        chunks = 6
        cells = chunkify(packages, chunks)
        cells = fill_chunks_equally_with_empty_values(cells)
        headers = list(str(x) for x in range(chunks))
        table = tabulate_table_factory(headers=headers, cells=cells, showindex=True, tablefmt="pipe")
        st.info(f'Number of Python modules: {len(packages)}')
        st.markdown(table)
        stringblock = tabulate_table_factory(headers=headers, cells=cells, showindex=True, tablefmt="fancy_grid")
    return stringblock


def st_test_pip_import(packages: TypeListStr) -> None:
    st.markdown("---")
    st.header("🐍 Test pip package import")
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


def generate_output_text(text_dict: TypeDictStr) -> str:
    output = str()
    for key, value in text_dict.items():
        output += "==========================================================================================\n"
        output += f'{key.capitalize()}\n'
        output += "==========================================================================================\n"
        output += '\n'
        output += f'{value}\n'
        output += '\n\n'
    return output


def download_link(object_to_download: str, download_filename: str, download_link_text: str) -> str:
    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(object_to_download.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'


def st_download_info(text_dict: Dict) -> None:
    st.markdown("---")
    st.header("📥 Download runtime informations")
    st.markdown(
        "Download all runtime informations above as `streamlit-info.txt` file.")
    if st.button('⬇️ Generate download text file'):
        content = generate_output_text(text_dict)
        tmp_download_link = download_link(content, 'streamlit-info.txt', 'Click here to download file')
        st.markdown(tmp_download_link, unsafe_allow_html=True)


def st_run_shell_commands() -> None:
    st.markdown("---")
    st.header("⌨ Run shell command")
    st.markdown(
        "Here you can run any shell command in the runtime. Enter the command and press enter to start execution.")
    command = st.text_input(label="Input of shell command - Press Enter to run command")
    if command:
        exitcode, output = run_subprocess(command)
        if exitcode:
            st.error(f'FAILED: {command}')
            st.code(output, language='logging')
        else:
            st.info(f'Success: {command}')
            st.code(output, language='logging')


def st_rerun() -> None:
    st.markdown("---")
    st.header("🔄 Rerun Streamlit App from Top")
    st.markdown("""
        Here you can trigger a manual rerun of the whole Streamlit App from the top.<br>
        Just for testing purposes.
        """, unsafe_allow_html=True)
    if st.button('Rerun Streamlit App'):
        st.experimental_rerun()


if __name__ == "__main__":
    st.set_page_config(page_title="Streamlit Sharing", page_icon='✅',
                    layout='wide', initial_sidebar_state='collapsed')
    st.title('Streamlit Sharing Test')
    st.markdown("""
        This app is designed to explore the Streamlit Sharing runtime a bit. <br>
        Color design was taken from the **`Shades of Purple`** theme from VSCode.
        """, unsafe_allow_html=True)
    output_text['Python'] = st_get_python_version()
    output_text['System'] = st_get_system_version()
    output_text['Apt'] = st_get_apt_packages()
    output_text['Sources'] = st_get_apt_sources()
    # output_text['freeze'] = st_get_pip_freeze()
    output_text['pip'] = st_get_pip_list()
    output_text['pipdeptree'] = st_get_pipdeptree()
    output_text['modules'] = st_get_packages_distributions()
    st_download_info(output_text)
    st_run_shell_commands()
    # st_test_pip_import(packages)
    st_rerun()
