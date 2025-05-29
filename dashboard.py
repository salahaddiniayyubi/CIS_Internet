import streamlit as st
import pickle
import os
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="CIS Internet QoS Dashboard", layout="wide")

st.title("CIS Countries Internet Quality Dashboard")
st.markdown("Compare internet quality indicators (QoS) across CIS countries. Data source: Speedtest.net Global Index.")

cis_pickle_path = os.path.join(os.path.dirname(__file__), 'cis_new')

# Load data
def load_data():
    with open(cis_pickle_path, 'rb') as f:
        data = pickle.load(f)
    return data

data = load_data()

# List of countries and metrics
countries = list(data.keys())
metrics = ['fixedMean', 'mobileMean', 'fixedMedian', 'mobileMedian']
metric_labels = {
    'fixedMean': 'Fixed Mean (Mbps)',
    'mobileMean': 'Mobile Mean (Mbps)',
    'fixedMedian': 'Fixed Median (Mbps)',
    'mobileMedian': 'Mobile Median (Mbps)'
}

# Sidebar controls
st.sidebar.header("Controls")
selected_metric = st.sidebar.selectbox("Select Metric", metrics, format_func=lambda x: metric_labels[x])
selected_countries = st.sidebar.multiselect("Select Countries", countries, default=countries)

# Prepare data for plotting
def prepare_df(selected_metric, selected_countries):
    rows = []
    skipped = 0
    for country in selected_countries:
        for entry in data[country][selected_metric]:
            date = entry.get('date')
            value = entry.get('value')
            if date is not None and value is not None:
                rows.append({
                    'Country': country.title(),
                    'Date': date,
                    'Value': value
                })
            else:
                skipped += 1
    if skipped > 0:
        st.warning(f"{skipped} data points were skipped due to missing 'date' or 'value'.")
    df = pd.DataFrame(rows)
    if not df.empty:
        df['Date'] = pd.to_datetime(df['Date'])
    return df

df = prepare_df(selected_metric, selected_countries)

# Plot
graph = px.line(
    df,
    x='Date',
    y='Value',
    color='Country',
    markers=True,
    title=f"{metric_labels[selected_metric]} Over Time"
)

graph.update_layout(legend_title_text='Country', xaxis_title='Date', yaxis_title=metric_labels[selected_metric])
st.plotly_chart(graph, use_container_width=True)

# Show data table
with st.expander("Show Data Table"):
    st.dataframe(df)
