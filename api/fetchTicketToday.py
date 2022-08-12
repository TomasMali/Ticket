import requests




def fetchTicketToday(comp):
    cookies = {
        'language': 'it',
        'sid': 'rgoumkdu3ndteo372j5vijpjm6',
    }

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'it-IT,it;q=0.9,la;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
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

    data = 'params=%7B%22where%22%3A%5B%7B%22field%22%3A%22and%22%2C%22group%22%3A%5B%7B%22field%22%3A%22DATE(segnalazioni.apertura)%22%2C%22comparison%22%3A%22%3D%22%2C%22value%22%3A%22TODAY%22%7D%2C%7B%22field%22%3A%22competenze.id%22%2C%22comparison%22%3A%22%3D%22%2C%22value%22%3A%22'+str(comp) +'  %22%7D%5D%7D%5D%2C%22headers%22%3A%5B%22ticket%22%2C%22data%22%2C%22stato%22%2C%22cliente%22%2C%22oggetto%22%2C%22segnalatore%22%2C%22gravita%22%2C%22priorita%22%2C%22competenza%22%5D%2C%22sorting%22%3A%5B%7B%22field%22%3A%22segnalazioni_apertura%22%2C%22order%22%3A%22desc%22%7D%5D%2C%22limit%22%3A100%7D'

    response = requests.post('https://tsnew.sanmarcoweb.com/it/ticket/search/get-tickets', cookies=cookies, headers=headers, data=data)

    content = response.text

    # with open('json/fetchTicketToday.json', 'w') as f:
    #     f.write(content)    
    # print(content)
    return content

# fetchTicketToday(1)