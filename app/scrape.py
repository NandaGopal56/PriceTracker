import requests
import bs4
import smtplib
from lxml.html import fromstring
import requests
import traceback
from random import choice
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler(daemon=True) #daemon is to kill the background process if we kill flask
proxies = []

def get_proxies():
    global proxies
    proxies = []    
    url = "https://www.sslproxies.org/"

    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.content,'html5lib')
    proxies = list(map(lambda x:x[0]+':'+x[1] , list(zip(map(lambda x:x.text, soup.findAll('td')[::8]),
                                                        map(lambda x:x.text, soup.findAll('td')[1::8] )))))
    
if len(proxies) == 0:
    get_proxies()

scheduler.add_job(get_proxies,'interval', hours=2)
scheduler.start()



user_agent_list = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]


def Get_details(link):     
        user_agent = choice(user_agent_list) 
        headers = {'User-Agent': user_agent}
        
        if 'amazon' in link:
            return check_amazon(link,headers)
        elif 'flipkart' in link:
            return check_flipkart(link,headers)
        else:
            return None
        


def check_flipkart(link,headers):
    for i in range(20):
        try:
            proxy = choice(proxies)
            proxy = {'https':proxy}

            page = requests.get(link,headers=headers, proxies=proxy, timeout=5)

            soup = bs4.BeautifulSoup(page.content,'lxml')
            product_price = soup.find('div',class_="_1vC4OE _3qQ9m1").text
            return product_price
        except:
            pass
    return None

def check_amazon(link,headers):
    for i in range(20):
        try:
            proxy = choice(proxies)
            proxy = {'https':proxy}

            page = requests.get(link, headers=headers, proxies=proxy, timeout=5)
            soup = bs4.BeautifulSoup(page.content,'lxml')
            product_price = soup.find('span', class_="a-size-medium a-color-price priceBlockBuyingPriceString").text
            return product_price
        except:
            pass
    return None



        