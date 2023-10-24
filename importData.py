import json
import psycopg2

def insert_data_from_json(json_file, database_connection_string):
    # Load JSON data from the file
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Connect to the PostgreSQL database
    connection = psycopg2.connect(database_connection_string)
    cursor = connection.cursor()

    # Iterate over the JSON objects and insert them into the database
    for record in data['data']:
        id = record.get('id', None)
        oggetto = record.get('oggetto', None)


        # Check if the record already exists in the database based on the 'id' field
        cursor.execute("SELECT id FROM ticket_big WHERE id = %s", (id,))
        existing_record = cursor.fetchone()

        if existing_record:
            # Update the record if it already exists (you can modify this part as needed)
             #cursor.execute("UPDATE ticket_big SET oggetto = %s WHERE id = %s", (oggetto, id))
            print("Already EXists...........") 
        else:
            
            descrizione = None  # You can set this to a value if you have one
            competenze = None  # You can set this to a value if you have one
            soluzione = None  # You can set this to a value if you have one
            prodotto = None  # You can set this to a value if you have one
            # Insert a new record if it doesn't exist
            cursor.execute(
                "INSERT INTO ticket_big (id, oggetto, descrizione, competenze, soluzione, prodotto) VALUES (%s, %s, %s, %s, %s, %s)",
                (id, oggetto, descrizione, competenze, soluzione, prodotto)
            )

    # Commit the changes and close the database connection
    connection.commit()
    cursor.close()
    connection.close()

# Usage:
json_file = "text.json"
database_connection_string = "postgresql://postgres:tommal@10.100.0.30:5432/ticket"
insert_data_from_json(json_file, database_connection_string)
