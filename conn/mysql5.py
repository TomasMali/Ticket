import mysql.connector
from mysql.connector import Error


def getMySqlConnection():
        connection = mysql.connector.connect(host='10.200.100.51',
                                            database='smits',
                                            user='reader',
                                            password='3pzg4853',
                                            charset='utf8')
        return connection


def closeConnection(connection,cursor):
    if connection:
        cursor.close()
        connection.close()



def getCompetences(competence_id=999999):
    connection = getMySqlConnection()
    cursor = connection.cursor()
    
    postgreSQL_select_Query = "select * from  competenze order by ID"
    if competence_id != 999999:
       postgreSQL_select_Query += " WHERE ID =" + str(competence_id)
 
    cursor.execute(postgreSQL_select_Query)
    publisher_records = cursor.fetchall()

    closeConnection(connection,cursor)
    return publisher_records

def getProducts(product_id=999999):
    connection = getMySqlConnection()
    cursor = connection.cursor()
    
    postgreSQL_select_Query = "select * from  prodotti order by ID"
    if product_id != 999999:
       postgreSQL_select_Query += " WHERE ID =" + str(product_id)
 
    cursor.execute(postgreSQL_select_Query)
    publisher_records = cursor.fetchall()

    closeConnection(connection,cursor)
    return publisher_records




def getTicket(filter_type="", filter_value=""):
    connection = getMySqlConnection()
    cursor = connection.cursor()
    postgreSQL_select_Query = ""
    if filter_type == "":
        postgreSQL_select_Query = "select * from  segnalazioni limit 2"
    elif filter_type == "C":
        postgreSQL_select_Query = "select s.TICKET,cl.INTESTATARIO,s.OGGETTO,g.GRAVITA ,c.COMPETENZA , p.PRODOTTO ,s.APERTURA from  segnalazioni as s join prodotti as p on  s.PRODOTTO=p.ID join competenze as c on  s.COMPETENZA=c.ID join gravita as g on s.GRAVITA = g.ID  join clienti as cl on cl.ID=s.CLIENTE" + " where s.COMPETENZA ='" +filter_value + "' AND DATE(APERTURA) = CURDATE()"
    elif filter_type == "P":
        postgreSQL_select_Query = "select s.TICKET,cl.INTESTATARIO,s.OGGETTO,g.GRAVITA ,c.COMPETENZA , p.PRODOTTO ,s.APERTURA from  segnalazioni as s join prodotti as p on  s.PRODOTTO=p.ID join gravita as g on s.GRAVITA = g.ID join competenze as c on s.COMPETENZA=c.ID join clienti as cl on cl.ID=s.CLIENTE where S.PRODOTTO='" + filter_value + "' AND DATE(APERTURA) = CURDATE()"
 
    cursor.execute(postgreSQL_select_Query)
    publisher_records = cursor.fetchall()

    closeConnection(connection,cursor)
    return publisher_records


# def getTicketTest(filter_type="", filter_value=""):
#     connection = getMySqlConnection()
#     cursor = connection.cursor()
#     postgreSQL_select_Query = ""
#     if filter_type == "":
#         postgreSQL_select_Query = "select * from  segnalazioni limit 10000"
#     elif filter_type == "C":
#         postgreSQL_select_Query = "select s.TICKET,cl.INTESTATARIO,s.OGGETTO,g.GRAVITA ,c.COMPETENZA , p.PRODOTTO ,s.APERTURA from  segnalazioni as s join prodotti as p on  s.PRODOTTO=p.ID join competenze as c on  s.COMPETENZA=c.ID join gravita as g on s.GRAVITA = g.ID  join clienti as cl on cl.ID=s.CLIENTE" + " where s.COMPETENZA ='" +filter_value + "' AND DATE(APERTURA) = CURDATE() limit 1 OR s.TICKET=194825"
#     elif filter_type == "P":
#         postgreSQL_select_Query = "select s.TICKET,cl.INTESTATARIO,s.OGGETTO,g.GRAVITA ,c.COMPETENZA , p.PRODOTTO ,s.APERTURA from  segnalazioni as s join prodotti as p on  s.PRODOTTO=p.ID join gravita as g on s.GRAVITA = g.ID join competenze as c on s.COMPETENZA=c.ID join clienti as cl on cl.ID=s.CLIENTE where S.PRODOTTO='" + filter_value + "' AND DATE(APERTURA) = CURDATE() limit 1 OR s.TICKET=194825"
 
#     cursor.execute(postgreSQL_select_Query)
#     publisher_records = cursor.fetchall()

#     closeConnection(connection,cursor)
#     return publisher_records



def getProductOrCompetence(type_,value_):
    connection = getMySqlConnection()
    cursor = connection.cursor()
 
    postgreSQL_select_product = "select prodotto from  prodotti WHERE ID="+value_
    postgreSQL_select_competence = "select COMPETENZA from  competenze WHERE ID="+value_
    if type_ == "P":
        cursor.execute(postgreSQL_select_product)
    elif type_ == 'C':
        cursor.execute(postgreSQL_select_competence)

    publisher_records = cursor.fetchall()

    closeConnection(connection,cursor)
    # print(publisher_records)
    return publisher_records


def getCompetenceOrProgram(ticket):
    connection = getMySqlConnection()
    cursor = connection.cursor()
 
    select_problem = "SELECT COMPETENZA,PROGRAMMA, PROBLEMA FROM segnalazioni where TICKET = " + str(ticket)
    cursor.execute(select_problem)

    publisher_records = cursor.fetchall()

    closeConnection(connection,cursor)
    return publisher_records[0][0],publisher_records[0][1],publisher_records[0][2]


def getProblemaBYCompetenzaOrProgramma(competence, program):
    connection = getMySqlConnection()
    cursor = connection.cursor()
    # From DB the competence is not null
    if program != None and competence != None:
        select_problem = "SELECT PROBLEMA  FROM segnalazioni where COMPETENZA = " + str(competence)  + "OR PROGRAMMA = " + str(program)+ ""
    elif program == None:
        select_problem = "SELECT PROBLEMA  FROM segnalazioni where COMPETENZA = " + str(competence) + ""

    cursor.execute(select_problem)

    publisher_records = cursor.fetchall()

    closeConnection(connection,cursor)
    return publisher_records


def getTicketByProblema(problem):
    connection = getMySqlConnection()
    cursor = connection.cursor()
 
    # Use placeholders for the query and pass the value as a parameter
    select_problem = "SELECT TICKET, SOLUZIONE, PROBLEMA FROM segnalazioni WHERE PROBLEMA = %s"
    cursor.execute(select_problem, (problem,))

    publisher_records = cursor.fetchall()

    closeConnection(connection,cursor)
    return publisher_records[0]
     


# print(getTicketByProblema("CERCA SABRINA"))
# print(getTicketTest("P", "24"))