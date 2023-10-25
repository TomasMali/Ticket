import sys
sys.path.append('../api')
import phrase_similarity
import detailTicket
sys.path.append('../conn')
import filters
import tickets
import mysql5



def getTicketToday(teleId):
    
    listOfStrings = []
    listFilters = filters.getFilters(teleId)
    ticketAsString = ""
    for j in listFilters:

        docList = mysql5.getTicket(j[2], j[3])
        ticketAsString = ""
        for i in docList:
            ticketAsString += "🎫 /Ticket_dettaglio_"+ str(i[0]) + "\n" +"🏢 Cliente: "+ str(i[1]) + "\n"  +"🔎 Oggetto: "+ str(i[2])+ "\n"  +"🎨 Gravita': "+ str(i[3])+ "\n"  + "🧑 Competenza': "+ str(i[4])+ "\n" + "📅 Apertura': "+ str(i[6])  + "\n\n"     
        if len(docList):
            # max char 4096
           listOfStrings.append(str(ticketAsString))
    return listOfStrings



def getTicketTodayForNotification(teleId):
    
    listOfStrings = []
    listFilters = filters.getFilters(teleId)

    # print("Lista di filtri: ",listFilters)
    # print("\n\n\n")

    # For each user Filters
    for j in listFilters:
        # Get the ticket for today based on the user filter
        filter_type, filter_value = j[2], j[3]
        # filter_type = "" # DA TOGLEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
        ticketTodayList = mysql5.getTicket(filter_type, filter_value)
        ticketAsString = ""
        for i in ticketTodayList:
            # Returns the only ticket by filter id and ticket number if it exists
            listOfTicket = tickets.getTickets(int(j[0]),int(i[0]) )
            # if not exsisted before, I add it now
            if len(listOfTicket) == 0:
               object_ = str(i[2])
               if len(object_) > 250:
                   object_ = object_[:250] + "..."
               ticketAsStringSingle = "🎫 /Ticket_dettaglio_"+ str(i[0]) + "\n https://tsnew.sanmarcoweb.com/it/ticket/index/index/operation/view/id/"+ str(i[0]) + "\n" +"🏢 Cliente: "+ str(i[1]) + "\n"  +"🔎 Oggetto: "+ str(object_) + "\n"  +"🎨 Gravita': "+ str(i[3])+ "\n"  + "🧑 Competenza: "+ str(i[4])+ "\n" + "📦 Prodotto:" + str(i[5])+ "\n" + "💜/preferito_"+ str(i[0])  + "\n\n"     
               ticketAsString += ticketAsStringSingle  
               # Insert the new ticket on the DB        
               tickets.insertTicket(int(j[0]),int(i[0]))
               # Append the new ticket to the complete message
               listOfStrings.append(str(ticketAsStringSingle))
    # print("Lista ticket finale:: ",len(listOfStrings))
    # print("\n\n\n")
    return listOfStrings








def getDetailTicket(ticketId):
    downloaded = detailTicket.getDetail(str(ticketId))
    return downloaded





    

# newTicketList = getTicketTodayForNotification(145645559)

# for ticket in newTicketList:
#         hole_message = ticket
#         # print("Messaggio: ", ticket)
#                # Guessing from other ticket
#         prefix = "🎫 /Ticket_dettaglio_"
#         ticket_value = ticket.split(prefix, 1)[-1].split("\n", 1)[0].strip()
   
#         best_matches_indices = phrase_similarity.start_guessing_new(ticket_value)
#         for ticket_info in best_matches_indices:
#             # print("Gesing Ticket: ", str(ticket_info))
#             hole_message += str(ticket_info)

#         hole_message += "\n\n\n\n"
#         print(hole_message)

