from telegram import *
from telegram.ext import *
import translate as tr
import sqlite3
import datetime
import pytz

token = ""
admins = []

global step
step = 0
global text
text = {}
bn = InlineKeyboardButton
start_key = InlineKeyboardMarkup([[bn("ðŸ“¢ Ú†Ù†Ù„ Ø³Ø§Ø²Ù†Ø¯Ù‡ ðŸ“¢", url="t.me/OneDev")],
                                  [bn("ðŸ‘¨â€ðŸ’» Ø¨Ø±Ù†Ø§Ù…Ù‡ Ù†ÙˆÛŒØ³ ðŸ‘¨â€ðŸ’»", url="t.me/a_Coder"),
                                   bn("ðŸ”… Ù¾ÛŒØ§Ù… Ø±Ø³Ø§Ù† ðŸ”…", url="t.me/OneDev_bot")],
                                  [bn("ðŸ¤– Ø±Ø¨Ø§Øª Ù‡Ø§ÛŒ Ø¯ÛŒÚ¯Ø± ðŸ¤–", url="t.me/OneDevs")]])

languages = InlineKeyboardMarkup([
                                      [bn("1ï¸âƒ£ ØµÙØ­Ù‡ Ø§ÙˆÙ„ 1ï¸âƒ£",callback_data="nothing")],
                                      [bn("âž–âž–âž–âž–âž–âž–âž–âž–âž–", callback_data="nothing")],
                                      [bn("ðŸ‡®ðŸ‡· ÙØ§Ø±Ø³ÛŒ ðŸ‡®ðŸ‡·",callback_data="fa")],
                                      [bn("ðŸ‡ºðŸ‡¸ Ø§Ù†Ú¯Ù„ÛŒØ³ÛŒ ðŸ‡¬ðŸ‡§",callback_data="en")],
                                      [bn("ðŸ‡©ðŸ‡ª Ø¢Ù„Ù…Ø§Ù†ÛŒ ðŸ‡©ðŸ‡ª", callback_data="de")],
                                      [bn("ðŸ‡«ðŸ‡· ÙØ±Ø§Ù†Ø³ÙˆÛŒ ðŸ‡«ðŸ‡·", callback_data="fr")],
                                      [bn("ðŸ‡¦ðŸ‡ª Ø¹Ø±Ø¨ÛŒ ðŸ‡¦ðŸ‡ª", callback_data="ar")],
                                      [bn("ðŸ‡ªðŸ‡¸ Ø§Ø³Ù¾Ø§Ù†ÛŒØ§ÛŒÛŒ ðŸ‡ªðŸ‡¸", callback_data="es")],
                                      [bn("ðŸ‡¨ðŸ‡³ Ú†ÛŒÙ†ÛŒ Ø³Ø§Ø¯Ù‡ ðŸ‡¨ðŸ‡³",callback_data="zh-CN")],
                                      [bn("ðŸ‡­ðŸ‡° Ú†ÛŒÙ†ÛŒ Ø³Ù†ØªÛŒ ðŸ‡­ðŸ‡°", callback_data="zh-TW")],
                                      [bn("ðŸ‡¯ðŸ‡µ Ú˜Ø§Ù¾Ù†ÛŒ ðŸ‡¯ðŸ‡µ", callback_data="ja")],
                                      [bn("ðŸ‡°ðŸ‡· Ú©Ø±Ù‡ Ø§ÛŒ ðŸ‡°ðŸ‡·", callback_data="ko")],
                                      [bn("ðŸ‡®ðŸ‡¹ Ø§ÛŒØªØ§Ù„ÛŒØ§ÛŒÛŒ ðŸ‡®ðŸ‡¹", callback_data="it")],
                                      [bn("ðŸ‡¹ðŸ‡· ØªØ±Ú©ÛŒ ðŸ‡¹ðŸ‡·", callback_data="tr")],
                                      [bn("âž–âž–âž–âž–âž–âž–âž–âž–âž–", callback_data="nothing")],
                                      [bn("ï¸âž¡ï¸ Ø¨Ø¹Ø¯ÛŒï¸", callback_data="page2")]
                                      ])

