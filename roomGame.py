import random

class Room:
    def __init__(self,p1,p2):
        self.player1 = p1
        self.player2 = p2

    def who_first(self):
        num = random.randint(1,2)
        return num


    def add_place_to_lst(self,lst):
        lst_new  = []
        for i in range(1,4):
            lst_new.append(lst[i])

        return lst_new