# standard libraries
import base64
import importlib
import json
import logging
import platform
import socket
import subprocess
import sys

# external libraries
import importlib_metadata
import plotly.graph_objects as go
import psutil
import streamlit as st

# import streamlit.components.v1 as components
from tabulate import tabulate

output_text = dict()

@st.cache
def getSystemInfoDict():
    try:
        info = dict()
        info['platform.system'] = platform.system()
        info['platform.release'] = platform.release()
        info['platform.version'] = platform.version()
        info['platform.machine'] = platform.machine()
        info['platform.node'] = platform.node()
        info['socket.gethostname'] = socket.gethostname()
        info['ip-address'] = socket.gethostbyname(socket.gethostname())
        info['platform.processor'] = platform.processor()
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
    return subprocess.getstatusoutput(r'pip list --format json')


@st.cache
def get_subprocess_pipdeptree():
    return subprocess.getstatusoutput(r'pipdeptree --json')


@st.cache
def get_subprocess_apt_list():
    # return subprocess.getstatusoutput(r'apt list --installed')
    # return subprocess.getstatusoutput(r'dpkg -l')
    return subprocess.getstatusoutput(r"dpkg-query --show --showformat='${Package;-26} ${Version;-24} \t${binary:Synopsis}\n'")


@st.cache
def get_subprocess_apt_sources():
    return subprocess.getstatusoutput(r'cat /etc/apt/sources.list')


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
    st.markdown("---")
    st.header("🐍 Python Version")
    st.markdown(
        "Show the currently used Python version in the runtime - acquired with **`sys.version`**")
    output = sys.version.replace('\n', '')
    st.code(output, language='logging')
    return output


def tabulate_table_factory(headers, cells, showindex=False, tablefmt="github"):
    cells =  [*zip(*cells)]  # Transpose the 2D array of cells
    tab = tabulate(cells, headers=headers, showindex=showindex, tablefmt=tablefmt)
    return tab


def ploty_fig_table_factory(header, cells):
    header = list([f'<b>{h}</b>' for h in header]) # bold header
    fig = go.Figure(data=[go.Table(
        header=dict(values=header,
                    # line_color='#eeeeee',
                    # fill_color='#B362FF',
                    align='left',
                    # height=40
                    ),
        cells=dict(values=cells,
                    # line_color='#eeeeee',
                    # fill_color='#2D2B55',
                    align='left',
                    # height=30
                    ))
        ])
    fig.update_layout(margin_l=0, margin_r=0, margin_t=10, margin_b=0)
    fig.update_layout(font_family="Arial", font_size=14)
    fig.update_layout(dragmode="select", selectdirection="v")
    fig.update_layout(autosize=True)  # does not work
    # fig.update_layout(height=28*len(cells[0])+40)  # dynamic height
    return fig


def st_get_system_version():
    st.markdown("---")
    st.header("ℹ️ System Information")
    st.markdown(
        "Show some basic system informations about the runtime")
    codeblock = str()
    sysinfos = getSystemInfoDict()
    if isinstance(sysinfos, dict):
        headers=['Parameter', 'Value']
        cells=[list(sysinfos.keys()), list(sysinfos.values())]
        # for key, value in sysinfos.items():
        #     codeblock += f"{key.capitalize(): <17}: {value}\n"
        # st.code(codeblock, language='logging')
        fig = ploty_fig_table_factory(
            header=headers,
            cells=cells)
        config = {'displayModeBar': False}
        # st.plotly_chart(fig, use_container_width=True, config=config)
        # st.code(tabulate_table_factory(headers, cells, showindex=True), language='logging')
        st.markdown(tabulate_table_factory(headers, cells, showindex=False))
    else:
        st.error('Acquisition of system infos failed')
        st.code(sysinfos, language='logging')
    return codeblock


def st_get_apt_packages():
    st.markdown("---")
    st.header("🐧 Apt Packages")
    st.markdown(
        "List all installed **`apt`** packages of the runtime - acquired with **`dpkg-query --show --showformat`**")
    exitcode, output = get_subprocess_apt_list()
    if exitcode:
        st.warning('FAILED: dpkg-query --show --showformat')
        # st.warning('FAILED: apt list --installed')
        st.code(output, language='logging')
    else:
        st.code(output, language='logging')
    return output


def st_get_apt_sources():
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


def st_get_pip_freeze():
    st.markdown("---")
    st.header("🐍 Pip Packages - pip freeze")
    exitcode, output = get_subprocess_pip_freeze()
    if exitcode:
        st.error('FAILED: pip freeze')
        st.code(output, language='logging')
    else:
        st.code(output, language='logging')
    return output


def get_dict_from_piplist(jsonified):
    packages = dict()
    for elem in jsonified:
        pkg = elem.get('name')
        ver = elem.get('version')
        packages[pkg] = ver
    return dict(sorted(packages.items()))


