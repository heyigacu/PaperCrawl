import requests
from bs4 import BeautifulSoup
import re

def search_paper(title):
    print(title)
    search_url = 'https://pubmed.ncbi.nlm.nih.gov/'
    params = {'term': title}
    response = requests.get(search_url, params=params)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        li_all = soup.find_all('a')
        for li in li_all:
            if li.has_key('class') and li.has_key('data-article-id'):
                if 'docsum-title' in li['class']:
                    print(li['data-article-id'])
                    return li['data-article-id']
            else:
                meta_all = soup.find_all('meta')
                for meta in meta_all:
                    if meta:
                        name = meta.get('name')
                        if name == 'keywords':
                            content = meta.get('content')
                            return content.split(',')[0].split(':')[1]



def download_nbib(pmid, file_name):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        'db': 'pubmed',          
        'id': pmid,              
        'retmode': 'text',      
        'rettype': 'medline'     
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        text_content = response.text
        with open(f"{file_name}_{pmid}.nbib", "w") as file:
            file.write(text_content)
        print(f"file saved as {file_name}_{pmid}.nbib")
    else:
        print(f"request faliedly: {response.status_code}")

def single_scratch(title = "Imaging of cervical lymph nodes in head and neck cancer: the basics",
    savename = '1',
    ):
    article_id = search_paper(title)
    if article_id:
        download_nbib(article_id, savename)
    else:
        print("Paper not found.")


def batch_scratch_from_list(input_path):
    lines = open(input_path, 'r').readlines()
    titles = [line.strip() for line in lines]
    for i,title in enumerate(titles):
        if title is None or title =='':
            continue
        single_scratch(title, str(i+1))

if __name__ == "__main__":
    # single_scratch()
    batch_scratch_from_list('input_titles.txt')
