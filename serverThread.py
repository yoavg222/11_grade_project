__author__ = 'Yoav'
import threading

class workerThread(threading.Thread):
    def __init__(self,game_logic,player1,player2):
        super().__init__()
        self.process_task = game_logic
        self.player1 = player1
        self.player2 = player2

    def run(self):
        self.process_task(self.player1,self.player2)
