
from lib2to3.pgen2 import driver
import os
import time
import telepot
from telepot.loop import MessageLoop
import keyboards


import ticketToday
import insertCompetence


import sys
sys.path.append('../conn')
import user
# sys.path.append('../telepot')
import filter
sys.path.append('../api')
import phrase_similarity






############################################################
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def on_chat_message(msg):
   
   try:
    first_name = msg['from']['first_name']
   #  last_name = msg['from']['last_name']
    last_name = "noname"
    if  "last_name" in msg['from']:
        last_name = msg['from']['last_name']
    user_id = msg['from']['id']
    content_type, chat_type, chat_id = telepot.glance(msg)
    print('Chat Message:', last_name, first_name, chat_id)
    print(content_type)

    # Always check if user has been inserted and authenticated successfully
    # Block only if the user is inserted and the status is "P" pending 
    userChecked = user.getUserByTid(user_id)
    if userChecked and (userChecked[0][3]) == 'P':
                   bot.sendMessage(user_id, "In attesa che un amministratore accetti la sua richiesta \n Per favore attendere a breve sarà approvata") 
                   bot.sendMessage(145645559, "🆕🆕🆕🆕🆕🆕🆕 Utente nuovo: [ " + str(user_id) + " " + first_name+ " "+ last_name + " ] Approva qui: \n" + "/Approval_"+ str(chat_id))
                   return
    
    if content_type == 'text':
       
       if msg['text'] == '/start':
            keyboard = keyboards.getKeyboard()
            # If user exists it shows the main meny
            if user.insertUser(user_id, first_name, last_name):
                bot.sendMessage(chat_id, 'Registrazione effettuata correttamente. \n Per favore attendere che un amministratore approvi la sua richiesta') 
                bot.sendDocument(chat_id=chat_id, document=open("gifs/welcome.gif", 'rb'))
                bot.sendMessage(145645559, "Utente nuovo: [ " + str(user_id) + " " + first_name+ " "+ last_name + " ] Approva qui: \n" + "/Approval_"+ str(chat_id))
                return           
            else:
                bot.sendMessage(chat_id, 'Sei nel menu principale', reply_markup=keyboard)  

       elif str(msg['text']).startswith("/Approval_"):
            telegramId = str(msg['text'])[10:]
            is_user_approved, alreadyApproved = user.approveUser(telegramId)

            if alreadyApproved and (alreadyApproved[0][3]) == 'A':
               bot.sendMessage(user_id, "Utente è stato approvato già precedentemente!")
               return 
            
            if is_user_approved:
                keyboard = keyboards.getKeyboard()
                bot.sendMessage(int(telegramId),  "🤝🤝🤝 L'approvazione avvenuta con successo. \n Adesso può usare il menu principale", reply_markup=keyboard) 
                bot.sendMessage(user_id, "Utente approvato correttamente")

       elif msg['text'] == '🖍 Crea filtro x Competenze':
             comp_first, comp_second = filter.get_competences()
             bot.sendMessage(chat_id,  comp_first)
             bot.sendMessage(chat_id,  comp_second)

       elif msg['text'] == '📦 Crea filtro x Prodotto':
             products = filter.get_products()
             bot.sendMessage(chat_id,  products)

       elif msg['text'] == '👥 Crea filtro x Area':
             areas = filter.get_areas()
             bot.sendMessage(chat_id,  areas)

       elif msg['text'] == '👥 Crea filtro x Sott.Area':
             areas = filter.get_sub_areas(chat_id)
             bot.sendMessage(chat_id,  areas)


       # Manage Single Ticket Match      
       elif str(msg['text']).startswith("/tic "):
            # Define the emoji and the text
            ticket_id = str(msg['text'])[len("/tic "):]
            bot.sendMessage(chat_id, "Attendere per favore sto cercando soluzioni...")
            print("Cerco ticket: ",ticket_id )
            hole_message =  "Ticket principale da cercare:  https://tsnew.sanmarcoweb.com/it/ticket/index/index/operation/view/id/" + str(ticket_id) + "\n\n"
            best_matches_indices = phrase_similarity.start_guessing_manual(ticket_id)
            if len(best_matches_indices) == 0:
                hole_message += "\n\n Non ho trovato alcun ticket con i parametri del ticket principale: " + str(ticket_id)
            for ticket_info in best_matches_indices:
                  hole_message += str(ticket_info)

            bot.sendMessage(chat_id, str(hole_message))
            if int(chat_id) != 145645559:
                  bot.sendMessage(145645559,  "Manuale "+  " Da "+ str(ticket_id) + " "+ str(first_name) + str(last_name))


       elif str(msg['text']).startswith("/preferito_"):
            # Define the emoji and the text
            ticket_id = str(msg['text'])[len("/preferito_"):]
            bot.sendMessage(145645559,  "Perfetto "+ str(ticket_id) + " Da "+ str(chat_id))

       elif str(msg['text']).startswith("/_id_c_"):  
            bot.sendMessage(chat_id, insertCompetence.manageCompetence(chat_id,str(msg['text'])[7:], "C" ) )

       elif str(msg['text']).startswith("/_id_p_"): 
            bot.sendMessage(chat_id, insertCompetence.manageCompetence(chat_id,str(msg['text'])[7:], "P") )

       elif str(msg['text']).startswith("/_id_area_"): 
             bot.sendMessage(chat_id, insertCompetence.manageCompetence(chat_id,str(msg['text'])[10:], "A") ) 

       elif str(msg['text']).startswith("/_id_suba_"): 
             bot.sendMessage(chat_id, insertCompetence.manageCompetence(chat_id,str(msg['text'])[10:], "S") ) 

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

       elif str(msg['text']).startswith("/Competen_id_cf_") or str(msg['text']).startswith("/Prodotto_id_cf_"): 
             bot.sendMessage(chat_id, filter.deleteFilter(chat_id, str(msg['text'])[16:] ) ) 


      
       elif str(msg['text']).startswith("/Ticket_dettaglio_"): 
             ticketId = str(msg['text'])[18:] 
             bot.sendMessage(chat_id, "Attendere per favore, sto caricando i dettagli per il ticket <b>" + ticketId +"</b> ....", parse_mode='HTML')
            # Send feedback
             if int(chat_id) != 145645559:
               print("SONO IO: ")
               bot.sendMessage(145645559, "👥👥👥👥 \n Aperto Dettaglio Ticket nr: " + ticketId + "  [ " + first_name+ last_name  + str(user_id) + " ]")
             readyPdf = ticketToday.getDetailTicket(ticketId)
             print(readyPdf)
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
   except:
      print("Error in on_chat_message")

