# Name: Halanna Yuh
# Course: 15112 at Carnegie Mellon University (Spring 2019)
# Instructor: Professor Kelly Rivers
# Mentor: Ria Pradeep

#TPGame.py file handles the quiz game.

import random
import matplotlib.pyplot as plt 

#15112 website: https://www.cs.cmu.edu/~112/notes/notes-strings.html
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

#Class for box containing game answer choices.
class answerBox(object):
    def __init__(self, data, x, y):
        self.x = x
        self.y = y
        self.width = data.width/2
        self.height = 80
        self.isCorrect = False
        self.color = None
        self.text = random.choice(list(data.translPairs.values()))
        
    def __eq__(self, other):
        return (isinstance(other, answerBox) and (self.x == other.x) and \
            (self.y == other.y))

    def draw(self, canvas):
        canvas.create_rectangle(self.x, self.y, self.x+self.width, 
            self.y+self.height, fill = self.color)
        canvas.create_text(self.x + self.width/2, self.y + self.height/2, 
        text = self.text)
    
    #Randomly chooses a translated word to place in answer box.
    def changeText(self, data):
        possChoice = random.choice(list(data.translPairs.values()))
        while possChoice in data.isPlaced:
            possChoice = random.choice(list(data.translPairs.values()))
        self.text = possChoice
        data.isPlaced.append(possChoice)

#Graph class for graphing progress report.  
#https://matplotlib.org/users/pyplot_tutorial.html      
class Graph(object):
    def __init__(self, xPoint, yPoint):
        self.xPoint = xPoint
        self.yPoint = yPoint
    
    def makeGraph(self):
        plt.plot(self.xPoint, self.yPoint, color='green', linestyle='dashed', 
            linewidth = 3, marker='p', markerfacecolor='blue', markersize=12) 
        
        # setting x and y axis range 
        plt.ylim(0, 100) 
        plt.xlim(1) 
        
        # naming the x axis 
        plt.xlabel('Quiz') 
        # naming the y axis 
        plt.ylabel('Percent Correct') 
        
        # giving a title to my graph 
        plt.title('Accuracy Progress')
        plt.show()
        
from tkinter import *
def init(data):
    data.mode = 'start'
    
    #dictionary for tracking how often users get a question wrong.
    data.optionProb = {}
    for key in data.translPairs:
        data.optionProb[key] = 1
    print(data.optionProb)

    data.option = selectChoice(data.optionProb)
    data.boxWidth = data.width/5
    data.boxHeight = data.height/10
    
    #Sets answer boxes on canvas.
    data.answerBoxes = []
    data.answerBoxes += [answerBox(data, data.width/2, data.height - 80)]
    data.answerBoxes += [answerBox(data, 0, data.height - 80)]
    data.answerBoxes += [answerBox(data, data.width/2, data.height - 160)]
    data.answerBoxes += [answerBox(data, 0, data.height - 160)]
    
    data.isQuestAns = False
    data.isRight = ''
    
    data.isPlaced = [data.translPairs[data.option]]
    
    #Randomly chooses 1 of 4 answer boxes to place correct answer in.
    chooseCorrectBox(data)
    for box in data.answerBoxes:
        if not box.text == data.translPairs[data.option] + ' *':
            box.changeText(data)
    #Question and score information.        
    data.totalQues = 20
    data.whichQues = 1
    data.numRight = 0
    data.scorePercent = 0
    data.quizAverage = 0
    #Progress information.
    data.accuracyData = []
    data.games = []
    data.currentGame = 0
    
    #Reads and accesses file that tracks user progress.
    try:
        s = readFile('accuracy.txt')
        #retrieves games list
        gamesStr = s.splitlines()[0]
        tokens = gamesStr[1:-1].split(",")
        for elem in tokens:
            data.games.append(int(elem))
        print(data.games, type(data.games))
        #retrieves accuracy data list
        accStr = s.splitlines()[1]
        tokens = accStr[1:-1].split(",")
        for elem in tokens:
            data.accuracyData.append(float(elem))
        data.currentGame = data.games[len(data.games) - 1]
        print(data.games, type(data.games), data.accuracyData, 
            type(data.accuracyData), data.currentGame)
    except:
        data.accuracyData = []
        data.games = []
        data.currentGame = 0
    #widget colors    
    data.colors = {
        'startButton': 'white', 
        'startText' : 'black', 
        'next':'gray',
        'reportButton': 'white',
        'reportText': 'black',
        'clearButton': 'white',
        'clearText': 'black',
        'nextQuizBtn': 'white',
        'nextQuizTxt': 'black',
        }

