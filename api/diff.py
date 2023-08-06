import difflib
import compareText

def get_similarity_ratio(s1, s2):
    matcher = difflib.SequenceMatcher(None, s1, s2)
    return matcher.ratio()

w_target = "JExp non funziona per un problema delle dogane:Esiste una procedura di emergenza per inviare i DAA?"

w_list = compareText.getObjectAndDescription('Assistenza Vinicoli','JExp')
w2_list = [item[0] for item in w_list]
w_list = w2_list
# Calculate similarity scores for each w in w_list
similarity_scores = [(w, get_similarity_ratio(w_target, w)) for w in w_list]

# Sort the list of tuples based on similarity score in descending order
sorted_similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

# Get the best 5 matches from the sorted list
best_matches = sorted_similarity_scores[:5]

# Print the best 5 matches
print("Top 5 matches:")
for match, similarity_score in best_matches:
    print("Match:", match)
    print("Similarity score:", similarity_score)
    print()
