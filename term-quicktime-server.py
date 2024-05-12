from multiprocessing.connection import Listener
from datetime import datetime, timedelta
from time import sleep
import threading

address = ('localhost', 28513)
listener = Listener(address)

end_time = datetime.now()

while True:
    conn = listener.accept()
    msg = conn.recv()
    tag = msg[0]

    if tag == 'set':
        delta = msg[1]
        end_time = datetime.now() + timedelta(milliseconds=delta)
        conn.close()

    if tag == 'get':
        delta = (end_time - datetime.now())
        delta_millis = delta.total_seconds() * 1000
        conn.send(delta_millis)

listener.close()
