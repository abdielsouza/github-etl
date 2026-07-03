import streamlit as st
from github_etl.warehouse import Warehouse
from github_etl.analytics import *

warehouse = Warehouse("data/warehouse.duckdb")
repos = RepositoryAnalytics(warehouse)
languages = LanguageAnalytics(warehouse)
overview = OverviewAnalytics(warehouse)

st.metric("Repositories", overview.summary()["repositories"][0])
st.bar_chart(languages.distribution(), x="language", y="stars")
st.dataframe(repos.top_starred())