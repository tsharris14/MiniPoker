# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 11:32:41 2019

@author: charl
"""

import random


#--------------  Class Definitions ----------------------------
class Card:#this class only creates the deck of cards
    def __init__ (self, s, v):#self references the objects P1 and P2
        # s is the suit: "spades" "hearts" "diamonds" "club"
        # v is value:   2-10 11(J)  12(Q)  13(K)  14(A)
        self.suit = s
        self.value = v
    
    def display(self):
        if (self.value == 14):
            value = 'A'
        elif (self.value == 11):
            value = 'J'
        elif (self.value == 12):
            value = 'Q'
        elif (self.value == 13):
            value = 'K'
        else:
            value = self.value

        
        if (self.suit == "spades"):        
             print("[\u2660", value,"]",sep='',end='')
        elif (self.suit == "hearts"):
             print("[\u2661", value,"]",sep='',end='')
        elif (self.suit == "diamonds"):
             print("[\u2662", value,"]",sep='',end='')            
        elif (self.suit == "clubs"):
             print("[\u2663", value,"]",sep='',end='')
    

class Deck:#this class manipulates the deck of cards created by class Card
    def __init__ (self):
        self.cards = [None] * 52
        
        for i in range(0,13,1):
            self.cards[i] = Card("spades", i+2)
        
        for i in range(0,13,1):
            self.cards[i+13] = Card("hearts", i+2)
        
        for i in range(0,13,1):
            self.cards[i+26] = Card("diamonds", i+2)
        
        for i in range(0,13,1):
            self.cards[i+39] = Card("clubs", i+2)

        self.topIdx = 0
    
    def display(self):
        for i in range(len(self.cards)):
            self.cards[i].display()
        print("")
            
    def shuffle(self):
        for k in range(100):
            idx1 = random.randint(0,51)
            idx2 = random.randint(0,51)
               
            temp = self.cards[idx1]
            self.cards[idx1] = self.cards[idx2]
            self.cards[idx2] = temp

    def dealCard(self):
        #  returns the card from the top of the deck
        #   and update the top index
                
        someCard = self.cards[ self.topIdx ]
        self.topIdx = self.topIdx + 1
        return someCard
    
    def reset(self):
        self.shuffle()
        self.topIdx = 0
        
        
        
class Player:#this class deals the hand from the deck of cards created by class Card and shuffled by class Deck
    def __init__(self, n, m, b):
        # n = name of the player (string)
        # m = amount of money the player has initially
        self.name = n
        self.wallet = m
        self.hand = [None] * 3
        self.bet = b
        while (self.bet > self.wallet or self.bet < 0):
                self.bet = int(input("What's your bet?"))
           
        
        self.nCards = 0 # num cards you actually have at the moment  
        
    def show(self):
        print("----------------")
        print((self.name)+str(": "), "$", self.wallet, " ", "Score:",self.getScore(), " Bet:",self.bet, sep='')
        
        for i in range(self.nCards):
            self.hand[i].display()
        print("")
    
        
    def getCard(self, c):
        # c = a card object
        self.hand[ self.nCards ] = c
        self.nCards = self.nCards + 1
        
    def __gt__(self, other):
        myScore = self.getScore()
        otherScore = other.getScore()
        if (myScore > otherScore):
            return True
        else:
            return False
    
    def __lt__(self, other):
        return self.getScore() < other.getScore()
    
    
    def getScore(self):
        # return the score for the player
        # if we don't have 3 cards yet, return a score of 0
        
        if (self.nCards != 3):
            return 0
        
        #three of a kind
        if (self.hand[0].value == self.hand[1].value and self.hand[1].value == self.hand[2].value):
            return 1000 + self.hand[0].value
        # two of a kind (pair)
        elif (self.hand[0].value == self.hand[1].value):
            return 100 + self.hand[0].value
        elif (self.hand[1].value == self.hand[2].value):
            return 100 + self.hand[1].value
        elif (self.hand[0].value == self.hand[2].value):
            return 100 + self.hand[0].value 
        
        #highest card
        else:
            max = self.hand[0].value#the value of the first card in the array hand
            suit = self.hand[0].suit#the suit of the first card in the array hand
            
            for i in range(len(self.hand)):#length of array hand
                if (self.hand[i].value > max):
                    max = self.hand[i].value
                    suit = self.hand[i].suit
                    
            if (suit == "spades"):
                pts = max + 0.4
            elif (suit == "hearts"):
                pts = max + 0.3
            elif (suit == "diamonds"):
                pts = max + 0.2
            elif (suit == "clubs"):
                pts = max + 0.1
            
            return pts
        
    def lose(self,other):
        #self is the player, other is the computer
        self.wallet = self.wallet - self.bet
        other.wallet = other.wallet + other.bet
        return self.wallet,other.wallet
    
        
                      
#--------------  main program ----------------------------
'''an object can only call a method of the class that it was created by'''
d = Deck() #d is an object for the class Deck, not for the class Card!
d.display()#calls the method display which is apart of the class Deck
p1 = Player(input("Who are you?"), int(input("What's in your wallet?")),int(input("What's your bet?")))#object 1

p2 = Player("Computer", 1000, 100)#object 2

while ( p1.wallet > 0):
    '''an object can only call a method of the class that it was created by'''
    d.shuffle()#calls the method shuffle which is apart of the class Deck
    
    for i in range(3):
        p1.getCard( d.dealCard() )#for object 1, call getCard method, pass in the deck that calls dealCard method
        #d.dealCard - calls the dealCard method for the deck (d) - dealCard method will 
        p2.getCard( d.dealCard()  )
    
    
    p1.show()
    p2.show()
    
    if (p1 > p2):
        p2.lose(p1)
        print("----------------")
        print(p1.name , "wins!")
        
    elif (p1 < p2):
        p1.lose(p2)
        print("------------------")
        print(p2.name , "wins!")
    else:
        print("tie")
    
    p1.show()
    p2.show()
    p1.nCards = 0
    p2.nCards = 0
    if (p1.wallet == 0):
        print("GAME OVER. THANKS FOR PLAYING.")
    else:
        p1.bet = int(input("What's your bet?"))
    
