import streamlit as st
import altair as alt
import asyncio
import os
from dotenv import load_dotenv
from pathlib import Path

from github_etl.warehouse import Warehouse
from github_etl.stores import DuckDBStore, PostgresStore
from github_etl.cli import scan_async

st.set_page_config(
    page_title="Github ETL",
    layout="wide",
)

@st.cache_resource
def create_store():
    load_dotenv()

    if os.getenv("RUNNING_MODE") == "prod":
        return PostgresStore(
            user=os.environ["POSTGRES_DB_USER"],
            dbname=os.environ["POSTGRES_DB_NAME"],
            host=os.environ["POSTGRES_DB_HOST"],
            password=os.environ["POSTGRES_DB_PASSWORD"],
            port=os.environ["POSTGRES_DB_PORT"]
        )

    return DuckDBStore(Path("data/warehouse.duckdb"))

async def retrieve_data():
    warehouse = Warehouse(create_store()) # receives a RepositoryStore instance
    return await warehouse.query("repositories", "SELECT * FROM repositories")

df = asyncio.run(retrieve_data())

with st.sidebar:
    st.header("Update Data")

    repos = st.text_area("Repositories", placeholder="owner/repo\nowner/repo")
    users = st.text_area("Users", placeholder="torvalds\nguido")
    orgs = st.text_area("Organizations", placeholder="microsoft\npython")

    update_btn = st.button("Run Pipeline")

    if update_btn:
        repo_list = [r.strip() for r in repos.splitlines() if r.strip()]
        user_list = [u.strip() for u in users.splitlines() if u.strip()]
        org_list = [o.strip() for o in orgs.splitlines() if o.strip()]

        with st.spinner("Updating..."):
            try:
                asyncio.run(scan_async(users=user_list, repos=repo_list, orgs=org_list))
                st.success("Atualização concluída")
            except:
                st.error("Atualização falhou! Tente novamente.")

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
