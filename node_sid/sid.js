var request = require('request');


var headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'it-IT,it;q=0.9,la;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'language=it; sid=secret',
    'Origin': 'https://tsnew.sanmarcoweb.com',
    'Referer': 'https://tsnew.sanmarcoweb.com/it/ticket',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"'
};

var dataString = 'username=TOMMAL&password=tomas63&submit=';

var options = {
    url: 'https://tsnew.sanmarcoweb.com/it/authentication',
    method: 'POST',
    headers: headers,
    body: dataString
};

function callback(error, response, body) {

    var objectValue =   JSON.parse(JSON.stringify(response.headers))
    var sidRow =((objectValue['set-cookie'])[1])
    var sid = sidRow.replace('sid=','').replace('; path=/','')
    console.log( sid );


    if (!error && response.statusCode == 200) {
        console.log(response);
    }
}

    request(options, callback) ;


