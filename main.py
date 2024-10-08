#main.py
#Provides a user interface to send and receive signals

import test_signal_generator as sig_gen
import message_parser as sig_par
import message_info as msg_template

import tkinter as tk

import AIS.AIS_Tx
import AIS.AIS_Rx

#Create input field with label (and default value?)
def input_field(parent, field_name, field_row, field_column, default_value):
    # Create label
    label = tk.Label(parent, text=field_name)
    label.grid(row=field_row, column=field_column*2, sticky="e")

    # Create entry widget for input
    field = tk.Entry(parent)
    field.grid(row=field_row, column=field_column*2+1, padx=5)
    field.insert(0, str(default_value))

    return field
    

#Takes user input for custom AIS message
def send_AIS():
    msg_info = msg_template.AIS_message_info
    func_picker.destroy()

    #Create variable input window
    func_window = tk.Tk()
    func_window.title("Send AIS Signal")
    func_window.geometry('820x600')
    func_window.grid()
    
    #Add Input fields for each variable
    field_row = 0
    field_column = 0
    fields = []
    max_inputs = len(msg_info)
    for key,value in msg_info.items():
        fields.append(input_field(func_window, key,field_row,field_column,value))   #Create input field per value in dictionary
        field_row += 1
        if field_row > max_inputs//4:   #Split fields into 4 columns
            field_row = 0
            field_column += 1
    
    #Submit Button
    def get_inputs():
        row = 0
        for key in msg_info.keys():
            inputted_value = fields[row].get()

            if inputted_value.startswith("b'"): #encode byte information when applicable
                msg_info[key] = inputted_value.lstrip("b'").rstrip("'").encode()

            else:
                try:    #keep integer values as integers
                    msg_info[key] = int(inputted_value)
                except:
                    msg_info[key] = inputted_value

            row += 1
        
        #Generate test signal
        with open('output_data.bin','wb') as bin_file:
            bin_file.write(sig_gen.gen_AIS(msg_info))
        
        AIS.AIS_Tx.main() #Comment this line to only create the message file 'output.bin'

    submit_button = tk.Button(func_window, height=2, width=30, text="Submit", command=get_inputs)
    submit_button.grid(row=max_inputs, columnspan=8)

    #Return Button
    def quit_window():
        func_window.destroy()
        main_window()
    return_button = tk.Button(func_window, height=2, width=10, text='Return', command=quit_window)
    return_button.grid(row=max_inputs+1, columnspan=8)

    func_window.mainloop()

def receive_AIS():
    
    func_picker.destroy()

    #Create variable input window
    func_window = tk.Tk()
    func_window.title("Receive AIS Signal")
    func_window.geometry('820x600')

    info_text = tk.Label(func_window, height = 30, width = 600)
    info_text.pack()

    def parse_signal():
        AIS.AIS_Rx.main() #Comment this to use already stored file 'input.bin'
        with open('input_data.bin','rb') as file:
            info = sig_par.read_AIS(file.read())
            info_text.config(text=info)

    receive_button = tk.Button(func_window, height=2, width=30, text="Receive", command=parse_signal)
    receive_button.pack()

    func_window.mainloop()

def main_window():
    global func_picker

    #Create function picking window
    func_picker = tk.Tk() 
    func_picker.title("Signal Test Bed") 
    func_picker.geometry('500x500') 

    #Introductory text saying to pick an option
    intro_text = tk.Label(func_picker, pady=30, text="Please pick an option:")
    intro_text.config(font=("Calibri", 14))
    intro_text.pack()

    #Function buttons
    tk.Button(func_picker, height=2, width=30, text ="Send AIS signal", command=send_AIS).pack()
    tk.Button(func_picker,height=2, width=30, text="Receive AIS signal", command=receive_AIS).pack()

    func_picker.mainloop() 

main_window()