import sys
sys.path.append('../api')

sys.path.append('../conn')
import filters
sys.path.append('../conn')
import mysql5


competenze = ""



'''Returns all the competences from db'''
def get_competences():
    docList = mysql5.getCompetences()
    competenze1 = ""
    competenze2 = ""
    docSize =  0
    for i in docList:
        docSize +=1 
        id_c = int(i[0])

        if id_c < 0:
            id_c = str( "_" + str(id_c)[1:] )
        else:
            id_c = str(id_c)

        competence = str(i[1])
        
        if docSize > 80:
           competenze2 +=  competence + " " + "/_id_c_" + id_c + "\n"
        else:
           competenze1 +=   competence + " " + "/_id_c_" + id_c + "\n"

    return competenze1, competenze2


def get_products():
    docList = mysql5.getProducts()
    productrs = ""
    print("lista:", docList)
    for i in docList:
        productrs +=   str(i[1]) + " " + "/_id_p_" + str(i[0]) + "\n"
    print(productrs)
    return productrs

def get_areas():
    area_list = mysql5.get_areas()
    areas = ""
    print("lista:", area_list)
    for i in area_list:
        areas +=  " " + str(i[2]) + "   "+   "/_id_area_" + str(i[0]) + "\n"
    print(areas)
    return areas

def get_sub_areas(tid):

    # fet the area for the user tid
    sub_areas = filters.get_area_from_tid(tid)
    if len(sub_areas) < 1:
        return "Non esiste Area per la sottoarea selezionata. Inserire prima l'area"

    s_area_list = mysql5.get_sub_areas(sub_areas[0][0])
    s_areas = ""
    print("lista:", s_area_list)
    for i in s_area_list:
        s_areas +=  " " + str(i[2]) + "   "+   "/_id_suba_" + str(i[0]) + "\n"
    print(s_areas)
    return s_areas



def decodeCompetence(cid,docList):
    for i in docList:
        if str(i['id']).strip() == cid:
            return str(i['label']).strip()
    return 0



def getMyFilters(tid):
     mylist = filters.getFilters(tid)
     listFilterAsString= ""
     for i in mylist:
         tipo = ""
         if str(i[2]) == "C":
             tipo = "Competenza"
         elif str(i[2]) == 'P':
             tipo = "Prodotto"
         elif str(i[2]) == 'A':
             tipo = "Area"
         elif str(i[2]) == 'S':
             tipo = "Sottoarea"
         listFilterAsString +=  tipo + ": (" + str(i[3]) + ")  " + mysql5.getProductOrCompetence(str(i[2]), str(i[3]))[0][0] + "\n"
     return listFilterAsString


def showFilterToBeDelete(tid):
     mylist = filters.getFilters(tid)
     listFilterAsString= ""
     for i in mylist:
         tipo = ""
         if str(i[2]) == "C":
             tipo = "Competen"
         elif str(i[2]) == 'P':
             tipo = "Prodotto"
         elif str(i[2]) == 'A':
             tipo = "Area"
         elif str(i[2]) == 'S':
             tipo = "Sottoarea"
         listFilterAsString +=  "/" + tipo + "_id_cf_" + str(i[0]) + ")  " + mysql5.getProductOrCompetence(str(i[2]), str(i[3]))[0][0] + "\n"
     return listFilterAsString



def deleteFilter(telid, fid):
    if filters.deleteFilter(telid, fid):
        return "Filtro cancellato con successo"
    else:
        "Non è stato possibile cancella il tuo filtro, riprova piu tardi!"



# print(getMyFilters(145645559))
#print(deleteFilter(145645559))
# get_competence()