# from bs4 import  BeautifulSoup
# import requests
# url='http://31f.cn/'
# url_for_test='http://bj.ganji.com/shouji/o2/'
# ip_lis=[]
# def find_ip(url):
#     wb_data=requests.get(url,timeout=15)
#     soup=BeautifulSoup(wb_data.text,'lxml')
#     lis=soup.select('table tr')
#     for add in lis[1:51]:
#         ip=add.text.split()
#         ip_lis.append('http//'+str(ip[1])+':'+str(ip[2]))
#     print(ip_lis)
#
# def ip_test(ipp):
#     proxy={'https':ipp}
#     try:
#         print(proxy)
#         wb_data=requests.get(url_for_test,timeout=10,proxies=proxy)
#         soup= BeautifulSoup(wb_data.text,'lxml')
#         title=soup.select('body div.nav a')
#         print(title)
#     except requests.exceptions.ConnectionError:
#         ip_lis.remove(ipp)
#         print('ip is not avialbe')
#
#
# find_ip(url)
# for ipp in ip_lis:
#     print(ipp)
#     ip_test(11111)
from bs4 import BeautifulSoup
import requests
url='http://31f.cn/'
url_for_test='http://bj.ganji.com/shouji/o2/'
ip_list=[]

def find_ip(url):
    wb_data=requests.get(url,timeout=15)
    soup=BeautifulSoup(wb_data.text,'lxml')
    lis=soup.select('table tr')
    for add in lis[1:51]:
        ip=add.text.split()
        ip_list.append('http//'+str(ip[1])+':'+str(ip[2]))
    #print(ip_list)

def ip_test(ipp):
    proxy={'https':ipp}
    try:
        wb_data=requests.get(url_for_test,timeout=10,proxies=proxy)
        soup= BeautifulSoup(wb_data.text,'lxml')
        title=soup.select('body div.nav a')
        print(title)
    except requests.exceptions.ConnectionError:
        ip_list.remove(ipp)
        print('ip is not avialbe')

find_ip(url)
for ipp in ip_list:
    pass
    # ip_test(ipp)