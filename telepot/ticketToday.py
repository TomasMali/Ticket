import sys
import json
sys.path.append('../api')
import fetchTicketToday
import fetchLast20Ticket
import detailTicket
sys.path.append('../conn')
import filters
import tickets



def getTicketToday(teleId):
    
    listOfStrings = []
    listFilters = filters.getFilters(teleId)
    ticketAsString = ""
    for j in listFilters:
        docList = json.loads(fetchTicketToday.fetchTicketToday(str(j[3])))
        ticketAsString = ""
        for i in docList['data']:
            ticketAsString += "🎫 /Ticket_dettaglio_"+ i['ticket'] + "\n" +"🏢 Cliente: "+ i['cliente'] + "\n"  +"🔎 Oggetto: "+ i['oggetto']+ "\n"  +"🎨 Gravita': "+ i['gravita']+ "\n"  + "🧑 Competenza': "+ i['competenza']+ "\n" + "📅 Apertura': "+ i['segnalazioni_apertura']  + "\n\n"     
        if len(docList['data']):
            # max char 4096
           listOfStrings.append(str(ticketAsString))
    return listOfStrings


def getTicketLast20(teleId):
    
    listOfStrings = []
    listFilters = filters.getFilters(teleId)
    ticketAsString = ""
    for j in listFilters:
        docList = json.loads(fetchLast20Ticket.getLast20Ticket(str(j[3])))
        ticketAsString = ""
        for i in docList['data']:
            ticketAsString += "🎫 /Ticket_dettaglio_"+ i['ticket'] + "\n" +"🏢 Cliente: "+ i['cliente'] + "\n"  +"🔎 Oggetto: "+ i['oggetto']+ "\n"  +"🎨 Gravita': "+ i['gravita']+ "\n"  + "🧑 Competenza': "+ i['competenza']+ "\n" + "📅 Apertura': "+ i['segnalazioni_apertura']  + "\n\n"     
        if len(docList['data']):
            # max char 4096
           listOfStrings.append(str(ticketAsString))
    return listOfStrings


def getTicketTodayForNotification(teleId):
    
    listOfStrings = []
    listFilters = filters.getFilters(teleId)
    ticketAsString = ""
    for j in listFilters:
        docList = json.loads(fetchTicketToday.fetchTicketToday(str(j[3])))
        ticketAsString = ""
        for i in docList['data']:
            ticketAsString += "🎫 Ticet: "+ i['ticket'] + "\n" +"🏢 Cliente: "+ i['cliente'] + "\n"  +"🔎 Oggetto: "+ i['oggetto']+ "\n"  +"🎨 Gravita': "+ i['gravita']+ "\n"  + "🧑 Competenza': "+ i['competenza']+ "\n" + "📅 Apertura': "+ i['segnalazioni_apertura']  + "\n\n"     
            # if not exsisted before, I add it now
            listOfTicket = tickets.getTickets(int(j[0]),i['ticket'] )
            if len(listOfTicket) == 0:
               tickets.insertTicket(int(j[0]), i['ticket'], i['cliente'], i['oggetto'], "noproblem",i['gravita'], i['competenza'], i['segnalazioni_apertura'])
               listOfStrings.append(str(ticketAsString))
            
    return listOfStrings




def getDetailTicket(ticketId):
    downloaded = detailTicket.getDetail(str(ticketId))
    return downloaded
    
# print(getTicketTodayForNotification(145645559))

