import requests
import time
import multiprocessing

import detect 

def process():
    url = 'http://192.168.1.26/'
    r = requests.get(url, allow_redirects=True)
    open('capture.jpg', 'wb').write(r.content)
    print( detect.main('capture.jpg') )
    print('finish')

def loop():
    p = multiprocessing.Process(target=process)
    p.start()
    p.join(timeout=1)
    if p.is_alive():
        print('terminate')
        # Terminate foo
        p.terminate()


if __name__ == '__main__':
    while(True):
        loop()
        # time.sleep(1)