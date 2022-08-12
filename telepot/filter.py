import sys
sys.path.append('../api')
import fetchCompetence
sys.path.append('../conn')
import filters


import json

competenze = ""

def createCompetence():
    docList = json.loads(fetchCompetence.getCompetence())
    competenze1 = ""
    competenze2 = ""
    docSize =  0
    for i in docList:
        docSize +=1 
        
        if docSize > 80:
           competenze2 +=  str(i['label']).strip() + " " + "/_id_c_" + str(i['id']).strip() + "\n"
        else:
           competenze1 += str(i['label']).strip() + " " + "/_id_c_" + str(i['id']).strip() + "\n"

    return competenze1, competenze2


def decodeCompetence(cid,docList):
    for i in docList:
        if str(i['id']).strip() == cid:
            return str(i['label']).strip()
    return 0



def getMyFilters(tid):
     mylist = filters.getFilters(tid)
     listFilterAsString= ""
     docList = json.loads(fetchCompetence.getCompetence())
     for i in mylist:
         listFilterAsString +=  "Competenza: (" + str(i[3]) + ")  " + decodeCompetence(str(i[3]),docList) + "\n"
     return listFilterAsString


# print(getMyFilters(145645559))