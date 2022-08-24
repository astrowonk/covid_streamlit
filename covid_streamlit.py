import streamlit as st
import plotly.express as px

from urllib.parse import quote
import requests
import pandas as pd

api_base_url = st.secrets['api_base_url']


class apiLoader:
    @staticmethod
    def process_json(json):
        df = pd.DataFrame(json)
        df['date'] = pd.to_datetime(df['date'])
        return df

    def all_counties(self):
        url = f"{api_base_url}/all_counties"
        response = requests.get(url)
        return response.json()

    def all_states(self):
        url = f"{api_base_url}/all_states"
        response = requests.get(url)
        return response.json()

    def get_cases(self, states):
        state_list = quote("+".join(states))
        url = f"{api_base_url}/cases/{state_list}"
        response = requests.get(url)
        return self.process_json(response.json())

    def get_deaths(self, states):
        state_list = quote("+".join(states))
        url = f"{api_base_url}/deaths/{state_list}"
        response = requests.get(url)
        return self.process_json(response.json())


myDataLoader = apiLoader()


@st.experimental_memo(ttl=3600)
def data_load_wrapper(data_type, regions=None):

    if data_type == 'all_counties':
        return myDataLoader.all_counties()
    elif data_type == 'all_states':
        return myDataLoader.all_states()
    elif data_type == 'cases':
        return myDataLoader.get_cases(regions)
    elif data_type == 'deaths':
        return myDataLoader.get_deaths(regions)


st.set_page_config(page_title="Covid Case Growth Plots", layout='wide')

st.title('Covid Case Growth Plots')
## layout
with st.sidebar:
    states = st.multiselect('State:', data_load_wrapper('all_states'),
                            ['Virginia'])
    counties = st.multiselect('Counties:', data_load_wrapper('all_counties'),
                              ['Harris, Texas'])
    data_type = st.selectbox('Data Type:', ['Cases', 'Deaths'])
    rolling_days = st.slider('Rolling Average Days:', 1, 14, 7)
    show_hover = st.radio('Show Hover Data:', ['none', 'minimal', 'full'], 2)
    show_spike = st.checkbox('Show Spikeline:', False)

    st.markdown("""

***
The source code for this streamlit version of my covid case app is [available on github](https://github.com/astrowonk/covid_streamlit). 

This streamlit data shares data with the [Dash version](https://marcoshuerta.com/dash/covid/), via a simple private [REST API](https://github.com/astrowonk/covid_dash/blob/main/rest_api.py).    


    """)

if data_type == 'Cases':
    y_axis_label = "New Reported Cases Per 100,000"
    y_variable = 'rolling_case_growth_per_100K'
    hover_data = [
        'date', 'rolling_new_cases', 'rolling_case_growth_per_100K',
        'New Cases', 'case_growth_per_100K'
    ]
    cases = True
else:
    y_axis_label = "New Reported Deaths Per 100,000"
    y_variable = 'rolling_new_deaths_per_100K'
    hover_data = ['date', 'rolling_new_deaths_per_100K', 'new_deaths_per_100K']
    cases = False

states_and_counties = sorted(
    states + counties
)  # sort to so the singleton decorator doesn't think Texas,Virginia is different than Virginia,Texas

if len(states_and_counties) > 15:
    #quietly limiting the length of the list to 15
    states_and_counties = states_and_counties[:15]

if cases:
    dff = data_load_wrapper('cases',
                            states_and_counties).sort_values(["date", "state"
                                                              ]).reset_index()
    dff["rolling_case_growth_per_100K"] = dff.groupby(
        'state')['case_growth_per_100K'].transform(
            lambda s: s.rolling(rolling_days, min_periods=1).mean())
    dff["rolling_new_cases"] = dff.groupby('state')['New Cases'].transform(
        lambda s: s.rolling(rolling_days, min_periods=1).mean())
else:
    dff = data_load_wrapper('deaths',
                            states_and_counties).sort_values(["date", "state"
                                                              ]).reset_index()
    dff["rolling_new_deaths_per_100K"] = dff.groupby(
        'state')['new_deaths_per_100K'].transform(
            lambda s: s.rolling(rolling_days, min_periods=1).mean())

fig = px.line(dff,
              x="date",
              y=y_variable,
              color="state",
              hover_data=hover_data,
              labels={'state': ''})
fig.update_layout(margin={
    'l': 1,
    'r': 1,
    'b': 3,
    't': 10,
    'pad': 8,
},
                  legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
                  xaxis_title=None,
                  yaxis_title=y_axis_label,
                  autosize=True,
                  font=dict(size=12),
                  hovermode='closest')
if show_hover == 'minimal':
    fig.update_layout(hovermode="x")
    fig.update_traces(hovertemplate=None)
elif show_hover == 'none':
    fig.update_traces(hovertemplate=None, hoverinfo='none')
fig.update_yaxes(
    automargin=True,
    showspikes=show_spike,
    spikemode="across",
)
fig.update_xaxes(automargin=True)

st.plotly_chart(fig, use_container_width=False)
