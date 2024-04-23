import requests
import pyperclip
import re
import sys
import asyncio

def start():
    print("====================================================")
    print("Welcome to the Zotero Batch Import Tool!")
    print("Please select the export format (enter the number):")
    print("1. arXiv")
    print("2. X-MOL")
    print("3. PubMed")
    print("(Press 'e' to exit the program)")
    print("====================================================")
    export_format = sys.stdin.readline().strip()
    return export_format

async def get_arxiv_codes(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Failed to retrieve arXiv codes!")
        print(e)
        return []
    print("arXiv codes copied to clipboard! (In page order)")
    arxiv_codes = re.findall(r'arXiv:(\d+\.\d+)', response.text)
    arxiv_codes = ['arXiv:' + arxiv_code for arxiv_code in arxiv_codes]
    return arxiv_codes

async def get_xmol_codes(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Failed to retrieve DOI codes!")
        print(e)
        return []
    print("DOI codes copied to clipboard! (In page order)")
    xmol_codes = re.findall(r"DOI:(.*)", response.text)
    xmol_codes = [xmol_code for xmol_code in xmol_codes]
    return xmol_codes

def get_pubmed_codes(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Failed to retrieve PMID codes!")
        print(e)
        return []
    print("PMID codes copied to clipboard! (In page order)")
    pubmed_codes = re.findall(r"PMID: <span class=\"docsum-pmid\">(\d+)", response.text)
    pubmed_codes = [pubmed_code for pubmed_code in pubmed_codes]
    return pubmed_codes

export_format = start()
while True:
    if export_format == '1':
        print("Please open the arXiv search results page in your browser, then copy and paste the URL here:")
        url = sys.stdin.readline().strip()
        print("Retrieving arXiv codes, please wait...")
        arxiv_codes = asyncio.run(get_arxiv_codes(url))
        arxiv_codes = '\n'.join(arxiv_codes)
        pyperclip.copy(arxiv_codes)
        print("(Press 'r' to return)")
        inp = sys.stdin.readline().strip()
        if inp.lower() == 'r':
            export_format = start()
            continue
        else:
            continue
    elif export_format == '2':
        print("Please open the X-MOL search results page in your browser, then copy and paste the URL here:")
        url = sys.stdin.readline().strip()
        print("Retrieving DOI codes, please wait...")
        xmol_codes = asyncio.run(get_xmol_codes(url))
        xmol_codes = '\n'.join(xmol_codes)
        pyperclip.copy(xmol_codes)
        print("(Press 'r' to return)")
        inp = sys.stdin.readline().strip()
        if inp.lower() == 'r':
            export_format = start()
            continue
        else:
            continue
    elif export_format == '3':
        print("Please open the PubMed search results page in your browser, then copy and paste the URL here:")
        url = sys.stdin.readline().strip()
        print("Retrieving PMID codes, please wait...")
        pubmed_codes = get_pubmed_codes(url)
        pubmed_codes = '\n'.join(pubmed_codes)
        pyperclip.copy(pubmed_codes)
        print("(Press 'r' to return)")
        inp = sys.stdin.readline().strip()
        if inp.lower() == 'r':
            export_format = start()
            continue
        else:
            continue
    elif export_format.lower() == 'e':
        print("Exiting the program...")
        break
    else:
        print("Invalid input!")
        export_format = start()