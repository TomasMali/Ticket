from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import connection
import requests
import traceback
import logging
import cockie
import re


def getConn():
    c = connection.conn()
    return c

def closeConnection(connection,cursor):
    if connection:
        cursor.close()
        connection.close()


def extract_text_between_markers(text, start_marker, end_marker):
    # print(text)
    # print(start_marker)
    # print(end_marker)
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
    # print(postgreSQL_select_Query)
    cursor.execute(postgreSQL_select_Query)
    publisher_records = cursor.fetchall()

    closeConnection(connection,cursor)
    # print(publisher_records)
    return publisher_records

def get_all_info(description):
    connection = getConn()
    cursor = connection.cursor()
 
    postgreSQL_select_Query = """select id,soluzione,descrizione from ticket_big where descrizione = %s """
    record_to_insert = (str(description),)

    cursor.execute(postgreSQL_select_Query, record_to_insert)

    # cursor.execute(postgreSQL_select_Query)
    publisher_records = cursor.fetchall()

    closeConnection(connection, cursor)
    # print(publisher_records)
    # print(publisher_records[0][0])
    return publisher_records[0]





def start_guessing(target_phrase, area, prodotto):

    # print("\nSearching: " + target_phrase + "\n Area: "+ area + " Prodoro: "+ prodotto + "\n")

    w_list = getObjectAndDescription(area,prodotto)
        # print("\n\n")
        # print(w_list)
        # print("\n\n")
    phrases = [item[0] for item in w_list]

    # Create the TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # Transform the target phrase and list of phrases
    tfidf_matrix = vectorizer.fit_transform([target_phrase] + phrases)
    similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])

    # Get the indices of the best 5 matches
    best_matches_indices = similarity_matrix.argsort()[0][-6:-1][::-1]

    final_list = []
    i = 1
    # Print the best matches
    for index in best_matches_indices:
        complete_ticket = get_all_info(phrases[index])

        print("Possibli soluzione " + str(i) + ") : https://tsnew.sanmarcoweb.com/it/ticket/details/index/id/" + complete_ticket[0])
        print("Solution: " + complete_ticket[1])
        final_list.append("Possibile soluzione "+ str(i) + ") : [ " + complete_ticket[0] + " ] \n DESCRIZIONE: [ " + str(complete_ticket[2]) + " ] \n SOLUZIONE [ " + str(complete_ticket[1]) + " ]" )
        print("\n")
        i +=1
    return final_list




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

        # print(ticketId+ " --> Cercando --> ", description)
        return start_guessing(description, competenze.strip(), prodotto.strip())
         

    except Exception as e:
          logging.error(traceback.format_exc())
          return False

# getDetail("505532")