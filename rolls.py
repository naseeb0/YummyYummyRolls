from tkinter import *
from random import *
import tkinter.messagebox



class ScoreBoard():
    
    def __init__(self,parent):
        self.parent = parent       
        self.initGUI()        
        self.reset()
        
    def initGUI(self):
        
        self.livesVar = IntVar()
        Label(self.parent, text="Lives:", font=("Helvetica", 16, "bold")).grid(row=1, column=2, padx=35, pady=100, sticky=N+W)        
        Label(self.parent, textvariable=self.livesVar, font=("Helvetica", 16, "bold")).grid(row=1, column=2, padx=60, pady=150, sticky=N+W)        
        
      
        self.scoreVar = IntVar()
        Label(self.parent, text="Score:", font=("Helvetica", 16, "bold")).grid(row=1, column=2, padx=35, pady=250, sticky=N+W)
        Label(self.parent, textvariable=self.scoreVar, font=("Helvetica", 16, "bold")).grid(row=1, column=2, padx=50, pady=300, sticky=N+W)        
        
       
        self.highScoreVar = IntVar()
        Label(self.parent, text="Highest Score:", font=("Helvetica", 16, "bold")).grid(row=1, column=2, padx=0, pady=400, sticky=N+W)
        Label(self.parent, textvariable=self.highScoreVar, font=("Helvetica", 16, "bold")).grid(row=1, column=2, padx=50, pady=450, sticky=N+W)

    def reset(self):
        self.lives = 5
        self.score = 0
        self.highScore = self.loadScore()
        
        self.livesVar.set(self.lives)
        self.scoreVar.set(self.score)
        self.highScoreVar.set(self.highScore)

    def loadScore(self):
        with open("high-score.txt", "r") as data:
            return int(data.read())                
        
    def saveScore(self):
        if self.score > self.highScore:
            with open("high-score.txt", "w") as data:
                data.write(str(self.score))
        
    def gameOver(self):
        self.saveScore()
        tkinter.messagebox.showinfo("Game Over?", "Aww. All chances gone")        
        if tkinter.messagebox.askyesno("Are You still hungry ?", "Play Again ?"):
            self.reset()
        else:
            exit()
            
    def updateBoard(self, livesStatus, scoreStatus):
        self.lives += livesStatus; self.score += scoreStatus
        if self.lives < 0: self.gameOver()        
        self.livesVar.set(self.lives); self.scoreVar.set(self.score)



class ItemsFallingFromSky():
    
    def __init__(self,parent,canvas,player,board):
        self.parent = parent                    
        self.canvas = canvas                    
        self.player = player                    
        self.board = board                     
        
        self.fallSpeed = 50                           
        self.xPosition = randint(50, 750)       
        self.isgood = randint(0, 1)            
        
        self.goodItems = ["roll1.png","roll2.png","roll3.png"] # good items
        self.badItems = ["veg1.png","veg2.png","veg3.png"] #bad Items
        
        
        if self.isgood:   
            self.itemPhoto = tkinter.PhotoImage(file = "images/{}" .format( choice(self.goodItems) ) )
            self.fallItem = self.canvas.create_image( (self.xPosition, 50) , image=self.itemPhoto , tag="good" )
        else:
            self.itemPhoto = tkinter.PhotoImage(file = "images/{}" . format( choice(self.badItems) ) )
            self.fallItem = self.canvas.create_image( (self.xPosition, 50) , image=self.itemPhoto , tag="bad" )
            
        
        self.move_object()
        
        
    def move_object(self):
       
        self.canvas.move(self.fallItem, 0, 15)
        
        if (self.check_touching()) or (self.canvas.coords(self.fallItem)[1] > 650):    
            self.canvas.delete(self.fallItem)                                           
        else:
            self.parent.after(self.fallSpeed, self.move_object)                         
            
        
    def check_touching(self):
      
        x0, y0 = self.canvas.coords(self.fallItem)
        x1, y1 = x0 + 50, y0 + 50
        
        
        overlaps = self.canvas.find_overlapping(x0, y0, x1, y1)
        
        if (self.canvas.gettags(self.fallItem)[0] == "good") and (len(overlaps) > 1) and (self.board.lives >= 0):   
            self.board.updateBoard(0, 100)                                              
            return True                                                                 
            
        elif (self.canvas.gettags(self.fallItem)[0] == "bad") and (len(overlaps) > 1) and (self.board.lives >= 0):  
            self.board.updateBoard(-1, 0)                                              
            return True                                                                
            
        return False                                                                   
    


class TheGame(ItemsFallingFromSky,ScoreBoard):
    
    def __init__(self,parent):
        self.parent = parent
        
        
        self.parent.geometry("1024x650")
        self.parent.title("Yummy Yummy Rolls")

       
        self.canvas = Canvas(self.parent, width=800, height=600)
        self.canvas.config(background="#96DEDA")
        self.canvas.bind("<Key>", self.keyMoving)      
        self.canvas.focus_set()
        self.canvas.grid(row=1, column=1, padx=25, pady=25, sticky=W+N)

        
        self.playerPhoto = tkinter.PhotoImage(file = "images/{}" .format( "1.png" ) ) 
        self.playerChar = self.canvas.create_image( (475, 560) , image=self.playerPhoto , tag="player" )

        
        self.personalboard = ScoreBoard(self.parent)

    
        self.createEnemies()
        
        
    def keyMoving(self, event):        
        if (event.char == "A") and (self.canvas.coords(self.playerChar)[0] > 50):
            self.canvas.move(self.playerChar, -50, 0)            
        if (event.char == "D") and (self.canvas.coords(self.playerChar)[0] < 750):
            self.canvas.move(self.playerChar, 50, 0)


    def createEnemies(self):
        ItemsFallingFromSky(self.parent, self.canvas, self.playerChar, self.personalboard)
        self.parent.after(1100, self.createEnemies)
        

        
if __name__ == "__main__":
    root = Tk()
    TheGame(root)
    root.mainloop()
