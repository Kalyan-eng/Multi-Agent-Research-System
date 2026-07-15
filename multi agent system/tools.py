from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print
load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
api_key = os.getenv("GOOGLE_API_KEY")

@tool
def web_search(query:str) -> str :
    """Search the web for recent and a reliable information on a topic . Return Titles , URLs and snippets"""
    result = tavily.search(query=query,max_results=4)
    out = []
     
    for r in result ['results'] :
        out.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'] [:300] }\n"
        )

    return"\n\----\n".join(out)

@tool
def scrape_url(url:str) -> str :
    """Scrape and return clean text content from the given url  for deeper reading."""
    try :
        resp= requests.get(url,timeout=8,headers={"User_agent":"Mozilla/5.0"})
        soup=BeautifulSoup(resp.text,"html.parser")
        for tag in soup (["script","style","nav","footer"]) :
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e :
        return f"could not able to scrap URL : {str(e)}"
