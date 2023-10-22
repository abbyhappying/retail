import streamlit as st
import streamlit as st
from langchain.llms import OpenAI
from snowflake.snowpark import Session
from snowflake.connector import connect  # Import the necessary module
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
from sqlalchemy.dialects import registry
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from snowflake.sqlalchemy import URL
import pandas as pd
from ast import literal_eval
import re
import os

st.title('🦜🔗 LongChain Agents')
registry.load("snowflake")
registry.register('snowflake', 'snowflake.sqlalchemy', 'dialect')

# connected with snowflake database retail
user = st.secrets.connections.snowpark.user
role = st.secrets.connections.snowpark.role
password = st.secrets.connections.snowpark.password
warehouse = st.secrets.connections.snowpark.warehouse
account = st.secrets.connections.snowpark.account
database = st.secrets.connections.snowpark.database
schema = st.secrets.connections.snowpark.schema
conn_string = f"snowflake://{user}:{password}@{account}/{database}/{schema}?warehouse={warehouse}&role_name={role}"
db = SQLDatabase.from_uri(conn_string)

# @st.cache_resource
# def create_session():
#     return Session.builder.configs(st.secrets.connections.snowpark).create()

# session = create_session()
# st.success("Connected to Snowflake!")


llm = OpenAI(api_key=st.secrets.openai_api_key,temperature=0, verbose=True)
openai_api_key = st.secrets.openai_api_key


#generate longchain sql agent to interact with the snowflake database
agent_executor = create_sql_agent(
    llm=OpenAI(temperature=0),
    toolkit=SQLDatabaseToolkit(db=db, llm=OpenAI(temperature=0)),
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    return_intermediate_steps=True
)

# agent_executor.run("how was the number of total orders")
# agent_executor.run("how was the top 3 selling products")
