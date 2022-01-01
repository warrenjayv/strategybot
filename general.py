from asyncio.events import Handle
import discord

class general:
    #~properties
    usr1 = [0] * 0x5
    usr2 = [0] * 0x5
    
    #~units
    trp = [ '░', '░' ]
    
    #~land
    acres = 0x8c       #plot size
    plot = [0] * acres #plot
    area1 = 0x0        #player 1 area
    area2 = 0x78       #player 2 area 
   # fma = 0x0        #player 1 message area
   # bta = 0x64       #battle area
   # sma = 0x80       #player 2 message area

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

    #~initial
    def __init__(self):
        for i in range(self.acres):
            self.plot[i] = "_"
            if i < 0x29:
                self.plot[i] = '_'
            if i%0x14 == 0:
                self.plot[i] = '\n'

    #~attack
    def go_attack(self, player, i, offset):
            self.plot[offset + i + self.D + 1] = self.trp[player]
            self.plot[offset + i + self.E ] = self.trp[player]
            self.plot[offset + i + self.F ] = self.trp[player]
            self.plot[offset + i + self.G + 1] = self.trp[player]
            if i > 0:
                self.plot[offset + i + self.D - 1 + 1] = '_'
                self.plot[offset + i + self.D + 1] = self.trp[player]
                self.plot[offset + i + self.E - 1] = '_'
                self.plot[offset + i + self.E ] = self.trp[player]
                self.plot[offset + i + self.F - 1] = '_'
                self.plot[offset + i + self.F ] = self.trp[player]
                self.plot[offset + i + self.G - 1 + 1] = '_'
                self.plot[offset + i + self.G + 1] = self.trp[player]

    def set_action(self, player):
        j = 0
        start = 0x7 + self.B 
        length = len(self.attack)

        for i in range( start , start + length ):
            self.plot[i] = self.attack[j] 
            j += 1


    def set_user(self, player, mention ):
        for i in range(0x5):
            self.usr2[i] = mention[i]
            self.plot[i + self.B ] = self.usr2[i]

        self.set_action(player)

    def clear_users(self):
        for i in range(0x5):
            self.usr1[i] = ' '
            self.usr2[i] = ' '
    
    def reset(self):   
        for i in range(self.acres):
            self.plot[i] = '_'
            if i%0x14 == 0:
               self.plot[i] = '\n'



#  plot (x2)
#       ----- zone 0 ------     ----- zone 1 ------
#      <-----  player 1 ------>      <----- action ------> 
#  A | 0x1  0x2  0x3  0x4  0x5  0x6  0x7  0x8  0x9  0xA  | message area
#      <-----  player 2 ------>
#  B | 0xB  0xC  0xD  0xD  0xE  0xF  0x11 0x12 0x13 0x14 | message area
#  C | 0x15 0x16 0x17 0x18 0x19 0x1A 0x1B 0x1C 0x1D 0x1E
#              <-------- battle area -------->
#  D | 0x1F 0x20 0x21 0x22 0x23 0x24 0x25 0x26 0x27 0x28
#  E | 0x29 0x2A 0x2B 0x2C 0x2D 0x2E 0x2F 0x30 0x31 0x32
#  F | 0x33 0x34 0x35 0x36 0x37 0x38 0x39 0x3A 0x3B 0x3C
#  G | 0x3D 0x3E 0x3F 0x41 0x42 0x43 0x44 0x45 0x46 0x47
#  H | 0x48 0x49 0x4A 0x4B 0x4C 0x4D 0x4E 0x4F 0x50 0x51

