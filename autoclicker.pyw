import tkinter as tk
import random
import pyautogui
import time
import threading
import pyHook
import subprocess
import os, os.path
import shutil

LargeFont = ('Futura', 12)

class AutoClicker(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title('AutoClicker')
        self.geometry('350x250+200+200')

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(2, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(2, weight=1)

        # template for new recorded clicking script instructions
        global instructionslist, instructions
        instructionslist = ["""import pyautogui, random, time

pyautogui.PAUSE = 0.15
pyautogui.FAILSAFE = True

while True:
"""]
        instructions = ''

        self.instructionnum = tk.StringVar()
        self.instructionnum.set(str(len(instructionslist)))

        self.frames = {}
        allPages = (MainMenu, ClickerPage, RegIntClicker1, RegIntClicker2, RandIntClicker1,
                    RandIntClicker2, RecordPage, NewPoint, PointArea, pointClickInstruction,
                    leftRightClick, waitPage, redoPage, keyboardPage, areaClickInstruction,
                    repeatPage, loopPage,saveComplete, loadPage, runLoad)

        # create frames for all the pages
        for F in allPages:
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=1, column=1, sticky='nsew')

        self.show_frame(MainMenu)

    # brings a frame to the top for visibility
    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()


class MainMenu(tk.Frame):

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master
        label = tk.Label(self, text='Main Menu', font=LargeFont)
        label.grid(row=0, columnspan=3, pady=10)
        button1 = tk.Button(self, text='Record',
                            command=lambda: controller.show_frame(RecordPage))
        button1.grid(row=1, column=0, padx=10, pady=10)
        button2 = tk.Button(self, text='Load',
                            command=lambda: self.load(controller))
        button2.grid(row=1, column=1, pady=5)
        button3 = tk.Button(self, text='Clicker',
                            command=lambda: controller.show_frame(ClickerPage))
        button3.grid(row=2, column=0, pady=10)
        button4 = tk.Button(self, text='Help')
        button4.grid(row=2, column=1, padx=5)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

    # lists recorded scripts from a directory called AutoClicker Scripts
    def load(self, controller):
        directory = os.path.dirname(os.path.abspath(__file__)) + '\\AutoClicker Scripts'
        box = controller.frames[loadPage].box3
        box.delete(0, 'end')
        for Folders, subFolders, Files in os.walk(directory):
            for script in Files:
                if script.endswith('.py'):
                    stripped = script.strip('.py')
                    box.insert('end', stripped)
                    
        controller.show_frame(loadPage)


class ClickerPage(tk.Frame):

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master
        label = tk.Label(self, text='Clicker', font=LargeFont)
        label.grid(row=0, columnspan=3, pady=10)
        button1 = tk.Button(self, text='Regular\nInterval',
                            command=lambda: controller.show_frame(RegIntClicker1))
        button1.grid(row=1, column=0, padx=10, pady=5)
        button2 = tk.Button(self, text='Random\nInterval',
                            command=lambda: controller.show_frame(RandIntClicker1))
        button2.grid(row=1, column=1, pady=5)
        button4 = tk.Button(self, text='Main Menu',
                            command=lambda: controller.show_frame(MainMenu))
        button4.grid(row=2, column=1, padx=5, pady=10)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        

class RegIntClicker1(tk.Frame):

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master
        label = tk.Label(self, text='Regular Interval', font=LargeFont)
        label.grid(row=0, column=1, columnspan=2, pady=10)
        label1 = tk.Label(self, text='Interval:')
        label1.grid(row=1, column=1, padx=10, pady=5)
        global regWait
        regWait = tk.StringVar()
        entry2 = tk.Entry(self, textvariable=regWait)
        entry2.grid(row=1, column=2, pady=10)
        label2 = tk.Label(self, text='Use only 1 decimal point and must be > 0.1 seconds.')
        label2.grid(row=2, column=1, columnspan=3)
        button3 = tk.Button(self, text='Start',
                            command=lambda: self.startRegClicker(controller, RegIntClicker2))
        button3.grid(row=3, column=1, pady=10)
        label5 = tk.Label(self, text='seconds')
        label5.grid(row=1, column=3, padx=10)
        button4 = tk.Button(self, text='Back',
                            command=lambda: controller.show_frame(ClickerPage))
        button4.grid(row=3, column=2, padx=10, sticky='E')

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(5, weight=1)

    def popup(self):
        self.pop = tk.Toplevel(bg='yellow')
        self.pop.title('Regular Interval Clicker')
        self.pop.overrideredirect(1)
        label = tk.Label(self.pop, text='Script Working', font=LargeFont)
        label.pack()
        label2 = tk.Label(self.pop, text='Press Esc to stop.', font=LargeFont)
        label2.pack()
        x = root.winfo_x()
        y = root.winfo_y()
        self.pop.geometry('200x100+'+str(x+75)+'+'+str(y+100))
        self.pop.attributes('-topmost', True)
        self.pop.update()

    def regIntClicker(self):
        seconds = int(float(self.s) * 10)
        while self.flag:
            for wait in range(seconds):
                time.sleep(0.1)
            pyautogui.click()

    # Keyboard hook to start and stop clicking
    def OnKeyboardEvent(self, event):
        if (event.Key == 'Escape'):
            self.flag = False
            self.pop.destroy()
        elif (event.Key == 'Oem_Plus'):
            if not hasattr(self, 'flag'):
                self.flag = True
                self.popup()
                self.s = regWait.get()
                threadObj = threading.Thread(target=self.regIntClicker)
                threadObj.start()
            elif hasattr(self, 'flag'):
                if self.flag == False:
                    self.flag = True
                    self.popup()
                    self.s = regWait.get()
                    threadObj = threading.Thread(target=self.regIntClicker)
                    threadObj.start()
        return True

    def startRegClicker(self, controller, page):
        controller.show_frame(RegIntClicker2)
        self.focus() # sets focus to window so you don't get stuck in entry box from previous frame
        controller.hm = pyHook.HookManager()
        controller.hm.KeyDown = self.OnKeyboardEvent
        controller.hm.HookKeyboard()


class RegIntClicker2(tk.Frame):

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master
        label = tk.Label(self, text='Regular Interval', font=LargeFont)
        label.grid(row=0, column=1, columnspan=3, pady=10)
        label1 = tk.Label(self, text='Interval:')
        label1.grid(row=1, column=1, padx=10, pady=5)
        label2 = tk.Label(self, textvariable=regWait)
        label2.grid(row=1, column=2, pady=10)
        button3 = tk.Button(self, text='Back',
                            command=lambda: self.stopRegClicker(controller))
        button3.grid(row=2, column=3, pady=10)
        label4 = tk.Label(self, text='Press = to start.\nPress ESC to stop.')
        label4.grid(row=2, column=1, padx=10)
        label5 = tk.Label(self, text='seconds')
        label5.grid(row=1, column=3, padx=10)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(5, weight=1)
 
    def stopRegClicker(self, controller):
        controller.show_frame(RegIntClicker1)
        controller.hm.__del__()
             

class RandIntClicker1(tk.Frame):

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master
        label = tk.Label(self, text='Random Interval', font=LargeFont)
        label.grid(row=0, column=1, columnspan=4, pady=10)

        label1 = tk.Label(self, text='Interval:')
        label1.grid(row=1, column=1, padx=10, pady=5)
        global randWait1
        randWait1 = tk.StringVar()
        entry2 = tk.Entry(self, width=6, textvariable=randWait1)
        entry2.grid(row=1, column=2, pady=10)
        label6 = tk.Label(self, text='-')
        label6.grid(row=1, column=3, padx=5)
        global randWait2
        randWait2 = tk.StringVar()
        entry7 = tk.Entry(self, width=6, textvariable=randWait2)
        entry7.grid(row=1, column=4)
        button3 = tk.Button(self, text='Start',
                            command=lambda: self.startRandClicker(controller))
        button3.grid(row=3, column=1, pady=10)
        label8 = tk.Label(self, text='Use only 1 decimal point. Must be > 0.1 seconds.')
        label8.grid(row=2, column=1, columnspan=5)
        
        label5 = tk.Label(self, text='seconds')
        label5.grid(row=1, column=5, padx=10)
        button4 = tk.Button(self, text='Back',
                            command=lambda: controller.show_frame(ClickerPage))
        button4.grid(row=3, column=4, padx=10)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(5, weight=1)

    def popup(self):
        self.pop = tk.Toplevel(bg='yellow')
        self.pop.title('Random Interval Clicker')
        self.pop.overrideredirect(1)
        label = tk.Label(self.pop, text='Script Working', font=LargeFont)
        label.pack()
        label2 = tk.Label(self.pop, text='Press Esc to stop.', font=LargeFont)
        label2.pack()
        x = root.winfo_x()
        y = root.winfo_y()
        self.pop.geometry('200x100+'+str(x+75)+'+'+str(y+100))
        self.pop.attributes('-topmost', True)
        self.pop.update()

    def randIntClicker(self):
        while self.flag:
            seconds = random.randint(int(float(self.a) * 100), int(float(self.b) * 100))
            for wait in range(seconds):
                time.sleep(0.01)
            pyautogui.click()

    def OnKeyboardEvent(self, event):
        if (event.Key == 'Escape'):
            self.flag = False
            self.pop.destroy()
        elif (event.Key == 'Oem_Plus'):
            if not hasattr(self, 'flag'):
                self.flag = True
                self.popup()
                self.s = regWait.get()
                threadObj = threading.Thread(target=self.randIntClicker)
                threadObj.start()
            elif hasattr(self, 'flag'):
                if self.flag == False:
                    self.flag = True
                    self.popup()
                    self.s = regWait.get()
                    threadObj = threading.Thread(target=self.randIntClicker)
                    threadObj.start()
        return True
    def intervalChecker(self):
        self.a = randWait1.get()
        self.b = randWait2.get()
        return float(self.a) < float(self.b)

    def errorPopUp(self):
        self.errpop = tk.Toplevel()
        self.errpop.title('Error')
        label = tk.Label(self.errpop, text='First number must be \nbigger than second number.')
        label.pack()
        x = root.winfo_x()
        y = root.winfo_y()
        self.errpop.attributes('-topmost', True)
        self.errpop.geometry('250x100+' + str(x + 50) + '+' + str(y + 80))
        self.errpop.update()

    def startRandClicker(self, controller):
        if self.intervalChecker():
            controller.show_frame(RandIntClicker2)
            self.focus()
            controller.hm = pyHook.HookManager()
            controller.hm.KeyDown = self.OnKeyboardEvent
            controller.hm.HookKeyboard()
        else:
            self.errorPopUp()


class RandIntClicker2(tk.Frame):

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master
        label = tk.Label(self, text='Random Interval', font=LargeFont)
        label.grid(row=0, columnspan=4, pady=10)
        label1 = tk.Label(self, text='Interval:')
        label1.grid(row=1, column=0, padx=10, pady=5)
        label2 = tk.Label(self, width=6, textvariable=randWait1)
        label2.grid(row=1, column=1, pady=10)
        label6 = tk.Label(self, text='-')
        label6.grid(row=1, column=2, padx=5)
        label7 = tk.Label(self, width=6, textvariable=randWait2)
        label7.grid(row=1, column=3)
        button3 = tk.Button(self, text='Back',
                            command=lambda: self.stopRandClicker(controller))
        button3.grid(row=2, column=3, pady=10)
        label4 = tk.Label(self, text='Press = to start.\nPress ESC to stop.')
        label4.grid(row=2, column=0, padx=10)
        label5 = tk.Label(self, text='seconds')
        label5.grid(row=1, column=4, padx=10)

    def stopRandClicker(self, controller):
        controller.show_frame(RandIntClicker1)
        controller.hm.__del__()


class RecordPage(tk.Frame):

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master
        label = tk.Label(self, text='Record', font=LargeFont)
        label.grid(row=0, columnspan=3, pady=10)
        button1 = tk.Button(self, text='Start New',
                            command=lambda: self.showPointNum(controller))
        button1.grid(row=1, column=0, padx=10, pady=10)
        button2 = tk.Button(self, text='Main Menu',
                            command=lambda: controller.show_frame(MainMenu))
        button2.grid(row=1, column=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def showPointNum(self, controller):
        controller.instructionnum.set(str(len(instructionslist)))
        controller.show_frame(NewPoint)
        

class NewPoint(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master
        label = tk.Label(self, text='Point #', font=LargeFont)
        label.grid(row=0, column=0, pady=10)
        label2 = tk.Label(self, textvariable=controller.instructionnum,
                          font=LargeFont)
        label2.grid(row=0, column=1)
        button1 = tk.Button(self, text='Set Point',
                            command=lambda: self.goToPointArea(controller))
        button1.grid(row=1, column=0, padx=10, pady=10)
        button2 = tk.Button(self, text='Redo Last Point',
                            command=lambda: self.redo(controller))
        button2.grid(row=1, column=1)
        button3 = tk.Button(self, text='Loop Back To\nStarting Point',
                            command=lambda: self.loop(controller))
        button3.grid(row=2, column=0)
        button4 = tk.Button(self, text='Cancel',
                            command=lambda: self.cancel(controller))
        button4.grid(row=2, column=1, pady=10)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        global point_coord, area_coordTopLeft, area_coordBotRight
        point_coord = tk.StringVar()
        area_coordTopLeft = tk.StringVar()
        area_coordBotRight = tk.StringVar()
        

    def goToPointArea(self, controller):
        point_coord.set('(???, ???)')
        controller.show_frame(PointArea)

    def redo(self, controller):
        global instructionslist
        if len(instructionslist)> 1:
            del instructionslist[-1]
            controller.show_frame(redoPage)
        else:
            self.errpop = tk.Toplevel()
            self.errpop.title('Error')
            label = tk.Label(self.errpop, text='No points have been created!')
            label.pack()
            x = root.winfo_x()
            y = root.winfo_y()
            self.errpop.attributes('-topmost', True)
            self.errpop.geometry('250x100+' + str(x + 50) + '+' + str(y + 80))
            self.errpop.update()

    def loop(self, controller):
        global instructionslist
        if len(instructionslist)> 1:
            controller.show_frame(loopPage)
        else:
            self.errpop = tk.Toplevel()
            self.errpop.title('Error')
            label = tk.Label(self.errpop, text='No points have been created!')
            label.pack()
            x = root.winfo_x()
            y = root.winfo_y()
            self.errpop.attributes('-topmost', True)
            self.errpop.geometry('250x100+' + str(x + 50) + '+' + str(y + 80))
            self.errpop.update()

    # resets the instructions
    def cancel(self, controller):
        global instructionslist, instructions
        instructionslist = ["""import pyautogui, random, time

pyautogui.PAUSE = 0.15
pyautogui.FAILSAFE = True

while True:
"""]
        instructions = ''
        controller.instructionnum.set(str(len(instructionslist)))
        controller.show_frame(RecordPage)

class PointArea(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master
        label = tk.Label(self, text='Point #', font=LargeFont)
        label.grid(row=0, column=0, pady=10)
        label2 = tk.Label(self, textvariable=controller.instructionnum,
                          font=LargeFont)
        label2.grid(row=0, column=1)
        button1 = tk.Button(self, text='Point Click',
                            command=lambda: self.pointClick(controller))
        button1.grid(row=1, column=0, padx=10, pady=10)
        button2 = tk.Button(self, text='Area Click',
                            command=lambda: self.areaClick(controller))
        button2.grid(row=1, column=1)
        button3 = tk.Button(self, text='Keyboard Type',
                            command=lambda: controller.show_frame(keyboardPage))
        button3.grid(row=2, column=0)
        button4 = tk.Button(self, text='Back',
                            command=lambda: controller.show_frame(NewPoint))
        button4.grid(row=2, column=1, pady=20)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.x = ''
        self.y = ''

    def OnMouseEvent(self, event):
        if (event.Message == 514):
            if self.flag == True:
                global instructions, point_coord, pointFlag
                self.x, self.y = pyautogui.position()
                # adds a 2x2 pixel random deviation to make the clicking a little more random
                instructions += '\tpyautogui.moveTo(' + str(self.x) + '+random.randint(-2, 2)' + ', ' + str(self.y) + '+random.randint(-2, 2)'+ ', duration=(random.randint(40, 80))/100)\n'
                self.flag = False
                pointFlag = True
                point_coord.set('(' + str(self.x) + ', ' + str(self.y) + ')')
        return True

    def pointClick(self, controller):
        global instructionslist, point_coord
        self.flag = True

        point_coord.set('(???, ???)')

        controller.show_frame(pointClickInstruction)

            
        controller.hm1 = pyHook.HookManager()
        controller.hm1.MouseAll = self.OnMouseEvent
        controller.hm1.HookMouse()

    def OnMouseEvent2(self, event):
        global instructions, area_coordTopLeft, area_coordBotRight, pointFlag
        if (event.Message == 513):
            if self.flag == True:
                self.x2, self.y2 = pyautogui.position()
                area_coordTopLeft.set('(' + str(self.x2) + ', ' + str(self.y2) + ')')
        elif (event.Message == 514):
            if self.flag == True:
                self.x3, self.y3 = pyautogui.position()
                instructions += '\tpyautogui.moveTo(random.randint(' + str(self.x2) + ', ' + str(self.x3) + '), random.randint(' + str(self.y2) + ', ' + str(self.y3) + '), duration=(random.randint(40, 80))/100)\n'
                self.flag = False
                pointFlag = True
                area_coordBotRight.set('(' + str(self.x3) + ', ' + str(self.y3) + ')')
        return True

    def areaClick(self, controller):
        global instructionslist, area_coordTopLeft, area_coordBotRight
        self.flag = True

        area_coordTopLeft.set('(???, ???)')
        area_coordBotRight.set('(???, ???)')

        controller.show_frame(areaClickInstruction)

            
        controller.hm2 = pyHook.HookManager()
        controller.hm2.MouseAll = self.OnMouseEvent2
        controller.hm2.HookMouse()


class pointClickInstruction(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master
        label = tk.Label(self, text='Point #', font=LargeFont)
        label.grid(row=0, column=0, pady=10)
        label2 = tk.Label(self, textvariable=controller.instructionnum,
                          font=LargeFont)
        label2.grid(row=0, column=1)
        label3 = tk.Label(self, text='Point Coordinates: ')
        label3.grid(row=1, column=0, padx=10, pady=10)
        label4 = tk.Label(self, textvariable=point_coord)
        label4.grid(row=1, column=1)
        button4 = tk.Button(self, text='Continue',
                            command=lambda: self.setWaitTime(controller))
        button4.grid(row=3, column=0, pady=10)
        button5 = tk.Button(self, text='Back',
                            command=lambda: self.backPoint(controller))
        button5.grid(row=3, column=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def setWaitTime(self, controller):
        if pointFlag == True:
            controller.show_frame(leftRightClick)
            controller.hm1.__del__()
            

    def backPoint(self,controller):
        global instructions
        if pointFlag == True:
            instructions = ''
            controller.show_frame(PointArea)
            controller.hm1.__del__()
            
        
class leftRightClick(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master
        label = tk.Label(self, text='Point #', font=LargeFont)
        label.grid(row=0, column=0, pady=10)
        label2 = tk.Label(self, textvariable=controller.instructionnum,
                          font=LargeFont)
        label2.grid(row=0, column=1)
        button3 = tk.Button(self, text='Left Click',
                            command=lambda: self.leftClick(controller))
        button3.grid(row=1, column=0, padx=10, pady=10)
        button4 = tk.Button(self, text='Right Click',
                            command=lambda: self.rightClick(controller))
        button4.grid(row=1, column=1)
        button5 = tk.Button(self, text='Left Auto-Click',
                            command=lambda: self.leftAutoClick(controller))
        button5.grid(row=2, column=0, padx=10, pady=10)
        button6 = tk.Button(self, text='Right Auto-Click',
                            command=lambda: self.rightAutoClick(controller))
        button6.grid(row=2, column=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        global autoflag
        autoflag = False

    def leftClick(self, controller):
        global instructions
        instructions += '\tpyautogui.click()\n'
        controller.show_frame(waitPage)

    def rightClick(self, controller):
        global instructions
        instructions += '\tpyautogui.rightClick()\n'
        controller.show_frame(waitPage)

    def leftAutoClick(self, controller):
        global instructions, autoflag
        instructions += '\tpyautogui.click()\n'
        autoflag = True
        controller.show_frame(waitPage)

    def rightAutoClick(self, controller):
        global instructions, autoflag
        instructions += '\tpyautogui.rightClick()\n'
        autoflag = True
        controller.show_frame(waitPage)


class waitPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master
        label = tk.Label(self, text='Point #', font=LargeFont)
        label.grid(row=0, column=2, pady=10)
        label2 = tk.Label(self, textvariable=controller.instructionnum,
                          font=LargeFont)
        label2.grid(row=0, column=3)
        
        label5 = tk.Label(self, text='Enter time to wait:')
        label5.grid(row=1, columnspan=5, pady=10)
        
        
        self.waitTime1 = tk.StringVar()
        entry2 = tk.Entry(self, width=6, textvariable=self.waitTime1)
        entry2.grid(row=2, column=1, pady=10)
        label6 = tk.Label(self, text='-')
        label6.grid(row=2, column=2, padx=5)
        self.waitTime2 = tk.StringVar()
        entry7 = tk.Entry(self, width=6, textvariable=self.waitTime2)
        entry7.grid(row=2, column=3)
        label8 = tk.Label(self, text='seconds')
        label8.grid(row=2, column=4, padx=15)

        label10 = tk.Label(self, text='Use only 1 decimal point. Must be > 0.1 seconds.')
        label10.grid(row=3, column=1, columnspan=4)

        button9 = tk.Button(self, text='Continue',
                            command=lambda: self.setWait(controller))
        button9.grid(row=4, column=4, pady=20)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(5, weight=1)

    def setWait(self, controller):
        global instructions, instructionslist, autoflag

        self.w1 = self.waitTime1.get()
        self.w2 = self.waitTime2.get()
        seconds1 = int(float(self.w1) * 100)
        seconds2 = int(float(self.w2) * 100)

        if seconds1 < seconds2:
            
            if autoflag == True:
                instructions += '\tfor wait in range(random.randint(' + str(seconds1) + ', ' + str(seconds2) +')):\n\atime.sleep(0.01)\n'
                autoflag = False
                controller.show_frame(repeatPage)
            else:
                instructions += '\tfor wait in range(random.randint(' + str(seconds1) + ', ' + str(seconds2) +')):\n\t\ttime.sleep(0.01)\n'
                instructionslist += [instructions]
                instructions = ''
                controller.instructionnum.set(str(len(instructionslist)))
                controller.show_frame(NewPoint)

        else:
            self.errorPopUp()

    def errorPopUp(self):
        self.errpop = tk.Toplevel()
        self.errpop.title('Error')
        label = tk.Label(self.errpop, text='First number must be \nbigger than second number.')
        label.pack()
        x = root.winfo_x()
        y = root.winfo_y()
        self.errpop.attributes('-topmost', True)
        self.errpop.geometry('250x100+' + str(x + 50) + '+' + str(y + 80))
        self.errpop.update()

class redoPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master

        label1 = tk.Label(self, text='Last point has been successfully removed.')
        label1.grid(row=0, column=1, columnspan=2, pady=10)

        button2 = tk.Button(self, text='Continue',
                            command=lambda: self.removed(controller))
        button2.grid(row=1, column=2, padx=10, pady=25)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(5, weight=1)

    def removed(self, controller):
        controller.instructionnum.set(str(len(instructionslist)))
        controller.show_frame(NewPoint)

class keyboardPage(tk.Frame):

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master
        label = tk.Label(self, text='Keyboard Type', font=LargeFont)
        label.grid(row=0, column=1, pady=10, columnspan=2)
        label1 = tk.Label(self, text='Enter keyboard input:')
        label1.grid(row=1, column=1, columnspan=2)
        self.keyboard = tk.StringVar()
        entry2 = tk.Entry(self, textvariable=self.keyboard)
        entry2.grid(row=2, column=1, pady=10, columnspan=2)
        
        button3 = tk.Button(self, text='Continue',
                            command=lambda: self.keyboardInput(controller))
        button3.grid(row=3, column=1, pady=10, padx=20, sticky='W')
        button4 = tk.Button(self, text='Back',
                            command=lambda: controller.show_frame(NewPoint))
        button4.grid(row=3, column=2, padx=20)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(5, weight=1)

    def keyboardInput(self, controller):
        global instructions
        tempKeyboard = self.keyboard.get()
        instructions += "\tpyautogui.typewrite('" + tempKeyboard + "', interval=(random.randint(10, 30))/100)\n"
        controller.show_frame(waitPage)


class areaClickInstruction(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master
        label = tk.Label(self, text='Point #', font=LargeFont)
        label.grid(row=0, column=0, pady=10)
        label2 = tk.Label(self, textvariable=controller.instructionnum,
                          font=LargeFont)
        label2.grid(row=0, column=1)
        label3 = tk.Label(self, text='Top Left Point Coordinates: ')
        label3.grid(row=1, column=0, padx=10, pady=10)
        label4 = tk.Label(self, textvariable=area_coordTopLeft)
        label4.grid(row=1, column=1)
        label5 = tk.Label(self, text='Bottom Right Point Coordinates: ')
        label5.grid(row=2, column=0, padx=10, pady=10)
        label6 = tk.Label(self, textvariable=area_coordBotRight)
        label6.grid(row=2, column=1)
        button4 = tk.Button(self, text='Continue',
                            command=lambda: self.setWaitTime(controller))
        button4.grid(row=3, column=0, pady=10)
        button5 = tk.Button(self, text='Back',
                            command=lambda: self.backPoint(controller))
        button5.grid(row=3, column=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def setWaitTime(self, controller):
        if pointFlag == True:
            controller.show_frame(leftRightClick)
            controller.hm2.__del__()
            

    def backPoint(self,controller):
        global instructions
        if pointFlag == True:
            instructions = ''
            controller.show_frame(PointArea)
            controller.hm2.__del__()

class repeatPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master
        label = tk.Label(self, text='Point #', font=LargeFont)
        label.grid(row=0, column=1, pady=10)
        label2 = tk.Label(self, textvariable=controller.instructionnum,
                          font=LargeFont)
        label2.grid(row=0, column=2)
        
        label5 = tk.Label(self, text='Enter number of times to click:')
        label5.grid(row=1, column=1, columnspan=2, pady=10)
        
        self.repeats = tk.StringVar()
        entry2 = tk.Entry(self, width=20, textvariable=self.repeats)
        entry2.grid(row=2, column=1, columnspan=2, pady=10)

        button9 = tk.Button(self, text='Continue',
                            command=lambda: self.setRepeats(controller))
        button9.grid(row=4, column=2, pady=20)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(5, weight=1)

    def setRepeats(self, controller):
        global instructions, instructionslist
        tempRepeats = self.repeats.get()
        a = instructions.split('\t')
        b = '\t\t'.join(a)
        c = b.split('\a')
        d = '\t\t\t'.join(c)
        instructions = '\tfor i in range(' + str(int(tempRepeats)) + '):\n' + d
        instructionslist += [instructions]
        instructions = ''
        controller.instructionnum.set(str(len(instructionslist)))
        controller.show_frame(NewPoint)


class loopPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master
        label = tk.Label(self, text='Save', font=LargeFont)
        label.grid(row=0, column=1, columnspan=2, pady=10)
        
        label5 = tk.Label(self, text='Name the script:')
        label5.grid(row=1, column=1, columnspan=2, pady=5)

        global loopName
        loopName = tk.StringVar()
        entry2 = tk.Entry(self, width=20, textvariable=loopName)
        entry2.grid(row=2, column=1, columnspan=2, pady=10)

        button3 = tk.Button(self, text='Save',
                            command=lambda: self.saveLoop(controller))
        button3.grid(row=4, column=1, pady=20, padx=20)

        button4 = tk.Button(self, text='Back',
                            command=lambda: controller.show_frame(NewPoint))
        button4.grid(row=4, column=2, pady=20, padx=20)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(5, weight=1)

    def saveLoop(self, controller):
        global loopName, instructionslist
        tempName = loopName.get()

        # makes a new directory to store scripts if not created.
        directory = os.path.dirname(os.path.abspath(__file__)) + '\\AutoClicker Scripts'
        if not os.path.exists(directory):
            os.makedirs(directory)
        fileName = tempName + '.py'
        file = os.path.join(directory, fileName)
        fileWrite = open(file, 'w')
        # write all the instructions in the list to the new program
        for i in instructionslist:
            fileWrite.write(i)
        fileWrite.close()
        instructionslist = ["""import pyautogui, random, time

pyautogui.PAUSE = 0.15
pyautogui.FAILSAFE = True

while True:
"""]
        controller.show_frame(saveComplete)
        
        
class saveComplete(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master

        label1 = tk.Label(self, text='Loop has been successfully saved.')
        label1.grid(row=0, column=1, columnspan=2, pady=10)

        button2 = tk.Button(self, text='Continue',
                            command=lambda: self.saved(controller))
        button2.grid(row=1, column=2, padx=10, pady=25)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(5, weight=1)

    def saved(self, controller):
        controller.instructionnum.set(str(len(instructionslist)))
        controller.show_frame(MainMenu)


class loadPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master
        label = tk.Label(self, text='Load', font=LargeFont)
        label.grid(row=0, column=1, columnspan=3, pady=5)
        
        label2 = tk.Label(self, text='Select script to run:')
        label2.grid(row=1, column=1, columnspan=3, pady=5)

        
        self.box3 = tk.Listbox(self, height=5, width=40)
        self.box3.grid(row=2, column=1, columnspan=3)
        scroll4 = tk.Scrollbar(self, orient='vertical')
        scroll4.grid(row=2, column=4)
        self.box3.config(yscrollcommand=scroll4.set)
        scroll4.config(command=self.box3.yview)

        button3 = tk.Button(self, text='Load',
                            command=lambda: self.load(controller))
        button3.grid(row=4, column=1, pady=20, padx=20)

        button5 = tk.Button(self, text='Delete',
                            command=lambda: self.delete())
        button5.grid(row=4, column=2, pady=20, padx=10)
                

        button4 = tk.Button(self, text='Back',
                            command=lambda: controller.show_frame(MainMenu))
        button4.grid(row=4, column=3, pady=20, padx=20)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(5, weight=1)

        self.flag = False

    

    def load(self, controller):
        if self.box3.curselection() == ():
            self.errorPopUp()

        else:
            controller.hm3 = pyHook.HookManager()
            controller.hm3.KeyDown = self.OnKeyboardEvent
            controller.hm3.HookKeyboard()
            scriptName = self.box3.get(self.box3.curselection())
            setName = controller.frames[runLoad].showScript.set(scriptName)
            controller.show_frame(runLoad)

    def delete(self):
        if self.box3.curselection() == ():
            self.errorPopUp()
        else:
            self.delPopUp()

    def delPopUp(self):
        self.delpop = tk.Toplevel()
        self.delpop.title('Confirm Selection')
        label = tk.Label(self.delpop, text='Are you sure you want to delete this script?')
        label.grid(row=0, column=1, pady=5, columnspan=2)

        scriptName = self.box3.get(self.box3.curselection())
        showScript = tk.StringVar()
        showScript.set(scriptName)
        label2 = tk.Label(self.delpop, textvariable=showScript, font=LargeFont)
        label2.grid(row=1, column=1, columnspan=2, pady=10)

        button3 = tk.Button(self.delpop, text='Confirm',
                            command=lambda: self.deleteScript())
        button3.grid(row=2, column=1, pady=10)

        button4 = tk.Button(self.delpop, text='  Back  ',
                            command=lambda: self.delpop.destroy())
        button4.grid(row=2, column=2, pady=10)

        self.delpop.grid_columnconfigure(0, weight=1)
        self.delpop.grid_columnconfigure(5, weight=1)

        x = root.winfo_x()
        y = root.winfo_y()
        self.delpop.attributes('-topmost', True)
        self.delpop.geometry('350x150+' + str(x) + '+' + str(y + 60))
        self.delpop.update()

    def errorPopUp(self):
        self.errpop = tk.Toplevel()
        self.errpop.title('Error')
        label = tk.Label(self.errpop, text='Please select a script!')
        label.grid(column=1, pady=35)
        self.errpop.grid_columnconfigure(0, weight=1)
        self.errpop.grid_columnconfigure(5, weight=1)
        x = root.winfo_x()
        y = root.winfo_y()
        self.errpop.attributes('-topmost', True)
        self.errpop.geometry('250x100+' + str(x + 50) + '+' + str(y + 80))
        self.errpop.update()

    def deleteScript(self):
        directory = os.path.dirname(os.path.abspath(__file__)) + '\\AutoClicker Scripts'
        fileName = self.box3.get(self.box3.curselection()) + '.py'
        file = os.path.join(directory, fileName)
        os.unlink(file)
        self.box3.delete(0, 'end')
        for Folders, subFolders, Files in os.walk(directory):
            for script in Files:
                if script.endswith('.py'):
                    stripped = script.strip('.py')
                    self.box3.insert('end', stripped)
        self.delpop.destroy()

    def popup(self):
        self.pop = tk.Toplevel(bg='yellow')
        self.pop.title('Regular Interval Clicker')
        self.pop.overrideredirect(1)
        label = tk.Label(self.pop, text='Script Working', font=LargeFont)
        label.pack()
        label2 = tk.Label(self.pop, text='Press ESC or keep mouse\nat upper left corner of \nscreen to stop.', font=LargeFont)
        label2.pack()
        x = root.winfo_x()
        y = root.winfo_y()
        self.pop.attributes('-topmost', True)
        self.pop.geometry('240x100+'+str(x+55)+'+'+str(y+125))
        self.pop.update()

    def OnKeyboardEvent(self, event):
        directory = os.path.dirname(os.path.abspath(__file__)) + '\\AutoClicker Scripts'
        fileName = self.box3.get(self.box3.curselection()) + '.py'
        file = os.path.join(directory, fileName)
        if (event.Key == 'Escape'):
            if self.flag == True:
                self.flag = False
                self.openscript.kill()
                self.pop.destroy()
        elif (event.Key == 'Oem_Plus'):
            if self.flag == False:
                self.flag = True
                self.popup()
                self.runScript()
        return True

    def runScript(self):
        directory = os.path.dirname(os.path.abspath(__file__)) + '\\AutoClicker Scripts'
        fileName = self.box3.get(self.box3.curselection()) + '.py'
        file = os.path.join(directory, fileName)
        self.openscript = subprocess.Popen(['pythonw.exe', file])   


class runLoad(tk.Frame):

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master
        label = tk.Label(self, text='Load Script', font=LargeFont)
        label.grid(row=0, column=1, columnspan=3, pady=10)

        self.showScript = tk.StringVar()
        label2 = tk.Label(self, textvariable=self.showScript, font=LargeFont)
        label2.grid(row=1, column=1, columnspan=3, pady=10)
        
        button3 = tk.Button(self, text='Back',
                            command=lambda: self.backLoad(controller))
        button3.place(x=190, y=115)
        label4 = tk.Label(self, text='Press = to start.\nPress ESC or keep mouse\nat upper left corner of \nscreen to stop.')
        label4.place(x=35, y=95)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(5, weight=1)

    def backLoad(self, controller):
        controller.show_frame(loadPage)
        controller.hm3.__del__()
   

        
root = AutoClicker()
root.attributes('-topmost', True)
root.mainloop()

        
        
        
    
