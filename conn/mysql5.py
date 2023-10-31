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



def get_areas():
    connection = getMySqlConnection()
    cursor = connection.cursor()
    
    postgreSQL_select_Query = "select * from aree"
 
    cursor.execute(postgreSQL_select_Query)
    publisher_records = cursor.fetchall()

    closeConnection(connection,cursor)
    return publisher_records

def get_sub_areas(area):

    connection = getMySqlConnection()
    cursor = connection.cursor()
    
    postgreSQL_select_Query = "select ID,SOTTOAREA,AREA  from sottoaree where area = %s"
 
    cursor.execute(postgreSQL_select_Query, (area,))
    publisher_records = cursor.fetchall()

    closeConnection(connection,cursor)
    return publisher_records





# print(get_sub_areas(2))



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



def getProductOrCompetence(type_,value_):
    connection = getMySqlConnection()
    cursor = connection.cursor()
 
    postgreSQL_select_product = "select prodotto from  prodotti WHERE ID="+value_
    postgreSQL_select_competence = "select COMPETENZA from  competenze WHERE ID="+value_
    postgreSQL_select_area = "select AREA from aree a where ID="+value_
    postgreSQL_select_sub_area = "select SOTTOAREA from sottoaree where ID="+value_

    if type_ == "P":
        cursor.execute(postgreSQL_select_product)
    elif type_ == 'C':
        cursor.execute(postgreSQL_select_competence)
    elif type_ == 'A':
        cursor.execute(postgreSQL_select_area)
    elif type_ == 'S':
        cursor.execute(postgreSQL_select_sub_area)

    publisher_records = cursor.fetchall()

    closeConnection(connection,cursor)
    # print(publisher_records)
    return publisher_records


def getCompetenceOrProdotto(ticket):
    connection = getMySqlConnection()
    cursor = connection.cursor()
 
    select_problem = "SELECT COMPETENZA,PRODOTTO, PROBLEMA, AREA , SOTTOAREA FROM segnalazioni where TICKET = " + str(ticket)
    cursor.execute(select_problem)

    publisher_records = cursor.fetchall()

    closeConnection(connection,cursor)

    # print( publisher_records[0])
   
    return str(publisher_records[0][0]) ,str(publisher_records[0][1]) ,str(publisher_records[0][2]) , str(publisher_records[0][3]) ,str(publisher_records[0][4])

# def getProblemaBYCompetenzaOrProgramma(competence, prodotto):
#     connection = getMySqlConnection()
#     cursor = connection.cursor()
#     # From DB the competence is not null
#     if prodotto != None and competence != None:
#         select_problem = "SELECT PROBLEMA  FROM segnalazioni where COMPETENZA = " + str(competence)  + " AND PRODOTTO = " + str(prodotto)+ ""
#     elif prodotto == None:
#         select_problem = "SELECT PROBLEMA  FROM segnalazioni where COMPETENZA = " + str(competence) + ""

#     cursor.execute(select_problem)

#     publisher_records = cursor.fetchall()

#     closeConnection(connection,cursor)
#     return publisher_records

def getProblemaBYCompetenzaOrProgramma_manul(competence, prodotto, area, sottoarea):
    connection = getMySqlConnection()
    cursor = connection.cursor()


    main_sql = "SELECT PROBLEMA  FROM segnalazioni WHERE "
    at_least_one_where_condition = False

    if prodotto is not None and prodotto.isdigit():
        print("Trovato prodotto: ", prodotto)
        main_sql += " PRODOTTO= " + str(prodotto) + " AND "
        at_least_one_where_condition = True
    
    if area is not None and area.isdigit():
        print("Trovato area: ", area)
        main_sql += " AREA= " + str(area) + " AND "
        at_least_one_where_condition = True      


    if  sottoarea is not None and sottoarea.isdigit():
        print("Trovato sottoarea: ", sottoarea)
        main_sql += " SOTTOAREA= " + str(sottoarea) + " AND "
        at_least_one_where_condition = True  

# If none of the where condition is satisfied 
    if  not at_least_one_where_condition:
        if competence is not None and isinstance(competence, (int, float)) and 0 <= competence:
            print("Trovato competence: ", competence)
            main_sql += " COMPETENZA= " + str(competence)
        else:
            print("Trovato : ", "Nulla")
            main_sql += " False "
    else:
        main_sql = main_sql[:-4]



    print(main_sql)
    cursor.execute(main_sql)

    publisher_records = cursor.fetchall()
    count = cursor.rowcount

    closeConnection(connection,cursor)
    # if count <1:
    #     print("FFFFFF")
    #     return  "Non ho trovato ticket con i filtri del ticket principale."
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