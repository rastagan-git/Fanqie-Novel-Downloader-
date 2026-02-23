import requests
from lxml import etree
import ast
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_cookies_via_selenium():
    """通过 Selenium 模拟登录并获取 Cookie"""
    print("\n" + "="*30)
    print("正在启动浏览器进行登录验证...")
    options = webdriver.ChromeOptions()
    # 如果你想保持登录状态，可以添加 user-data-dir 路径
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    driver.get("https://fanqienovel.com/")
    print("请在弹出的浏览器中完成登录（扫码或手机号）。")
    print("登录成功并跳转到首页后，请回到这里按回车键继续...")
    
    input("确认已登录成功？（按回车继续）")
    
    # 获取并格式化 Cookie
    selenium_cookies = driver.get_cookies()
    cookie_str = "; ".join([f"{c['name']}={c['value']}" for c in selenium_cookies])
    
    driver.quit()
    print("Cookie 获取成功！")
    print("="*30 + "\n")
    return cookie_str

def get_chapter_list(book_id, headers):
    """获取书籍的所有章节 ID 和 标题"""
    url = f"https://fanqienovel.com/page/{book_id}"
    try:
        response = requests.get(url, headers=headers)
        et = etree.HTML(response.text)
        links = et.xpath('//div[@class="chapter-item"]/a')
        chapters = []
        for link in links:
            href = link.get('href')
            title = link.text
            if href:
                cid = href.split('/')[-1]
                chapters.append((cid, title))
        return chapters
    except Exception as e:
        print(f"获取目录失败: {e}")
        return []

def spider_chapter(chapter_id, charmap_dic, headers):
    """抓取单章内容并解密"""
    url = f"https://fanqienovel.com/reader/{chapter_id}"
    try:
        # 使用传入的带有 Cookie 的 headers
        response = requests.get(url, headers=headers)
        et = etree.HTML(response.text)
        p_elements = et.xpath('//div[contains(@class, "muye-reader-content")]//p')
        article = "\n".join([p.text for p in p_elements if p.text])
        
        # 你的原有的解密逻辑
        if not os.path.exists(charmap_dic):
            return article # 如果没映射表就返回原样
            
        with open(charmap_dic, "r", encoding="utf-8") as f:
            dic = ast.literal_eval(f.read().strip())

        right_article = ""
        for letter in article:
            key = str(ord(letter)) + ".jpg"
            if key in dic:
                right_article += dic[key].strip()
            else:
                right_article += letter
        return right_article
    except:
        return ""

if __name__ == '__main__':
    book_id = input("请输入番茄小说【书籍ID】: ").strip()
    mapping_file = "./output/charmap_dic.txt"
    
    # 1. 先登录获取 Cookie
    my_cookie = get_cookies_via_selenium()
    
    # 2. 构造通用的 Headers
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "referer": "https://fanqienovel.com/",
        "cookie": my_cookie
    }
    
    if not os.path.exists(mapping_file):
        print(f"警告：找不到映射文件 {mapping_file}，内容可能保持加密状态。")
    
    print("正在获取完整目录...")
    chapters = get_chapter_list(book_id, headers)
    
    if not chapters:
        print("未能获取目录，请确认书籍 ID 是否正确或登录是否有效。")
    else:
        print(f"身份验证成功！共发现 {len(chapters)} 个章节，准备开始下载...")
        full_path = f"book_{book_id}.txt"
        
        with open(full_path, "w", encoding="utf-8") as f:
            for idx, (cid, title) in enumerate(chapters):
                print(f"正在下载第 {idx+1}/{len(chapters)} 章: {title}...")
                content = spider_chapter(cid, mapping_file, headers)
                
                f.write(f"\n\n### {title} ###\n\n")
                f.write(content)
                time.sleep(1) 
        
        print("-" * 30)
        print(f"整本书已下载完成！保存路径: {os.path.abspath(full_path)}")
