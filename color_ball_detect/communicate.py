import requests
import time
import multiprocessing

import detect 
URL = 'http://172.20.10.14'


def ctl(direction):
    requests.get('{}/{}'.format(URL,direction), allow_redirects=True)

def process():
    r = requests.get('{}/'.format(URL), allow_redirects=True)
    open('capture.jpg', 'wb').write(r.content)
    profile = detect.main('capture.jpg')
    closest = 0
    direction = 'clear'
    for color in profile:
        if profile[color]['max'] > closest:
            closest = profile[color]['max']
            direction = profile[color]['direction']
    ctl(direction)
    print(direction)

def loop():
    p = multiprocessing.Process(target=process)
    p.start()
    p.join(timeout=1.5)
    if p.is_alive():
        print('terminate')
        # Terminate foo
        p.terminate()


if __name__ == '__main__':
    while(True):
        loop()
        # time.sleep(1)