def on_callback_query(msg):
   try:
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
   # print('Callback Query:', query_id, from_id, query_data)
    bot.answerCallbackQuery(query_id, text='Got it')
   #  file="das/" + query_data
   # bot.sendDocument(chat_id=from_id, document=open(file, 'rb')) 
    print(query_data)
   except:
      print("Error in on_callback_query")



test = ""
prod = ""
bot = telepot.Bot(prod)

import traceback






try:
   MessageLoop(bot, {'chat': on_chat_message,
                     'callback_query': on_callback_query}).run_as_thread()
   print('Listening ...')
   starttime = time.time()

   while 1:

      print("Passati 30 Secondi \n")
      tids = user.getUsers()
      # For each user
      for u in tids:
         if u is not None and u[0] is not None:
            newTicketList = ticketToday.getTicketTodayForNotification(int(u[0]))
            for ticket in newTicketList:
               hole_message = ticket
               # bot.sendMessage(int(u[0]), ticket)
               # Guessing from other ticket
               prefix = "🎫 /Ticket_dettaglio_"
               ticket_value = ticket.split(prefix, 1)[-1].split("\n", 1)[0].strip()
               # print(str(ticket_value))
               best_matches_indices = phrase_similarity.start_guessing_manual(ticket_value)
               for ticket_info in best_matches_indices:
                   hole_message += str(ticket_info)

               bot.sendMessage(int(u[0]), str(hole_message))


      time.sleep(30)
      #time.sleep((60.0 * 1) - ((time.time() - starttime) % 60.ticketToday.getTicketToday(chat_id)ticketToday.getTicketToday(chat_id)0))
except Exception:
    traceback.print_exc()