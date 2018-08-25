# -*- coding: utf-8 -*-
import time
import requests
import smtplib
from config import *
import tweepy
from datetime import datetime
from twilio.rest import Client
from bs4 import BeautifulSoup
from selenium import webdriver

def send_email(user, pwd, recipient, product): #snippet courtesy of david / email sending function
    SUBJECT             = product.encode('ascii', 'ignore') #message subject
    body                = 'SITE UPDATED AT ' + str(url) #message body
    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    #try:
    server = smtplib.SMTP("smtp.mail.me.com", 587) #start smtp server on port 587
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pwd) #login to gmail server
    server.sendmail(FROM, TO, message) #actually perform sending of mail
    #server.close() #end server
    print('[+]Successfully sent email notification') #alert user mail was sent
    # except: #else tell user it failed and why (exception e)
    #     print("[-]Failed to send notification email")

def sendtweet(consumer_key, consumer_secret,access_token, access_token_secret,status_string):
    try:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        api.update_status(status_string)
    except tweepy.error.TweepError:
        print("[-]Error, invalid or expired twitter tokens, visit http://apps.twitter.com to retrieve or refresh them")

def sendtext(message):
    print("[+]Sending text message....")
    try:
        twilioCli = Client(accountSID, authToken)
        twilioCli.messages.create(body=message, from_=twilioNumber, to=myNumber)
    except:
        print("[-]Error " )

def main():
        print("[+]Starting up monitor on " +url)
        print("[+]Email on change detect is set to " +str(notify))

        with requests.Session() as c:
            #try:
            # page1 = c.get(url,headers={'User-Agent':"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"}) #base page that will be compared against
            PHANTOMJS_PATH = '/usr/local/Cellar/phantomjs/2.1.1/bin/phantomjs'

            browser = webdriver.PhantomJS(PHANTOMJS_PATH)
            browser.get(url)
            soup = BeautifulSoup(browser.page_source, 'html.parser')

            first_product_1 = soup.find_all('a', {'data-qa': 'product-card-link'})[0].get('aria-label')

            # except:
            #     print("[-]Error Encountered during initial page retrieval: ")

            count = 1
            while 1:
                    time.sleep(wait_time) #wait beetween comparisons
                    try:
                        # page2 = c.get(url, headers={'User-Agent':"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"}) #page to be compared against page1 / the base page
                        browser.get(url)
                        soup = BeautifulSoup(browser.page_source, 'html.parser')

                        first_product_2 = soup.find_all('a', {'data-qa': 'product-card-link'})[0].get('aria-label')
                    except:
                        print("[+]Error Encountered during comparison page retrieval: " )

                    if first_product_1 == first_product_2: #if else statement to check if content of page remained same
                    #if page1.content == page2.content:
                        print('[-]No Change Detected on ' +str(url)+ "\n" +str(datetime.now()) + ' First product is ' + first_product_1)
                        # if count == 1:
                        #     send_email(user, pwd, recipient, first_product_1)
                        #     count += 1
                    else:
                        status_string = 'Change Detected at ' +str(url)+ "\n" +str(datetime.now())
                        message = status_string
                        print("[+]"+status_string)
                        if notify == True:
                            send_email(user, pwd, recipient, first_product_2) #send notification email
                        # else:
                        #     pass
                        # if tweet == True:
                        #     sendtweet(consumer_key, consumer_secret,access_token, access_token_secret,status_string)
                        # else:
                        #     pass
                        # if text == True:
                        #     sendtext(message)
                        print('\n[+]Retrieving new base page and restarting\n')
                        main()
if __name__ == '__main__':
    main()
    # start_time = time.time()
    #send_email(user, pwd, recipient, "女款 Air Jordan XII 'Moon Particle' 发布日期")
    # print("--- %s seconds passed ---" % (time.time() - start_time))

