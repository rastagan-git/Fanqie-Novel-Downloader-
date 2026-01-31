import requests
from lxml import etree
import ast
import os
import time

def get_chapter_list(book_id):
    """获取书籍的所有章节 ID 和 标题"""
    url = f"https://fanqienovel.com/page/{book_id}"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        et = etree.HTML(response.text)
        # 获取目录中的章节链接和标题
        links = et.xpath('//div[@class="chapter-item"]/a')
        chapters = []
        for link in links:
            href = link.get('href') # 格式通常为 /reader/12345
            title = link.text
            if href:
                cid = href.split('/')[-1]
                chapters.append((cid, title))
        return chapters
    except Exception as e:
        print(f"获取目录失败: {e}")
        return []

def spider_chapter(chapter_id, charmap_dic):
    """抓取单章内容并解密"""
    url = f"https://fanqienovel.com/reader/{chapter_id}"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "referer": "https://fanqienovel.com/"
    }
    try:
        response = requests.get(url, headers=headers)
        et = etree.HTML(response.text)
        p_elements = et.xpath('//div[contains(@class, "muye-reader-content")]//p')
        article = "\n".join([p.text for p in p_elements if p.text])
        
        # 解码逻辑
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
    book_id = input("请输入番茄小说【书籍ID】(如 7076047336530510370): ").strip()
    mapping_file = "./output/charmap_dic.txt"
    
    if not os.path.exists(mapping_file):
        print(f"致命错误：找不到映射文件 {mapping_file}")
    else:
        print("正在获取目录...")
        chapters = get_chapter_list(book_id)
        
        if not chapters:
            print("未能获取目录，请确认书籍 ID 是否正确。")
        else:
            print(f"共发现 {len(chapters)} 个章节，准备开始下载...")
            full_path = f"book_{book_id}.txt"
            
            with open(full_path, "w", encoding="utf-8") as f:
                for idx, (cid, title) in enumerate(chapters):
                    print(f"正在下载第 {idx+1}/{len(chapters)} 章: {title}...")
                    content = spider_chapter(cid, mapping_file)
                    
                    f.write(f"\n\n### {title} ###\n\n")
                    f.write(content)
                    
                    # 适当暂停，防止被封 IP
                    time.sleep(1) 
            
            print("-" * 30)
            print(f"整本书已下载完成！保存路径: {os.path.abspath(full_path)}")