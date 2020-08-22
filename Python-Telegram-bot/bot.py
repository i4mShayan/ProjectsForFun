from hotgram import proxy
from telegram.ext import *
from telegram import *
from time import sleep
import datetime
import pytz
import logging
import pprint


admin = 767417022
token = "597164507:AAHY9XCWnaGJZ_keuBV7_1hcu114J-vzdRo"



global answer
answer = 0
global timer
timer = 900
global channel
channel = None
global user_step
user_step = {}

english = {"greet":"Hi !","default timer":"the default timer is %s","timer changed":"Timer changed to %s :D","timer value":"please enter integer or float number !!",
"channel changed":"Channel Changed to %s",
"not admin":"Robot isn't admin in %s","default channel":"Default channel is %s","at at":"please enter '@' at begining !","not found":"I can't understand it :(",
"button":{"disable":"❌ Disable Robot ❌","enable":"✅ Enable Robot ✅","change channel":"〽️Change Channel 〽️","change timer":"⏰ Change timer ⏰","info":"ℹ️ Show information ℹ️","back":"🔙 Back"},
"panel":"Hello Admin :D\n\nchoose one :",
"not admin msg":"You aren't a admin :|","not admin q":"Fucking {} ,You aren't a admin :|","disabled":"Bot Disabled","enabled":"Bot Enabled",
"info":"ℹ️ information ℹ️",
"en":"Enabled","dis":"Disabled","timer input":"Please enter a integer or float number :","ch input":"Please enter valid channel address with '@' at the Beginning :",
"connect":"Connect to Proxy !","proxy info":"*IP* : `{}`\n*Port* : `{}`\n*user* : `{}`\n*pass* : `{}`\n*Live Time* : {} Min\n\n*Expiration Time* : {}\n",
           "state":{1:"Enabled",0:"Disabled","ch":"Channel :","time":"Timer :","bot":"Robot :","sec":" seconds"},"none ch":"First please set a channel from\nPanel > Change Channel !"}

persian = {"greet":"سلام !","default timer":"تایمر پیش فرض %s می باشد","timer changed":"تایمر به %s تغییر یافت !","timer value":"لطفا عدد صحیح یا اعشاری وارد کنید !",
"channel changed":"چنل به %s تغییر یافت",
"not admin":"ربات در %s ادمین نیست","default channel":"چنل پیش فرض %s می باشد !!","at at":"لطفا اولش '@' بزن !!","not found":"متوجه نمیشم :(",
"button":{"disable":"❌ غیرفعال کردن ❌","enable":"✅ فعال کردن ✅","change channel":"〽️تغییر چنل 〽️","change timer":"⏰ تغییر تایمر ⏰","info":"ℹ️ اطلاعات ℹ️","back":"بازگشت 🔙"},
"panel":"سلام ادمین :D\n\n لطفا یکی رو انتخاب بکن :",
"not admin msg":"شما ادمین نیستی :|","not admin q":"{} عزیز, شما ادمین نیستی :)","disabled":"ربات غیر فعال شد","enabled":"ربات فعال شد",
"info":"ℹ️ اطلاعات ℹ️",
"en":"فعال","dis":"غیر فعال","timer input":"لطفا یک عدد صحیح یا اعشاری وارد کنید :","ch input":"لطفا ادرس یک چنل رو همراه با @ وارد کنید :",
"connect":"وصل شو !","proxy info":"*آی پی* : `{}`\n*پورت* : `{}`\n*یوزر* : `{}`\n*پسورد* : `{}`\n*فعال بودن* : {} دقیقه\n\n*انقضا* : {}\n",
"state":{1:"فعال",0:"غیر فعال","ch":":‌ چنل","time":": تایمر","bot":":‌ ربات","sec":" ثانیه"},"none ch":"چنل تعریف نشده !\nلطفا اول از طریق پنل > تغییر چنل اقدام به تعریف چنل کنید !"}

# Default language is english
global language
language = english


# this is for robot proxy connection :D

# REQUEST_KWARGS={
#     'proxy_url': 'URL_OF_THE_PROXY_SERVER',
#     # Optional, if you need authentication:
#     'urllib3_proxy_kwargs': {
#         'username': 'PROXY_USER',
#         'password': 'PROXY_PASS',
#     }
# }


