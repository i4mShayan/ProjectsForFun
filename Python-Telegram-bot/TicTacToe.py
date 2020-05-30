import logging
from telegram import *
from telegram.ext import *
from telegram.error import NetworkError, Unauthorized

global player1, player2, current_player, game_over, board
def start(bot,update):
    global player1
    global game_over
    global board
    board = ["⚪️"] * 9
    game_over=0
    player1=update.message.from_user
    if update.message.chat.type in ["group", "supergroup"]:
        button = [[InlineKeyboardButton(text="من پایم",callback_data="player2")]]
        keyboard = InlineKeyboardMarkup(button)
        bot.send_message(update.message.chat_id,"کی پایست با {} بازی کنه؟".format(player1["first_name"]),reply_markup=keyboard)

def hand(bot,update,job_queue):
    global player1
    global player2
    global current_player
    global game_over
    global board
    query = update.callback_query
    keyboard=None
    p1=InlineKeyboardButton(text=board[0],callback_data="z1")
    p2=InlineKeyboardButton(text=board[1],callback_data="z2")
    p3=InlineKeyboardButton(text=board[2],callback_data="z3")
    p4=InlineKeyboardButton(text=board[3],callback_data="z4")
    p5=InlineKeyboardButton(text=board[4],callback_data="z5")
    p6=InlineKeyboardButton(text=board[5],callback_data="z6")
    p7=InlineKeyboardButton(text=board[6],callback_data="z7")
    p8=InlineKeyboardButton(text=board[7],callback_data="z8")
    p9=InlineKeyboardButton(text=board[8],callback_data="z9")
    button = [[p1,p2,p3], [p4,p5,p6], [p7,p8,p9]]
    keyboard = InlineKeyboardMarkup(button)
    if query.data=="player2":
        player2=query.from_user
        current_player=player1
        bot.edit_message_text(text=""" بازیکنان : {} 💢 {}\n
        نوبت: {}
        """.format(player1["first_name"], player2["first_name"], current_player["first_name"])
        ,chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=keyboard)

    elif query.data[0] == 'z':
        def check(): #returns 1 if game is over and 2 if is draw
            flag = 1
            for i in range(9):
                if(board[i] == "⚪️"):
                    flag=0
                    break
            if flag:
                return 2
            if ((board[2]!="⚪️" and board[2]==board[4] and board[4]==board[6])
            or (board[0]!="⚪️" and board[0]==board[4] and board[4]==board[8])
            or (board[0]!="⚪️" and board[0]==board[1] and board[1]==board[2])
            or (board[0]!="⚪️" and board[0]==board[3] and board[3]==board[6])
            or (board[1]!="⚪️" and board[1]==board[4] and board[4]==board[7])
            or (board[3]!="⚪️" and board[3]==board[4] and board[4]==board[5])
            or (board[2]!="⚪️" and board[2]==board[5] and board[5]==board[8])
            or (board[6]!="⚪️" and board[6]==board[7] and board[7]==board[8])):
                return 1
            return 0


        if query.from_user.id == current_player.id:
            place=int(query.data[1])
            if(game_over):
                bot.answer_callback_query(query.id,"بازی تموم شده!")
            elif(board[place-1]=="⚪️"):
                if(current_player==player1):
                    board[place-1]="🔵"
                    current_player=player2
                else:
                    board[place-1]="🔴"
                    current_player=player1
                p1=InlineKeyboardButton(text=board[0],callback_data="z1")
                p2=InlineKeyboardButton(text=board[1],callback_data="z2")
                p3=InlineKeyboardButton(text=board[2],callback_data="z3")
                p4=InlineKeyboardButton(text=board[3],callback_data="z4")
                p5=InlineKeyboardButton(text=board[4],callback_data="z5")
                p6=InlineKeyboardButton(text=board[5],callback_data="z6")
                p7=InlineKeyboardButton(text=board[6],callback_data="z7")
                p8=InlineKeyboardButton(text=board[7],callback_data="z8")
                p9=InlineKeyboardButton(text=board[8],callback_data="z9")
                button = [[p1,p2,p3], [p4,p5,p6], [p7,p8,p9]]
                keyboard = InlineKeyboardMarkup(button)
                bot.edit_message_text(text=""" بازیکنان : {} 💢 {} \n
                نوبت: {}
                """.format(player1["first_name"], player2["first_name"], current_player["first_name"])
                ,chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=keyboard)
                is_over=check()
                if is_over:
                    game_over=1
                    if(is_over==1):
                        bot.edit_message_text(text="بازی تموم شد!\nبرنده : {}".format(current_player["first_name"]),chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=keyboard)
                    else:
                        bot.edit_message_text(text="بازی بین {} و {}\nمساوی شد!".format(player1["first_name"], player2["first_name"]),chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=keyboard)
            else:
                bot.answer_callback_query(query.id,"این خانه سفید نیست!")
        else:
            if(query.data.from_user.id == player1 or query.data.from_user.id == player2):
                bot.answer_callback_query(query.id,"نوبت شما نیست!")
            else:
                bot.answer_callback_query(query.id,"شما تو بازی نیستید!")



def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

token=""
updater = Updater(token)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(hand,pass_job_queue=True))
updater.dispatcher.add_error_handler(error)

print("robot started..")
updater.start_polling()
updater.idle()
