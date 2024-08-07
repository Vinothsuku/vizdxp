import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re
from pandas.api.types import is_numeric_dtype, is_string_dtype, is_datetime64_any_dtype, is_bool_dtype, is_float_dtype
from vizdxp.graphs import scatter_plot, goscatter_plot, bar_plot, pie_plot, heatmap_plot, histogram_plot, box_plot
import os

st.set_page_config(
    page_title="vizdxp",
    page_icon=":koala:",
    layout="wide",
    initial_sidebar_state="expanded",
 )

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
	
target_css = os.path.join(os.path.dirname(__file__), 'style.css')

local_css(target_css)

st.markdown('<style>div.Widget.row-widget.stRadio> div{flex-direction:row;}</style>', unsafe_allow_html=True)

header1 = "<div><span class='highlight darkblue'><span class='bold'>Dataset stats</span></span> </div>"
header2 = "<div><span class='highlight darkblue'><span class='bold'>Visual Data Explorer</span> </span></div>"

main1 = "<div><span class='fontteal'>vizdxp is an open-source visualization tool that helps in quick exploratory data analysis and lets user to report findings as an application\
\
</span></div>"

main2 = """
A **big heartfelt Thanks** for your time in trying our tiny-simple-data visualization tool.<br>

<p>vizdxp is an open-source web app designed via streamlit weaved with plotly library. <span class='fontteal'><b>Its incredibly Simple - Just drag & drop any csv and explore the data visually.</b></span> By default the application will figure out better visualization based on user selections. \
Feel free to customize as needed. </p>

<b>Advantages</b>
- **Simple** and quick for any <span class='fontteal'>**Exploratory Data Analysis**</span>
- Create interactive <span class='fontteal'>**Dashboard web app within minutes**</span> from any csv and share the findings
- <span class='fontteal'>**Deploy**</span> it as a web application in your own workstations too
- By <span class='fontteal'>**Default**</span> - chart types and aggregations are applied based on columns selected by user, null rows are removed, Date fields are converted to multiple subfields
- Highly <span class='fontteal'>**Customizable**</span>
- No more static reports<br>
"""

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def convert_date(df):
    df = df.apply(lambda label: pd.to_datetime(label, errors='ignore', infer_datetime_format=True)
        if label.dtypes == object
        else label, axis=0)
    return df

@st.cache_data(show_spinner=False)
def process_date(df):
    for label,content in df.items():
        if is_datetime64_any_dtype(content):
            df[label].fillna(value=0)
            fld = df[label]
            targ_pre = re.sub('[Dd]ate$', '', label)
            attr = ['Year', 'Month', 'Day', 'Dayofweek', 'Dayofyear','Quarter']
            for n in attr: df[targ_pre + n] = getattr(fld.dt, n.lower())

@st.cache_data(show_spinner=False)
def load_dataset(df):
    df_raw = pd.read_csv(df, low_memory=False, encoding='latin-1')
    df_raw.dropna(how='all', inplace=True)
    rows = df_raw.shape[0]; cols = df_raw.shape[1]
    return df_raw, rows, cols

@st.cache_data(show_spinner=False)
def fillna_values(df):
    for label,content in df.items():
        if is_string_dtype(content):
            df[label].fillna(value='Null', inplace=True)
    return df

@st.cache_data(show_spinner=False)
def video():
    demo_file1 = open('vizdxp_ctds.mp4', 'rb')
    demo_rec1 = demo_file1.read()
    return demo_rec1

