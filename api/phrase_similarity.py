from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import connection
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
        solution_ = str(complete_ticket[1])
        if len(solution_) > 400:
            solution_ = solution_[:400] + "..."
        separator = "\n\n🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹\n\n"  
        if i ==1:
            separator = "\n\n🔹🔹🔹🔹🔹🔹🔹🔹🔹1⃣🔹🔹🔹🔹🔹🔹🔹🔹🔹\n"
        elif i == 2:
            separator = "🔹🔹🔹🔹🔹🔹🔹🔹🔹2⃣🔹🔹🔹🔹🔹🔹🔹🔹🔹\n"  
        elif i== 3:
            separator = "🔹🔹🔹🔹🔹🔹🔹🔹🔹3⃣🔹🔹🔹🔹🔹🔹🔹🔹🔹\n" 
        elif i== 4:
            separator = "🔹🔹🔹🔹🔹🔹🔹🔹🔹4⃣🔹🔹🔹🔹🔹🔹🔹🔹🔹\n" 
        elif i== 5:
            separator = "🔹🔹🔹🔹🔹🔹🔹🔹🔹5⃣🔹🔹🔹🔹🔹🔹🔹🔹🔹\n" 

        # print("Solution: " + complete_ticket[1])
        final_list.append(separator + " \n [ 🎫 /Ticket_dettaglio_" + str(complete_ticket[0]) + " ] \n https://tsnew.sanmarcoweb.com/it/ticket/index/index/operation/view/id/" + str(complete_ticket[0]) + " \n SOLUZIONE [ " + str(solution_) + " ] \n\n" )
        # print("\n")
        i +=1
    return final_list



# getDetail("505532")

# print(start_guessing_new(493309))