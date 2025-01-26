import os
import telebot
from telebot import types
from bs4 import BeautifulSoup
import requests
from requests.exceptions import Timeout
import datetime
from mysql import connector
import time
import threading

#################################################################################################
API_TOKEN = telebot.TeleBot('YOUR_API_TOKEN')
CHANNEL_LINK = "https://t.me/YOUR_CHANNEL"
####################################################################################################
#BeautifulSoup code

def request_page_news_and_get_url_first_news(url,T_F):
    page = requests.get(url)

    soup = BeautifulSoup(page.text,"html.parser")
    if T_F:
        news_details(soup)
    
    link=soup.find_all('a')
    
    today=datetime.date.today()
    
    print(today.strftime("%Y/%#m/%#d"))
    url_news='https://www.aljazeera.com'
    for first_url in link:
        if 'news' in first_url.get('href')[1:5] and today.strftime("%Y/%#m/%#d") in first_url.get('href'):
            print(first_url.get('href'))
            url_news+=first_url.get('href')
            request_page_news_and_get_url_first_news(url_news,True)
            
            
def news_details(soup) :
    title_string=""
    for title in soup.title.string.split():
        if title == "|":
            break
        title_string+=title+" "
        
    print(title_string.lstrip())              


#####################################################################################################

@API_TOKEN.message_handler(commands=['start'])
def send_welcom(chat_id):
    if type(chat_id)==list:
        API_TOKEN.delete_message(chat_id[0],chat_id[1])
        chat_id=chat_id[0]

        
    
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("درباره ما", callback_data='درباره ما')
    button2 = types.InlineKeyboardButton("تماس با ما", callback_data='تماس با ما')
    button3 = types.InlineKeyboardButton("عضویت", callback_data='عضویت')
    keyboard.row(button1, button2,button3)
    
    if type(chat_id)==int:
        API_TOKEN.send_message(chat_id,'شما به منوی اصلی باز گردانده شدید',reply_markup=keyboard)
    else:  
        
        API_TOKEN.reply_to(chat_id,'سلام به رباط خبر خوش آمدید لطفا یکی از گزینه های زیرا انتخاب نمایید',reply_markup=keyboard)
        # API_TOKEN.delete_message(chat_id.from_user.id,chat_id.message_id)  
        
    
def send_membership_plane(messages,msg_id):
    API_TOKEN.delete_message(messages,msg_id)
    markup=types.InlineKeyboardMarkup()
    Button1=types.InlineKeyboardButton('سه ماهه',callback_data='سه ماهه')
    Button2=types.InlineKeyboardButton('شش ماهه',callback_data='شش ماهه')
    markup.row(Button1,Button2)
    return_button=types.InlineKeyboardButton('بازگشت',callback_data='بازگشت به منوی اصلی')
    markup.add(return_button)
    API_TOKEN.send_message(messages,'زمان مورد نیاز برای استفاده از رباط را انتخاب نمایید.',reply_markup=markup)
    
def about_us(messages,msg_id):
    
    # API_TOKEN.delete_message(messages,LIST_ID_MESSAGE[len(LIST_ID_MESSAGE)-1])
    API_TOKEN.delete_message(messages,msg_id)
    markup=types.InlineKeyboardMarkup()
    return_button=types.InlineKeyboardButton('بازگشت',callback_data='بازگشت به منوی اصلی')
    markup.add(return_button)
    API_TOKEN.send_message(messages,'این رباط توسط مهراد نوروززادگان توسعه داده شده است',reply_markup=markup) 
    
      
     
def call_us(messages,msg_id):
        API_TOKEN.delete_message(messages,msg_id)
        markup=types.InlineKeyboardMarkup()
        return_button=types.InlineKeyboardButton('بازگشت',callback_data='بازگشت به منوی اصلی')
        markup.add(return_button)
        phone='09361541818'
        email='mehrad.noroz1998@gmail.com'
        API_TOKEN.send_message(messages,f'اطلاعات تماس:\nشماره تماس:{phone}\n ایمیل: {email}',reply_markup=markup)
        
def choose_bank(messages,Which,msg_id):
    API_TOKEN.delete_message(messages,msg_id)
    Button1=types.InlineKeyboardButton('بانک ملت',callback_data='بانک ملت')
    Button2=types.InlineKeyboardButton('بانک آینده',callback_data='بانک آینده')
    markup=types.InlineKeyboardMarkup()
    markup.row(Button1,Button2)
    return_button=types.InlineKeyboardButton('بازگشت',callback_data='بازگشت به منوی انتخاب زمان')
    markup.add(return_button)
    if Which=="سه ماهه":
        API_TOKEN.send_message(messages,'مبلق قابل پرداخت:200000 تومان\nلطفا بانک مورد نظر خود را انتخاب کنید ',reply_markup=markup)
    else:
        API_TOKEN.send_message(messages,'مبلق قابل پرداخت:500000 تومان\nلطفا بانک مورد نظر خود را انتخاب کنید ',reply_markup=markup)

                
        
@API_TOKEN.callback_query_handler(func=lambda call:True) 
def handel_other_messages(call):
    if call.data=='درباره ما':
        
        about_us(call.message.chat.id,call.message.id)
    elif call.data=='تماس با ما':
        call_us(call.message.chat.id,call.message.id)
    elif call.data=='عضویت':
        send_membership_plane(call.message.chat.id,call.message.id)
    elif call.data=="سه ماهه" or call.data=="شش ماهه":
        choose_bank(call.message.chat.id,call.data,call.message.id)    

    elif call.data=='بازگشت به منوی اصلی' or call.data=="بازگشت به منوی انتخاب زمان":
        if call.data=='بازگشت به منوی اصلی':
            
            send_welcom([call.message.chat.id,call.message.id])   
        else:
            send_membership_plane(call.message.chat.id,call.message.id)


def send_news_to_telegram():
    while True:
        news_url = request_page_news_and_get_url_first_news("https://www.aljazeera.com/news/", False)
        if news_url:
            API_TOKEN.send_message(CHANNEL_LINK, f"📢 خبر فوری: {news_url}")
        time.sleep(3600)    
                    
          
if __name__== '__main__':
    threading.Thread(target=send_news_to_telegram, daemon=True).start()
    API_TOKEN.polling()    







request_page_news_and_get_url_first_news("https://www.aljazeera.com/news/",False)









