import sys
from tkinter import *
from make_qc_shapefiles.interpretation_extraction import ExtractInterpretationToPoints, CompleteQCAttributes

 
class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)               
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("Extract to points")
        self.pack(fill=BOTH, expand=1)
        orthoInput = Entry(self)
        orthoInput.place(x=10, y=80)
        submitButton = Button(self, text="Extract", command= lambda: self.extract_to_points(orthoInput.get()))
        quitButton = Button(self, text="Quit", command=self.client_exit)
        submitButton.place(x=10, y=40)    
        quitButton.place(x=60, y=40)


    def client_exit(self):
        exit()

    def extract_to_points(self, message):
        #print(othoInput.get())
        self.show_text(message)
        ExtractInterpretationToPoints(message)

    def show_text(self, message):
        for key, _ in self.children.items():
            if key.startswith('!label'):
                self.children[key].destroy()
                break
        text = Label(self, text=message)
        text.pack()
        
        



root = Tk()
root.geometry("400x200")
app = Window(root)
root.mainloop()