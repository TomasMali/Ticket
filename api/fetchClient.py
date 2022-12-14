
import requests
import cockie


def getCleint():

    cookies = {
        'language': 'it',
        'sid': cockie.id,
    }

    headers = {
        'Accept': 'application/javascript, application/json',
        'Accept-Language': 'it-IT,it;q=0.9,la;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'language=it; sid=ajlquaj1g3el263gi52empm763',
        'Referer': 'https://tsnew.sanmarcoweb.com/it/ticket/index/index/operation/accept/id/456427',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
    }

    params = {
        'label': '',
    }
    response = requests.get('https://tsnew.sanmarcoweb.com/it/ticket/search/get-clients', params=params, cookies=cookies, headers=headers)
    content = response.text

    # with open('clients.json', 'w') as f:
    #     f.write(content)
    return content
        




#print(getCleint())

 