def st_get_pip_list():
    st.markdown("---")
    st.header("🐍 Pip Packages")
    st.markdown(
        "List all installed **`pip`** packages of the runtime - acquired with **`pip list`**")
    exitcode, output = get_subprocess_pip_list()
    if exitcode:
        st.error('FAILED: pip list')
        st.code(output, language='logging')
    else:
        jsonified = json.loads(output)
        jsonified = get_dict_from_piplist(jsonified)
        if isinstance(jsonified, dict):
            headers = ["Package", "Version"]
            cells=[list(jsonified.keys()), list(jsonified.values())]
            header1 = "Package<br>"
            header2 = "Version<br>"
            fig = ploty_fig_table_factory(
                header=headers,
                cells=cells)
            config = {'displayModeBar': False}
            # st.plotly_chart(fig, use_container_width=True, config=config)
            st.markdown(tabulate_table_factory(headers, cells, showindex=True))
        # st.json(jsonified)
        # st.code(output, language='logging')
        # pip_list = json.loads(output)
        # pip_list = list(dict({item['name'] : item['version']}) for item in pip_list)
        # pip_list = tabulate(pip_list, headers=['Package', 'Version'], tablefmt="grid")
        # pip_list = tabulate(pip_list, tablefmt="html")
        # components.html(pip_list)
        # st.json(pip_list)
        # st.table(pd.DataFrame.from_dict(pip_list, orient='index', dtype='str', columns=['Version']))
    return output


def get_dependencies(jsonified):
    dependencies = str()
    if jsonified:
        for pkg in jsonified:
            pkg_str = f"{pkg['key']}:{pkg['package_name']}:{pkg['installed_version']}:{pkg['required_version']}"
            dependencies += f"{pkg_str}\n"
    return dependencies.strip()


def get_dict_from_pipdeptree(jsonified):
    packages = dict()
    for elem in jsonified:
        pkg = elem.get('package')
        pkg_str = f"{pkg['key']}:{pkg['package_name']}:{pkg['installed_version']}"
        dep = get_dependencies(elem.get('dependencies'))
        packages[pkg_str] = dep
    return dict(sorted(packages.items()))


def st_get_pipdeptree():
    st.markdown("---")
    st.header("🐍 Pipdeptree Output")
    st.markdown(
        "List all installed python packages of the runtime - acquired with **`pipdeptree`**")
    exitcode, output = get_subprocess_pipdeptree()
    if exitcode:
        st.warning('FAILED: pipdeptree --json')
        st.code(output, language='logging')
    else:
        jsonified = json.loads(output)
        jsonified = get_dict_from_pipdeptree(jsonified)
        if isinstance(jsonified, dict):
            headers = ["Package\nkey:package_name:installed_version", "Dependencies\nkey:package_name:installed_version:required_version"]
            cells=[list(jsonified.keys()), list(jsonified.values())]
            header1 = "Package<br>key:package_name:installed_version"
            header2 = "Dependencies<br>key:package_name:installed_version:required_version"
            fig = ploty_fig_table_factory(
                header=[header1, header2],
                cells=cells)
            config = {'displayModeBar': False}
            # st.plotly_chart(fig, use_container_width=True, config=config)
            st.code(tabulate_table_factory(headers, cells, showindex=True, tablefmt="grid"), language="logging")
        # else:
        #     st.code(get_dict_from_pipdeptree(jsonified), language='logging')
    return output


def st_get_packages_distributions():
    st.markdown("---")
    st.header("🐍 Pip Modules")
    st.markdown(
        "List all importable python modules of the runtime - acquired with **`importlib_metadata.packages_distributions`**")
    packages = get_packages_distributions()
    output = '\n'.join(packages)
    st.code(output, language='logging')
    return output


def st_test_pip_import(packages):
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


def generate_output_text(text_dict):
    output = str()
    for key, value in text_dict.items():
        output += "==========================================================================================\n"
        output += f'{key.capitalize()}\n'
        output += "==========================================================================================\n"
        output += '\n'
        output += f'{value}\n'
        output += '\n\n\n'
    return output


def download_link(object_to_download, download_filename, download_link_text):
    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(object_to_download.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'


def st_download_info(text_dict):
    st.markdown("---")
    st.header("📥 Download runtime informations")
    st.markdown(
        "Download all runtime informations above as `streamlit-info.txt` file.")
    if st.button('⬇️ Generate download text file'):
        content = generate_output_text(text_dict)
        tmp_download_link = download_link(content, 'streamlit-info.txt', 'Click here to download file')
        st.markdown(tmp_download_link, unsafe_allow_html=True)


def st_run_shell_commands():
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


def st_rerun():
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
    output_text['python'] = st_get_python_version()
    st_get_system_version()
    output_text['apt'] = st_get_apt_packages()
    output_text['sources'] = st_get_apt_sources()
    # output_text['freeze'] = st_get_pip_freeze()
    output_text['pip'] = st_get_pip_list()
    output_text['pipdeptree'] = st_get_pipdeptree()
    output_text['modules'] = st_get_packages_distributions()
    st_download_info(output_text)
    st_run_shell_commands()
    # st_test_pip_import(packages)
    st_rerun()
