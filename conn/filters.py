
import connection

def getConn():
    c = connection.conn()
    return c

def closeConnection(connection,cursor):
    if connection:
        cursor.close()
        connection.close()
    #     print("POstgres connection closed successfully")
    # print("Connection was closed before")




# Insert a filter if not exsists
def insertFilter(tid, sort, sort_value ):
    if str(sort_value).strip().startswith("_"):
        sort_value =  "-" + (str(sort_value).strip())[1:]
    if getFilterByParam(tid, sort, sort_value):
        return False

    connection = getConn()
    cursor = connection.cursor()

    postgres_insert_query = """ INSERT INTO filters (tid, sort, sort_value) VALUES (%s,%s,%s)"""
    record_to_insert = (tid, sort, sort_value)
    cursor.execute(postgres_insert_query, record_to_insert)

    connection.commit()
    count = cursor.rowcount
    if count <1:
        return False
    print(count, "Record inserted successfully into sort table")
    closeConnection(connection,cursor)
    return True


# Returns all the filters inserted by a user
def getFilters(tid):
    connection = getConn()
    cursor = connection.cursor()
    
    postgreSQL_select_Query = "select * from filters where tid =" + str(tid) + " order by sort"
 
    cursor.execute(postgreSQL_select_Query)
    publisher_records = cursor.fetchall()

    closeConnection(connection,cursor)
    return publisher_records

# Returns all the filters inserted by a user
def getFilterByParam(tid,sort, sort_value):
    connection = getConn()
    cursor = connection.cursor()
    
    postgreSQL_select_Query = """select * from filters where tid = %s and sort= %s and sort_value = %s"""
    record_to_insert = (tid, sort, sort_value)
 
    cursor.execute(postgreSQL_select_Query,record_to_insert)
    publisher_records = cursor.fetchall()
    if cursor.rowcount > 0:
        return True
    closeConnection(connection,cursor)
    return False

# Returns all the filters inserted by a user
def getAllFilters():
    connection = getConn()
    cursor = connection.cursor()

    postgreSQL_select_Query = "select * from filters "
 
    cursor.execute(postgreSQL_select_Query)
    publisher_records = cursor.fetchall()
 
    for row in publisher_records:
        print( row, "\n")

    closeConnection(connection,cursor)
    return publisher_records



# Delete a single filter
def deleteFilter(telid, id):
        connection = getConn()
        cursor = connection.cursor()

#       Delete first all the ticket
        sql_delete_query = """Delete from tickets where fid = %s"""
        cursor.execute(sql_delete_query, (id,))
        connection.commit()

        sql_delete_query = """Delete from filters where tid= %s and fid = %s"""
        cursor.execute(sql_delete_query, (telid,id))
        connection.commit()
        count = cursor.rowcount
        print(count, "Record deleted successfully ")

        closeConnection(connection,cursor)
        return count > 0

  
#insertFilter(965744443, 'competenza','itech')
#getUsers()
#isUserRegisterd(222222)


#getFilters(965744443)
#deleteFilter(8)
# print(getFilters(145645559))