from multiprocessing.connection import Client
import argparse

parser = argparse.ArgumentParser('term-quicktime-client', description='gets the current timer from the server')
parser.add_argument('--hours', help='number of hours used with set', type=int)
parser.add_argument('--minutes', help='number of minutes used with set', type=int)
parser.add_argument('--seconds', help='number of seconds used with set', type=int)
parser.add_argument('--millis', help='number of milliseconds used with set', type=int)
args = parser.parse_args()
address = ('localhost', 28513)

def get_readable_str(ms):
    if ms < 0:
        return 'completed'

    hours = int(ms / (1000 * 60 * 60))
    ms = ms % (1000 * 60 * 60)

    minutes = int(ms / (1000 * 60))
    ms = ms % (1000 * 60)

    seconds = int(ms / 1000)

    if hours != 0:
        return f'{hours}h {minutes}m {seconds}s'
    if minutes != 0:
        return f'{minutes}m {seconds}s'
    if seconds != 0:
        return f'{seconds}s'
    return '0'

set_mode = args.hours != None or args.minutes != None or args.seconds != None or args.millis != None

try:
    conn = Client(address)
    time = 0

    if set_mode:
        if args.hours != None:
            time += args.hours * 1000 * 60 * 60
        elif args.minutes != None:
            time += args.minutes * 1000 * 60
        elif args.seconds != None:
            time += args.seconds * 1000
        elif args.millis != None:
            time += args.millis

        conn.send(['set', time])
    else:
        conn.send(['get'])
        curr_time = conn.recv()
        s = get_readable_str(curr_time)
        print(s)
        conn.close()

except Exception as e:
    print(e)