def main():
    prodheader = "<div><span class='fontteal'><span class='bold'>vizdxp</span></div>"
    st.sidebar.markdown(prodheader, unsafe_allow_html=True)
    df = st.sidebar.file_uploader('Upload data in csv format', type='csv')
    page = st.sidebar.radio("Go-To",('Getting started','Dataset stats','Visual data explorer', 'Report'), key="page_selection")
    if page == 'Getting started':
        st.markdown("# Welcome.")
        st.markdown(main2, unsafe_allow_html=True)
        st.markdown("Please provide your valuable suggestions, feature requests, notifying issues in [github](https://github.com/Vinothsuku/vizdxp)", unsafe_allow_html=True)
        st.sidebar.markdown("")
        # st.markdown(slide_link, unsafe_allow_html=True)
        st.sidebar.markdown("")
        st.sidebar.markdown("<br><br><br> <br><br><br><br> <br><br><br><br><br> <br><br><br><br><br> ", unsafe_allow_html=True)
        st.sidebar.markdown("")
        st.sidebar.markdown("### contact: vizdxp@gmail.com")
    if df is not None:
        df_raw, rows, cols = load_dataset(df)
        if page == 'Dataset stats':
            st.markdown("# Dataset stats.")
            st.markdown(f"- Number of records: **{rows}**")
            st.markdown("<style>p{color:#008ae6;}</style>", unsafe_allow_html=True)
            st.markdown('**Few rows from the dataset**', unsafe_allow_html=True)
            st.write(df_raw.astype('object').head(5))
            stats_n = st.checkbox("Quick stats")
            if stats_n:
                st.markdown('**Few stats on the dataset**')
                st.cache(st.write(df_raw.describe(include='all').T, width=600, height=900))
        elif page == 'Visual data explorer':
            df_raw = convert_date(df_raw)
            process_date(df_raw)
            df_raw = fillna_values(df_raw)
            clrchk = st.sidebar.selectbox("Color Palette",('Viridis','Cividis','Inferno', 'Plasma', 'Electric', 'Rainbow', 'Sunset','Purpor','Teal','Dense', 'Deep','Speed'))
            viz_page = st.sidebar.radio("Let's do",('Plot 1','Plot 2'), key="plot_selection")
            st.markdown("# Visual data explorer.")
            col_list = list(df_raw.columns)
            col_list.insert(0,'None')
            if viz_page == 'Plot 1':
                x_axis1 = st.sidebar.selectbox('select xaxis',(df_raw.columns), 1)
                y_axis1 = st.sidebar.selectbox('select yaxis',(df_raw.columns), 2)
                z_axis1 = st.sidebar.selectbox('Addn col for color coding / zaxis',(col_list))
                if x_axis1 == y_axis1:
                    st.error("Pls choose different columns in x and y axis for generating plots")
                plot1 = st.checkbox("Generate Plot 1", key='Plot1_Generate')
                if z_axis1 == 'None' and is_numeric_dtype(df_raw[y_axis1]):
                    acheck1 = st.radio("Aggregate options [bar and scatter]",('None','mean','sum','count'), index=1, key="sidebar_agg_plot1")
                else:
                    acheck1 = st.radio("Aggregate options [bar and scatter]",('None','count'), index=1, key="sidebar_agg_plot2")
                charts = st.sidebar.selectbox("Chart Type",('default','scatter','bar','pie', 'heatmap','histogram','box','multi_yaxis_scatter'), key="sidebar_chart_plot1")
                if plot1 and x_axis1 != y_axis1:
                    if charts=='default':
                        if df_raw[x_axis1].nunique() > 100:
                            scmodechk1 = st.radio("Scatter Mode",('markers','markers+lines','lines'), 0, key="scatter_m_radio")
                            fig = scatter_plot(df_raw, x_axis1, y_axis1, z_axis1, scmodechk1, aggfunc=acheck1, color=clrchk)
                            st.plotly_chart(fig)
                        else:
                            barmodechk1 = st.radio("Bar Mode",('relative','stack','group','overlay'), key="bar_mode_radio")
                            fig = bar_plot(df_raw, x_axis1, y_axis1, z_axis1, barmodechk1, aggfunc=acheck1, color=clrchk)
                            st.plotly_chart(fig)
                    elif charts =='scatter':
                            scmodechk1 = st.radio("Scatter Mode",('markers','markers+lines','lines'), 0, key="scatter_m_radio")
                            fig = scatter_plot(df_raw, x_axis1, y_axis1,z_axis1, scmodechk1, aggfunc=acheck1, color=clrchk)
                            st.plotly_chart(fig)
                    elif charts =='bar':
                        barmodechk1 = st.radio("Bar Mode",('relative','stack','group','overlay'), key="bar_mode_radio")
                        fig = bar_plot(df_raw, x_axis1, y_axis1, z_axis1, barmodechk1, aggfunc=acheck1, color=clrchk)
                        st.plotly_chart(fig)
                    elif charts =='pie':
                        pieaxis = st.radio("Pie plot on",('xaxis','yaxis'), 0, key="pie_axis_radio")
                        fig = pie_plot(df_raw, x_axis1, y_axis1, pieaxis, color=clrchk)
                        st.plotly_chart(fig)
                    elif charts == 'heatmap':
                        if z_axis1 == 'None':\
                            st.error("Error: Pls choose zaxis as well in the side pane for generating heatmap")
                        elif is_numeric_dtype(df_raw[z_axis1]):
                            htmap_agg1 = st.sidebar.radio("Aggregate options by zaxis [heatmap] ",('mean','sum','count'), key="heatmap_agg")
                            fig = heatmap_plot(df_raw, x_axis1, y_axis1, z_axis1, htmap_agg1, color=clrchk)
                            st.plotly_chart(fig)
                        else:
                            fig = heatmap_plot(df_raw, x_axis1, y_axis1, z_axis1, 'count', color=clrchk)
                            st.plotly_chart(fig)
                    elif charts == 'histogram':
                        histbox = st.radio("Histogram Norm",('count','percent','probability','density','probability density'), 0, key="hist_norm_radio")
                        histaxis = st.radio("Histogram on",('xaxis','yaxis','x and yaxis'), 0, key="hist_axis_radio")
                        fig = histogram_plot(df_raw, x_axis1, y_axis1, histbox, histaxis)
                        st.plotly_chart(fig)
                    elif charts == 'box':
                        boxpt = st.radio("Box plot data points",('False','all','outliers','suspectedoutliers'), 1, key="box_points_radio")
                        boxaxis = st.radio("Boxplot on",('xaxis','yaxis','x and yaxis'), 0, key="box_axis_radio")
                        fig = box_plot(df_raw, x_axis1, y_axis1, boxpt, boxaxis)
                        st.plotly_chart(fig)
                    else:
                        selected_multiaxis = st.multiselect('Select multiple yaxis traces-', df_raw.columns)
                        fig = goscatter_plot(df_raw,x_axis1, selected_multiaxis, aggfunc=acheck1)
                        st.plotly_chart(fig)
                    plot1_text = st.text_area("Text area for marking observations", key="Plot1_textarea")
            else:
            #Plot 2 visualizations
                x_axis2 = st.sidebar.selectbox('select xaxis ',(df_raw.columns), 1, key="plt2_xaxis")
                y_axis2 = st.sidebar.selectbox('select yaxis ',(df_raw.columns), 2, key="plt2_yaxis")
                z_axis2 = st.sidebar.selectbox('Addn col for color coding / zaxis',(col_list), key="plt2_zaxis")
                if x_axis2 == y_axis2:
                    st.error("Pls choose different columns in x and y axis for generating plots")
                plot2 = st.checkbox("Generate Plot 2", key='Plot2_Generate')
                if z_axis2 == 'None' and is_numeric_dtype(df_raw[y_axis2]):
                    acheck2 = st.radio("Aggregate options - [bar and scatter]",('None','mean','sum','count'), index=1, key="sidebar_agg_plot2")
                else:
                    acheck2 = st.radio("Aggregate options - [bar and scatter]",('None','count'), index=1, key="sidebar_agg_plot2b")
                charts2 = st.sidebar.selectbox("Chart Type: ",('default','scatter','bar','pie', 'heatmap', 'histogram','box', 'multi_yaxis_scatter'), key="sb_chart_plot2")
                if plot2 and x_axis2 != y_axis2:
                    if charts2 =='default':
                        if df_raw[x_axis2].nunique() > 100:
                            scmodechk2 = st.radio("Scatter Mode",('markers','markers+lines','lines'), 0, key="scatter_m_radio2")
                            fig2 = scatter_plot(df_raw, x_axis2, y_axis2, z_axis2, scmodechk2, aggfunc=acheck2, color=clrchk)
                            st.plotly_chart(fig2)
                        else:
                            barmodechk2 = st.radio("Bar Mode",('relative','stack','group','overlay'), key="bar_mode_radio2")
                            fig2 = bar_plot(df_raw, x_axis2, y_axis2, z_axis2, barmodechk2, aggfunc=acheck2, color=clrchk)
                            st.plotly_chart(fig2)
                    elif charts2 =='scatter':
                            scmodechk2 = st.radio("Scatter Mode",('markers','markers+lines','lines'), 0, key="scatter_m_radio2")
                            fig2 = scatter_plot(df_raw, x_axis2, y_axis2, z_axis2, scmodechk2, aggfunc=acheck2, color=clrchk)
                            st.plotly_chart(fig2)
                    elif charts2 =='bar':
                        barmodechk2 = st.radio("Bar Mode",('relative','stack','group','overlay'), key="bar_mode_radio2")
                        fig2 = bar_plot(df_raw, x_axis2, y_axis2, z_axis2, barmodechk2, aggfunc=acheck2, color=clrchk)
                        st.plotly_chart(fig2)
                    elif charts2 =='pie':
                        pieaxis2 = st.radio("Pie plot on",('xaxis','yaxis'), 0, key="pie_axis_radio2")
                        fig2 = pie_plot(df_raw, x_axis2, y_axis2, pieaxis2, color=clrchk)
                        st.plotly_chart(fig2)
                    elif charts2 == 'heatmap':
                        if z_axis2 == 'None':
                            st.error("Error: Pls choose zaxis as well in the side pane for generating heatmap")
                        elif is_numeric_dtype(df_raw[z_axis2]):
                            htmap_agg2 = st.sidebar.radio("Aggregate options by zaxis  [heatmap]",('mean','sum','count'), key="heatmap_agg2")
                            fig2 = heatmap_plot(df_raw, x_axis2, y_axis2, z_axis2, htmap_agg2, color=clrchk)
                            st.plotly_chart(fig2)
                        else:
                            fig2 = heatmap_plot(df_raw, x_axis2, y_axis2, z_axis2, 'count', color=clrchk)
                            st.plotly_chart(fig2)
                    elif charts2 == 'histogram':
                        histbox2 = st.radio("Histogram Norm ",('count','percent','probability','density','probability density'), 0, key="hist_norm_radio2")
                        histaxis2 = st.radio("Histogram on ",('xaxis','yaxis','x and yaxis'), 0, key="hist_axis_radio2")
                        fig2 = histogram_plot(df_raw, x_axis2, y_axis2, histbox2, histaxis2)
                        st.plotly_chart(fig2)
                    elif charts2 == 'box':
                        boxpt2 = st.radio("Box plot points Norm ",('False','all','outliers','suspectedoutliers'), 1, key="box_points_radio2")
                        boxaxis2 = st.radio("Boxplot on ",('xaxis','yaxis','x and yaxis'), 0, key="box_axis_radio2")
                        fig2 = box_plot(df_raw, x_axis2, y_axis2, boxpt2, boxaxis2)
                        st.plotly_chart(fig2)
                    else:
                        selected_multiaxis2 = st.multiselect('Select multiple yaxis traces ', df_raw.columns)
                        fig2 = goscatter_plot(df_raw,x_axis2, selected_multiaxis2, aggfunc=acheck2)
                        st.plotly_chart(fig2)
                    plot2_text = st.text_area("Text area to provide addn details ", key="Plot2_textarea")
        else:
            st.markdown('')

#if __name__ == "__main__":
main()
