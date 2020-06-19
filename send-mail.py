import requests
import bs4
import smtplib

url = "https://www.flipkart.com/boat-micro-usb-500-black-1-5m-1-5-m-cable/p/itmf29shm8mk8gbz?pid=ACCF23XZE7HGWSCA&lid=LSTACCF23XZE7HGWSCAA2SYEC&marketplace=FLIPKART&srno=b_1_1&otracker=hp_omu_Deals%2Bof%2Bthe%2BDay_4_3.dealCard.OMU_Deals%2Bof%2Bthe%2BDay_VWG8IKYDNWI8_2&otracker1=hp_omu_SECTIONED_neo%2Fmerchandising_Deals%2Bof%2Bthe%2BDay_NA_dealCard_cc_4_NA_view-all_2&fm=neo%2Fmerchandising&iid=5c00ff5d-cd6e-41a2-8f51-8b17d40de94b.ACCF23XZE7HGWSCA.SEARCH&ppt=browse&ppn=browse&ssid=ejg8bykey80000001591551712449"

page = requests.get(url)

#making the soup object
soup = bs4.BeautifulSoup(page.content,'lxml')

#getting the title of the page
print(soup.title.string)

#getting the product title
product_title = soup.find('span',class_="_35KyD6")
print(product_title.text)

#getting the product price
product_price = soup.find('div',class_="_1vC4OE _3qQ9m1")
print("price is: ",product_price.text)

def send_mail():
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('ngopal561998@gmail.com',"gwfowjouiogmctlf")

    sub = "hey price fell down"
    link = url
    msg = f"{sub}\n\n check out the product {link}"
    
    
    server.sendmail('ngopal561998@gmail.com','nandagopalpattanayak@gmail.com',msg)
    print("hey email has been sent")

desired_peice = int(input('enter desired price: '))
price = ''
for i in product_price.text:
    if i.isdigit():
        price += i
if  int(price)<= desired_peice:
    send_mail()
else:
    print("product is costly than your price")