import spacy
import compareText

nlp = spacy.load('it_core_news_lg')


def s_match(w_target):
    # w_target = "JExp non funziona per un problema delle dogane:Esiste una procedura di emergenza per inviare i DAA?"

    # List of w1 to w500
    # w_list = [
    #     ("VIOLAZIONE REGOLA C070 non riusciamo a fare l'EAD"),
    #     ("L'invio dell'E-ad si blocca per la presenza dell'errore violazione regola C070")
    # ]

    w_list = compareText.getObjectAndDescription('Assistenza Vinicoli','JExp')
    w_list = [item[0] for item in w_list]

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
