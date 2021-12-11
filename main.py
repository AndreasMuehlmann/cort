from collections import deque
from dataclasses import dataclass
from multiprocessing import Process, Queue
import time
import winsound

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
    queue.append(Person(input(), time.time()))

    while queue:
        if time.time() - queue[0].time >= TIME_TEST:
            make_sound(queue.pop())

        message = input()

        if message:
            if message == 'show':
                print_queue(queue)
            else:
                queue.append(Person(message, time.time()))

if __name__ == '__main__':
    main()