#Randomly chooses 1 of 4 answer boxes to place correct answer in.    
def chooseCorrectBox(data):
    data.correctBox = random.choice(data.answerBoxes)
    data.correctBox.text = data.translPairs[data.option] + ' *'

###### MODE DISPATCHER ########
def mousePressed(event, data):
    if data.mode == 'start': startMousedPressed(event, data)
    elif data.mode == 'play': playMousedPressed(event, data)
    elif data.mode == 'end': endMousePressed(event, data)
#Detects if mouse is hovering over a button in each screen.    
def hoverDetect(event, data):
    if data.mode == 'start': startHoverDetect(event, data)
    elif data.mode == 'play': playHoverDetect(event, data)
    elif data.mode == 'end': endHoverDetect(event, data)
    
def redrawAll(canvas, data):
    if data.mode == 'start': startRedrawAll(canvas, data)
    elif data.mode == 'play': playRedrawAll(canvas, data)
    elif data.mode == 'end': endRedrawAll(canvas, data)

def keyPressed(event, data):
    if data.mode == 'play': playKeyPressed(event, data)


#Checks when the game should end        
def timerFired(data):
    if data.whichQues > data.totalQues and data.mode != 'end':
        data.mode = 'end'
        data.currentGame += 1
        data.games.append(data.currentGame)
        data.accuracyData.append((data.numRight / data.totalQues) * 100)
        graphPoints = str(data.games) + '\n' + str(data.accuracyData) 
        writeFile('accuracy.txt', graphPoints)

#selects questions that users get wrong more often    
def selectChoice(d):
    dictSum = 0
    total = sum(d.values())
    d1 = []
    for key in d:
        dictSum += d[key]
        d1.append([key, dictSum])
    choice = None
    while choice == None:
        randomInt = random.randint(1, total)
        for key in d1:
                if randomInt <= key[1]:
                    choice = key[0]
                    break
    return choice

### HOVER DETECT - detects if mouse is hovering over buttons. 
def onStartButton(data, x, y):
    if (x > data.width/2 - 75 and x < data.width/2 + 75 and
        y > data.height*(3/4)-30 and y < data.height*(3/4)+30):
            return True
    return False
    
def onNext(data, x, y):
    if (x > data.width - 70 and x < data.width - 10 and y < 30 and y > 10):
        return True
    return False
    
def onClear(data, x, y):
    if x > 10 and y > data.height - 80 and x < 160 and y < data.height - 20:
        return True
    return False
    
def onReport(data, x, y):
    if x > 10 and y > data.height - 150 and x < 160 and y < data.height - 90:
        return True
    return False
    
def onQuiz(data, x, y):
    if x > data.width-160 and y > data.height - 80 and x < data.width-10 and \
    y < data.height - 20:
        return True
    return False
    
######################## START ###########################################    
def startRedrawAll(canvas, data):
    canvas.create_text(data.width/2, data.height/4, text = 'QUIZ YOURSELF!', 
    font ='Helvetica 40 bold', fill = "#3E92CC")
    canvas.create_text(data.width/2, data.height/2, text = '''Take a 20 question 
    quiz \nto test your knowledge.''', font = 'Helvetica 20')
    canvas.create_rectangle(data.width/2-75, data.height*(3/4)-30, 
    data.width/2+75, data.height*(3/4)+30, fill=data.colors['startButton'])
    canvas.create_text(data.width/2, data.height*(3/4), text="START", 
    font="Helvetica 18", fill=data.colors['startText'])
    
def startMousedPressed(event, data):
    if onStartButton(data, event.x, event.y):
        data.mode = 'play'
    
def startHoverDetect(event, data):
    if onStartButton(data, event.x, event.y):
        data.colors['startButton'] = 'black'
        data.colors['startText'] = 'white'
    else:
        data.colors['startButton'] = 'white'
        data.colors['startText'] = 'black'
        
######################## PLAY #############################################
def playRedrawAll(canvas, data):
    canvas.create_text(30, 10, text = '%d of %d' %(data.whichQues, data.totalQues))
    canvas.create_rectangle(data.width/2 - data.boxWidth, data.height/4 - data.boxHeight, 
    data.width/2 + data.boxWidth, data.height/4 + data.boxHeight)
    canvas.create_text(data.width/2, data.height/4, text = data.option, font = 20)
    for box in data.answerBoxes:
        box.draw(canvas)
    
    if data.isQuestAns == True:
        canvas.create_text(data.width/2, data.height/2, text = data.isRight, 
        font='Helvetica 16')
        
    canvas.create_text(data.width - 40, 20, text="NEXT", font="Helvetica 16 bold",
                        fill=data.colors['next'])
        
