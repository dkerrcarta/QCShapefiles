import sys
from tkinter import *
from make_qc_shapefiles.interpretation_extraction import ExtractInterpretationToPoints, CompleteQCAttributes

 
class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)               
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("Complete QC attributes")
        self.pack(fill=BOTH, expand=1)
        orthoInput = Entry(self)
        orthoInput.place(x=10, y=80)
        orthoInput.insert(0, 'OrthoID')
        nameInput = Entry(self)
        nameInput.place(x=10, y=120)
        nameInput.insert(0, 'Name')
        submitButton = Button(self, text="Complete attributes", command= lambda: self.fill_attributes(orthoInput.get(), nameInput.get()))
        quitButton = Button(self, text="Quit", command=self.client_exit)
        submitButton.place(x=10, y=40)    
        quitButton.place(x=140, y=40)


    def client_exit(self):
        exit()

    def fill_attributes(self, message, name):
        #print(othoInput.get())
        self.show_text(message)
        CompleteQCAttributes(message, name)

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