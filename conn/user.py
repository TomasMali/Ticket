
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


# Insert a telegram user if not exsists
def insertUser(tid, name, surname, status='P', admin=False ):
    if isUserRegisterd(tid):
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
    print("Selecting rows from publisher table using cursor.fetchall")
    publisher_records = cursor.fetchall()
    closeConnection(connection,cursor)
    return publisher_records

#  Checks if a user is registred
def isUserRegisterd(tid):
    connection = getConn()
    cursor = connection.cursor()

    postgreSQL_select_Query = "select * from users where tid=" + str(tid)
 
    cursor.execute(postgreSQL_select_Query)
    print("Selecting rows from publisher table using cursor.fetchall")
    publisher_records = cursor.fetchall()

    closeConnection(connection,cursor)

    if not publisher_records:
        return False
    else:
        return True    
  

# insertUser(22222, 'boh','bah')
#getUsers()
#isUserRegisterd(222222)

