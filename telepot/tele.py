
from lib2to3.pgen2 import driver
import os
import time
import telepot
from telepot.loop import MessageLoop
#from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import keyboards

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
   #  last_name = msg['from']['last_name']
    last_name = "noname"
    if  "last_name" in msg['from']:
        last_name = msg['from']['last_name']
    user_id = msg['from']['id']
    content_type, chat_type, chat_id = telepot.glance(msg)
    print('Chat Message:', last_name, first_name, chat_id)
    print(content_type)
    if content_type == 'text':
       if msg['text'] == '/start':
            keyboard = keyboards.getKeyboard()
            if user.insertUser(user_id, first_name, last_name):
                bot.sendMessage(chat_id, 'Registrazione effettuata correttamente!', reply_markup=keyboard) 
                bot.sendDocument(chat_id=chat_id, document=open("gifs/welcome.gif", 'rb'))
                bot.sendMessage(145645559, "Utente nuovo: [ " + str(user_id) + " " + first_name+ " "+ last_name + " ]")
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
                bot.sendMessage(chat_id,  filterToBeDeletedList) 

       elif str(msg['text']).startswith("/Competenza_id_cf_"): 
             bot.sendMessage(chat_id, filter.deleteFilter(chat_id, str(msg['text'])[18:] ) ) 

       elif msg['text'] == '🕘 Ticket oggi':
             listOfStrings =  ticketToday.getTicketToday(chat_id)
             for ticketItem in listOfStrings:
                if len(ticketItem) > 4000:
                   firstpart, secondpart = ticketItem[:int(len(ticketItem)/2)], ticketItem[int(len(ticketItem)/2):]
                   bot.sendMessage(chat_id, firstpart, parse_mode='HTML')
                   bot.sendMessage(chat_id, secondpart, parse_mode='HTML')
                else:
                   bot.sendMessage(chat_id, ticketItem, parse_mode='HTML') 
             if len(listOfStrings) < 1:
                bot.sendMessage(chat_id, "Non esistono ticket oggi")

       elif msg['text'] == '🗂 Ticket ultimi 20': 
             listOfStrings =  ticketToday.getTicketLast20(chat_id)
             for ticketItem in listOfStrings:
                if len(ticketItem) > 4000:
                   firstpart, secondpart = ticketItem[:int(len(ticketItem)/2)], ticketItem[int(len(ticketItem)/2):]
                   bot.sendMessage(chat_id, firstpart, parse_mode='HTML')
                   bot.sendMessage(chat_id, secondpart, parse_mode='HTML')
                else:
                   bot.sendMessage(chat_id, ticketItem, parse_mode='HTML')
             if len(listOfStrings) < 1:
                bot.sendMessage(chat_id, "Non esistono ticket")

      
       elif str(msg['text']).startswith("/Ticket_dettaglio_"): 
             ticketId = str(msg['text'])[18:] 
             bot.sendMessage(chat_id, "Attendere per favore, sto caricando i dettagli per il ticket <b>" + ticketId +"</b> ....", parse_mode='HTML')
             # Send feedback
             bot.sendMessage(145645559, "📌📌📌📌📌 \n Aperto Dettaglio Ticket nr: " + ticketId + "  [ " + str(user_id) + " " + first_name+ " "+ last_name + " ]")

             readyPdf = ticketToday.getDetailTicket(ticketId)
            #  pdf_file = "json/" + str(ticketId) + "_details.pdf"
             html_file = "json/" + str(ticketId) + "_details.html"
             if readyPdf:
                bot.sendDocument(chat_id=chat_id, document=open(html_file, 'rb'), parse_mode='HTML')
                if os.path.exists(html_file):
                   os.remove(html_file)
                  #  os.remove(pdf_file)
             else:
                bot.sendMessage(chat_id, "Non è stato possibile scaricare i dettagli")
    
       else:
             bot.sendMessage(chat_id, 'Commando non riconosciuto! Premere /start per iniziare.') 

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
   # print('Callback Query:', query_id, from_id, query_data)
    bot.answerCallbackQuery(query_id, text='Got it')
   #  file="das/" + query_data
   # bot.sendDocument(chat_id=from_id, document=open(file, 'rb')) 
    print(query_data)



test = "5528961366:AAEiCxFr3VwObL3c1zzUXyTAZYRecBZMlWM"
prod = "5424429330:AAHMMqsta1BeYhWtl5Pb0Mvbj_1B9Gn8YRg"
bot = telepot.Bot(prod)

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