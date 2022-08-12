

import sys
sys.path.append('../conn')
import filters


def manageCompetence(tid,cid):
    if filters.insertFilter(tid, "C", cid):
        return "Filtro inserito con successo"
    else:
        return "Filtro gia' esistente!"
