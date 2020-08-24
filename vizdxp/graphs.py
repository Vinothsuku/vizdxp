import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

@st.cache(suppress_st_warning=True, allow_output_mutation=True, show_spinner=False)
def scatter_plot(df,xaxis,yaxis,zaxis,modchk,aggfunc, color):
    if aggfunc == 'None':
        if zaxis == 'None':
            fig = px.scatter(df, x=xaxis, width=1200,hover_data=[yaxis], color=yaxis, opacity=0.8,render_mode='svg', color_continuous_scale=color, title= f"<b>{xaxis} Vs {yaxis}")
            fig.update_yaxes(showgrid=False, zeroline=False, title=f'<b>{yaxis}</b>')
        else:
            fig = px.scatter(df, x=xaxis, y=yaxis, width=1200,hover_data=[yaxis], color=zaxis, opacity=0.8,render_mode='svg', color_continuous_scale=color, title= f"<b>{xaxis} Vs {yaxis}")
            fig.update_yaxes(showgrid=False, zeroline=False, title=f'<b>{yaxis}</b>')
    elif aggfunc == 'mean':
        df_tmp = df.groupby([xaxis])[yaxis].mean().reset_index()
        fig = px.scatter(df_tmp, x=xaxis, y=yaxis, width=1200,hover_data=[yaxis], color=yaxis, opacity=0.9, render_mode='svg',color_continuous_scale=color, title= f"<b>{xaxis} Vs {yaxis}")
        fig.update_yaxes(showgrid=False, zeroline=False, title=f'<b>{yaxis}-mean</b>')
    elif aggfunc == 'sum':
        df_tmp = df.groupby([xaxis])[yaxis].sum().reset_index()
        fig = px.scatter(df_tmp, x=xaxis, y=yaxis, width=1200,hover_data=[yaxis], color=yaxis, opacity=0.9, render_mode='svg',color_continuous_scale=color, title= f"<b>{xaxis} Vs {yaxis}")
        fig.update_yaxes(showgrid=False, zeroline=False, title=f'<b>{yaxis}-sum</b>')
    else:
        if zaxis == 'None':
            df_tmp = df.groupby([xaxis])[yaxis].count().reset_index()
            fig = px.scatter(df_tmp, x=xaxis, width=1200,hover_data=[yaxis], color=yaxis, opacity=0.9,render_mode='svg', color_continuous_scale=color, title= f"<b>{xaxis} Vs {yaxis}")
            fig.update_yaxes(showgrid=False, zeroline=False)
        else:
            df_tmp = df.groupby([xaxis, yaxis])[zaxis].count().reset_index()
            fig = px.scatter(df_tmp, x=xaxis, y=yaxis, width=1200,hover_data=[yaxis], color=zaxis, opacity=0.8,render_mode='svg', color_continuous_scale=color, title= f"<b>{xaxis} Vs {yaxis}")
            fig.update_yaxes(showgrid=False, zeroline=False, title=f'<b>{yaxis}</b>')
    fig.update_layout(legend_orientation="v", plot_bgcolor='rgb(255,255,255)')
    fig.update_xaxes(showgrid=True, zeroline=False)
    fig.update_traces(mode=modchk)
    return fig

@st.cache(suppress_st_warning=True, allow_output_mutation=True, show_spinner=False)
def goscatter_plot(df,xaxis,multiaxis,aggfunc):
    fig = go.Figure()
    for i in range(len(multiaxis)):
        fig.add_trace(go.Scatter(x=df[xaxis], y=df[multiaxis[i]], name=multiaxis[i], mode='markers+lines'))
    fig.update_xaxes(showgrid=False, zeroline=False, title=f'<b>{xaxis}</b>')
    fig.update_layout(legend_orientation="v", plot_bgcolor='rgb(255,255,255)', width=1200)
    return fig


@st.cache(suppress_st_warning=True, allow_output_mutation=True, show_spinner=False)
def bar_plot(df,xaxis,yaxis,zaxis,modechk, aggfunc,color):
    if aggfunc == 'None':
        if zaxis == 'None':
            fig = px.bar(df, x=xaxis, height=450, width=1200, color=yaxis, color_continuous_scale=color, barmode =modechk, title= f"<b>{xaxis} Vs {yaxis}")
            fig.update_yaxes(showgrid=False, zeroline=False, title=f'<b>{yaxis}</b>')
        else:
            fig = px.bar(df, x=xaxis, y=yaxis, height=450, width=1200, color=zaxis, color_continuous_scale=color, barmode =modechk, title= f"<b>{xaxis} Vs {yaxis}")
            fig.update_yaxes(showgrid=False, zeroline=False, title=f'<b>{yaxis}</b>')
    elif aggfunc == 'mean':
        df_tmp = df.groupby([xaxis])[yaxis].mean().reset_index()
        fig = px.bar(df_tmp, x=xaxis, y=yaxis, width=1200, text=yaxis, hover_data=[yaxis], color=yaxis, color_continuous_scale=color, barmode ='group', title= f"<b>{xaxis} Vs {yaxis}")
        fig.update_traces(texttemplate='%{text:.1f}', textposition='auto')
        fig.update_yaxes(showgrid=False, zeroline=False, title=f'<b>{yaxis}-mean</b>')
    elif aggfunc == 'sum':
        df_tmp = df.groupby([xaxis])[yaxis].sum().reset_index()
        fig = px.bar(df_tmp, x=xaxis, y=yaxis, width=1200, text=yaxis, hover_data=[yaxis], color=yaxis, color_continuous_scale=color, barmode ='group', title= f"<b>{xaxis} Vs {yaxis}")
        fig.update_traces(texttemplate='%{text:.0f}', textposition='auto')
        fig.update_yaxes(showgrid=False, zeroline=False, title=f'<b>{yaxis}-sum</b>')
    else:
        if zaxis == 'None':
            df_tmp = df.groupby([xaxis])[yaxis].count().reset_index()
            fig = px.bar(df_tmp, x=xaxis, y =yaxis, height = 450, width=1200, hover_data=[yaxis], color=yaxis, color_continuous_scale=color, barmode = 'group', title= f"<b>{xaxis} Vs {yaxis}")
            fig.update_yaxes(showgrid=False, zeroline=False, title='count')
        else:
            df_tmp = df.groupby([xaxis, yaxis])[zaxis].count().reset_index()
            fig = px.bar(df_tmp, x=xaxis, y=yaxis, height = 450, width=1200, hover_data=[yaxis], color=zaxis, color_continuous_scale=color, barmode ='group', title= f"<b>{xaxis} Vs {yaxis}")
            fig.update_yaxes(showgrid=False, zeroline=False, title=f'<b>{yaxis}</b>')
    fig.update_layout(legend_orientation="v", plot_bgcolor='rgb(255,255,255)')
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    return fig

