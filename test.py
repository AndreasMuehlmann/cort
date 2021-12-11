from collections import deque
from dataclasses import dataclass
import time
import winsound
from multiprocessing import Process, Queue

#TODO: use PyQt

#time in seconds
TIME_TEST = 1 * 10
SLEEP_TIME = 3

@dataclass
class Person:
    name : str
    time : int 

def make_sound(person):
    print(f'for {person.name} the time is up') 
    winsound.Beep(440, 500)
    winsound.Beep(490, 500)
    winsound.Beep(300, 500)
    winsound.Beep(440, 500) 

def print_queue(queue):
    print('\npersons in queue:\n')
    for person in queue:
        print(f'{person.name}: {(int(((TIME_TEST - (time.time() - person.time)) / 60) * 10)) / 10}min')
    print()

def main():
    queue = deque()
    processqueue = Queue()
    p = Process(target=get_input, args= (processqueue, ))
    p.start()

    while True:
        if queue and time.time() - queue[0].time >= TIME_TEST:
            make_sound(queue.pop())

        message = processqueue.get()

        if message:
            if message == 'show':
                print_queue(queue)
            else:
                queue.append(Person(message, time.time()))

def get_input(processqueue):
    while True:
        message = input()
        processqueue.put(message)


if __name__ == '__main__':
    main()