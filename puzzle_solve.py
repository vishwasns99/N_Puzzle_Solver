import random
from algorithms.tree_search import Node
from algorithms.bfs import search as bfs_search
from algorithms.manhattan_distance import search as man_search
from algorithms.misplaced_tiles import search as mis_search
from algorithms.custom import search1 as cus_search1
from algorithms.custom import search2 as cus_search2
from tkinter import *
import time

random.seed(31)

searches = [bfs_search, man_search, mis_search, cus_search1]
names = ['BFS', 'A* Search with manhattan distance heuristic',
         'A* Search with misplaced tile count heuristic', 'A* search with custom distance heuristic']


def draw_puzzle():

    global puzzle_frame, m, n

    for i in range(n):
        for j in range(m):
            number = states[state_index][i][j]
            number = str(number) if number else "-"
            message = grid_objects[i][j]
            message.configure(text=number)

    window.after(20, draw_puzzle)


def prev_state():
    global state_index

    if(state_index == 0):
        return False

    state_index -= 1
    return True


def next_state():
    global state_index

    if(state_index == number_of_states-1):
        return False
    print(state_index)
    state_index += 1

    draw_puzzle()
    return True


print("--------------------------------------")
print("Puzzle solver using state-space-search")
print("--------------------------------------")
print()

# Get puzzle size
n = 0
m = 0

while(n < 2 and m < 3):
    n, m = [int(i) for i in input("Enter puzzle size (n,m): ").split()]
    if(n < 2 or m < 3):
        print("Cannot take n<2 and m<3.")

print("--------------------------------------")
print()

# Create goal state
goal_state = []
for i in range(n):
    temp = []
    for j in range(m):
        temp.append(i*m+j)
    goal_state.append(temp)

# Get start state
choice = 0
start_state = []

print("1. Enter own start state.")
print("2. Take random start state.")
while(choice != 1 and choice != 2):

    print()
    choice = int(input("Enter choice: "))
    print()

    # Own start state
    if(choice == 1):
        print("Enter state for "+str(n)+"X"+str(m)+" puzzle:")
        for i in range(n):
            temp = []
            while(len(temp) != m):
                temp = [int(i) for i in input().split()]
                if(len(temp) != m):
                    print("Wrong row size. Enter row again")
            start_state.append(temp)

    # Random start state
    elif(choice == 2):
        steps = int(input("Enter number of steps: "))

        visited = []

        start_node = Node(goal_state)
        for i in range(steps):
            visited.append(start_node)
            start_node.expand()
            children_nodes = [
                node for node in start_node.children if not start_node.is_same(node)]
            for child in children_nodes:
                f = 1
                for vis in visited:
                    if(child.state == vis.state):
                        f = 0
                        break
                if(f):
                    start_node = child
        start_state = start_node.state

print("--------------------------------------")
print()

for i in range(len(names)):
    print(str(i+1)+'.', names[i])

print()
choice = -1
while(not(choice >= 0 and choice < len(names))):
    choice = int(input("Enter choice: "))-1

print("--------------------------------------")
print()

# Enter details
print("Start state: ", start_state)
print("Goal state: ", goal_state)
print("Search function: ", names[choice])

print("--------------------------------------")
print()

print("Enter any key to start state space search.")
input()

print("--------------------------------------")
print()

# Start
states = searches[i](start_state, goal_state)

state_index = 0
number_of_states = len(states)
print(number_of_states)
# Create window
window = Tk()
window.title("Puzzle solver")
window.geometry("750x750")
window.resizable(0, 0)
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=0)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)

# Create control buttons
prev_btn = Button(window, text="<<", width=25, height=2, command=prev_state)
prev_btn.grid(row=1, column=0)

next_btn = Button(window, text=">>", width=25, height=2, command=next_state)
next_btn.grid(row=1, column=2)

# Create puzzle frame
puzzle_frame = Frame(window, bg="black")
puzzle_frame.grid(row=0, column=0, sticky='WENS', padx=5, pady=5, columnspan=3)

# Create grids
grid_objects = []

for i in range(n):
    temp = []
    for j in range(m):
        message = Message(puzzle_frame, justify='center', bg='white')
        message.grid(row=i, column=j, sticky='WENS', padx=1, pady=1)
        puzzle_frame.grid_rowconfigure(j, weight=1)
        temp.append(message)
    puzzle_frame.grid_columnconfigure(i, weight=1)
    grid_objects.append(temp)

draw_puzzle()

window.mainloop()
