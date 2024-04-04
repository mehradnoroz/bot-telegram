import os
import telebot
from telebot import types
from bs4 import BeautifulSoup
import requests
from requests.exceptions import Timeout
import datetime
import click
import telebot
from telebot import types


# bot = telebot.TeleBot("6861150251:AAEUH2NzjB9RJSevqTuZENA7YDvroA6KdYA")


# user_menu = {}

# # Function to send the main menu
# def send_main_menu(chat_id):
#     keyboard = types.InlineKeyboardMarkup()
#     button1 = types.InlineKeyboardButton("Option 1", callback_data='option1')
#     button2 = types.InlineKeyboardButton("Option 2", callback_data='option2')
#     keyboard.row(button1, button2)
#     bot.send_message(chat_id, "Main Menu:", reply_markup=keyboard)

# # Function to send the sub-menu
# def send_sub_menu(chat_id):
#     keyboard = types.InlineKeyboardMarkup()
#     button1 = types.InlineKeyboardButton("Sub Option 1", callback_data='sub_option1')
#     button2 = types.InlineKeyboardButton("Sub Option 2", callback_data='sub_option2')
#     keyboard.row(button1, button2)
#     # Adding a "Return" button to go back to the main menu
#     return_button = types.InlineKeyboardButton("Return", callback_data='return_main_menu')
#     keyboard.add(return_button)
#     bot.send_message(chat_id, "Sub Menu:", reply_markup=keyboard)

# # Handler for callback queries
# @bot.callback_query_handler(func=lambda call: True)
# def callback_query(call):
#     chat_id = call.message.chat.id
#     if call.data == 'option1':
#         send_sub_menu(chat_id)
#         user_menu[chat_id] = 'sub_menu'
#     elif call.data == 'option2':
#         bot.send_message(chat_id, "You selected Option 2")
#     elif call.data == 'sub_option1':
#         bot.send_message(chat_id, "You selected Sub Option 1")
#     elif call.data == 'sub_option2':
#         bot.send_message(chat_id, "You selected Sub Option 2")
#     elif call.data == 'return_main_menu':
#         send_main_menu(chat_id)
#         user_menu[chat_id] = 'main_menu'

# # Handler for /start command
# @bot.message_handler(commands=['start'])
# def send_start(message):
#     send_main_menu(message.chat.id)
#     user_menu[message.chat.id] = 'main_menu'

# # Start the bot
# if __name__=='__main__':
#     bot.polling()

API_TOKEN =telebot.TeleBot( '6861150251:AAEUH2NzjB9RJSevqTuZENA7YDvroA6KdYA')

@API_TOKEN.message_handler(commands=['start'])
def send_welcom(chat_id):
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("درباره ما", callback_data='درباره ما')
    button2 = types.InlineKeyboardButton("تماس با ما", callback_data='تماس با ما')
    button3 = types.InlineKeyboardButton("عضویت", callback_data='عضویت')
    keyboard.row(button1, button2,button3)
    if type(chat_id)==int:
        API_TOKEN.send_message(chat_id,'شما به منوی اصلی باز گردانده شدید',reply_markup=keyboard)
    else:    
        API_TOKEN.reply_to(chat_id,'سلام به رباط خبر خوش آمدید لطفا یکی از گزینه های زیرا انتخاب نمایید',reply_markup=keyboard)
    
def send_membership_plane(messages):
    markup=types.InlineKeyboardMarkup()
    Button1=types.InlineKeyboardButton('سه ماهه',callback_data='سه ماهه')
    Button2=types.InlineKeyboardButton('شش ماهه',callback_data='شش ماهه')
    markup.row(Button1,Button2)
    return_button=types.InlineKeyboardButton('بازگشت',callback_data='بازگشت به منوی اصلی')
    markup.add(return_button)
    API_TOKEN.send_message(messages,'زمان مورد نیاز برای استفاده از رباط را انتخاب نمایید.',reply_markup=markup)
    
def about_us(messages):
    API_TOKEN.send_message(messages,'این رباط توسط مهراد نوروززادگان توسعه داده شده است')   
     
def call_us(messages):
        phone='09361541818'
        email='mehrad.noroz1998@gmail.com'
        API_TOKEN.send_message(messages,f'اطلاعات تماس:\nشماره تماس:{phone}\n ایمیل: {email}')
        
def choose_bank(messages,Which):
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
        about_us(call.message.chat.id)
    elif call.data=='تماس با ما':
        call_us(call.message.chat.id)
    elif call.data=='عضویت':
        send_membership_plane(call.message.chat.id)
    elif call.data=="سه ماهه" or call.data=="شش ماهه":
        choose_bank(call.message.chat.id,call.data)    

    elif call.data=='بازگشت به منوی اصلی' or call.data=="بازگشت به منوی انتخاب زمان":
        if call.data=='بازگشت به منوی اصلی':
        
            send_welcom(call.message.chat.id)   
        else:
            send_membership_plane(call.message.chat.id)
                
          
if __name__== '__main__':
    API_TOKEN.polling()    

# CHANNEL_link = 'https://t.me/+R0LchXBgCWZlNDk0'

# max_retries = 3
# def request_page_news_and_get_url_first_news(url,T_F):
#     page = requests.get(url)#Request URL

#     soup = BeautifulSoup(page.text,"html.parser")#Fetch webpage
#     if T_F:
#         news_details(soup)
    
#     link=soup.find_all('a')
    
#     today=datetime.date.today()
    
#     print(today.strftime("%Y/%#m/%#d"))
#     url_news='https://www.aljazeera.com'
#     for first_url in link:
#         if 'news' in first_url.get('href')[1:5] and today.strftime("%Y/%#m/%#d") in first_url.get('href'):
#             print(first_url.get('href'))
#             url_news+=first_url.get('href')
#             request_page_news_and_get_url_first_news(url_news,True)
            
# def news_details(soup) :
#     title_string=""
#     for title in soup.title.string.split():
#         if title == "|":
#             break
#         title_string+=title+" "
        
#     print(title_string.lstrip())  




# request_page_news_and_get_url_first_news("https://www.aljazeera.com/news/",False)






