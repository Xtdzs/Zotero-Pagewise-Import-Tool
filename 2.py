import requests
import pyperclip
import re
import sys
import asyncio
from bs4 import BeautifulSoup

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def start():
    print("=====================================")
    print("Welcome to the Zotero Batch Import Tool!")
    print("Please select the export option:")
    print("1. Search Page > Import All Papers")
    print("2. Paper Details Page > Import All Citations")
    print("<Press e to exit>")
    print("=====================================")
    export_format = sys.stdin.readline().strip()
    return export_format


def search_page_import():
    print("-------------------------------------")
    print("Please select a database website to export (enter the number):")
    print("1. arXiv")
    print("2. X-MOL")
    print("3. PubMed")
    print("4. Nature")
    print("5. SciSpace (ensure Google Chrome version is 124 or higher.)")
    print("<Press r to return><Press e to exit the program>")
    print("-------------------------------------")
    export_format = sys.stdin.readline().strip()
    return export_format


async def get_arxiv_codes(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.URLRequired as e:
        print("Failed to retrieve arXiv numbers!")
        print(e)
        return []
    except requests.exceptions.Timeout as e:
        print("Failed to retrieve arXiv numbers!")
        print(e)
        return []
    except requests.exceptions.HTTPError as e:
        print("Failed to retrieve arXiv numbers!")
        print(e)
        return []
    except requests.exceptions.ConnectionError as e:
        print("Failed to retrieve arXiv numbers!")
        print(e)
        return []
    except requests.exceptions.RequestException as e:
        print("Failed to retrieve arXiv numbers!")
        print(e)
        return []
    print("arXiv numbers have been copied to the clipboard! (in the order they appear on the page)")
    arxiv_codes = re.findall(r'arXiv:(\d+\.\d+)', response.text)
    arxiv_codes = ['arXiv:' + arxiv_code for arxiv_code in arxiv_codes]
    return arxiv_codes


async def get_xmol_codes(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.URLRequired as e:
        print("Failed to retrieve DOI numbers!")
        print(e)
        return []
    except requests.exceptions.Timeout as e:
        print("Failed to retrieve DOI numbers!")
        print(e)
        return []
    except requests.exceptions.HTTPError as e:
        print("Failed to retrieve DOI numbers!")
        print(e)
        return []
    except requests.exceptions.ConnectionError as e:
        print("Failed to retrieve DOI numbers!")
        print(e)
        return []
    except requests.exceptions.RequestException as e:
        print("Failed to retrieve DOI numbers!")
        print(e)
        return []
    print("DOI numbers have been copied to the clipboard! (in the order they appear on the page)")
    # Find strings after "DOI:"
    xmol_codes = re.findall(r"DOI:(.*)", response.text)
    xmol_codes = [xmol_code for xmol_code in xmol_codes]
    return xmol_codes


async def get_pubmed_codes(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.URLRequired as e:
        print("Failed to retrieve PMID numbers!")
        print(e)
        return []
    except requests.exceptions.Timeout as e:
        print("Failed to retrieve PMID numbers!")
        print(e)
        return []
    except requests.exceptions.HTTPError as e:
        print("Failed to retrieve PMID numbers!")
        print(e)
        return []
    except requests.exceptions.ConnectionError as e:
        print("Failed to retrieve PMID numbers!")
        print(e)
        return []
    except requests.exceptions.RequestException as e:
        print("Failed to retrieve PMID numbers!")
        print(e)
        return []
    print("PMID numbers have been copied to the clipboard! (in the order they appear on the page)")
    pubmed_codes = re.findall(r"PMID: <span class=\"docsum-pmid\">(\d+)", response.text)
    pubmed_codes = [pubmed_code for pubmed_code in pubmed_codes]
    return pubmed_codes


async def get_nature_codes(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.URLRequired as e:
        print("Failed to retrieve DOI numbers!")
        print(e)
        return []
    except requests.exceptions.Timeout as e:
        print("Failed to retrieve DOI numbers!")
        print(e)
        return []
    except requests.exceptions.HTTPError as e:
        print("Failed to retrieve DOI numbers!")
        print(e)
        return []
    except requests.exceptions.ConnectionError as e:
        print("Failed to retrieve DOI numbers!")
        print(e)
        return []
    except requests.exceptions.RequestException as e:
        print("Failed to retrieve DOI numbers!")
        print(e)
        return []
    print("DOI numbers have been copied to the clipboard! (in the order they appear on the page)")
    nature_codes = re.findall(r'<a\s+href="(/articles/[a-zA-Z0-9\-]+)"', response.text)
    nature_codes = ["DOI:10.1038" + nature_code[9:] for nature_code in nature_codes]
    return nature_codes


def scroll_and_refresh(driver, scroll_pause_time, max_scrolls):
    last_height = driver.execute_script("return document.body.scrollHeight")
    scrolls = 0
    while scrolls < max_scrolls:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        scrolls += 1


async def get_SciSpace_codes(url, start, end):
    start = int(start)
    end = int(end)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--window-size=1920,1050")
    options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36')
    s = Service('chromedriver-win64-124/chromedriver.exe')
    driver = webdriver.Chrome(service=s, options=options)
    try:
        driver.get(url)
        paperNum = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//th[contains(text(),'Papers (')]"))
        )
        num = int(paperNum[0].text[-3:-1])

        patience = 3
        cnt = 0

        while num < end:
            # Scroll down and refresh page content
            scroll_and_refresh(driver, scroll_pause_time=1.5, max_scrolls=4)
            paperNum = WebDriverWait(driver, 10000).until(
                EC.presence_of_all_elements_located((By.XPATH, "//th[contains(text(),'Papers (')]"))
            )
            num1 = int(paperNum[0].text[-3:-1])
            if num1 <= num:
                cnt += 1
            else:
                cnt = 0
            num = num1

            if cnt >= patience:
                break

        if start > num:
            print(f"Warning: The page contains a maximum of {num} papers, unable to retrieve from paper {start}!")
            return 's<n'

        doi_elements = driver.find_elements(By.XPATH, "//a[contains(@href,'doi.org')]")
        dois = [element.get_attribute("href") for element in doi_elements]

        driver.quit()

        dois = dois[start - 1:min(num, end)]

        print("DOI numbers have been copied to the clipboard! (in page order)")
        if cnt >= patience:
            print(f"Warning: The page contains a maximum of {num} papers, unable to retrieve up to paper {end}!")
        return dois
    except:
        print("Scraping failed!")
        return []



def paper_page_import():
    print("-------------------------------------")
    print("Please select the database to export (enter the number):")
    print("1. ACS Publications")
    print("<Press r to return><Press e to exit>")
    print("-------------------------------------")
    export_format = sys.stdin.readline().strip()
    return export_format


async def get_acs_codes_cite(url):
    headers = {
        'authority': 'pubs.acs.org',
        'method': 'GET',
        'scheme': 'https',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'max-age=0',
        'Priority': 'u=0, i',
        'Sec-Ch-Ua': '"Chromium";v="124", "Microsoft Edge";v="124", "Not-A.Brand";v="99"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.URLRequired as e:
        print("Failed to retrieve DOI numbers!")
        print(e)
        return []
    except requests.exceptions.Timeout as e:
        print("Failed to retrieve DOI numbers!")
        print(e)
        return []
    except requests.exceptions.HTTPError as e:
        print("Failed to retrieve DOI numbers!")
        print(e)
        return []
    except requests.exceptions.ConnectionError as e:
        print("Failed to retrieve DOI numbers!")
        print(e)
        return []
    except requests.exceptions.RequestException as e:
        print("Failed to retrieve DOI numbers!")
        print(e)
        return []
    print("DOI numbers have been copied to the clipboard! (in the order they appear on the page)")
    soup = BeautifulSoup(response.content, 'html.parser')
    # cited_content = soup.find_all('div', class_='cited-content hlFld-Abstract')
    acs_codes = soup.find_all('li', class_='citedByEntry', attrs={'data-doi': True})
    acs_codes = [code['data-doi'] for code in acs_codes]
    return acs_codes


export_format = start()
while True:
    if export_format == '1':
        website_idx = search_page_import()
        if website_idx == 'r' or website_idx == 'R':
            export_format = start()
            continue
        elif website_idx == 'e' or website_idx == 'E':
            break
        else:
            while True:
                if website_idx == '1':
                    print("Please open the search results page of arXiv in your browser, then copy and paste the URL here:")
                    url = sys.stdin.readline().strip()
                    print("Fetching arXiv numbers, please wait...")
                    arxiv_codes = asyncio.run(get_arxiv_codes(url))
                    arxiv_codes = '\n'.join(arxiv_codes)
                    pyperclip.copy(arxiv_codes)
                    print("<Press any key to continue><Press r to return>")
                    inp = sys.stdin.readline().strip()
                    if inp == 'r' or inp == 'R':
                        website_idx = search_page_import()
                        continue
                    else:
                        continue
                elif website_idx == '2':
                    print("Please open the search results page of X-MOL in your browser, then copy and paste the URL here:")
                    url = sys.stdin.readline().strip()
                    print("Fetching DOI numbers, please wait...")
                    xmol_codes = asyncio.run(get_xmol_codes(url))
                    xmol_codes = '\n'.join(xmol_codes)
                    pyperclip.copy(xmol_codes)
                    print("<Press any key to continue><Press r to return>")
                    inp = sys.stdin.readline().strip()
                    if inp == 'r' or inp == 'R':
                        website_idx = search_page_import()
                        continue
                    else:
                        continue
                elif website_idx == '3':
                    print("Please open the search results page of PubMed in your browser, then copy and paste the URL here:")
                    url = sys.stdin.readline().strip()
                    print("Fetching PMID numbers, please wait...")
                    pubmed_codes = asyncio.run(get_pubmed_codes(url))
                    pubmed_codes = '\n'.join(pubmed_codes)
                    pyperclip.copy(pubmed_codes)
                    print("<Press any key to continue><Press r to return>")
                    inp = sys.stdin.readline().strip()
                    if inp == 'r' or inp == 'R':
                        website_idx = search_page_import()
                        continue
                    else:
                        continue
                elif website_idx == '4':
                    print("Please open the search results page of Nature in your browser, then copy and paste the URL here:")
                    url = sys.stdin.readline().strip()
                    print("Fetching DOI numbers, please wait...")
                    nature_codes = asyncio.run(get_nature_codes(url))
                    nature_codes = '\n'.join(nature_codes)
                    pyperclip.copy(nature_codes)
                    print("<Press any key to continue><Press r to return>")
                    inp = sys.stdin.readline().strip()
                    if inp == 'r' or inp == 'R':
                        website_idx = search_page_import()
                        continue
                    else:
                        continue
                elif website_idx == '5':
                    print("Please open the SciSpace search results page in your browser, then copy and paste the URL here:")
                    url = sys.stdin.readline().strip()
                    print("Please provide the DOI range of the papers to export (enter numbers):")
                    print("Start (from which paper):")
                    start = sys.stdin.readline().strip()
                    print("End (to which paper):")
                    end = sys.stdin.readline().strip()
                    if int(start) > int(end):
                        print("The start paper cannot be after the end paper!")
                        continue
                    print("Retrieving DOI numbers, please wait...")
                    SciSpace_codes = asyncio.run(get_SciSpace_codes(url, start, end))
                    if SciSpace_codes == 's<n':
                        continue
                    SciSpace_codes = '\n'.join(SciSpace_codes)
                    pyperclip.copy(SciSpace_codes)
                    print("<Press any key to continue><Press r to return>")
                    inp = sys.stdin.readline().strip()
                    if inp.lower() == 'r':
                        website_idx = search_page_import()
                        continue
                    else:
                        continue
                elif website_idx == 'e' or website_idx == 'E':
                    print("Exiting the program...")
                    break
                elif website_idx == 'r' or website_idx == 'R':
                    export_format = start()
                    break
                else:
                    print("Invalid input!")
                    website_idx = search_page_import()
                    continue
    elif export_format == '2':
        website_idx = paper_page_import()
        if website_idx == 'r' or website_idx == 'R':
            export_format = start()
            continue
        elif website_idx == 'e' or website_idx == 'E':
            break
        else:
            while True:
                if website_idx == '1':
                    print("Please open the details page of ACS Publications paper in your browser, then copy and paste the URL here:")
                    url = sys.stdin.readline().strip()
                    print("Fetching DOI numbers, please wait...")
                    acs_codes = asyncio.run(get_acs_codes_cite(url))
                    acs_codes = '\n'.join(acs_codes)
                    pyperclip.copy(acs_codes)
                    print("<Press any key to continue><Press r to return>")
                    inp = sys.stdin.readline().strip()
                    if inp == 'r' or inp == 'R':
                        website_idx = paper_page_import()
                        continue
                    else:
                        continue
                elif website_idx == 'e' or website_idx == 'E':
                    print("Exiting the program...")
                    break
                elif website_idx == 'r' or website_idx == 'R':
                    export_format = start()
                    break
                else:
                    print("Invalid input!")
                    website_idx = paper_page_import()
                    continue
    elif export_format == 'e' or export_format == 'E':
        print("Exiting the program...")
        break

print("Program has exited!")
