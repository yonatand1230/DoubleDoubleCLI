import requests, sys

if len(sys.argv) < 2: 
    print("No URL provided!")
    exit()

url = sys.argv[1]
print(url)
#url = ""#"https://open.spotify.com/track/0VE4kBnHJUgtMf0dy6DRmW"
api_url = "https://doubledouble.top/dl"

# init downloading
response = requests.get(api_url, 
            params={
                "url":url,
                "format":"ogg"
            }
        )
try:
    j = response.json()
except Exception as e:
    print(e, '\n---------\n', response.text)

if not j.get('success'): exit()

id = j.get('id')
print(f'Init downloading...\nid={id}')

# finish initiating 
status_url = api_url + f'/{id}'

downloading = False
while not downloading:
    response = requests.get(status_url)
    if response.json().get('status') == 'downloading':
        downloading = True

# downloading - print status
percent = 0
done = False
while not done:
    response = requests.get(status_url)
    if response.status_code != 200: exit()
    j = response.json()
    if j.get('status') == 'done':
        done = True
    else:
        if int(j.get("percent"))-percent>3 or percent==100:
            percent = int(j.get("percent"))
            print(f'{j.get("friendlyStatus")} | {percent}%')
    

# done - print info
print('Done | 100%')

final_url = 'https://doubledouble.top' + j.get('url')[1:]
print(final_url)