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
start_key = InlineKeyboardMarkup([[bn("📢 چنل سازنده 📢", url="t.me/OneDev")],
                                  [bn("👨‍💻 برنامه نویس 👨‍💻", url="t.me/a_Coder"),
                                   bn("🔅 پیام رسان 🔅", url="t.me/OneDev_bot")],
                                  [bn("🤖 ربات های دیگر 🤖", url="t.me/OneDevs")]])

languages = InlineKeyboardMarkup([
                                      [bn("1️⃣ صفحه اول 1️⃣",callback_data="nothing")],
                                      [bn("➖➖➖➖➖➖➖➖➖", callback_data="nothing")],
                                      [bn("🇮🇷 فارسی 🇮🇷",callback_data="fa")],
                                      [bn("🇺🇸 انگلیسی 🇬🇧",callback_data="en")],
                                      [bn("🇩🇪 آلمانی 🇩🇪", callback_data="de")],
                                      [bn("🇫🇷 فرانسوی 🇫🇷", callback_data="fr")],
                                      [bn("🇦🇪 عربی 🇦🇪", callback_data="ar")],
                                      [bn("🇪🇸 اسپانیایی 🇪🇸", callback_data="es")],
                                      [bn("🇨🇳 چینی ساده 🇨🇳",callback_data="zh-CN")],
                                      [bn("🇭🇰 چینی سنتی 🇭🇰", callback_data="zh-TW")],
                                      [bn("🇯🇵 ژاپنی 🇯🇵", callback_data="ja")],
                                      [bn("🇰🇷 کره ای 🇰🇷", callback_data="ko")],
                                      [bn("🇮🇹 ایتالیایی 🇮🇹", callback_data="it")],
                                      [bn("🇹🇷 ترکی 🇹🇷", callback_data="tr")],
                                      [bn("➖➖➖➖➖➖➖➖➖", callback_data="nothing")],
                                      [bn("️➡️ بعدی️", callback_data="page2")]
                                      ])

languages2 = InlineKeyboardMarkup([
    [bn("2️⃣ صفحه دوم 2️⃣", callback_data="nothing")],
    [bn("➖➖➖➖➖➖➖➖➖", callback_data="nothing")],
    [bn("آفریقایی", callback_data="af"), bn("آلبانی", callback_data="sq")],
    [bn("امریکایی", callback_data="am"), bn("کبوانویی", callback_data="ceb")],
    [bn("ارمنی", callback_data="hy"), bn("آذربایجانی", callback_data="az")],
    [bn("باسکی", callback_data="eu"), bn("بلاروسی", callback_data="be")],
    [bn("بنگالی", callback_data="bn"), bn("بوسنی", callback_data="bs")],
    [bn("بلغاری", callback_data="bg"), bn("کاتالانی", callback_data="ca")],
    [bn("چیکوایی", callback_data="ny"), bn("مرجانی", callback_data="co")],
    [bn("کرواتی", callback_data="hr"), bn("چک", callback_data="cs")],
    [bn("دانمارکی", callback_data="da"), bn("هلندی", callback_data="nl")],
    [bn("اسپرانتو", callback_data="eo"), bn("ارمنستانی", callback_data="et")],
    [bn("فیلیپینی", callback_data="tl"), bn("فنلاندی", callback_data="fi")],
    [bn("فریسین", callback_data="fy"), bn("گالیکسی", callback_data="gl")],
    [bn("➖➖➖➖➖➖➖➖➖", callback_data="nothing")],
    [bn("قبلی ⬅️", callback_data="page1"),bn("➡️ بعدی️", callback_data="page3")]
])
languages3 = InlineKeyboardMarkup([
                                  [bn(" 3️⃣ صفحه سوم 3️⃣", callback_data="nothing")],
                                  [bn("➖➖➖➖➖➖➖➖➖", callback_data="nothing")],
                                  [bn("زبانی که میخواستی رو پیدا نکردی؟ 😓", callback_data="nolang")],
                                  [bn("➖➖➖➖➖➖➖➖➖", callback_data="nothing")],
                                  [bn("قبلی ⬅️", callback_data="page2"), bn("🏠 صفحه اول️ 🏠", callback_data="page1")]
                                  ])

nolang_key = InlineKeyboardMarkup([[bn("📢 چنل سازنده 📢", url="t.me/OneDev")],
                                  [bn("👨‍💻 برنامه نویس 👨‍💻", url="t.me/a_Coder"),
                                   bn("🔅 پیام رسان 🔅", url="t.me/OneDev_bot")],
                                  [bn("➖➖➖➖➖➖➖➖➖", callback_data="nothing")],
                                  [bn("➰ انتخاب زبان مقصد ➰", callback_data="page1"),]
                                  ])
