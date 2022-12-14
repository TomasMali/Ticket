import requests
import os


import traceback
import logging
import cockie
import time





def deleteDocs(ticketId):
    time.sleep(2)
    if os.path.exists("json/detailTicket.html"):
        os.remove("json/detailTicket.html")
        # os.remove('json/' + str(ticketId)+'_details.pdf')


def getDetail(ticketId):
    # print("arrivato con :   " + str(ticketId))

    pdf_file = "json/" + str(ticketId) + "_details.pdf"
    html_file = "json/" + str(ticketId) + "_details.html"
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

        content = response.text

        with open(html_file, 'w') as f:
            f.write(str(content.replace('rows="7"', ' rows="10" cols="100" ')).encode('latin1').decode('utf8'))  

            #  json/" + str(ticketId) + "_details.pdf" 


    # Write the messages 
        response2 = requests.get('https://tsnew.sanmarcoweb.com/it/ticket/messages/index/id/' + str(ticketId), cookies=cookies, headers=headers)

        content2 = response2.text

        with open(html_file, 'a', encoding='utf-8') as b:
            b.write(content2.replace('rows="7"', ' rows="10" cols="100" ').encode('latin1').decode('utf8'))  

    # Append notes
        response3 = requests.get('https://tsnew.sanmarcoweb.com/it/ticket/notes/index/id/' + str(ticketId), cookies=cookies, headers=headers)

        content3 = response3.text     

        with open(html_file, 'a', encoding='utf-8') as c:
            c.write(content3.replace('rows="7"', ' rows="10" cols="100" ').encode('latin1').decode('utf8'))    

    # Append the attachments

        response4 = requests.get('https://tsnew.sanmarcoweb.com/it/ticket/attachments/index/id/' + str(ticketId), cookies=cookies, headers=headers)

        content4 = response4.text
        with open(html_file, 'a', encoding='utf-8') as d:
            d.write(content4.replace('rows="7"', ' rows="10" cols="100" ').encode('latin1').decode('utf8'))

    # Convert into pdf
        # path_wkhtmltopdf = '/usr/bin/wkhtmltopdf'
        # config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        # pdfkit.from_file(html_file, pdf_file, configuration=config)  

        return True
    
    except Exception as e:
          logging.error(traceback.format_exc())
          return False


# getDetail(456427)

# deleteDocs(456292)






