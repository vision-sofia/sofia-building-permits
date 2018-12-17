import requests
import logging
import json

if True:
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

s = requests.Session()
s.get('https://www.sofia-agk.com/RegisterBuildingPermitsPortal/Index')

total = 9999999
obtained = 0
page = 424
page_size = 100

while page * page_size < total:
    request_data = "sort=&page=%d&pageSize=%d&group=&filter=" % (page, page_size)
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Cookie": "_ga=GA1.2.1195547853.1543676906; _gid=GA1.2.729920264.1543676906; ASP.NET_SessionId=mfnuhxli1uiqp3slkpzdju3x",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Content-Length": str(len(request_data)),
        "Referer": "https://www.sofia-agk.com/RegisterBuildingPermitsPortal/Index",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

    response = s.post('https://www.sofia-agk.com/RegisterBuildingPermitsPortal/Read',
                      headers = headers, data=request_data)

    try:
        resp = response.content.decode('utf-8')
        print(resp)
        with open('resp-%d.json' % (page), 'w') as outfile:
            outfile.write(resp)
        data = json.loads(resp)
        total = data["Total"]
        with open('page-%d.json' % (page), 'w') as outfile:
            json.dump(data, outfile)
        print("page %d fetched" % page)
    except:
        print("failed to obtain page %d" % page)

    page += 1

