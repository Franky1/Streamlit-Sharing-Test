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
import plotly.graph_objects as go

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


headers = ["Package", "Version"]
cells = []

# for key, value in sysinfos.items():
#     codeblock += f"{key.capitalize(): <17}: {value}\n"
# st.code(codeblock, language='logging')
fig = ploty_fig_table_factory(
    header=headers,
    cells=cells)
config = {'displayModeBar': False}
# st.plotly_chart(fig, use_container_width=True, config=config)


header1 = "Package<br>"
header2 = "Version<br>"
fig = ploty_fig_table_factory(
    header=headers,
    cells=cells)
config = {'displayModeBar': False}
# st.plotly_chart(fig, use_container_width=True, config=config)


header1 = "Package<br>key:package_name:installed_version"
header2 = "Dependencies<br>key:package_name:installed_version:required_version"
fig = ploty_fig_table_factory(
    header=[header1, header2],
    cells=cells)
config = {'displayModeBar': False}
# st.plotly_chart(fig, use_container_width=True, config=config)
