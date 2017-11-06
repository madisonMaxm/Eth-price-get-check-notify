#!/usr/bin/env python
import config
import smtplib
import time
import urllib2
import traceback

from bs4 import BeautifulSoup

# Coinmarket Cap ETH
search_url = 'https://coinmarketcap.com/currencies/'

run = True

#returns price as float
def parse_price(index):
    content = urllib2.urlopen(search_url + config.currency_array[index].name + '/').read()
    soup = BeautifulSoup(content, "lxml")

    #convert text from unicode to float with 2 degrees of precision
    str_price = soup.find(id = 'quote_price').getText()
    price = int(float(str_price[1:].encode('utf-8'))*100)/100.0
    
    #print type(price)
    print "Log: $%.2f" % (price)
    
    soup.decompose()
    return price

def compare_price(value, index):
    evaluate = False
    if value <= config.currency_array[index].low or value >= config.currency_array[index].high:
        evaluate = True
    return evaluate

#sends email from email in config file to same email
def send_email(address, password, price, index):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(address, password)
    
    msg = "The price of " + str(config.currency_array[index].name) +  " is outside your limit $" + str(price) + "."
    server.sendmail(address, address, msg)
    server.quit()

if __name__ == '__main__':
    
    while run:
        try:

            count = 0
            for element in config.currency_array:
                
                print config.currency_array[count].name
                
                current_price = parse_price(count)
            
                if compare_price(current_price, count):
                    send_email(config.email_address, config.password, current_price, count)

                    print "email sent"
                count += 1
            count = 0 
            time.sleep(config.time_interval) 
            

        except:
            print("Error. Script aborted.")
            traceback.print_exc()
            run = False