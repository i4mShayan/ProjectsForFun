import logging
from telegram import *
from telegram.ext import *
from telegram.error import NetworkError, Unauthorized

bot_username = ""
token=""
admin=0
userinfo = {}
ans = [None]*10
ans[0] = [['صبح'], ['عصر و غروب'], ['شب']]
ans[1] = [['نسبتاً سریع، با قدم های بلند'],['نسبتاً سریع، با قدمهای کوتاه ولی تند و پشت سر هم'],['آهسته تر، با سری صاف روبرو'],['آهسته و سربه زیر'],['خیلی آهسته']]
ans[2] = [['می ایستید و دست به سینه حرف می زنید'],['دستها را در هم قلاب می کنید'],['یک یا هر دو دست را در پهلو می گذارید'],['دست به شخصی که با او صحبت می کنید، می زنید'],['با گوش خود بازی می کنید، به چانه تان دست می زنید یا موهایتان را صاف میکنید']]
ans[3] = [['زانوها خم و پاها تقریباً کنار هم'],['چهارزانو'],['پای صاف و دراز به بیرون'],['یک پا زیر دیگری خم']]
ans[4] = [['خنده ای بلند که نشان دهد چقدر موضوع جالب بوده'],['خنده، اما نه بلند'],['با پوزخند کوچک'],['لبخند بزرگ'],['لبخند کوچک']]
ans[5] = [[' با صدای بلند سلام و حرکتی که همه متوجه شما شوند، وارد می شوید'],['با صدای آرامتر سلام می کنید و سریع به دنبال شخصی که می شناسید، می گردید'],['با پوزخند کوچک'],['در حد امکان آرام وارد می شوید، سعی می کنید به نظر سایرین نیایید']]
ans[6] = [['از وقفه ایجاد شده راضی هستید و از آن استقبال می کنید'],['بسختی ناراحت می شوید'],['حالتی بینابین این ۲ حالت ایجاد می شود']]
ans[7] = [['قرمز یا نارنجی'],['سیاه'],['زرد یا آبی کمرنگ'],['سبز'],['آبی تیره یا ارغوانی'],['سفید'],['قهوه ای، خاکستری، بنفش']]
ans[8] = [['به پشت'],['روی شکم (دمر)'],['به پهلو و کمی خم و دایره ای'],['سر بر روی یک دست'],['سر زیر پتو یا ملافه...']]
ans[9] = [['از جایی می افتید.'],['مشغول جنگ و دعوا هستید.'],['به دنبال کسی یا چیزی هستید.'],['پرواز می کنید یا در آب غوطه ورید.'],['اصلاً خواب نمی بینید.'],['معمولاً خواب های خوش می بینید']]
question = [None]*10
question[0] = '1) چه موقع از روز بهترین و آرام ترین احساس را دارید؟'
question[1] = '۲) معمولاً چگونه راه می روید؟'
question[2] = '۳) وقتی با دیگران صحبت می کنید؛'
question[3] = '۴) وقتی آرام هستید، چگونه می نشینید؟'
question[4] = '۵) وقتی چیزی واقعاً برای شما جالب است، چگونه واکنش نشان می دهید؟'
question[5] = '۶) وقتی وارد یک میهمانی یا جمع می شوید؛'
question[6] = '۷) سخت مشغول کاری هستید، بر آن تمرکز دارید، اما ناگهان دلیلی یا شخصی آن را قطع می کند؛'
question[7] = '۸) کدامیک از مجموعه رنگ های زیر را بیشتر دوست دارید؟'
question[8] = '۹) وقتی در رختخواب هستید (در شب) در آخرین لحظات پیش از خواب، در چه حالتی دراز می کشید؟'
question[9] = '۱۰) آیا شما غالباً خواب می بینید که:'

Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8,Q9,Q10,Finish=range(11)
def start(update, context):
    reply_keyboard = [['💠 شروع کن 💠']]
    context.message.reply_text('سلام {} عزیز!\n'
    'این آزمون شامل 10 سوال استاندارد چند گزینه ایست.\n'
    'سعی کنید با صداقت کامل و با دقت به سوالات جواب بدهید.\n'
    'موفق باشید!😐🔥'.format(context.message.from_user["first_name"]),
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return Q1


def q1(update, context):
    context.message.reply_text(question[0],
                              reply_markup=ReplyKeyboardMarkup(ans[0], one_time_keyboard=True))

    return Q2


def q2(update, context):
    user = context.message.from_user
    userinfo[user.id]=[None]*10
    userinfo[user.id][0]=context.message.text
    context.message.reply_text(question[1],
                              reply_markup=ReplyKeyboardMarkup(ans[1], one_time_keyboard=True))

    return Q3

def q3(update, context):
    user = context.message.from_user
    userinfo[user.id][1]=context.message.text
    context.message.reply_text(question[2],
                              reply_markup=ReplyKeyboardMarkup(ans[2], one_time_keyboard=True))

    return Q4

def q4(update, context):
    user = context.message.from_user
    userinfo[user.id][2]=context.message.text
    context.message.reply_text(question[3],
                              reply_markup=ReplyKeyboardMarkup(ans[3], one_time_keyboard=True))
    return Q5

def q5(update, context):
    user = context.message.from_user
    userinfo[user.id][3]=context.message.text
    context.message.reply_text(question[4],
                              reply_markup=ReplyKeyboardMarkup(ans[4], one_time_keyboard=True))
    return Q6

def q6(update, context):
    user = context.message.from_user
    userinfo[user.id][4]=context.message.text
    context.message.reply_text(question[5],
                              reply_markup=ReplyKeyboardMarkup(ans[5], one_time_keyboard=True))
    return Q7
    
def q7(update, context):
    user = context.message.from_user
    userinfo[user.id][5]=context.message.text
    context.message.reply_text(question[6],
                              reply_markup=ReplyKeyboardMarkup(ans[6], one_time_keyboard=True))
    return Q8

def q8(update, context):
    user = context.message.from_user
    userinfo[user.id][6]=context.message.text
    context.message.reply_text(question[7],
                              reply_markup=ReplyKeyboardMarkup(ans[7], one_time_keyboard=True))
    return Q9

def q9(update, context):
    user = context.message.from_user
    userinfo[user.id][7]=context.message.text
    context.message.reply_text(question[8],
                              reply_markup=ReplyKeyboardMarkup(ans[8], one_time_keyboard=True))
    return Q10
def q10(update, context):
    user = context.message.from_user
    userinfo[user.id][8]=context.message.text
    context.message.reply_text(question[9],
                              reply_markup=ReplyKeyboardMarkup(ans[9], one_time_keyboard=True))
    return Finish

def fin(update, context):
    user = context.message.from_user
    userinfo[user.id][9]=context.message.text
    uans = userinfo[user.id]
    mark=0
    # 1st
    if(ans[0][0][0] == uans[0]):
        mark+=2
    elif(ans[0][1][0] == uans[0]):
        mark+=4
    elif(ans[0][2][0] == uans[0]):
        mark+=6
    # 2nd
    if(ans[1][0][0] == uans[1]):
        mark+=6
    elif(ans[1][1][0] == uans[1]):
        mark+=4
    elif(ans[1][2][0] == uans[1]):
        mark+=7
    elif(ans[1][3][0] == uans[1]):
        mark+=2
    elif(ans[1][4][0] == uans[1]):
        mark+=1
    # 3rd
    if(ans[2][0][0] == uans[2]):
        mark+=4
    elif(ans[2][1][0] == uans[2]):
        mark+=2
    elif(ans[2][2][0] == uans[2]):
        mark+=5
    elif(ans[2][3][0] == uans[2]):
        mark+=7
    elif(ans[2][4][0] == uans[2]):
        mark+=6
    # 4th
    if(ans[3][0][0] == uans[3]):
        mark+=4
    elif(ans[3][1][0] == uans[3]):
        mark+=6
    elif(ans[3][2][0] == uans[3]):
        mark+=2
    elif(ans[3][3][0] == uans[3]):
        mark+=1
    # 5th
    if(ans[4][0][0] == uans[4]):
        mark+=6
    elif(ans[4][1][0] == uans[4]):
        mark+=4
    elif(ans[4][2][0] == uans[4]):
        mark+=3
    elif(ans[4][3][0] == uans[4]):
        mark+=5
    elif(ans[4][4][0] == uans[4]):
        mark+=2
    # 6th
    if(ans[5][0][0] == uans[5]):
        mark+=6
    elif(ans[5][1][0] == uans[5]):
        mark+=4
    elif(ans[5][2][0] == uans[5]):
        mark+=2
    # 7th
    if(ans[6][0][0] == uans[6]):
        mark+=6
    elif(ans[6][1][0] == uans[6]):
        mark+=2
    elif(ans[6][2][0] == uans[6]):
        mark+=4
    # 8th
    if(ans[7][0][0] == uans[7]):
        mark+=6
    elif(ans[7][1][0] == uans[7]):
        mark+=7
    elif(ans[7][2][0] == uans[7]):
        mark+=5
    elif(ans[7][3][0] == uans[7]):
        mark+=4
    elif(ans[7][4][0] == uans[7]):
        mark+=3
    elif(ans[7][5][0] == uans[7]):
        mark+=2
    elif(ans[7][6][0] == uans[7]):
        mark+=1
    # 9th
    if(ans[8][0][0] == uans[8]):
        mark+=7
    elif(ans[8][1][0] == uans[8]):
        mark+=6
    elif(ans[8][2][0] == uans[8]):
        mark+=4
    elif(ans[8][3][0] == uans[8]):
        mark+=2
    elif(ans[8][4][0] == uans[8]):
        mark+=1
    # 10th
    if(ans[9][0][0] == uans[9]):
        mark+=4
    elif(ans[9][1][0] == uans[9]):
        mark+=2
    elif(ans[9][2][0] == uans[9]):
        mark+=3
    elif(ans[9][3][0] == uans[9]):
        mark+=5
    elif(ans[9][4][0] == uans[9]):
        mark+=6
    elif(ans[9][5][0] == uans[9]):
        mark+=1
    result = ""
    for i in range(10):
        result += question[i] + "\n💢 " + uans[i] + "\n"
    result += 'نتیجه:\n⬇️⬇️⬇️⬇️\n'
    if mark>60:
        result += 'دیگران در ارتباط و رفتار با شما شدیداً مراقب و هوشیار هستند آنها شما را مغرور، خودمحور و بی نهایت سلطه جو می دانند، گرچه شما را تحسین می کنند و به ظ اهر می گویند«کاش من جای تو بودم!!» اما معمولاً به شما اعتماد ندارند و نسبت به ایجاد رابطه ای عمیق و دوستانه بی میل و فراری هستند.'
    elif mark>=51:
        result += 'به خود امیدوار باشید ، دیگران شما را بانشاط، سرزنده، سرگرم کننده و جالب و جذاب می بینند. شما دائماً مرکز توجه جمع هستید و از تعادل رفتاری خوبی بهره مند هستید. فردی مهربان، ملاحظه کار و فهمیده به نظر می رسید. قادر هستید به موقع باعث شادی و خوشی دوستانتان شوید و اسباب هلهله و خنده آنها را فراهم کنید و در همان شرایط و در صورت لزومبهترین کمک بر اعضای گروه هستید.'
    elif mark>=31:
        result += 'بدانید در نظر سایرین معقول، هوشیار، دقیق ، ملاحظه کار و اهل عمل هستید.. همه می دانند شما باهوش و با استعداد هستید اما مهمتر از همه فروتن و متواضع هستید. به سرعت و سادگی با دیگران باب دوستی را باز نمی کنید. اما اگر با کسی دوست شوید صادق، باوفا و وظیفه شناس هستید. اما انتظار بازگشت این صداقت و صمیمیت از طرف دوستانتان را دارید گرچه سخت دوست می شوید اما سخت تر دوستی ها را رها می کنید.'
    elif mark>=21:
        result += 'در نظر سایرین فردی زحمت کش هستید اما متأسفانه گاهی اوقات ایرادگیر هستید. شما بسیار بسیار محتاط و بی نهایت ملاحظه کار به نظر می رسید. زحمتکشی که در کمال آرامش و با صرف زمان زیاد در جمع بار دیگران را بردوش می کشد و بدون فکر و براساس تحریک لحظه ای و آنی هرگز نظر نمی دهد. دیگران می دانند شما همیشه تمام جوانب کارها را می سنجید و سپس تصمیم می گیرید.'
    else:
        result += 'دیگران شما را خجالتی، عصبی و آدمی شکاک و دودل می دانند شخصی که همیشه سایرین به عوض او فکر می کنند، برایش تصمیم می گیرند و از او مراقبت می کنند. کسی که اصلاً تمایل به درگیرشدن در کارهای گروهی و ارتباط با افراد دیگر را ندارد!'
    update.send_message(admin, '@' + user['username'] + "\n" + result)
    update.send_message(user.id, result)
                


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
updater = Updater(token)

updater.dispatcher.add_error_handler(error)

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],

    states={
        Q1: [MessageHandler(Filters.text, q1)],
        Q2: [MessageHandler(Filters.text, q2)],
        Q3: [MessageHandler(Filters.text, q3)],
        Q4: [MessageHandler(Filters.text, q4)],
        Q5: [MessageHandler(Filters.text, q5)],
        Q6: [MessageHandler(Filters.text, q6)],
        Q7: [MessageHandler(Filters.text, q7)],
        Q8: [MessageHandler(Filters.text, q8)],
        Q9: [MessageHandler(Filters.text, q9)],
        Q10: [MessageHandler(Filters.text, q10)],
        Finish: [MessageHandler(Filters.text, fin)]
    },
    fallbacks=[CommandHandler('start', start)]
)
updater.dispatcher.add_handler(conv_handler)

print("robot started...")
updater.start_polling()
updater.idle()
