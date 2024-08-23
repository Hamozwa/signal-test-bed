# signal-test-bed
Horizon Technologies SPIN Signal Acquisition Algorithm Project

## Project Description 

The project is comprised of the simulation of several signals and their acquisition. Utilising HackRF hardware and python-based software (the latter including GNU Radio Companion-initialised files as well as modules and scripts), the chosen signals’ carried information can be custom crafted by the user. 

The intent is a simple-to-use software tool that can be configured to send these custom signals and read test signals via an SDR (software-defined radio). 

Currently only AIS is fully supported, but other signals, such as VDES and ADS-B have partial implementations as described in this document. Other signal types can also be easily added. 

## Setup 

### Python 

This project requires python 3.10 or later. This can be downloaded here. 

If using Visual Studio Code, the python extension will need to be installed by clicking Extensions on the vertical menu on the left side. Here, search for and select Python and Install. 

### GNU Radio 

GNU Radio is used for signal modulation and demodulation, and it can be downloaded here. 

### Radioconda 

Anaconda is a package manager for python, containing what is essentially external code useful to supporting local python files. Radioconda is a custom variant of this with SDR (Software-Defined Radio) capabilities allowing the user to use GNU Radio functionality within python scripts and, very crucially, interface with a HackRF. 

The download instructions are in the README in the GitHub repository here. 

Once installed, radioconda has to be selected as the chosen python interpreter. To do this in Visual Studio Code, go to  

View -> Command Palette 
 
This will open the search bar, where you can type (and select when it appears) Python: Select Interpreter. Then select Enter interpreter path... and find and select your installation \radioconda\python.exe 
 

### Python Packages 

After Radioconda has been installed, radioconda Prompt can be found as an application in the PC’s main search bar. Here, run these commands: 

pip install bitarray 

pip install pyais 

## Usage Instructions 

Run main.py to start the program. 

### Send AIS 

To send AIS signals, select Send AIS Signal. These fields can be changed according to the desired message and have been set to a default value. Types and their fields are all explained here. 

 Please note that values exceeding what the field should contain may cause a crash or unexpected result. Also, any fields containing b’’ as a default require byte data to be inputted in the python style, which you can learn more about here. 

### Receive AIS 

To receive AIS signals, select Receive AIS Signal and select Receive every time an updated reception is desired. 

### Workaround for Issues 

When tested, transmitting and receiving functions did not display issues. However, if installation has not been correct or unanticipated issues do arise, a counter-measure is available. 

GNU Radio Companion can be used to open .grc files in the AIS folder. Two python lines (indicated below) in main.py can be commented out and the program can be used to write or read from the .bin files, with the GNU Radio flowgraphs being used directly to send or receive these same files. 

## Files 

### main.py 

This python script provides a user interface (using the tkinter package) to the functions from the modules. 
 
When used to send signals, it takes an input for each field and passes it on to test_signal_generator in the form of a dict (more explanation in the message_info section on this). The function’s return is in byte format and saved to output_data.bin. 

When used to receive signals, it reads input_data.bin and prints the information available after parsing. 

### test_signal_generator.py 

Signal packets can be created via this module. It defines functions for each signal type in which information about the intended message is passed in as a parameter, before being encoded in a manner corresponding to that described in official documentation. 
 
The gen_AIS function relies on the pyais python module for the main encoding section (mostly for creating the payload as described in Annex 8 of ITU-R M.1371-5). CRC (cyclic redundancy check) is handled via CRC.py; byte reversal, bit stuffing, and NRZI encoding are handled similarly. More explanation on these functions can be found in this file’s section in this documentation. 

gen_ADSB creates its corresponding packet without the use of external code. Information concerning packet structure was sourced from The 1090MHz Riddle (mode-s.org) by Dr Junzi Sun, an assistant professor at TU Delft. The official ICAO standards, unfortunately, required a fee beyond reasonable feasibility for the project. After the corresponding CRC and PPM (Pulse Position Modulation) are applied, the packet is returned. 

gen_VDES, similarly to the ADS-B function, depends on its own code to form a packet encoding input data. ITU-R M.2092-1 It was used to inform this packet structure and message types. 

 

