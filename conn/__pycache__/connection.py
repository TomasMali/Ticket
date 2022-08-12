from pickle import FALSE
import psycopg2





def conn():
    try:
        connection = psycopg2.connect(user="postgres",
                                    password="tommal",
                                    host="10.100.0.30",
                                    port="5432",
                                    database="ticket")

        return connection
        # cursor = connection.cursor()

        # postgres_insert_query = """ INSERT INTO mobile (ID, MODEL, PRICE) VALUES (%s,%s,%s)"""
        # record_to_insert = (5, 'One Plus 6', 950)
        # cursor.execute(postgres_insert_query, record_to_insert)

        # connection.commit()
        # count = cursor.rowcount
        # print(count, "Record inserted successfully into mobile table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into mobile table", error)
        return FALSE

    # finally:
    #     # closing database connection.
    #     if connection:
    #         connection.cursor().close()
    #         connection.close()
    #         print("PostgreSQL connection is closed")


