<h1 align="center">Github ETL Pipeline</h1>

<p align="center">
A project for data science made by Abdiel Souza.
</p>

---

## What it does?

This ETL pipeline extracts data from Github repositories and stores it in a database. The stored data is transformed into many different metrics and displayed in a Streamlit dashboard.

## Tech stack:

- **Programming Language**: Python
- **Data Extraction**: Httpx
- **Data Processing**: Polars
- **Data Storage**: DuckDB
- **Data Presentation**: Streamlit
- **Data Streaming/Pipeline**: Aiostream
- **CLI**: Typer/Rich
- **Project Manager**: UV

## How to configure it

To configure the pipeline, you need to create an `etl.toml` file inside a folder called `config` at the project root.

Place the following content in the file:

```toml
[github]
token = "your_github_token_here"
users = [
    # github usernames...
]
orgs = [
    # github organizations...
]
repos = [
    # github repositories...
]

[database]
path = "data/warehouse.duckdb"

[pipeline]
batch_size = 100 # this section is optional and out of use
```

Based on this config file, the code will extract repositories either by their own names or usernames and orgs. A Github token is required to make it work.

## How to run

To test this project on your own machine, you need to run the following commands in sequence:

```bash
# create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# install the requirements
pip install -r requirements.txt

# run the pipeline
python -m github_etl.cli
```