# Name: Halanna Yuh
# Course: 15112 at Carnegie Mellon University (Spring 2019)
# Instructor: Professor Kelly Rivers
# Mentor: Ria Pradeep

#TPmain.py handles the main application and translation components.

from PIL import Image
import pytesseract

from tkinter import filedialog
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
import tkinter as tk

#https://pypi.org/project/googletrans/
from googletrans import Translator

import string

import TPGame as tp

#Creates a SmartTranslate class.
#Window design inspired by LiveThesaurus: https://www.youtube.com/watch?v=QUXn-8Eoq7w
class SmartTranslate(object):
    def __init__(self, master):
        self.readText = ''
        self.translated = ''
        self.detailWords = {}
        self.highlightWords = {}
        self.pairs = {}
        self.unacceptedStrings = ' \n-ー' #do not translate these characters.
        self.detectLang = ''
        
        self.master = master
        self.instructionsFrame = Frame(self.master)
        self.instructionsLabel = Label(self.instructionsFrame, 
                                    text="SmartTranslate",
                                    anchor=N, borderwidth=5, relief="groove")
        self.instructionsFrame.pack(side=TOP, fill=BOTH, padx=5, pady=(5,0))
        self.instructionsLabel.pack(side=TOP, fill=BOTH, padx=3, pady=3)
        
        self.instructionsFrame.config(background="blue")
        self.instructionsLabel.config(font=("Helvetica", 22, "bold"))
        
        self.instructions = "SmartTranslate Instructions\n" + \
                            "Upload image of text you want to translate.\n" + \
                            "Select a language from the drop down menu.\n" + \
                            "Direct: Translate your paragraph as is.\n" + \
                            "Detail: Translate individual words or characters.\n" + \
                            "Highlight: Select phrases you want to translate and\n" + \
                            "hit the Translate button.\n\n" + \
                            "To play game, either add your 'Detail' or 'Highlight'\n" + \
                            "translations or both!\n" + \
                            "You need at least 5 translations to begin game."
        
############## LEFT FRAME ############################        
        self.leftFrame = Frame(self.master)
        self.textFrame = Frame(self.leftFrame, borderwidth=2, relief="solid")
        self.uploadFrame = Frame(self.leftFrame, borderwidth=2, relief="solid")
        
        self.originalBox = Text(self.textFrame, borderwidth=2)
        self.originalBox.insert(END, self.instructions)

        self.uploadButton = Button(self.uploadFrame, width=35, height=1, 
                                  text="Upload Image", command=self.onUpload)
        self.textScrollBar = Scrollbar(self.textFrame)
        
        self.textScrollBar.config(command=self.originalBox.yview)

        self.originalBox.config(yscrollcommand=self.textScrollBar.set)
        self.originalBox.tag_configure("highlight", background="lightskyblue1")


        self.leftFrame.config(background="blue")
        self.textFrame.config(background="gainsboro")

        
        # packs all widgets in the left frame of the application
        self.leftFrame.pack(side=LEFT, fill=BOTH, expand=YES, padx=5, pady=5)
        self.textFrame.pack(side=TOP, fill=BOTH, expand=YES, padx=3, pady=(3,0))
        self.originalBox.pack(side=LEFT, fill=BOTH, expand=YES, padx=2, pady=2)
        self.textScrollBar.pack(side=LEFT, fill=Y)
        self.uploadFrame.pack(side=TOP, fill=BOTH, padx=3, pady=3)
        self.uploadButton.pack(side=TOP, padx=2, pady=2)
        
############# RIGHT FRAME ##########        
        
        self.rightFrame = Frame(self.master)
        self.text1Frame = Frame(self.rightFrame, borderwidth=2, relief="solid")
        self.buttonsFrame = Frame(self.rightFrame, borderwidth = 2)
        
        #option menu for choosing language to translate to
        self.var = StringVar()
        self.var.set('Language')
        
        self.destLang = ''

        self.languageList = ["Chinese", "English", "French", "German", 
        "Italian", "Japanese", "Korean", "Spanish"]
        
        self.optionmenu = OptionMenu(self.text1Frame, self.var, 
        *self.languageList, command = self.setLanguage)  
        
        self.nb = ttk.Notebook(self.text1Frame)
        self.direct = ttk.Frame(self.nb)
        self.detail = ttk.Frame(self.nb)
        self.highlight = ttk.Frame(self.nb)
        
        self.optionmenu.pack()
        
        self.translatedBox = Text(self.direct, borderwidth=2)
        self.translatedBox.pack(side=LEFT, fill=BOTH, expand=YES, padx=2, pady=2)
        self.translatedBox2 = Text(self.detail, borderwidth=2)
        self.translatedBox2.pack(side=LEFT, fill=BOTH, expand=YES, padx=2, pady=2)
        self.translatedBox3 = Text(self.highlight, borderwidth=2)
        self.translatedBox3.pack(side=LEFT, fill=BOTH, expand=YES, padx=2, pady=2)
        
        self.nb.add(self.direct, text = 'Direct')
        self.nb.add(self.detail, text = 'Detail')
        self.nb.add(self.highlight, text = 'Highlight')
        self.nb.pack()
        
        self.translateButton = Button(self.buttonsFrame, width=35, height=1, 
                                  text="Translate", command=self.onTranslate)
        self.getHighlightButton = Button(self.buttonsFrame, width=35, height=1, 
                                   text="Add Highlights", command=self.getHighlight)
        self.getDetailButton = Button(self.buttonsFrame, width=35, height=1, 
                                   text="Add Details", command=self.getDetail)  
        self.beginGameButton = Button(self.buttonsFrame, width=35, height=1, 
                                   text="Begin Game", command=self.beginGame)  
        self.text1ScrollBar = Scrollbar(self.text1Frame)
        
        self.text1ScrollBar.config(command=self.translatedBox.yview)
        self.translatedBox.config(yscrollcommand=self.text1ScrollBar.set)
        
        self.rightFrame.config(background="blue")
        self.text1Frame.config(background="gainsboro")
        
        self.rightFrame.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0,5), 
                                                                pady=2)
        
        self.text1Frame.pack(side=TOP, fill=BOTH, expand=YES, padx=3, pady=(3,0))

        self.buttonsFrame.pack(side=TOP, fill=BOTH, padx=3, pady=3)
        self.translateButton.pack(side=TOP, padx=2, pady=2)
        self.getDetailButton.pack(side=TOP, padx=2, pady=2)
        self.getHighlightButton.pack(side=TOP, padx=2, pady=2)
        self.beginGameButton.pack(side=TOP, padx=2, pady=2)

