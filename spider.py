import requests
from urllib.parse import urlencode
from requests.exceptions import RequestException
import json
from find_url import ip_list
import random
import re
import codecs
import pymongo
import  os
from hashlib import md5
from multiprocessing import Pool

client=pymongo.MongoClient('localhost',27017)
toutiao=client['toutiao']
jiepai=toutiao['jiepai']


def set_header():
    header={
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'cookie':'tt_webid=6589804057601443341; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6589804057601443341; UM_distinctid=1653be708df1f7-0d7545fea73e11-3467790a-13c680-1653be708e03fe; CNZZDATA1259612802=92891570-1534307387-https%253A%252F%252Fwww.baidu.com%252F%7C1534307387; __tasessionId=kh4xyj34q1534308321715; csrftoken=f7569ab0e5f2af9e8208af05a4b5e4a9; sso_login_status=0'
    }
    return header
def set_ip():
    ip=random.choice(ip_list)
    print(ip)
    return ip

def get_page_index(offset,keyword):
    header=set_header()
    proxy={
        'http':set_ip()
    }
    data={
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': 3,
        'from': 'search_tab'
    }
    url='https://www.toutiao.com/search_content/?'+urlencode(data)
    test_url='http://bj.58.com/'
    try:
        response=requests.get(url,headers=header,proxies=proxy)
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        print('bad request')
        return None

def parse_page_index(html):
    if html!=None:
        html_json=json.loads(html)
        return html_json
    else:
        return None

def show_content(html_json):
    print(type(html_json))
    for url in html_json:
        print(url)

def get_page_url(wb_data):
    index=0
    if wb_data and 'data' in wb_data.keys():
        for item in wb_data.get('data'):
            # print(item)
            index+=1
            yield {
                'index':index,
                'img_url':item.get('article_url'),
                'title':item.get('title')
            }

def get_imgage_page(url):
    print(url)
    header=set_header()
    proxy={
        'https':set_ip()
    }
    try:
        wb_img=requests.get(url,headers=header,)
        if wb_img.status_code==200:
            pattern=re.compile('gallery: JSON.parse\(\"(.*?)\),',re.S)
            return re.search(pattern,wb_img.text)[1]
        else:
            return None
    except RequestException:
        return None

def parse_img_info(page_source):
    wb_data=codecs.escape_decode(page_source)[0]
    wb_data=bytes.decode(wb_data)
    wb_data=wb_data.lstrip('b\'').rstrip('\'')
    wb_data=json.loads(wb_data)
    items=wb_data.get('sub_images')
    list_url_img=[item.get('url') for item in items]
    # img_url=[item for item in wb_data.get('sub_images')]
    return list_url_img

def download_image(urls):
    header=set_header()
    for url in urls:
        proxy={
            'https':set_ip()
        }
        try:
            response=requests.get(url,headers=header,proxies=proxy)
            save_images_to_file(response.content)
        except RequestException:
            print('download_image is bad request')

def sava_to_db(data):
    jiepai.insert_one(data)

def save_images_to_file(img_info):
    file_path='{}/{}.{}'.format(os.getcwd(), md5(img_info),'jpg')
    if not os.path.exists(file_path):
        with open(file_path,'wb') as f:
            f.write(img_info)
            f.close()


def main(offset):
    keyword='街拍'
    html=get_page_index(offset,keyword)
    html_json=parse_page_index(html)
    # show_content(html_json)
    img_info=get_page_url(html_json)
    # show_content(img_info)
    for item in img_info:
        try:
            img=get_imgage_page(item.get('img_url'))[0:-1]
            list_img_url=parse_img_info(img)
            download_image(list_img_url)
            info_imgs={
                'title':item.get('title'),
                'imgs_list':list_img_url
            }
            sava_to_db(info_imgs)
        except TypeError:
            print('fail')
            pass


if __name__=='__main__':
    groups=[x*20 for x in range(1,20)]
    main('1')
    pool=Pool()
    pool.map(main,groups)