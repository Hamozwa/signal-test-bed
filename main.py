#main.py
#Provides a user interface to send and receive signals

import test_signal_generator as sig_gen
import message_parser as sig_par
import message_info as msg_template

import tkinter as tk

#Takes user input for custom AIS message
def send_AIS():
    msg_info = msg_template.AIS_message_info
    func_picker.destroy()

    #Create variable input window
    func_window = tk.Tk()
    func_window.title("Send AIS Signal")
    func_window.geometry('600x600')



    func_window.mainloop()
    
def main_window():
    global func_picker

    #Create function picking window
    func_picker = tk.Tk() 
    func_picker.title("Signal Test Bed") 
    func_picker.geometry('500x500') 

    #Create introductory text saying to pick an option
    intro_text = tk.Label(func_picker, pady=30, text="Please pick an option:")
    intro_text.config(font=("Calibri", 14))
    intro_text.pack()

    tk.Button(func_picker, height=2, width=30, text ="Send AIS signal", command=send_AIS).pack()
    tk.Button(func_picker,height=2, width=30, text="Receive AIS signal").pack()

    func_picker.mainloop() 

main_window()