### message_parser.py 

This module is the inverse of test_signal_generator: it takes an input of binary information from input_data.bin and parses it dependent on the signal type. 

### message_info.py 

The dictionaries available in message_info form the main method of information spread through modules. Each dictionary has fields for each possible variable in the relevant signal type. 

To be initialised, a new variable is set to the value of the default dictionaries available here. The intention was to create a pseudo-object that worked in a more simplified and efficient way, given the information did not require any in-built functions. For this reason, dictionaries were used and not classes. 
 
Another advantage to this implementation is the simplicity of setting default values for fields. This, as well as the listing of all possible values, simplifies the GUI application and allows similar code to be reused for each signal’s transmit window. 

### CRC.py 

Despite being named CRC, this module also contains much of the bit manipulation logic necessary for error checking in general. CRC, however, is the main section. 

CRC (Cyclic Redundancy Check) is an error checking method that relies heavily on a strategy known as modulo-2 division. Put simply, this process leaves a remainder that is added to the end of the bits being protected before transmission. After receiving these bits, if there is no error, the remainder of division of the protected bits and their CRC should leave a predicted value. This “division” method requires a specific divisior to work both for CRC calculation and validation. More details concerning CRC can be found here. 

Despite the presence of CRC python modules online, none of these seemed to fit the technique described in ISO/IEC 13239:2002 to an accurate degree (this document being the one referenced by the AIS ITU document as describing its CRC). Therefore, CRC was implemented manually by creation of a custom CRC module that could be used for formation of signals depending on divisor and method. 

### input_data.bin / output_data.bin 

These store binary data to pass between the python code and the GNU Radio files. output_data.bin stores the packet generator’s output for transmission while input_data.bin stores the Rx output for parsing. 

### AIS 

#### AIS_Tx 

GNU Radio-based grc and py files that modulate and transmit AIS messages in output_data.bin 

 

#### AIS_Rx 

GNU Radio-based grc and py files that receive AIS signals, demodulate them and store the binary data in input_data.bin for parsing 

 

#### AIS_channel_simulator 

Combined modulation and demodulation grc and py files with channel simulator in between. This allows for the testing of both functions without requiring HackRF hardware to be set up on two separate PCs. This simplifies the testing process. 

## Possible Improvements 

### Signal Completion/Addition 

ADS-B requires modulation and demodulation implementations in GNU Radio. The main blocker in pursuit of this has been in the research of the techniques applied for transmitting.  

VDES also requires modulation, but also lacks FEC encoding according to the specification. The payload can be formed, but the error correction (Turbo encoding) and modulation for transmitting have not yet been implemented. 

Other signals can also be implemented similarly, including satellite phone L-Band signals or other satellite-based signals. 

#### ADS-B Details for Completion 

ADS-B requires modulation research to implement. The packetisation and parsing python functions have been written and the widget options for AIS can easily be replicated. However, the GNU Radio Flowgraphs and their respective python files have not yet been written due to a lack of success in finding modulation schemes for ADS-B. 

#### VDES Details for Completion 

VDES, like ADS-B, has not yet been modulated. The information on which schemes are applied for each type of VDES message are detailed in the ITU M.2092-1 specification. In particular, tables 7-11 (pages 21-25) are useful to this end. 

Another requirement for VDES functionality is FEC encoding and bit scrambling. Figure 6 in the document above (page 13) shows the steps for signal generation. Turbo Code is the form of FEC encoding used (basics of turbo code explained here). The specifics of the implementation are, again, in the ITU spec section 1.2.4 (pages 14-19). 

#### GUI Improvements 

The current available GUI was the simplest possible version that would contain all the fields necessary to send any AIS signal. This focus on accessing all the functionality available rather than ease of use was due to time constraint. 

For QoL (Quality of Life) improvement, a drop-down list for signal type could be employed to determine which fields are necessary and only display fields relevant to the message type. 
 
Also, input sanitisation could be applied such that the field requirements and limits are communicated, perhaps by hovering over the field. Currently, ensuring valid input is left as the user’s responsibility. 
