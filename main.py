from collections import deque
from dataclasses import dataclass
from threading import Thread
import sys
import time
import winsound

#TODO: better sound
#TODO: delete from queue

#time in seconds
TIME_TEST = 15 * 60

@dataclass
class Person:
    name : str
    time : int 

class MyThread (Thread) :
    def __init__(self, queue, method, pipe):
        Thread.__init__(self)
        self.queue = queue
        self.method = method
        self.pipe = pipe

    def run(self):
        self.method(self.queue, self.pipe)

def make_sound(person):
    print(f'for {person.name} the time is up') 
    winsound.Beep(440, 500)
    winsound.Beep(490, 500)
    winsound.Beep(300, 500)
    winsound.Beep(440, 500) 

def print_queue(queue):
    print('\npersons in queue:\n')
    for person in queue:
        print(f'{person.name}: {(round(((TIME_TEST - (time.time() - person.time)) / 60) * 10 + 0.5)) / 10}min')
    print()

def get_input(queue, pipe):
    while True:
        message = input()

        if message:
            if message == 'show':
                print_queue(queue)

            elif message == 'exit':
                pipe.append('exit')
                sys.exit(0)

            else:
                queue.append(Person(message, time.time()))

def check_ready(queue, pipe):
    while True:
        if queue and time.time() - queue[0].time >= TIME_TEST:
            make_sound(queue.popleft())

        if pipe and pipe[0] == 'exit':
            sys.exit(0)

def main():
    queue = deque()
    pipe = []

    t1 = MyThread(queue, get_input, pipe)
    t2 = MyThread(queue, check_ready, pipe)

    t1.start()
    t2.start()

if __name__ == '__main__':
    main()