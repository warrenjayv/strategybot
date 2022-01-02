from asyncio.events import Handle
from math import expm1
from os import dup2
from time import daylight
import discord
import random

class general:
    #~properties
    usr1 = [0] * 0x6
    usr2 = [0] * 0x6
    
    health1 = 1000
    health2 = 1000

    #~units
    trp = [ '░', '░' ]
    
    #~land
    acres = 0xB4       #plot size
    plot = [0] * acres #plot
    area1 = 0x0        #player 1 area
    area2 = 0xA        #player 2 area 
   # fma = 0x0         #player 1 message area
   # bta = 0x64        #battle area
   # sma = 0x80        #player 2 message area
 
    #~vertical zones
    A = 0              #0
    B = 0x14           #20
    C = 0x28           #40
    D = 0x3C           #60
    E = 0x50           #80
    F = 0x64           #100
    G = 0x78           #120
    H = 0x8C           #140

    #~actions
    attack = "attacking"
    defend = "defending"
    march  = "marching"
    defeat = "defeated"

    #~initial
    def __init__(self):
        for i in range(self.acres):
            self.plot[i] = "_"
            if i%0x14 == 0:
                self.plot[i] = '\n'

    def set_health(self):

        h1 = '{}'.format(self.health1)
        h2 = '{}'.format(self.health2)
     
        #~clear first
        for j in range(0x5):
            self.plot [ 0x5 + self.C + self.area1 + j] = '_'
            self.plot [ 0x5 + self.C + self.area2 + j] = '_'
        
        #~setter
        for i in range(len(h1)):
            self.plot [ 0x5 + self.C + self.area1 + i ] = h1[i]
        for k in range(len(h2)):
            self.plot [ 0x5 + self.C + self.area2 + k ] = h2[k]
        
    #~battle
    def do_battle(self):

        #~dices for user1
        D1 =   random.randint(0, 20)
        E1 =   random.randint(0, 20)
        F1 =   random.randint(0, 20)
        G1 =   random.randint(0, 20) 

        #~dices for user2
        D2 =   random.randint(0, 20)
        E2 =   random.randint(0, 20)
        F2 =   random.randint(0, 20)
        G2 =   random.randint(0, 20)


        #~apply damage
        self.health1 -= D2
        self.health1 -= E2
        self.health1 -= F2
        self.health1 -= G2

        self.health2 -= D1
        self.health2 -= E1
        self.health2 -= F1
        self.health2 -= G1

        self.plot [ 0x5 + self.D + self.area2 ] = str(D1)
        self.plot [ 0x5 + self.E + self.area2 ] = str(E1)   
        self.plot [ 0x5 + self.F + self.area2 ] = str(F1)
        self.plot [ 0x5 + self.G + self.area2 ] = str(G1)

        self.plot [ 0x6 + self.D + self.area2 ] = str(D2)
        self.plot [ 0x6 + self.E + self.area2 ] = str(E2)
        self.plot [ 0x6 + self.F + self.area2 ] = str(F2)
        self.plot [ 0x6 + self.G + self.area2 ] = str(G2)

    #~conclude
    def conclude( self ):
        if (self.health1 > self.health2):
            end ="attacker won !".format(self.usr1)
        else:
            end ="defender won !".format(self.usr2)

        print(end)
        
        for i in range(len(end)):
            self.plot[0x8D + self.area1 + i + 1] = end[i]
    
    #~attack
    def go_attack(self, i, offset):
            self.plot[offset + i + self.D + 1] = self.trp[0]
            self.plot[offset + i + self.E ] = self.trp[0]
            self.plot[offset + i + self.F ] = self.trp[0]
            self.plot[offset + i + self.G + 1] = self.trp[0]
            if i > 0:
                self.plot[offset + i + self.D - 1 + 1] = '_'
                self.plot[offset + i + self.D + 1] = self.trp[0]
                self.plot[offset + i + self.E - 1] = '_'
                self.plot[offset + i + self.E ] = self.trp[0]
                self.plot[offset + i + self.F - 1] = '_'
                self.plot[offset + i + self.F ] = self.trp[0]
                self.plot[offset + i + self.G - 1 + 1] = '_'
                self.plot[offset + i + self.G + 1] = self.trp[0]
            
    def go_defend(self):

                self.plot[ 0x9 + self.D + self.area2 ] = self.trp[0]
                self.plot[ 0x9 + self.E + self.area2 ] = self.trp[0]
                self.plot[ 0x9 + self.F + self.area2 ] = self.trp[0]
                self.plot[ 0x8 + self.G + self.area2 ] = self.trp[0]                

    def set_action(self):

        start1 = 0x8 + self.A
        start2 = 0x8 + self.B 
        length = len(self.attack)

        j = 0
        for i in range( start2 , start2 + length ):
            self.plot[i] = self.defend[j] 
            j += 1

        j = 0
        for i in range ( start1 , start1 + length ):
            self.plot[i] = self.attack[j]
            j += 1 
            
    def set_user(self, author, mention ):
        for i in range(0x6):

            #mentioned
            self.usr2[i] = mention[i]
            self.plot[i + self.B + 1] = self.usr2[i]

            #author
            self.usr1[i] = author[i]
            self.plot[i + self.A] = self.usr1[i]

        self.set_action()

    def clear_users(self):
        for i in range(0x6):
            self.usr1[i] = ' '
            self.usr2[i] = ' '
    
    def reset(self):   
        for i in range(self.acres):
            self.plot[i] = '_'
            if i%0x14 == 0:
               self.plot[i] = '\n'


#  plot (x2)
#       ----- zone 0 ------     ----- zone 1 ------
#      <-----  player 1 ------>           <--- action ---->
#  A | 0x1  0x2  0x3  0x4  0x5  0x6  0x7  0x8  0x9  0xA  | message area
#      <-----  player 2 ------>
#  B | 0xB  0xC  0xD  0xD  0xE  0xF  0x11 0x12 0x13 0x14 | message area
#      <----- player 1 health --->
#  C | 0x15 0x16 0x17 0x18 0x19 0x1A 0x1B 0x1C 0x1D 0x1E
#              <-------- battle area -------->  
#  D | 0x1F 0x20 0x21 0x22 0x23 0x24 0x25 0x26 0x27 0x28
#  E | 0x29 0x2A 0x2B 0x2C 0x2D 0x2E 0x2F 0x30 0x31 0x32
#  F | 0x33 0x34 0x35 0x36 0x37 0x38 0x39 0x3A 0x3B 0x3C
#  G | 0x3D 0x3E 0x3F 0x41 0x42 0x43 0x44 0x45 0x46 0x47
#  H | 0x48 0x49 0x4A 0x4B 0x4C 0x4D 0x4E 0x4F 0x50 0x51
#       1    2     3    4   5       <-- dice -->
