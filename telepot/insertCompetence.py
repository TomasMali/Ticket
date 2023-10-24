

import sys
sys.path.append('../conn')
import filters


def manageCompetence(tid,cid, sort):
    if filters.insertFilter(tid, sort, cid):
        return "Filtro inserito con successo"
    else:
        return "Filtro gia' esistente!"