@st.cache(suppress_st_warning=True, show_spinner=False)
def pie_plot(df, xaxis, yaxis, pieaxis, color):
    if pieaxis == 'xaxis':
        tmp1 = df[xaxis].value_counts().reset_index()[:10]
        fig = px.pie(tmp1, values=xaxis, title=xaxis, labels='index', names='index', width=1100, color_discrete_sequence=px.colors.sequential.Teal_r)
    else:
        tmp1 = df[yaxis].value_counts().reset_index()[:10]
        fig = px.pie(tmp1, values=yaxis, title=yaxis, labels='index', names='index', width=1100, color_discrete_sequence=px.colors.sequential.Teal_r)
    fig.update_traces(textposition='outside', textinfo='percent+label')
    return fig

@st.cache(suppress_st_warning=True, show_spinner=False)
def heatmap_plot(df, xaxis, yaxis, zaxis, hagg, color):
    if hagg == 'mean':
        df_temp = df.groupby([xaxis, yaxis])[zaxis].mean().reset_index()
    elif hagg == 'sum':
        df_temp = df.groupby([xaxis, yaxis])[zaxis].sum().reset_index()
    else:
        df_temp = df.groupby([xaxis, yaxis])[zaxis].count().reset_index()
    fig = go.Figure(data=go.Heatmap(x = df_temp[xaxis], y=df_temp[yaxis], z=df_temp[zaxis], colorbar = dict(title=f'{zaxis}'),hoverongaps=False, colorscale=color))
    fig.update_xaxes(showgrid=False, zeroline=False, title=f'<b>{xaxis}</b>')
    fig.update_yaxes(showgrid=False, zeroline=False, title=f'<b>{yaxis}</b>')
    fig.update_layout(plot_bgcolor='rgb(255,255,255)')
    # st.plotly_chart(fig)
    return fig

@st.cache(suppress_st_warning=True, show_spinner=False)
def histogram_plot(df, xaxis, yaxis, histbox, histaxis):
    fig = go.Figure()
    if histbox=='count': histbox=''
    if histaxis == 'xaxis':
        fig.add_trace(go.Histogram(x=df[xaxis], histnorm=histbox, name=f'{xaxis}', marker_color='#636EFA'))
    elif histaxis == 'yaxis':
        fig.add_trace(go.Histogram(x=df[yaxis], histnorm=histbox, name=f'{yaxis}', marker_color='#19D3F3'))
    else:
        fig.add_trace(go.Histogram(x=df[xaxis], histnorm=histbox, name=f'{xaxis}', marker_color='#636EFA'))
        fig.add_trace(go.Histogram(x=df[yaxis], histnorm=histbox, name=f'{yaxis}', marker_color='#19D3F3'))
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    fig.update_layout(plot_bgcolor='rgb(255,255,255)', height=450, width=1200)
    return fig

@st.cache(suppress_st_warning=True, show_spinner=False)
def box_plot(df, xaxis, yaxis, boxpt, boxaxis):
    fig = go.Figure()
    if boxpt=='False': boxpt=False
    if boxaxis == 'xaxis':
        fig.add_trace(go.Box(x=df[xaxis], boxpoints=boxpt, name=f'{xaxis}', marker_color='#636EFA'))
    elif boxaxis == 'yaxis':
        fig.add_trace(go.Box(x=df[yaxis], boxpoints=boxpt, name=f'{yaxis}', marker_color='#19D3F3'))
    else:
        fig.add_trace(go.Box(x=df[xaxis], boxpoints=boxpt, name=f'{xaxis}', marker_color='#636EFA'))
        fig.add_trace(go.Box(x=df[yaxis], boxpoints=boxpt, name=f'{yaxis}', marker_color='#19D3F3'))
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    fig.update_layout(plot_bgcolor='rgb(255,255,255)', height=450, width=1200)
    return fig