def playMousedPressed(event, data):
    if data.isQuestAns == False:
        for box in data.answerBoxes:
            if event.x > box.x and event.x < box.x + box.width and \
            event.y > box.y and event.y < box.y + box.height:
                data.isQuestAns = True
                if box == data.correctBox:
                    box.color = 'green'
                    data.isRight = 'Correct'
                    data.numRight += 1
                    data.optionProb[data.option] = 1
                else:
                    box.color = 'red'
                    data.isRight = 'Wrong'
                    data.optionProb[data.option] *= 2
    
    if onNext(data, event.x, event.y):
        data.isQuestAns = False
        data.option = selectChoice(data.optionProb)
        data.isPlaced = [data.translPairs[data.option]]
        for box in data.answerBoxes:
            box.changeText(data)
            box.color = None
        chooseCorrectBox(data)
        data.whichQues += 1
        print(data.optionProb)
        
                    
def playHoverDetect(event, data):
    if onNext(data, event.x, event.y):
        data.colors['next'] = 'black'
    else:
        data.colors['next'] = 'gray'
                    
def playKeyPressed(event, data):
    if event.keysym == 'e':
        data.isQuestAns = False
        #data.option = random.choice(list(data.translPairs.keys()))
        data.option = selectChoice(data.optionProb)
        data.isPlaced = [data.translPairs[data.option]]
        for box in data.answerBoxes:
            box.changeText(data)
            box.color = None
        chooseCorrectBox(data)
        data.whichQues += 1
        print(data.optionProb)
        
###################### END #################################
        
def endRedrawAll(canvas, data):
    data.scorePercent = (data.numRight / data.totalQues) * 100
    if len(data.accuracyData) == 0:
        data.quizAverage = 0
    else:
        data.quizAverage = sum(data.accuracyData) / len(data.accuracyData)
    canvas.create_text(data.width/2, 40, text = 'GAME OVER', 
    font = 'Helvetica 40 bold', fill = "#3E92CC")
    
    canvas.create_text(data.width/2, data.height/3, 
    text = 'Your score: \n%d/%d\n%0.1f %s\nCumulative Quiz Average: %0.1f%s'
     %(data.numRight, data.totalQues, data.scorePercent, '%', data.quizAverage, 
     '%'), font = 'Helvetica 16')
     
    #clear report button
    canvas.create_rectangle(10, data.height - 80, 160, data.height - 20, 
    fill=data.colors['clearButton'])
    canvas.create_text(85, data.height - 50, text='Clear Progress', 
    fill=data.colors['clearText'])
    #progress report button
    canvas.create_rectangle(10, data.height - 150, 160, data.height - 90, 
    fill=data.colors['reportButton'])
    canvas.create_text(85, data.height - 120, text='Progress Report', 
    fill=data.colors['reportText'])
    #next quiz button
    canvas.create_rectangle(data.width-160, data.height - 80, data.width-10, 
    data.height - 20, fill=data.colors['nextQuizBtn'])
    canvas.create_text(data.width-85, data.height - 50, text='Next Quiz', 
    fill=data.colors['nextQuizTxt'])

def endMousePressed(event, data):
    if onClear(data, event.x, event.y):
        writeFile('accuracy.txt', '')
        data.accuracyData = []
        data.games = []
        data.currentGame = 0
    
    if onReport(data, event.x, event.y):
        accuracy = Graph(data.games, data.accuracyData)
        accuracy.makeGraph()
        
    if onQuiz(data, event.x, event.y):
        data.numRight = 0
        data.whichQues = 1
        for key in data.translPairs:
            data.optionProb[key] = 1
        data.mode = 'play'
        
def endHoverDetect(event, data):
    if onClear(data, event.x, event.y):
        data.colors['clearButton'] = 'black'
        data.colors['clearText'] = 'white'
    else:
        data.colors['clearButton'] = 'white'
        data.colors['clearText'] = 'black'
    
    if onReport(data, event.x, event.y):
        data.colors['reportButton'] = 'black'
        data.colors['reportText'] = 'white'
    else:
        data.colors['reportButton'] = 'white'
        data.colors['reportText'] = 'black'
    
    if onQuiz(data, event.x, event.y):
        data.colors['nextQuizBtn'] = 'black'
        data.colors['nextQuizTxt'] = 'white'
    else:
        data.colors['nextQuizBtn'] = 'white'
        data.colors['nextQuizTxt'] = 'black'
        

#112 website: https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
def run(width=300, height=300, pairs = None):
    if pairs == None:
        pairs = {}
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)
        
    def hoverDetectWrapper(event, canvas, data):
        hoverDetect(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
        
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    data.translPairs = pairs
    init(data)
    # create the root and the canvas
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    root.bind("<Motion>", lambda event:
                            hoverDetectWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed

#run(600, 400)
