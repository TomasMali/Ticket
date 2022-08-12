
import connection

def getConn():
    c = connection.conn()
    return c

def closeConnection(connection,cursor):
    if connection:
        cursor.close()
        connection.close()
        print("POstgres connection closed successfully")
    print("Connection was closed before")



# Insert a ticket if not exsists
def insertTicket(fid, ticket, client, subject, problem, criticity, team, opened_day):
    connection = getConn()
    cursor = connection.cursor()

    postgres_insert_query = """ INSERT INTO tickets (fid, ticket, client, subject, problem, criticity, team, opened_day) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
    record_to_insert = (fid, ticket, client, subject, problem, criticity, team, opened_day)
    cursor.execute(postgres_insert_query, record_to_insert)

    connection.commit()
    count = cursor.rowcount
    if count <1:
        return False
    print(count, "Record inserted successfully into ticket table")


    closeConnection(connection,cursor)
    return True


def getTicketsByTid(tid):
    connection = getConn()
    cursor = connection.cursor()

    postgreSQL_select_Query = """select * from tickets join filters on tickets.fid  = filters.fid where filters.tid = %s order by filters.tid"""
    record_to_insert = (tid,)
    cursor.execute(postgreSQL_select_Query, record_to_insert)
    publisher_records = cursor.fetchall()
 
    closeConnection(connection,cursor)
    return publisher_records

# Returns all the ticket by telegram id and sort
def getTickets(fid, ticket):
    connection = getConn()
    cursor = connection.cursor()

    postgreSQL_select_Query = """select * from tickets where tickets.fid = %s and tickets.ticket = %s"""
    record_to_insert = (fid, ticket)
    cursor.execute(postgreSQL_select_Query, record_to_insert)
    publisher_records = cursor.fetchall()
 
    closeConnection(connection,cursor)
    return publisher_records

# def getTickets(tid, fid):
#     connection = getConn()
#     cursor = connection.cursor()

#     postgreSQL_select_Query = """select * from tickets join filters on tickets.fid  = filters.fid where filters.tid = %s and filters.fid = %s"""
#     record_to_insert = (tid, fid)
#     cursor.execute(postgreSQL_select_Query, record_to_insert)
#     publisher_records = cursor.fetchall()
 
#     closeConnection(connection,cursor)
#     return publisher_records

#getTickets(965744443, 'itech')
#insertTicket(8, 35345,'Bertin', 'Problemi accise', 'Camion fermo', 'Rosso', 'vinicoli', '01/08/2022 13:06:09')


# print(getTicketsByTid(145645559))