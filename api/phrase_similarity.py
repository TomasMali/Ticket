from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import connection
import requests
import traceback
import logging
import cockie
import re
import sys
sys.path.append('../conn')
import mysql5

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
# def getObjectAndDescription(area,prodotto):
#     connection = getConn()
#     cursor = connection.cursor()
    
#     postgreSQL_select_Query = "select descrizione AS result from ticket_big where competenze ='" + str(area) + "' AND prodotto = '" + prodotto + "' " #+ " OR prodotto ='' "
#     # print(postgreSQL_select_Query)
#     cursor.execute(postgreSQL_select_Query)
#     publisher_records = cursor.fetchall()

#     closeConnection(connection,cursor)
#     # print(publisher_records)
#     return publisher_records


def start_guessing_new(ticket):

    competence_origin, program_origin, problem_origin = mysql5.getCompetenceOrProgram(ticket)
    w_list = mysql5.getProblemaBYCompetenzaOrProgramma(competence_origin,program_origin)
        # print("\n\n")
    # print(w_list)
        # print("\n\n")
    phrases = [item[0] for item in w_list]

    # Create the TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # Transform the target phrase and list of phrases
    tfidf_matrix = vectorizer.fit_transform([problem_origin] + phrases)
    similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])

    # Get the indices of the best 5 matches
    best_matches_indices = similarity_matrix.argsort()[0][-6:-1][::-1]

    final_list = []
    i = 1
    # Print the best matches
    for index in best_matches_indices:
        complete_ticket = mysql5.getTicketByProblema(str(phrases[index]))

        # print("Solution: " + complete_ticket[1])
        final_list.append("Possibile soluzione "+ str(i) + ") : [ 🎫 /Ticket_dettaglio_" + str(complete_ticket[0]) + " ] \n https://tsnew.sanmarcoweb.com/it/ticket/index/index/operation/view/id/" + str(complete_ticket[0]) + " \n SOLUZIONE [ " + str(complete_ticket[1]) + " ]" )
        # print("\n")
        i +=1
    return final_list



# getDetail("505532")

# print(start_guessing_new(493309))