languages2 = InlineKeyboardMarkup([
    [bn("2ï¸âƒ£ ØµÙØ­Ù‡ Ø¯ÙˆÙ… 2ï¸âƒ£", callback_data="nothing")],
    [bn("âž–âž–âž–âž–âž–âž–âž–âž–âž–", callback_data="nothing")],
    [bn("Ø¢ÙØ±ÛŒÙ‚Ø§ÛŒÛŒ", callback_data="af"), bn("Ø¢Ù„Ø¨Ø§Ù†ÛŒ", callback_data="sq")],
    [bn("Ø§Ù…Ø±ÛŒÚ©Ø§ÛŒÛŒ", callback_data="am"), bn("Ú©Ø¨ÙˆØ§Ù†ÙˆÛŒÛŒ", callback_data="ceb")],
    [bn("Ø§Ø±Ù…Ù†ÛŒ", callback_data="hy"), bn("Ø¢Ø°Ø±Ø¨Ø§ÛŒØ¬Ø§Ù†ÛŒ", callback_data="az")],
    [bn("Ø¨Ø§Ø³Ú©ÛŒ", callback_data="eu"), bn("Ø¨Ù„Ø§Ø±ÙˆØ³ÛŒ", callback_data="be")],
    [bn("Ø¨Ù†Ú¯Ø§Ù„ÛŒ", callback_data="bn"), bn("Ø¨ÙˆØ³Ù†ÛŒ", callback_data="bs")],
    [bn("Ø¨Ù„ØºØ§Ø±ÛŒ", callback_data="bg"), bn("Ú©Ø§ØªØ§Ù„Ø§Ù†ÛŒ", callback_data="ca")],
    [bn("Ú†ÛŒÚ©ÙˆØ§ÛŒÛŒ", callback_data="ny"), bn("Ù…Ø±Ø¬Ø§Ù†ÛŒ", callback_data="co")],
    [bn("Ú©Ø±ÙˆØ§ØªÛŒ", callback_data="hr"), bn("Ú†Ú©", callback_data="cs")],
    [bn("Ø¯Ø§Ù†Ù…Ø§Ø±Ú©ÛŒ", callback_data="da"), bn("Ù‡Ù„Ù†Ø¯ÛŒ", callback_data="nl")],
    [bn("Ø§Ø³Ù¾Ø±Ø§Ù†ØªÙˆ", callback_data="eo"), bn("Ø§Ø±Ù…Ù†Ø³ØªØ§Ù†ÛŒ", callback_data="et")],
    [bn("ÙÛŒÙ„ÛŒÙ¾ÛŒÙ†ÛŒ", callback_data="tl"), bn("ÙÙ†Ù„Ø§Ù†Ø¯ÛŒ", callback_data="fi")],
    [bn("ÙØ±ÛŒØ³ÛŒÙ†", callback_data="fy"), bn("Ú¯Ø§Ù„ÛŒÚ©Ø³ÛŒ", callback_data="gl")],
    [bn("âž–âž–âž–âž–âž–âž–âž–âž–âž–", callback_data="nothing")],
    [bn("Ù‚Ø¨Ù„ÛŒ â¬…ï¸", callback_data="page1"),bn("âž¡ï¸ Ø¨Ø¹Ø¯ÛŒï¸", callback_data="page3")]
])
languages3 = InlineKeyboardMarkup([
                                  [bn(" 3ï¸âƒ£ ØµÙØ­Ù‡ Ø³ÙˆÙ… 3ï¸âƒ£", callback_data="nothing")],
                                  [bn("âž–âž–âž–âž–âž–âž–âž–âž–âž–", callback_data="nothing")],
                                  [bn("Ø²Ø¨Ø§Ù†ÛŒ Ú©Ù‡ Ù…ÛŒØ®ÙˆØ§Ø³ØªÛŒ Ø±Ùˆ Ù¾ÛŒØ¯Ø§ Ù†Ú©Ø±Ø¯ÛŒØŸ ðŸ˜“", callback_data="nolang")],
                                  [bn("âž–âž–âž–âž–âž–âž–âž–âž–âž–", callback_data="nothing")],
                                  [bn("Ù‚Ø¨Ù„ÛŒ â¬…ï¸", callback_data="page2"), bn("ðŸ  ØµÙØ­Ù‡ Ø§ÙˆÙ„ï¸ ðŸ ", callback_data="page1")]
                                  ])

