# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import socket
import json
from collections import deque

# <codecell>

global map_width
global map_height

# <codecell>

def readLine(sck):
    res = ""
    c = ""
    while(1):
        c=sck.recv(1)
        if(c=='\n'):
            break
        res+=c
    return res

# <codecell>

def getMapSize(string):
    if "CITY:" in string:
        width = ""
        count = 0
        for i in string[5:]:
            count+=1
            if i not in "0123456789":
                break
            width+=i
        return (int(width), int(string[5+count:]))
    else:
        return

# <codecell>

def getVal(string, beg):
    return int(string[len(beg):])

# <codecell>

def calculateEstimite(tab):
    
    visited = tab #[[False for x in range(map_width)] for x in range(map_height)]
    
    #for y in range(map_height):
    #    for x in range(map_width):
    #        visited[y][x] = tab[y][x]
            
    estimite = [[0 for x in range(map_width)] for x in range(map_height)]
    
    q = deque()
    
    for y in range(map_height):
        for x in range(map_width):
            if visited[y][x]:
                q.append((x,y))
            
    while(len(q)):
        cur = q.popleft()
        
        for dx in range(-1,2):
            for dy in range(-1,2):
                
                next_x = (cur[0]+dx)%map_width
                next_y = (cur[1]+dy)%map_height
                
                if not visited[next_y][next_x]:
                    visited[next_y][next_x] = True
                    estimite[next_y][next_x] = estimite[cur[1]][cur[0]]+1
                    q.append((next_x,next_y))
        
    return estimite

# <codecell>

def calculateBest(step):
    
    tab = [[False for x in range(map_width)] for x in range(map_height)]
    estimite = [[0 for x in range(map_width)] for x in range(map_height)]
    
    for bomb in step["targets"]:
        for dx in range(-1,2):
            for dy in range(-1,2):
                tab[(bomb[1]+dy)%map_height][(bomb[0]+dx)%map_width] = True
                
    estimite = calculateEstimite(tab)
    
    #for i in range(map_height):
    #    print estimite[i]
        
    cur_max = 0
    best_dx = 0
    best_dy = 0
        
    for dx in range(-2,3):
            for dy in range(-2,3):
                new_x = (step["player"][0]+dx)%map_width
                new_y = (step["player"][1]+dy)%map_height
                
                if cur_max<estimite[new_y][new_x]:
                    cur_max = estimite[new_y][new_x]
                    best_dx = dx
                    best_dy = dy
        
    return (best_dx,best_dy)
                

# <codecell>

#print calculateBest(json.loads("{\"player\": [3, 2], \"targets\": [[7, 4], [1, 3], [8, 0], [9, 7], [8, 6]]}"));

# <codecell>

def processStep(sck):
    line = readLine(sck)
    
    if "ROUND:" in line:
        #print "Procesing round: ", getVal(line, "ROUND:")
        return 1
    
    #print "Procesing step: ", getVal(line, "STEP:")
    step = json.loads(readLine(sck))
    (dx, dy) = calculateBest(step)
    #print step["player"]
    sck.send("{\"x\":"+str(dx)+",\"y\":"+str(dy)+"}\n")
    return 0

# <codecell>

def play(sck):
    while(1):
        #print "Procesing round: ", getVal(readLine(sck), "ROUND:")
        
        while(1):
            if processStep(sck):
                continue
            ans = readLine(sck)
            if ans == "DEAD":
                return
            if ans == "OK":
                continue

# <codecell>

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 31415))

(map_width, map_height) = getMapSize(readLine(s))
    
play(s)
s.close()

# <codecell>


