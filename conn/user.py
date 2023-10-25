
import connection



def getConn():
    c = connection.conn()
    return c

def closeConnection(connection,cursor):
    if connection:
        cursor.close()
        connection.close()


'''Insert a telegram user if it doesnt exist
   Return True if user has been inserted successfully, False otherwise
'''
def insertUser(tid, name, surname, status='P', admin=False ):
    if getUserByTid(tid):
        return False
 
    connection = getConn()
    cursor = connection.cursor()
        

    postgres_insert_query = """ INSERT INTO users (tid, username, surname, status, user_admin) VALUES (%s,%s,%s,%s,%s)"""
    record_to_insert = (tid, name, surname, status, admin)
    cursor.execute(postgres_insert_query, record_to_insert)

    connection.commit()
    count = cursor.rowcount

    closeConnection(connection,cursor)

    if count <1:
        return False
    print(count, "Record inserted successfully into users table")
    return True


# Returns all the user registered on bot
def getUsers():
    connection = getConn()
    cursor = connection.cursor()

    postgreSQL_select_Query = "select users.tid from users"
 
    cursor.execute(postgreSQL_select_Query)
    publisher_records = cursor.fetchall()
    closeConnection(connection,cursor)
    return publisher_records

'''  Gets the user by telegram id '''
def getUserByTid(tid):
    connection = getConn()
    cursor = connection.cursor()

    postgreSQL_select_Query = "select * from users where tid=" + str(tid)
 
    cursor.execute(postgreSQL_select_Query)
    publisher_records = cursor.fetchall()

    closeConnection(connection,cursor)
    return publisher_records
    # if not publisher_records:
    #     return False
    # else:
    #     return True    
  

def approveUser(tid):

    alreadyApproved = getUserByTid(tid)
    connection = getConn()
    cursor = connection.cursor()

    postgreSQL_update_Query = "UPDATE users SET status = 'A' WHERE tid = %s"
 
    cursor.execute(postgreSQL_update_Query, (tid,))
    connection.commit()
    count = cursor.rowcount
    print(count, "Record updated successfully ")
    closeConnection(connection,cursor)
    return count > 0, alreadyApproved


# insertUser(22222, 'boh','bah')
#getUsers()
# if getUserByTid(145645559):
#     print(getUserByTid(145645559)[0][3])

