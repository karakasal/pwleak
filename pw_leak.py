import requests
import hashlib
import sys

def request_api_data(query_char):
    url = "https://api.pwnedpasswords.com/range/" + query_char
    res = requests.get(url) 
    if res.status_code != 200: 
        raise RuntimeError(f"Error {res.status_code()}")
    return res

def get_password_leak_count(hashes, hash_to_check):
    hashes = (line.split(":") for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

def pwned_api_check(password):
    sha1pass = hashlib.sha1(password.encode("utf-8")).hexdigest().upper() 
    first5, tail = sha1pass[:5], sha1pass[5:]
    response = request_api_data(first5)
    return get_password_leak_count(response, tail)

def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(password, count)
        else:
            print("Secure!")

sys.exit(main(sys.argv[1:]))
