import requests
import pyperclip
import re
import sys
import asyncio
from bs4 import BeautifulSoup

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def start():
    print("=====================================")
    print("欢迎使用zotero批量导入工具！")
    print("请选择导出功能：")
    print("1. 文献检索页>所有论文一键导入")
    print("2. 文献详情页>所有引文一键导入")
    print("<按e退出程序>")
    print("=====================================")
    export_format = sys.stdin.readline().strip()
    return export_format


def search_page_import():
    print("-------------------------------------")
    print("请选择导出数据库网站（输入序号）：")
    print("1. arXiv")
    print("2. X-MOL")
    print("3. PubMed")
    print("4. Nature")
    print("5. SciSpace（确保谷歌浏览器版本大于等于124.）")
    print("<按r返回><按e退出程序>")
    print("-------------------------------------")
    export_format = sys.stdin.readline().strip()
    return export_format


async def get_arxiv_codes(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.URLRequired as e:
        print("获取arxiv编号失败！")
        print(e)
        return []
    except requests.exceptions.Timeout as e:
        print("获取arxiv编号失败！")
        print(e)
        return []
    except requests.exceptions.HTTPError as e:
        print("获取arxiv编号失败！")
        print(e)
        return []
    except requests.exceptions.ConnectionError as e:
        print("获取arxiv编号失败！")
        print(e)
        return []
    except requests.exceptions.RequestException as e:
        print("获取arxiv编号失败！")
        print(e)
        return []
    print("已将arxiv编号复制到剪切板！（按照页面顺序）")
    arxiv_codes = re.findall(r'arXiv:(\d+\.\d+)', response.text)
    arxiv_codes = ['arXiv:' + arxiv_code for arxiv_code in arxiv_codes]
    return arxiv_codes


async def get_xmol_codes(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.URLRequired as e:
        print("获取DOI编号失败！")
        print(e)
        return []
    except requests.exceptions.Timeout as e:
        print("获取DOI编号失败！")
        print(e)
        return []
    except requests.exceptions.HTTPError as e:
        print("获取DOI编号失败！")
        print(e)
        return []
    except requests.exceptions.ConnectionError as e:
        print("获取DOI编号失败！")
        print(e)
        return []
    except requests.exceptions.RequestException as e:
        print("获取DOI编号失败！")
        print(e)
        return []
    print("已将DOI编号复制到剪切板！（按照页面顺序）")
    # 找DOI:后面的字符串（没有10也同样找）
    xmol_codes = re.findall(r"DOI:(.*)", response.text)
    xmol_codes = [xmol_code for xmol_code in xmol_codes]
    return xmol_codes


async def get_pubmed_codes(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.URLRequired as e:
        print("获取PMID编号失败！")
        print(e)
        return []
    except requests.exceptions.Timeout as e:
        print("获取PMID编号失败！")
        print(e)
        return []
    except requests.exceptions.HTTPError as e:
        print("获取PMID编号失败！")
        print(e)
        return []
    except requests.exceptions.ConnectionError as e:
        print("获取PMID编号失败！")
        print(e)
        return []
    except requests.exceptions.RequestException as e:
        print("获取PMID编号失败！")
        print(e)
        return []
    print("已将PMID编号复制到剪切板！（按照页面顺序）")
    pubmed_codes = re.findall(r"PMID: <span class=\"docsum-pmid\">(\d+)", response.text)
    pubmed_codes = [pubmed_code for pubmed_code in pubmed_codes]
    return pubmed_codes


async def get_nature_codes(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.URLRequired as e:
        print("获取DOI编号失败！")
        print(e)
        return []
    except requests.exceptions.Timeout as e:
        print("获取DOI编号失败！")
        print(e)
        return []
    except requests.exceptions.HTTPError as e:
        print("获取DOI编号失败！")
        print(e)
        return []
    except requests.exceptions.ConnectionError as e:
        print("获取DOI编号失败！")
        print(e)
        return []
    except requests.exceptions.RequestException as e:
        print("获取DOI编号失败！")
        print(e)
        return []
    print("已将DOI编号复制到剪切板！（按照页面顺序）")
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
        paperNum = WebDriverWait(driver, 10000).until(
            EC.presence_of_all_elements_located((By.XPATH, "//th[contains(text(),'Papers (')]"))
        )
        num = int(paperNum[0].text[-3:-1])

        patience = 3
        cnt = 0

        while num < end:
            # 下滑并刷新页面内容
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
            print(f"warning：页面论文数最多仅有{num}篇，无法从第{start}篇获取！")
            return 's<n'

        doi_elements = driver.find_elements(By.XPATH, "//a[contains(@href,'doi.org')]")
        dois = [element.get_attribute("href") for element in doi_elements]

        driver.quit()

        dois = dois[start - 1:min(num, end)]

        print("已将DOI编号复制到剪切板！（按照页面顺序）")
        if cnt >= patience:
            print(f"warning：页面论文数最多仅有{num}篇，无法获取到第{end}篇！")
        return dois
    except:
        print("爬取失败！")
        return []


def paper_page_import():
    print("-------------------------------------")
    print("请选择导出数据库网站（输入序号）：")
    print("1. ACS Publications")
    print("<按r返回><按e退出程序>")
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
        print("获取DOI编号失败！")
        print(e)
        return []
    except requests.exceptions.Timeout as e:
        print("获取DOI编号失败！")
        print(e)
        return []
    except requests.exceptions.HTTPError as e:
        print("获取DOI编号失败！")
        print(e)
        return []
    except requests.exceptions.ConnectionError as e:
        print("获取DOI编号失败！")
        print(e)
        return []
    except requests.exceptions.RequestException as e:
        print("获取DOI编号失败！")
        print(e)
        return []
    print("已将DOI编号复制到剪切板！（按照页面顺序）")
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
                    print("请在浏览器中打开arxiv的搜索结果页面，然后复制URL粘贴到此处：")
                    url = sys.stdin.readline().strip()
                    print("正在获取arxiv编号，请稍等...")
                    arxiv_codes = asyncio.run(get_arxiv_codes(url))
                    arxiv_codes = '\n'.join(arxiv_codes)
                    pyperclip.copy(arxiv_codes)
                    print("<按任意键继续><按r返回>")
                    inp = sys.stdin.readline().strip()
                    if inp == 'r' or inp == 'R':
                        website_idx = search_page_import()
                        continue
                    else:
                        continue
                elif website_idx == '2':
                    print("请在浏览器中打开X-MOL的搜索结果页面，然后复制URL粘贴到此处：")
                    url = sys.stdin.readline().strip()
                    print("正在获取DOI编号，请稍等...")
                    xmol_codes = asyncio.run(get_xmol_codes(url))
                    xmol_codes = '\n'.join(xmol_codes)
                    pyperclip.copy(xmol_codes)
                    print("<按任意键继续><按r返回>")
                    inp = sys.stdin.readline().strip()
                    if inp == 'r' or inp == 'R':
                        website_idx = search_page_import()
                        continue
                    else:
                        continue
                elif website_idx == '3':
                    print("请在浏览器中打开PubMed的搜索结果页面，然后复制URL粘贴到此处：")
                    url = sys.stdin.readline().strip()
                    print("正在获取PMID编号，请稍等...")
                    pubmed_codes = asyncio.run(get_pubmed_codes(url))
                    pubmed_codes = '\n'.join(pubmed_codes)
                    pyperclip.copy(pubmed_codes)
                    print("<按任意键继续><按r返回>")
                    inp = sys.stdin.readline().strip()
                    if inp == 'r' or inp == 'R':
                        website_idx = search_page_import()
                        continue
                    else:
                        continue
                elif website_idx == '4':
                    print("请在浏览器中打开Nature的搜索结果页面，然后复制URL粘贴到此处：")
                    url = sys.stdin.readline().strip()
                    print("正在获取DOI编号，请稍等...")
                    nature_codes = asyncio.run(get_nature_codes(url))
                    nature_codes = '\n'.join(nature_codes)
                    pyperclip.copy(nature_codes)
                    print("<按任意键继续><按r返回>")
                    inp = sys.stdin.readline().strip()
                    if inp == 'r' or inp == 'R':
                        website_idx = search_page_import()
                        continue
                    else:
                        continue
                elif website_idx == '5':
                    print("请在浏览器中打开SciSpace的搜索结果页面，然后复制URL粘贴到此处：")
                    url = sys.stdin.readline().strip()
                    print("请给出需导出论文的DOI范围（输入数字）：")
                    print("开始（从第几篇开始）：")
                    start = sys.stdin.readline().strip()
                    print("结束（从第几篇结束）：")
                    end = sys.stdin.readline().strip()
                    if start > end:
                        print("开始篇不能在结束篇之后！")
                        continue
                    print("正在获取DOI编号，请稍等...")
                    SciSpace_codes = asyncio.run(get_SciSpace_codes(url, start, end))
                    if SciSpace_codes == 's<n':
                        continue
                    SciSpace_codes = '\n'.join(SciSpace_codes)
                    pyperclip.copy(SciSpace_codes)
                    print("<按任意键继续><按r返回>")
                    inp = sys.stdin.readline().strip()
                    if inp == 'r' or inp == 'R':
                        website_idx = search_page_import()
                        continue
                    else:
                        continue
                elif website_idx == 'e' or website_idx == 'E':
                    print("程序正在退出...")
                    break
                elif website_idx == 'r' or website_idx == 'R':
                    export_format = start()
                    break
                else:
                    print("输入错误！")
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
                    print("请在浏览器中打开ACS Publications论文的详情页，然后复制URL粘贴到此处：")
                    url = sys.stdin.readline().strip()
                    print("正在获取DOI编号，请稍等...")
                    acs_codes = asyncio.run(get_acs_codes_cite(url))
                    acs_codes = '\n'.join(acs_codes)
                    pyperclip.copy(acs_codes)
                    print("<按任意键继续><按r返回>")
                    inp = sys.stdin.readline().strip()
                    if inp == 'r' or inp == 'R':
                        website_idx = paper_page_import()
                        continue
                    else:
                        continue
                elif website_idx == 'e' or website_idx == 'E':
                    print("程序正在退出...")
                    break
                elif website_idx == 'r' or website_idx == 'R':
                    export_format = start()
                    break
                else:
                    print("输入错误！")
                    website_idx = paper_page_import()
                    continue
    elif export_format == 'e' or export_format == 'E':
        print("程序正在退出...")
        break

print("程序已退出！")