logger = logging.getLogger(__name__)

updater = Updater(token)


def lang(bot,update):
    if update.message.from_user.id == admin:
        buts = [[InlineKeyboardButton(text="English", callback_data="english")],
                [InlineKeyboardButton(text="فارسی", callback_data="persian")]]
        key = InlineKeyboardMarkup(buts)
        bot.send_message(update.message.chat_id, "Please select robot language :", reply_markup=key)
    else :
        update.message.reply_text(language["not admin msg"])

def commands(bot,update):
    bot.send_message(update.message.chat_id,"/start\n/lang\n/panel")

def start(bot,update):
    global language
    update.message.reply_text(language["greet"])

#message handler
def inputer(bot,update):
    global language
    global user_step
    msg = update.message
    try :
        if user_step[msg.from_user.id] == "timer":
            
            global timer
            if msg.text == str(timer):
                bot.send_message(msg.chat_id,language["default timer"]%msg.text,reply_to_message_id=msg.message_id)
            else:
                try:
                    timer = float(msg.text)
                    bot.send_message(msg.chat_id,language["timer changed"]%msg.text,reply_to_message_id=msg.message_id)
                    timer = int(msg.text)
                except ValueError:
                    bot.send_message(msg.chat_id,language["timer value"],reply_to_message_id=msg.message_id)

            user_step[update.message.from_user.id] = 0

        elif user_step[msg.from_user.id] == "channel":
            global channel
            

            if msg.text.startswith("@"):
                try :
                    test_msg = bot.send_message(msg.text,"test from robot !!")
                    bot.delete_message(msg.text,message_id=test_msg.message_id)
                    channel = msg.text
                    bot.send_message(msg.chat_id,language["channel changed"]%channel,reply_to_message_id=msg.message_id)

                except :
                    bot.send_message(msg.chat_id,language["not admin"]%msg.text,reply_to_message_id=msg.message_id)
            elif msg.text == channel:
                bot.send_message(msg.chat_id,language["default channel"]%msg.text,reply_to_message_id=msg.message_id)
            else :
                bot.send_message(msg.chat_id,language["at at"],reply_to_message_id=msg.message_id)

            user_step[update.message.from_user.id] = 0

        

        else :
            bot.send_message(msg.chat_id,language["not found"],reply_to_message_id=msg.message_id)
    except :
        user_step[msg.from_user.id] = 0
        bot.send_message(msg.chat_id,language["not found"],reply_to_message_id=msg.message_id)



# show inline keyboard
def panel(bot,update):
    global language
    global answer
    global user_step

    if update.message.from_user.id == admin:
        if answer == 1:
            button = [[InlineKeyboardButton(text=language["button"]["disable"],callback_data="Disable")]]
        else :
            button = [[InlineKeyboardButton(text=language["button"]["enable"],callback_data="Enable")]]

        button.append([InlineKeyboardButton(text=language["button"]["change channel"],callback_data="channel")])
        button.append([InlineKeyboardButton(text=language["button"]["change timer"],callback_data="timer")])
        button.append([InlineKeyboardButton(text=language["button"]["info"],callback_data="info")])

        keyboard1 = InlineKeyboardMarkup(button)

        bot.send_message(update.message.chat_id,language["panel"],reply_markup=keyboard1)

    else :
        update.message.reply_text(language["not admin msg"])



