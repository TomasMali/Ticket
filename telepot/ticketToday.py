import sys
import json
sys.path.append('../api')
import fetchTicketToday
import fetchLast20Ticket
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

        # docList = json.loads(fetchTicketToday.fetchTicketToday(str(j[3])))
        docList = mysql5.getTicket(j[2], j[3])
        ticketAsString = ""
        for i in docList:
            ticketAsString += "🎫 /Ticket_dettaglio_"+ str(i[0]) + "\n" +"🏢 Cliente: "+ str(i[1]) + "\n"  +"🔎 Oggetto: "+ str(i[2])+ "\n"  +"🎨 Gravita': "+ str(i[3])+ "\n"  + "🧑 Competenza': "+ str(i[4])+ "\n" + "📅 Apertura': "+ str(i[6])  + "\n\n"     
        if len(docList):
            # max char 4096
           listOfStrings.append(str(ticketAsString))
    return listOfStrings


# def getTicketLast20(teleId):
    
#     listOfStrings = []
#     listFilters = filters.getFilters(teleId)
#     ticketAsString = ""
#     for j in listFilters:
#         docList = json.loads(fetchLast20Ticket.getLast20Ticket(str(j[3])))
#         ticketAsString = ""
#         for i in docList['data']:
#             ticketAsString += "🎫 /Ticket_dettaglio_"+ i['ticket'] + "\n" +"🏢 Cliente: "+ i['cliente'] + "\n"  +"🔎 Oggetto: "+ i['oggetto']+ "\n"  +"🎨 Gravita': "+ i['gravita']+ "\n"  + "🧑 Competenza': "+ i['competenza']+ "\n" + "📅 Apertura': "+ i['segnalazioni_apertura']  + "\n\n"     
#         if len(docList['data']):
#             # max char 4096
#            listOfStrings.append(str(ticketAsString))
#     return listOfStrings


def getTicketTodayForNotification(teleId):
    
    listOfStrings = []
    listFilters = filters.getFilters(teleId)

    # For each user Filters
    for j in listFilters:
        # Get the ticket for today based on the user filter
        ticketTodayList = mysql5.getTicket(j[2], j[3])
        ticketAsString = ""
        for i in ticketTodayList:
            # Returns all the ticket by filter id and ticket number
            listOfTicket = tickets.getTickets(int(j[0]),int(i[0]) )
            # if not exsisted before, I add it now
            if len(listOfTicket) == 0:
               ticketAsString += "🎫 /Ticket_dettaglio_"+ str(i[0]) + "\n https://tsnew.sanmarcoweb.com/it/ticket/index/index/operation/view/id/"+ str(i[0]) + "\n" +"🏢 Cliente: "+ str(i[1]) + "\n"  +"🔎 Oggetto: "+ str(i[2])+ "\n"  +"🎨 Gravita': "+ str(i[3])+ "\n"  + "🧑 Competenza: "+ str(i[4])+ "\n" + "📦 Prodotto:" + str(i[5])+ "\n" + "💜💜💜/preferito_"+ str(i[0])  + "\n\n"     
               tickets.insertTicket(int(j[0]),int(i[0]))
        if len(str(ticketAsString)) > 3:
           listOfStrings.append(str(ticketAsString))

    return listOfStrings








def getDetailTicket(ticketId):
    downloaded = detailTicket.getDetail(str(ticketId))
    return downloaded
    
# print(getTicketTodayForNotification(145645559))

# print(getTicketToday(145645559))