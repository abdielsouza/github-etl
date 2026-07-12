import streamlit as st
import altair as alt

from github_etl.warehouse import Warehouse

warehouse = Warehouse("data/warehouse.duckdb")

st.set_page_config(
    page_title="Github ETL",
    layout="wide",
)

df = warehouse.query("SELECT * FROM repositories")

st.title("Github ETL Dashboard")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Repositories", len(df))
c2.metric("Stars", int(df["stars"].sum()))
c3.metric("Languages", df["language"].n_unique())
c4.metric("Biggest Star Count", str(df["stars"].max()))

st.dataframe(df, use_container_width=True)

top_repos = df.sort("stars", descending=True).head(20).select("name", "stars")
top_repos_chart = (
    alt.Chart(top_repos.to_pandas())
    .mark_bar()
    .encode(
        x=alt.X("stars:Q"),
        y=alt.Y("name:N", sort="-x"),
    )
)

st.subheader("Top 20 repositories by stars")
st.altair_chart(top_repos_chart, use_container_width=True)

languages = df.drop_nulls("language").group_by("language").len().sort("len", descending=True)
languages_chart = (
    alt.Chart(languages.to_pandas())
    .mark_bar()
    .encode(
        x=alt.X("len:Q"),
        y=alt.Y("language:N", sort="-x"),
    )
)

st.subheader("Languages")
st.altair_chart(languages_chart, use_container_width=True)