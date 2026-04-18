from langchain.tools import tool
import requests

from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
load_dotenv()

tavily=TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))




#####################################################################################3
@tool
def web_search(query:str) ->str:
    '''Search thee web for recent and reliable information on topics.Returns titles, URLs and snippets.'''
    results=tavily.search(query=query, num_results=5, language="en")

    out=[]

    for r in results['results']:
        out.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
            )
    return '\n-------\n'.join(out)




#####################################################################################33
@tool
def scrape_url(url:str) ->str :
    '''scrape and return clean text content from a given URL for deeper reading'''  
    try:
        resp=requests.get(url, timeout=20,headers={'User-Agent':'Mozilla/5.0'})
        soup=BeautifulSoup(resp.text,'html.parser')
        for tag in soup(['script','style','footer','nav']):
            tag.decompose()
        return soup.get_text(separator=' ', strip=True)[:3000]
    except Exception as e:
        return f"Error scraping {url}: {str(e)}"
        





