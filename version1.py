# -*- coding: utf-8 -*-

#Supermarket Process Modeller
#The aim of this program is to model the process/throughput flow of a supermarket in a step wise fashion

from random import randrange

timestep = 0.5
#customers_per_step = 1
store_capacity = 60
time_browsing = 10
time_checkout = 2
till_space = 3
store_space = 60
last_customer = "AA"
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
first = 0
second = 0
#Available states
states = ['Store Queue', 'Shopping', 'Checkout Queue', 'Checking Out', 'Left']

#Generate new customer IDs based on the previous customer's ID
def next_customer(last):
    if last == "ZZ":
        next_customer = "AA"
        return next_customer
    for i,x in enumerate(alphabet):
        if x == last[0]:
            first = i
        if x == last[1]:
            second = i + 1
    if second == 26:
        first += 1
        second = 0
    next_customer = alphabet[first] + alphabet[second]
    return next_customer

#How would people based look?
    # customer[]
class Customer:
    def __init__(self,name):
        self.name = name
        self.current_time = 0
        self.total_time = 0
        self.state_index = 0
       # self.state = states[self.state_index]
        self.browse_time = time_browsing
        self.checkout_time = time_checkout 
        
    
    def advance_time(self):
        self.current_time += timestep
        self.total_time += timestep
        if self.state_index ==3 :
            if self.current_time >= self.checkout_time:
                self.state_index += 1
                self.current_time = 0
                global till_space
                till_space += 1
                global store_space
                store_space += 1
            return
        elif self.state_index == 1:
            if self.current_time >= self.browse_time:
                self.state_index += 1
                self.current_time = 0
            return
        else:
            return
        
    def state(self):
        return states[self.state_index]
    
    #This moves customers from a queue they are in into the activity (no check to see if actually in queue)
    def advance_state(self):
        if self.state_index == 4:
            return
        self.current_time = 0
        self.state_index += 1
        return

#I want shopping queues that keep track of people
class Queue:
    def __init__(self,index):
        self.customers = []
        self.index = index
    
    def sort_queue(self,universe):
        self.customers = []
        for person in universe.everyone:
            if person.state_index == self.index:
                self.customers.append(person)
        self.customers.sort(key = lambda x: x.current_time)
        return
    def print_queue(self):
        for x in self.customers:
            print(x.name)
        return
        
class Universe:
    def __init__(self):
        self.everyone = []
        self.queues = []
        self.total_time = 0

        
    def sort_universe(self):
        self.everyone.sort(key = lambda x: x.state_index, reverse=True)
        return
      
    def create_life(self,people = 1):
        for x in range(0,people):
            global last_customer
            next_name = next_customer(last_customer)
            self.everyone.append(Customer(next_name))
            self.queues[0].customers.append(self.everyone[-1])
            last_customer = next_name
        return
    
    def roll_call(self):
        for person in self.everyone:
            print(person.name)
        return
    
    def advance_time(self, steps = 1):
        for i in range(0,steps):
            self.total_time += timestep
            for person in self.everyone:
                person.advance_time()
            global till_space
            global store_space
            for line in self.queues:
                line.sort_queue(self)
                if len(self.queues) == 0:
                    return
                while line.index == 0 and store_space > 0 and len(line.customers) != 0:
                    line.sort_queue(self)
                    line.customers[0].advance_state()
                    line.customers.pop(0)
                    store_space += -1
                while line.index == 2 and till_space > 0 and len(line.customers) != 0:
                    line.sort_queue(self)
                    line.customers[0].advance_state()
                    line.customers.pop(0)
                    till_space += -1            
        return
    
    def count(self):
        numbers = [0,0,0,0,0]
        for person in self.everyone:
            numbers[person.state_index] += 1
        return numbers
    
    def visualise(self):
        numbers = self.count()
        print('#' * 15 + '\n')
        print(f'Time: {self.total_time} \n')
        print(f'Store Queue')
        print(f'*' * numbers[0] + '\n')
        print(f'Shop Floor')
        print(f'*' * numbers[1] + '\n')
        print(f'Till Queue')
        print(f'*' * numbers[2] + '\n')
        print(f'Checking Out')
        print(f'*' * numbers[3] + '\n')   
        print(f'Served')
        print(numbers[4])
        if self.total_time == 0:
            print(f'Average Throughput = 0 customers per minute')
        else:
            print(f'Average Throughput = {numbers[4]/self.total_time} customers per minute')   
        print('#' * 15 + '\n')
        return
    
universe = Universe()
universe.queues.append(Queue(0))
universe.queues.append(Queue(2))    



#for x in range(0,1):
#    universe.create_life(randrange(10))
#    universe.advance_time()
#    universe.visualise()
#        
#debug
#time = 0
#for x in range(0,5):
#    universe.create_life(5)
#    universe.advance_time()
#    for queue in universe.queues:
#    print(states[queue.index])
#    queue.print_queue()

#    
#        
#for person in universe.everyone:
#    #print(person.name)
#    print(f'{states[person.state_index]} - {person.state_index}')
#    print(person.total_time)
#    
    


    
