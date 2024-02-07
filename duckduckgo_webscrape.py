## TODO: create a similarity search between the description and company's feature list

# Web scrapping
from bs4 import BeautifulSoup
import requests

# openAI
from openai import ChatCompletion
import openai

# retrieve .env
from dotenv import load_dotenv
import os

# Web Search
from langchain_community.tools import DuckDuckGoSearchRun, DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper


# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OpenAI API key not found. Please set it in the .env file.")

wrapper = DuckDuckGoSearchAPIWrapper(region="de-de", time="d", max_results=2)
search = DuckDuckGoSearchResults(api_wrapper=wrapper, source="news")
result = search.run("Obama")
print(result)