nolang_key = InlineKeyboardMarkup([[bn("ðŸ“¢ Ú†Ù†Ù„ Ø³Ø§Ø²Ù†Ø¯Ù‡ ðŸ“¢", url="t.me/OneDev")],
                                  [bn("ðŸ‘¨â€ðŸ’» Ø¨Ø±Ù†Ø§Ù…Ù‡ Ù†ÙˆÛŒØ³ ðŸ‘¨â€ðŸ’»", url="t.me/a_Coder"),
                                   bn("ðŸ”… Ù¾ÛŒØ§Ù… Ø±Ø³Ø§Ù† ðŸ”…", url="t.me/OneDev_bot")],
                                  [bn("âž–âž–âž–âž–âž–âž–âž–âž–âž–", callback_data="nothing")],
                                  [bn("âž° Ø§Ù†ØªØ®Ø§Ø¨ Ø²Ø¨Ø§Ù† Ù…Ù‚ØµØ¯ âž°", callback_data="page1"),]
                                  ])
panel_key = InlineKeyboardMarkup([
    [bn("ðŸ‘€ ØªØ¹Ø¯Ø§Ø¯ Ú©Ø§Ø±Ø¨Ø±Ø§Ù† ðŸ‘€",callback_data="check_user")],
    [bn("ðŸ—£ Ø§Ø±Ø³Ø§Ù„ Ù¾ÛŒØ§Ù… Ø¨Ù‡ Ú©Ø§Ø±Ø¨Ø±Ø§Ù† ðŸ—£",callback_data="send_user")]
])
try :
    users = sqlite3.connect("users.db")
    users.execute("CREATE TABLE USERS (ID NOT NULL, NAME NOT NULL ,USERNAME NOT NULL ,BLOCKED)")
    users.close()
    print("database created !")
except :
    print("database has created later...")

def start(bot,update):
    msg = update.message
    users = sqlite3.connect("users.db")
    users_list = list(users.execute("SELECT ID FROM USERS"))
    is_user = False
    for user in users_list:
        if str(msg.chat.id) == user[0]:
            is_user = True
            break
    if not is_user:
        users.execute("INSERT INTO USERS(ID,NAME,USERNAME,BLOCKED) VALUES(?,?,?,?)",(str(msg.chat.id),
                                                                           str(msg.chat.first_name)+" "+str(msg.chat.last_name),
                                                                           "@"+str(msg.chat.username),"false"))
        users.commit()
    users.close()
    bot.send_message(msg.chat.id,"Ø³Ù„Ø§Ù… {} Ø¹Ø²ÛŒØ² !\n\n"
                                 "Ø¨Ø±Ø§ÛŒ Ø§Ø³ØªÙØ§Ø¯Ù‡ Ø§Ø² Ù…Ù† ÙÙ‚Ø· Ú©Ø§ÙÛŒÙ‡ Ú©Ù‡ Ù…ØªÙ†Øª Ø±Ùˆ Ø¨ÙØ±Ø³ØªÛŒ ðŸ˜\n\n"
                                 "Ù…Ù† Ø¨Ù‡ Ø·ÙˆØ± Ø®ÙˆØ¯Ú©Ø§Ø± Ø²Ø¨Ø§Ù†Ø´ Ø±Ùˆ Ø´Ù†Ø§Ø³Ø§ÛŒÛŒ Ù…ÛŒÚ©Ù†Ù… !ðŸ˜Ž\n\n"
                                 "ÙÙ‚Ø· Ø­ÙˆØ§Ø³Øª Ø¨Ø§Ø´Ù‡ Ú©Ù‡ Ù…Ù† ÙÙ‚Ø· Ø¨Ù‡ Ù…ØªÙ† Ø¬ÙˆØ§Ø¨ Ù…ÛŒØ¯Ù…...".format(msg.chat.first_name),reply_markup = start_key)

