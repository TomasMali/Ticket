import requests
import re
import json

import traceback
import logging
import cockie
import connection
import spacy_match

import spacy

nlp = spacy.load('it_core_news_lg')

def getConn():
    c = connection.conn()
    return c

def closeConnection(connection,cursor):
    if connection:
        cursor.close()
        connection.close()

file_path = "output.json"

def extract_text_between_markers(text, start_marker, end_marker):
    pattern = re.compile(f'{re.escape(start_marker)}(.*?){re.escape(end_marker)}', re.DOTALL)
    match = pattern.search(text)
    if match:
        return match.group(1).strip()
    return None



# Returns all the filters inserted by a user
def getObjectAndDescription(area,prodotto):
    connection = getConn()
    cursor = connection.cursor()
    
    postgreSQL_select_Query = "select descrizione AS result from ticket_big where competenze ='" + str(area) + "' AND prodotto = '" + prodotto + "' " #+ " OR prodotto ='' "
    print(postgreSQL_select_Query)
    cursor.execute(postgreSQL_select_Query)
    publisher_records = cursor.fetchall()

    closeConnection(connection,cursor)
    # print(publisher_records)
    return publisher_records


def getDetail(ticketId):

    try:

        cookies = {
            'language': 'it',
            'sid': cockie.id,
        }

        headers = {
            'Accept': '*/*',
            'Accept-Language': 'it-IT,it;q=0.9,la;q=0.8',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            # Requests sorts cookies= alphabetically
            # 'Cookie': 'language=it; sid=89q0fl4j3r54600e2fdbf952t1',
            'Referer': 'https://tsnew.sanmarcoweb.com/it/ticket',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
        }   

        response = requests.get('https://tsnew.sanmarcoweb.com/it/ticket/details/index/id/'+ str(ticketId), cookies=cookies, headers=headers)

        oggetto_start = 'name="oggetto" value="'
        oggetto_end = '"'
        start_marker = 'true,required: false">'
        end_marker = '</textarea>'
        competenza_start = '<img class="rightIcon" width="16" height="16" src="/img/_core/ticket/competence.png" />'
        competenza_end = '/option>'
        competenze_final_start = '" selected="selected">'
        competenze_final_end = '<'
        soluzione_start = '[]);}">'
        soluzione_end = '</textarea>'
        prodotto_start = 'id="prodotto_'+ str(ticketId)
        prodotto_end = '/option>'
        prodotto_final_start = 'selected="selected">'
        prodotto_final_end = '<'
        
        content = response.text
        # print(content)

        oggetto = extract_text_between_markers(content, oggetto_start, oggetto_end)
        description = extract_text_between_markers(content, start_marker, end_marker)
        competenze = extract_text_between_markers(content, competenza_start, competenza_end)
        competenze = extract_text_between_markers(competenze, competenze_final_start, competenze_final_end)
        soluzione = extract_text_between_markers(content, soluzione_start, soluzione_end)
        prodotto = extract_text_between_markers(content, prodotto_start, prodotto_end)
        prodotto = extract_text_between_markers(prodotto, prodotto_final_start, prodotto_final_end)

        print(ticketId+ " --> Cercando --> ", description)
        # print("Descrizione: ", description)
        # print("Competenze: ", competenze)
        # print("Soluzione: ", soluzione)
        # print("Prodotto: ", prodotto)


        # getObjectAndDescription('Assistenza Vinicoli','JExp')
        # s_match(description)

         
        if not soluzione.replace("\n", ""):
            return False
        
        connection = getConn()
        cursor = connection.cursor()

        postgres_insert_query = """ INSERT INTO ticket_big (id, oggetto,descrizione, competenze, soluzione,prodotto) VALUES (%s,%s,%s,%s,%s,%s)"""
        record_to_insert = (str(ticketId), oggetto.replace("\n", ""),description.replace("\n", ""), competenze.replace("\n", ""),soluzione.replace("\n", ""),prodotto.replace("\n", ""))
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
        count = cursor.rowcount
        if count <1:
            return False
        print(count, "Record inserted successfully into sort table")
        closeConnection(connection,cursor)
        return True
    
    except Exception as e:
          logging.error(traceback.format_exc())
          return False


# for ticket in range(456424,456429):
#         getDetail(ticket)

def get_ids_from_json_file(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

    ids = [item['id'] for item in data['data']]
    return ids



file_path = 'data.json'
ids_list = get_ids_from_json_file("/Users/tommal/Desktop/tickets.json")
# print(ids_list)


for ticket in ids_list:
    getDetail(ticket)


############################################################


def s_match(w_target):
    # w_target = "JExp non funziona per un problema delle dogane:Esiste una procedura di emergenza per inviare i DAA?"

    # List of w1 to w500
    # w_list = [
    #     ("VIOLAZIONE REGOLA C070 non riusciamo a fare l'EAD"),
    #     ("L'invio dell'E-ad si blocca per la presenza dell'errore violazione regola C070")
    # ]

    w_list = getObjectAndDescription('Assistenza Vinicoli','JExp')
    # print("\n\n")
    # print(w_list)
    # print("\n\n")
    w_list = [item[0] for item in w_list]
    # w_list = ["tempo bello", "molto", "usciamo fuori"]


    # Calculate similarity scores for each w in w_list and create a list of tuples
    similarity_scores = [(w, nlp(w_target).similarity(nlp(w))) for w in w_list]

    # Sort the list of tuples based on similarity score in descending order
    sorted_similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    # Get the best 5 matches from the sorted list
    best_matches = sorted_similarity_scores[:5]

    # Print the best 5 matches
    print("\n\n")
    print("Top 5 matches:")
    for match, similarity_score in best_matches:
        print("Match:", match)
        print("Similarity score:", similarity_score)
        print("\n")










