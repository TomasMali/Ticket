import requests

import json

def getLast20Ticket(comp):

    cookies = {
        'language': 'it',
        'sid': 'rgoumkdu3ndteo372j5vijpjm6',
    }

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'it-IT,it;q=0.9,la;q=0.8',
        'Connection': 'keep-alive',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'language=it; sid=rgoumkdu3ndteo372j5vijpjm6',
        'Origin': 'https://tsnew.sanmarcoweb.com',
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

     

    data = {
        'params': '{"where":[{"field":"and","group":[{"field":"competenze.id","comparison":"=","value":'+ str(comp) + '}]}],"headers":["ticket","data","stato","cliente","oggetto","segnalatore","gravita","priorita","competenza"],"sorting":[{"field":"segnalazioni_apertura","order":"desc"}],"limit":20}',
    }

    response = requests.post('https://tsnew.sanmarcoweb.com/it/ticket/search/get-tickets', cookies=cookies, headers=headers, data=data)
    content = response.text

    data = json.loads(content)

    with open('json/getLast20Ticket.json', 'w') as f:
        f.write(content)    

    return data['data']

print(getLast20Ticket(63))