def translate(bot,update):
    global step
    global text
    text[update.message.chat.id] = update.message.text
    if step == 1 :
        users = sqlite3.connect("users.db")
        users_list = list(users.execute("SELECT ID,BLOCKED FROM USERS"))

        for user in users_list:
            if user[1] != "true":
                try:
                    test_msg = bot.send_message(user[0], update.message.text)
                except:
                    users.execute("UPDATE USERS SET BLOCKED='true' WHERE ID=?", (user[0],))
                    users.commit()
        users.close()
        bot.send_message(update.message.chat.id,"Ø§Ø±Ø³Ø§Ù„ Ø´Ø¯ !")
        step = 0
    else:
        bot.send_message(update.message.chat.id,"Ø²Ø¨Ø§Ù† Ù…Ù‚ØµØ¯ Ø±Ùˆ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù† :",reply_markup = languages)

def answer(bot,update):
    global text
    q = update.callback_query
    update_key = InlineKeyboardMarkup([[bn("ðŸ”„ Ø¨Ø±ÙˆØ²Ø±Ø³Ø§Ù†ÛŒ ðŸ”„", callback_data="update")],
                                      [bn("Ø¨Ø±Ú¯Ø±Ø¯ â¬…ï¸", callback_data="panel")]])

    if q.data == "nothing":
        pass
    elif q.data == "page1":
        q.message.edit_text(q.message.text, reply_markup=languages)
    elif q.data == "page2":
        q.message.edit_text(q.message.text, reply_markup=languages2)
    elif q.data == "page3":
        q.message.edit_text(q.message.text, reply_markup=languages3)
    elif q.data == "nolang":
        bot.answer_callback_query(q.id,"Ø¨Ø±Ø§ÛŒ Ø«Ø¨Øª Ø²Ø¨Ø§Ù†ÛŒ Ú©Ù‡ Ù…ÛŒØ®ÙˆØ§ÛŒ Ø¨Ù‡ Ø³Ø§Ø²Ù†Ø¯Ù‡ Ù¾ÛŒØ§Ù… Ø¨Ø¯Ù‡"
                                       "\nØªØ§ Ø³Ø±ÛŒØ¹ Ø¨Ø±Ø§ØªÙˆÙ† Ø§Ø¶Ø§ÙÙ‡ Ú©Ù†Ù‡ ðŸ˜"
                                       "\nØ§ÛŒÙ† Ù¾Ù†Ø¬Ø±Ù‡ Ø±Ùˆ Ø¨Ø¨Ù†Ø¯ ØªØ§ Ø¨ØªÙˆÙ†ÛŒ Ø¨Ù‡ Ø³Ø§Ø²Ù†Ø¯Ù‡ Ù¾ÛŒØ§Ù… Ø¨Ø¯ÛŒ...",show_alert=True)
        q.message.edit_text("Ø­Ø§Ù„Ø§ Ø¨Ù‡Ù…ÙˆÙ† Ù¾ÛŒØ§Ù… Ø¨Ø¯Ù‡ ØªØ§ Ø²Ø¨Ø§Ù† Ù…ÙˆØ±Ø¯ Ù†Ø¸Ø±Øª Ø±Ùˆ Ø§Ø¯Ø¯ Ú©Ù†ÛŒÙ… ðŸ™‚", reply_markup=nolang_key)
    elif q.data == "check_user":
        started,live = check_user(bot,update)
        q.message.edit_text("ðŸ‘ª ØªØ¹Ø¯Ø§Ø¯ ÛŒÙˆØ²Ø± Ù‡Ø§ÛŒ Ø§Ø³ØªØ§Ø±Øª Ø²Ø¯Ù‡ : {}\nâœ… ØªØ¹Ø¯Ø§Ø¯ ÛŒÙˆØ²Ø± Ù‡Ø§ÛŒ ÙØ¹Ø§Ù„ : {}\n".format(started,live),reply_markup=update_key)
    elif q.data == "panel":
        q.message.edit_text("Ø¨Ú¯Ùˆ Ú†ÛŒÚ©Ø§Ø± Ú©Ù†Ù… :", reply_markup=panel_key)
    elif q.data == "update":
        bot.answer_callback_query(q.id, "Ù„Ø·ÙØ§ Ú©Ù…ÛŒ ØµØ¨Ø± Ú©Ù†ÛŒØ¯...")
        started,live = check_user(bot,update)
        time_zone = pytz.timezone("Asia/Tehran")
        time_now = datetime.datetime.now(time_zone)
        time = time_now.strftime("%H:%M:%S")
        q.message.edit_text("ðŸ‘ª ØªØ¹Ø¯Ø§Ø¯ ÛŒÙˆØ²Ø± Ù‡Ø§ÛŒ Ø§Ø³ØªØ§Ø±Øª Ø²Ø¯Ù‡ : {}\n"
                            "âœ… ØªØ¹Ø¯Ø§Ø¯ ÛŒÙˆØ²Ø± Ù‡Ø§ÛŒ ÙØ¹Ø§Ù„ : {}\n\n"
                            "Ø¢Ø®Ø±ÛŒÙ† Ø¨Ø±ÙˆØ² Ø±Ø³Ø§Ù†ÛŒ : {}".format(started,live,time),reply_markup=update_key)

    elif q.data == "send_user":
        bot.send_message(q.message.chat.id,"Ø­Ø§Ù„Ø§ Ù…ØªÙ†ÛŒ Ø±Ùˆ Ú©Ù‡ Ù…ÛŒØ®ÙˆØ§ÛŒ Ø±Ùˆ Ø¨Ø¯Ù‡ Ø¨ÙØ±Ø³ØªÙ… :")
        global step
        step = 1
    else:
        bot.answer_callback_query(q.id, "Ù„Ø·ÙØ§ Ú©Ù…ÛŒ ØµØ¨Ø± Ú©Ù†ÛŒØ¯...")
        bot.send_message(q.message.chat.id,"Ø§ÛŒÙ† Ù‡Ù… Ø§Ø² Ù…ØªÙ† ØªØ±Ø¬Ù…Ù‡ Ø´Ø¯Ù‡ ðŸ‘‡ðŸ‘‡ðŸ‘‡")
        bot.send_message(q.message.chat.id, tr.translate(str(text[q.message.chat.id]),lang=q.data))