panel_key = InlineKeyboardMarkup([
    [bn("👀 تعداد کاربران 👀",callback_data="check_user")],
    [bn("🗣 ارسال پیام به کاربران 🗣",callback_data="send_user")]
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
    bot.send_message(msg.chat.id,"سلام {} عزیز !\n\n"
                                 "برای استفاده از من فقط کافیه که متنت رو بفرستی 😁\n\n"
                                 "من به طور خودکار زبانش رو شناسایی میکنم !😎\n\n"
                                 "فقط حواست باشه که من فقط به متن جواب میدم...".format(msg.chat.first_name),reply_markup = start_key)

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
        bot.send_message(update.message.chat.id,"ارسال شد !")
        step = 0
    else:
        bot.send_message(update.message.chat.id,"زبان مقصد رو انتخاب کن :",reply_markup = languages)

def answer(bot,update):
    global text
    q = update.callback_query
    update_key = InlineKeyboardMarkup([[bn("🔄 بروزرسانی 🔄", callback_data="update")],
                                      [bn("برگرد ⬅️", callback_data="panel")]])

    if q.data == "nothing":
        pass
    elif q.data == "page1":
        q.message.edit_text(q.message.text, reply_markup=languages)
    elif q.data == "page2":
        q.message.edit_text(q.message.text, reply_markup=languages2)
    elif q.data == "page3":
        q.message.edit_text(q.message.text, reply_markup=languages3)
    elif q.data == "nolang":
        bot.answer_callback_query(q.id,"برای ثبت زبانی که میخوای به سازنده پیام بده"
                                       "\nتا سریع براتون اضافه کنه 😁"
                                       "\nاین پنجره رو ببند تا بتونی به سازنده پیام بدی...",show_alert=True)
        q.message.edit_text("حالا بهمون پیام بده تا زبان مورد نظرت رو ادد کنیم 🙂", reply_markup=nolang_key)
    elif q.data == "check_user":
        started,live = check_user(bot,update)
        q.message.edit_text("👪 تعداد یوزر های استارت زده : {}\n✅ تعداد یوزر های فعال : {}\n".format(started,live),reply_markup=update_key)
    elif q.data == "panel":
        q.message.edit_text("بگو چیکار کنم :", reply_markup=panel_key)
    elif q.data == "update":
        bot.answer_callback_query(q.id, "لطفا کمی صبر کنید...")
        started,live = check_user(bot,update)
        time_zone = pytz.timezone("Asia/Tehran")
        time_now = datetime.datetime.now(time_zone)
        time = time_now.strftime("%H:%M:%S")
        q.message.edit_text("👪 تعداد یوزر های استارت زده : {}\n"
                            "✅ تعداد یوزر های فعال : {}\n\n"
                            "آخرین بروز رسانی : {}".format(started,live,time),reply_markup=update_key)

    elif q.data == "send_user":
        bot.send_message(q.message.chat.id,"حالا متنی رو که میخوای رو بده بفرستم :")
        global step
        step = 1
    else:
        bot.answer_callback_query(q.id, "لطفا کمی صبر کنید...")
        bot.send_message(q.message.chat.id,"این هم از متن ترجمه شده 👇👇👇")
        bot.send_message(q.message.chat.id, tr.translate(str(text[q.message.chat.id]),lang=q.data))

def check_user(bot,update):
    users = sqlite3.connect("users.db")
    users_list = list(users.execute("SELECT ID,BLOCKED FROM USERS"))

    for user in users_list:
        if user[1] != "true":
            try :
                test_msg = bot.send_message(user[0],"این فقط یک تست می باشد،لطفا نادیده بگیرید!")
                bot.delete_message(user[0],test_msg.message_id)
            except :
                users.execute("UPDATE USERS SET BLOCKED='true' WHERE ID=?",(user[0],))
                users.commit()
    live_users = list(users.execute("SELECT ID FROM USERS WHERE BLOCKED='false'"))
    users.close()
    return (str(len(users_list)),str(len(live_users)))


def panel(bot,update):
    if update.message.chat.id in admins:
        bot.send_message(update.message.chat.id,"بگو چیکار کنم :",reply_markup = panel_key)
u = Updater(token)
u.dispatcher.add_handler(CommandHandler("start",start))
u.dispatcher.add_handler(CommandHandler("panel",panel))
u.dispatcher.add_handler(MessageHandler(Filters.text,translate))
u.dispatcher.add_handler(CallbackQueryHandler(answer))
print("started ...")
u.start_polling()
u.idle()
