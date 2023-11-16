import requests

r = requests.get("https://bing.com")

print(r.text)
print(r.headers)
for cookies in r.cookies:
    print(cookies)