def check_user(bot,update):
    users = sqlite3.connect("users.db")
    users_list = list(users.execute("SELECT ID,BLOCKED FROM USERS"))

    for user in users_list:
        if user[1] != "true":
            try :
                test_msg = bot.send_message(user[0],"Ø§ÛŒÙ† ÙÙ‚Ø· ÛŒÚ© ØªØ³Øª Ù…ÛŒ Ø¨Ø§Ø´Ø¯ØŒÙ„Ø·ÙØ§ Ù†Ø§Ø¯ÛŒØ¯Ù‡ Ø¨Ú¯ÛŒØ±ÛŒØ¯!")
                bot.delete_message(user[0],test_msg.message_id)
            except :
                users.execute("UPDATE USERS SET BLOCKED='true' WHERE ID=?",(user[0],))
                users.commit()
    live_users = list(users.execute("SELECT ID FROM USERS WHERE BLOCKED='false'"))
    users.close()
    return (str(len(users_list)),str(len(live_users)))


def panel(bot,update):
    if update.message.chat.id in admins:
        bot.send_message(update.message.chat.id,"Ø¨Ú¯Ùˆ Ú†ÛŒÚ©Ø§Ø± Ú©Ù†Ù… :",reply_markup = panel_key)
u = Updater(token)
u.dispatcher.add_handler(CommandHandler("start",start))
u.dispatcher.add_handler(CommandHandler("panel",panel))
u.dispatcher.add_handler(MessageHandler(Filters.text,translate))
u.dispatcher.add_handler(CallbackQueryHandler(answer))
print("started ...")
u.start_polling()
u.idle()
