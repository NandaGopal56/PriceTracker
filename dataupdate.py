from app.db import db, User, Information
from app import app
import datetime
import time
from app import scrape
import multiprocessing


def infinite_data_update():
    
    while True:
        try:
            print("########################################################################")
            infos = Information.query.all()
                
            ################################################################################################
            for info in infos:
                    
                print('----------------------------------------------------------------------------')
                print(info.current_price,info.target_price,info.new_price)
                    
                updated_price = scrape.Get_details(info.link)
                    
                if updated_price:
                    updated_price = updated_price[1:len(updated_price)]
                    price = ''
                    check = ['0','1','2','3','4','5','6','7','8','9']
                    for digit in str(updated_price):
                        if digit in check:
                            price += digit
                        elif digit in ['!','@','#','$','%','^','&','*','~','.']:
                            break
                    updated_price = int(price)
                    print("updated_price:",updated_price)

                    
                    #######################################################################################################
                    
                    if updated_price <= int(info.target_price):
                        send_mail_taget_reached(info)

                        Information.query.filter_by(info_id=info.info_id).delete()
                        db.session.commit()

                    elif updated_price <= int(info.new_price):
                        send_mail_price_dropped(info)
                        
                        info.new_price = updated_price
                        db.session.commit()
                else:
                    print('exception raised.............')
                    ############################################################################################################

                today = datetime.date.today()        
                date_posted = info.date_posted.date()
                date_difference = today-info.date_posted.date()
                if int(date_difference.days) >= 60:
                    Information.query.filter_by(email=info.email).delete()
                    db.session.commit()
        except Exception as e:
            print("updation failed.....",e)

def start_data_update():

    p1 = multiprocessing.Process(target=infinite_data_update)
    p1.start()


def send_mail_taget_reached(info):
    print("awesome its working........")

def send_mail_price_dropped(info):
    pass