# inline keyboard handler
def hand(bot,update,job_queue):

    query = update.callback_query
    global answer
    global timer
    global channel
    global user_step
    global language


    def main_panel():
        if query.from_user.id == admin:
            if answer == 1:
                button = [[InlineKeyboardButton(text=language["button"]["disable"],callback_data="Disable")]]
            else :
                button = [[InlineKeyboardButton(text=language["button"]["enable"],callback_data="Enable")]]

            button.append([InlineKeyboardButton(text=language["button"]["change channel"],callback_data="channel")])
            button.append([InlineKeyboardButton(text=language["button"]["change timer"],callback_data="timer")])
            button.append([InlineKeyboardButton(text=language["button"]["info"],callback_data="info")])

            keyboard1 = InlineKeyboardMarkup(button)

            bot.edit_message_text(text=language["panel"],chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=keyboard1)
        else :
            bot.answer_callback_query(query.id,language["not admin q"].format(query.from_user.first_name))



    
    if query.from_user.id == admin:
        back_button = [[InlineKeyboardButton(text=language["button"]["back"],callback_data="back")]]
        keyboard_back = InlineKeyboardMarkup(back_button)

        if query.data == "Disable":
            answer = 0
            # update.answer_callback_query(query.id,"bot Disabled !")
            bot.edit_message_text(text=language["disabled"],chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=keyboard_back)

        elif query.data == "Enable":
            if channel == None:
                bot.edit_message_text(text=language["none ch"],chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=keyboard_back)
            else :
                answer = 1
                # update.answer_callback_query(query.id,"bot Enabled !")
                bot.edit_message_text(text=language["enabled"],chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=keyboard_back)

        elif query.data == "info":
            buttons = [[InlineKeyboardButton(text=language["state"]["bot"],callback_data="nothing"),InlineKeyboardButton(text="{}".format(language["state"][0] if answer==0 else language["state"][1]),callback_data="nothing")]
            ,[InlineKeyboardButton(text=language["state"]["time"],callback_data="nothing"),InlineKeyboardButton(text=str(timer)+language["state"]["sec"]
            ,callback_data="nothing")],[InlineKeyboardButton(text=language["state"]["ch"],callback_data="nothing"),InlineKeyboardButton(text=str(channel)
            ,callback_data="nothing")],[InlineKeyboardButton(text=language["button"]["back"],callback_data="back")]]


            bot.edit_message_text(text=language["info"]
            .format( language["state"][0] if answer==0 else language["state"][1] ,timer,channel)
            ,chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=InlineKeyboardMarkup(buttons))

        elif query.data == "back":
            main_panel()

        elif query.data == "timer" :
            user_step[query.from_user.id] = "timer"
            force = ForceReply()
            bot.send_message(query.message.chat_id,language["timer input"],reply_markup=force)

        elif query.data == "channel":
            user_step[query.from_user.id] = "channel"
            force = ForceReply()
            bot.send_message(query.message.chat_id,language["ch input"],reply_markup=force)

        elif query.data == "english":
            language = english
            print(english)
            bot.send_message(query.message.chat_id, 'Robot ia English !')
        elif query.data == "persian":
            language = persian
            bot.send_message(query.message.chat_id, 'ربات فارسی است !')


        if answer == 1:
            job_minute = job_queue.run_repeating(send_channel_proxy, interval=timer)
            jobq.start()
        elif answer == 0 :
            jobq.stop()
            job_minute.schedule_removal()
        
    else :
        bot.answer_callback_query(query.id,language["not admin q"].format(query.from_user.first_name))



# method for job queue to do
def send_channel_proxy(bot,job):
    global language
    proxy_info = proxy.return_proxy()
    ip = proxy_info["ip"]
    port = proxy_info["prt"]
    user_name = proxy_info["usr"]
    password = proxy_info["pwd"]
    time_till_end = proxy_info["ttl"]

    time_zone = pytz.timezone("Asia/Tehran")
    time_now = datetime.datetime.now(time_zone)
    time = time_now + datetime.timedelta(0,time_till_end)
    time_format = time.strftime("%H:%M:%S")

            
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text=language["connect"],url="https://t.me/socks?server={}&port={}&user={}&pass={}".format(ip,port,user_name,password))]])

    bot.send_message(channel,language["proxy info"]
    .format(ip,port,user_name,password,str(time_till_end//60),str(time_format))
    ,reply_markup=keyboard,parse_mode="Markdown")

# error handler
def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)









jobq = updater.job_queue
updater.dispatcher.add_handler(CommandHandler('panel', panel))
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('lang', lang))
updater.dispatcher.add_handler(CommandHandler('commands', commands))
updater.dispatcher.add_handler(CallbackQueryHandler(hand,pass_job_queue=True))
updater.dispatcher.add_error_handler(error)
updater.dispatcher.add_handler(MessageHandler(Filters.text, inputer))

print("robot started..")
updater.start_polling()
updater.idle()
