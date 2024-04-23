import requests
import pyperclip
import re
import sys
import asyncio

def start():
    print("=====================================")
    print("欢迎使用zotero批量导入工具！")
    print("请选择导出数据库网站（输入序号）：")
    print("1. arXiv")
    print("2. X-MOL")
    print("3. PubMed")
    print("（按e退出程序）")
    print("=====================================")
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

def get_pubmed_codes(url):
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

export_format = start()
while True:
    if export_format == '1':
        print("请在浏览器中打开arxiv的搜索结果页面，然后复制URL粘贴到此处：")
        url = sys.stdin.readline().strip()
        print("正在获取arxiv编号，请稍等...")
        arxiv_codes = asyncio.run(get_arxiv_codes(url))
        arxiv_codes = '\n'.join(arxiv_codes)
        pyperclip.copy(arxiv_codes)
        print("（按r返回）")
        inp = sys.stdin.readline().strip()
        if inp == 'r' or inp == 'R':
            export_format = start()
            continue
        else:
            continue
    elif export_format == '2':
        print("请在浏览器中打开X-MOL的搜索结果页面，然后复制URL粘贴到此处：")
        url = sys.stdin.readline().strip()
        print("正在获取DOI编号，请稍等...")
        xmol_codes = asyncio.run(get_xmol_codes(url))
        xmol_codes = '\n'.join(xmol_codes)
        pyperclip.copy(xmol_codes)
        print("（按r返回）")
        inp = sys.stdin.readline().strip()
        if inp == 'r' or inp == 'R':
            export_format = start()
            continue
        else:
            continue
    elif export_format == '3':
        print("请在浏览器中打开PubMed的搜索结果页面，然后复制URL粘贴到此处：")
        url = sys.stdin.readline().strip()
        print("正在获取PMID编号，请稍等...")
        pubmed_codes = get_pubmed_codes(url)
        pubmed_codes = '\n'.join(pubmed_codes)
        pyperclip.copy(pubmed_codes)
        print("（按r返回）")
        inp = sys.stdin.readline().strip()
        if inp == 'r' or inp == 'R':
            export_format = start()
            continue
        else:
            continue
    elif export_format == 'e' or export_format == 'E':
        print("程序正在退出...")
        break
    else:
        print("输入错误！")
        export_format = start()