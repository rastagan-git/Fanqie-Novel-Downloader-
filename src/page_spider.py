import requests

novel_name = "惊鸿"

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "priority": "u=1, i",
    "referer": f"https://fanqienovel.com/search/{novel_name}",
    "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}
url = "https://fanqienovel.com/api/author/search/search_book/v1"
params = {
    "filter": "127,127,127,127",
    "page_count": "10",
    "page_index": "0",
    "query_type": "0",
    "query_word": novel_name,
    "msToken": "1g8XjSvBgdT591KVZfXORgdVYKBq7YIx30uIkfL_SKd9Ks0leybEPt8_Isqb1ZmvLoHO5oFMQpyYJvMi7i-4YwPMDLu0xEI-AwhORz5u5t2VJ9AD7YPhgA==",  # 待解密
    "a_bogus": "Yy0mkOZVMsm1UjvGJXkz9Hkmadg0YW53gZEzEMjyG0L5"  # 待解密
}
response = requests.get(url, headers=headers, params=params)

print(response.text)
print(response)