#Retrieves language code for translation library depending on which language option
# user chooses.        
    def setLanguage(self, value):
        if value == 'Chinese':
            self.destLang = 'zh-CN'
        elif value == 'English':
            self.destLang = 'en'
        elif value == 'French':
            self.destLang = 'fr'
        elif value == 'German':
            self.destLang = 'de'
        elif value == 'Italian':
            self.destLang = 'it'
        elif value == 'Japanese':
            self.destLang = 'ja'
        elif value == 'Korean':
            self.destLang = 'ko'
        elif value == 'Spanish':
            self.destLang = 'es'
        self.clearBox()
        self.insertTranslate()
        
    def run(self):
        self.master.mainloop()
    
    #Clears text box on the right where translations will be.    
    def clearBox(self):
        self.translatedBox.delete(1.0, END)
        self.translatedBox2.delete(1.0, END)
        self.translatedBox3.delete(1.0, END)
    
    #Inserts translations inside text box on right.    
    def insertTranslate(self):
        #Direct translation
        self.translated = Translator().translate(self.readText, \
        dest = self.destLang).text
        self.translatedBox.insert(END, self.translated)
        #Detail translation
        self.detectLang = Translator().detect(self.readText).lang
        if self.detectLang in ['en', 'es', 'fr', 'it', 'de']:
            words = self.readText.split()
            for word in words[0:10]:
                if word in string.punctuation or word in self.unacceptedStrings \
                or word in string.digits:
                    continue
                wordTranslate = Translator().translate(word, \
                dest = self.destLang).text
                self.translatedBox2.insert(END, '%s : %s\n'%(word, wordTranslate))
                self.detailWords[word] = wordTranslate
        elif self.detectLang in ['zh-CN', 'ko', 'ja']:
            for word in self.readText[0:10]:
                if word in string.punctuation or word in self.unacceptedStrings \
                or word in string.digits:
                    continue
                wordTranslate = Translator().translate(word, dest = self.destLang).text
                self.translatedBox2.insert(END, '%s : %s\n'%(word, wordTranslate))
                self.detailWords[word] = wordTranslate
    
    #Uploading of image file into program.    
    def onUpload(self):
        img = filedialog.askopenfilename(initialdir = "/Desktop",title = "Select file", 
            filetypes = (('png files', '*.png'), ('jpeg files', '*.jpg'),
            ("all files","*.")))
        self.readText = pytesseract.image_to_string(img, 
            lang = 'chi_tra+chi_sim+kor+eng+jpn')
        self.originalBox.delete(1.0, END)
        self.originalBox.insert(END, self.readText)
        self.clearBox()
        self.insertTranslate()
    
    #Handles highlighted translations.
    def onTranslate(self):
        selectedText = self.originalBox.get(SEL_FIRST, SEL_LAST)
        selectedTranslation = Translator().translate(selectedText, \
        dest = 'en').text
        self.translatedBox3.insert(END, "%s : %s\n" % (selectedText, \
        selectedTranslation))
        self.highlightWords[selectedText] = selectedTranslation
    
    #Adds detail words into game.
    def getDetail(self):
        self.pairs.update(self.detailWords)
        
    #Adds highlighted words into game.
    def getHighlight(self):
        self.pairs.update(self.highlightWords)
        print(self.pairs)
    
    #Handles quiz game when user presses 'Begin Game'.
    def beginGame(self):
        if len(self.pairs) < 5:
            self.popupBox()
        else:
            self.master.destroy()
            tp.run(600, 400, self.pairs)
    
    #Pop up box for when there are not enough translations to begin game.        
    def popupBox(self):
        win = tk.Toplevel()
        popup = tk.Label(win, text="You need at least 5 translations to begin game.")
        popup.grid(row=50, column=50)
        
root = Tk()
application = SmartTranslate(root)
application.run()