
import time
import telepot
from telepot.loop import MessageLoop
import keyboards
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

import filter
import ticketToday
import insertCompetence

import sys
sys.path.append('../conn')
import user




############################################################
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def on_chat_message(msg):
    first_name = msg['from']['first_name']
    last_name = msg['from']['last_name']
    user_id = msg['from']['id']
    content_type, chat_type, chat_id = telepot.glance(msg)
    print('Chat Message:', content_type, chat_type, chat_id)
    print(content_type)
    if content_type == 'text':
       if msg['text'] == '/start':
            keyboard = keyboards.getKeyboard()
            if user.insertUser(user_id, first_name, last_name):
                bot.sendMessage(chat_id, 'Registrazione effettuata correttamente!', reply_markup=keyboard)   
            else:
                bot.sendMessage(chat_id, 'Sei nel menu principale', reply_markup=keyboard)   

       elif msg['text'] == '🖍 Crea filtro x Competenze':
             comp_first, comp_second = filter.createCompetence()
             bot.sendMessage(chat_id,  comp_first)
             bot.sendMessage(chat_id,  comp_second)

       elif msg['text'] == '🖍 Crea filtro x Cliente': 
             bot.sendMessage(chat_id, 'dua' )

       elif str(msg['text']).startswith("/_id_c_"):  
            bot.sendMessage(chat_id, insertCompetence.manageCompetence(chat_id,str(msg['text'])[7:]) )

       elif msg['text'] == '📌 I mie filtri': 
             filtersList = filter.getMyFilters(chat_id)
             if len(filtersList) <1:
                bot.sendMessage(chat_id, "Non hai creato ancora un filtro!" )
             else:
                bot.sendMessage(chat_id, filtersList )

       elif msg['text'] == '✖ Cancella filtro': 
             filterToBeDeletedList = filter.showFilterToBeDelete(chat_id)
             if len(filterToBeDeletedList)<1:
                bot.sendMessage(chat_id,  "Non esistono filtri da cancellare")
             else:
                bot.sendMessage(chat_id,  ) 

       elif str(msg['text']).startswith("/Competenza_id_cf_"): 
             bot.sendMessage(chat_id, filter.deleteFilter(chat_id, str(msg['text'])[18:] ) ) 

       elif msg['text'] == '🕘 Ticket oggi':
             listOfStrings =  ticketToday.getTicketToday(chat_id)
             for ticketItem in listOfStrings:
                bot.sendMessage(chat_id, ticketItem)  
             if len(listOfStrings) < 1:
                bot.sendMessage(chat_id, "Non esistono ticket oggi")
    
       else:
             bot.sendMessage(chat_id, 'Commando non riconosciuto! Premere /start per iniziare.') 

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
   # print('Callback Query:', query_id, from_id, query_data)
    bot.answerCallbackQuery(query_id, text='Got it')
   #  file="das/" + query_data
   # bot.sendDocument(chat_id=from_id, document=open(file, 'rb')) 
    print(query_data)




bot = telepot.Bot("5424429330:AAHMMqsta1BeYhWtl5Pb0Mvbj_1B9Gn8YRg")
MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread()
print('Listening ...')
starttime = time.time()

while 1:
    print("\n tick ogni 10 sec \n")
    #    bot.sendMessage(145645559, found )
    tids = user.getUsers()
    for u in tids:
        newTicketList = ticketToday.getTicketTodayForNotification(int(u[0]))
        for ticket in newTicketList:
            bot.sendMessage(int(u[0]), ticket)

    time.sleep(10)
    #time.sleep((60.0 * 1) - ((time.time() - starttime) % 60.ticketToday.getTicketToday(chat_id)ticketToday.getTicketToday(chat_id)0))