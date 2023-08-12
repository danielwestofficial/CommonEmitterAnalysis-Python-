    # This function performs an analysis of a common emitter amplifier. 
    # The code takes in the inputs which are the amplitude of the DC source (VCC). 
    # The amplitude, impedance, frequency, and duration of the AC voltage source.
    # The transistor characteristics including Beta gain and Early Voltage.
    # The voltage divider resistances that bias the base. The swamped and
    # unswamped emitter resistances. The resistance of the collector and the load.

    # Inputs 
    # * VCC          = Voltage at the Common Collector;.1
    # * RS           = Series Resistance;
    # * R1           = Voltage Divider Resistance connected to VCC;
    # * R2           = Voltage Divider Resistance connected to Ground;
    # * RE1          = Swamped Emitter Resistance;
    # * RE2          = Emitter Resistance;
    # * RC           = Collector Resistance;
    # * RL           = Load Resistance;
    # * Zg           = Impedance of the signal source;
    # * Vs           = Amplitude of the signal source;
    # * Frequency    = Frequency of the signal source;
    # * Beta         = Ampification Factor;
    # * VA           = Early Voltage of the Transistor;
    #
    # Outputs 
    # * VB           = Voltage at the Base
    # * VE           = Voltage at the Emitter
    # * ICEQ         = Current at the Emitter/Collecture. Assumes IC = IE
    # * VC           = Voltage at the Collector
    # * VCEQ         = Voltage between the Collector and Emitter
    # * ro           = Output Resistance due to the Early Effect
    # * re           = Resistance of the Base-Emitter Junction
    # * rc           = Resistance of Collector in parallel with Load
    # * Zbase        = Input Impedance at the Base 
    # * Zin          = Total Input Impedance
    # * Zout         = Output Impedance
    # * vin          = Input Signal 
    # * Av           = Total Gain 
    # * Vout         = Output Signal 
    # * REop         = Optimum Emitter Resistance
    # * MPP          = Maximum Output Swing/Max Peak-to-peak
    # * Ibias        = Current through the Voltage Divider
    # * Is           = Total Current from the Source
    # * PD           = DC Input Power
    # * PL           = AC Power at the Load
    # * PS           = Total Power from the Source
    # * Efficiency   = Efficiency of Circuit (%)
    # * VCEcutoff    = Voltage at Cutoff 
    # * ICsaturation = Saturation Current
    # * ACcutoff     = AC Cutoff 
    # * ACsaturation = AC Saturation

import tkinter as tk
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

################################# Format Window ##############################################################
# Create the main window
root = tk.Tk()
root.title("Transistor Amplifier Calculator")

# Get the width and height of the screen
#screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Define the position and size of the main window
root.geometry("{}x{}+0+0".format(1110, screen_height))

################################################# Function Definitions ###########################################
# DC Analysis 
def DCAnalysis(VCC, Beta, RS, R1, R2, RE1, RE2, RC, RL):
    VB = VCC*(R2/(R2+R1))
    VE = VB - 0.7
    ICEQ = VE/(RE1+RE2)
    VC = VCC-(ICEQ*RC)
    VCEQ = VC - VE
    return VB, VE, ICEQ, VC, VCEQ

# AC Analysis
def ACAnalysis(ICEQ, VCC, Beta, RS, R1, R2, RE1, RE2, RC, RL, Zg, Vs, VA, Frequency):
    ro = VA/ICEQ
    re = .025/(ICEQ)
    rc = 1/((1/RC)+(1/RL))
    Zbase = (RE1+re)*Beta
    Zin = RS + (1/((1/R1)+(1/R2)+(1/(Beta*(RE1+re)))))
    Zout = 1/((1/RC)+(1/RL)+(1/ro))
    Vin = Vs*(Zin/(Zin+Zg+RS))
    Av = rc/(RE1+re)
    Vout=Av*(Vin)
    return ro, re, rc, Zbase, Zin, Zout, Vin, Av, Vout

# Optimizing Q-Point
def Qpoint(VCC, VE, rc, RC):
    REop = VE*(RC+rc)/(VCC-VE)
    return REop

# Maximum Peak to Peak 
def MPP(VCEQ,ICEQ,rc):
    Mpp = min(2*(ICEQ * rc), 2*(VCEQ)) # Take the minimum of MPP1 and MPP2
    return Mpp

# Current Drain
def CurrentDrain(VCC,ICEQ,R1,R2):
    Ibias = VCC/(R1+R2)
    IS = Ibias + ICEQ
    return Ibias, IS

# Power and Efficiency
def Power(VCEQ,ICEQ,Mpp,RL,VCC,IS):
    PD = VCEQ  * ICEQ
    PL = (Mpp**2)/(8 * RL)
    PS = VCC * IS
    Efficiency = PL/PS * 100 
    return PD, PL, PS, Efficiency

######## Plotting Q-Point #########
# DC Loadline
def DCLoadline(VCC, VE, RC):
    VCEcutoff = VCC - VE
    ICsaturation = (VCC-VE)/RC
    return VCEcutoff, ICsaturation

 # AC Loadline
def ACLoadline(VCEQ,ICEQ,rc):
    ACcutoff = VCEQ + (ICEQ * rc)
    ACsaturation = ICEQ + (VCEQ/rc)
    return ACcutoff, ACsaturation

# Load Line Plot
def Loadlineplot(VCEcutoff, ICsaturation, ACcutoff, ACsaturation, VCC, rc):
    #VCEcutoff, ICsaturation = DCLoadline(VCEQ)
    xDC = np.linspace(0, VCEcutoff)
    yDC = np.linspace(ICsaturation, 0)
  
    #ACcutoff, ACsaturation = ACLoadline(VCEQ, ICEQ, rc)
    xAC = np.linspace(ACcutoff, 0)
    yAC = np.linspace(0, ACsaturation)

    # Plot DC and AC loadlines
    fig = Figure(figsize=(6, 4), dpi=100, constrained_layout=True)
    ax = fig.add_subplot(111)
    ax.plot(xDC, yDC, 'b', label='DC Loadline')
    ax.plot(xAC, yAC, 'r', label='AC Loadline')
    ax.set_xlim([0, VCC])
    ax.set_ylim([0, VCC/rc])
    ax.set_xlabel('VCE (volts)')
    ax.set_ylabel('IC (amps)')
    ax.legend() 

    # Embed the matplotlib plot in a tkinter Frame widget
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()

    #Determine the number of columns in the window and set to far right of window
    canvas.get_tk_widget().place(x=500, y=0)

# Plot input and output waveforms
def Waveforms(Duration, Frequency, Vs, Vout):
    T1 = Duration
    fs1 = 50*Frequency
    Ts1 = 1/fs1
    t1 = np.arange(0, T1+Ts1, Ts1)
    a1 = Vs*np.sin(2*np.pi*Frequency*t1)
    a2 = -1*Vout*np.sin(2*np.pi*Frequency*t1)
    fig = Figure(figsize=(6, 4), dpi=100, constrained_layout=True)
    ax = fig.add_subplot(111)
    ax.plot(t1, a1, t1, a2)
    ax.set_xlabel('Duration (seconds)')
    ax.set_ylabel('Magnitude (millivolts)')
    ax.legend(['Input', 'Output'])

    # Embed the matplotlib plot in a tkinter Frame widget
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()

    #Determine the number of columns in the window and set to far right of window
    canvas.get_tk_widget().place(x=500, y=400)
  
########################################## Function for the GUI #####################################################
# Calculate button function
def calculate():
    VCC = float(entry1.get())
    RS = float(entry2.get())
    R1 = float(entry3.get())
    R2 = float(entry4.get())
    RE1 = float(entry5.get())
    RE2 = float(entry6.get())
    RC = float(entry7.get())
    RL = float(entry8.get())
    Beta = float(entry9.get())
    VA = float(entry10.get())
    Zg = float(entry11.get())
    Vs = float(entry12.get())
    Frequency = float(entry13.get())
    Duration = float(entry14.get())
   
    
    # Call DCAnalysis function
    VB, VE, ICEQ, VC, VCEQ = DCAnalysis(VCC, Beta, RS, R1, R2, RE1, RE2, RC, RL)
    # Call ACAnalysis function
    ro, re, rc, Zbase, Zin, Zout, Vin, Av, Vout = ACAnalysis(ICEQ, VCC, Beta, RS, R1, R2, RE1, RE2, RC, RL, Zg, Vs, VA, Frequency)
    # Call Optimizing Q-Point function
    REop = Qpoint(VCC, VE, rc, RC)
    # Call Maximum Output Swing function
    Mpp = MPP(VCEQ,ICEQ,rc)
    # Call Current Drain function
    Ibias, IS = CurrentDrain(VCC, ICEQ, R1, R2)
    # Call Power and Efficiency function
    PD, PL, PS, Efficiency = Power(VCEQ,ICEQ,Mpp,RL,VCC,IS)
    # Call DC Load Line
    VCEcutoff, ICsaturation = DCLoadline(VCC, VE, RC)
    # AC Load Line function
    ACcutoff, ACsaturation = ACLoadline(VCEQ,ICEQ,rc)
    # Plot/Embed Load lines function
    Loadlineplot(VCEcutoff, ICsaturation, ACcutoff, ACsaturation, VCC, rc)
    # Plot/Embed Waveforms function
    Waveforms(Duration, Frequency, Vs, Vout)
    # Update labels with calculated values
    label_VB.config(text="VB: {:.6f} V".format(VB))
    label_VE.config(text="VE: {:.6f} V".format(VE))
    label_ICEQ.config(text="ICEQ: {:.6f} A".format(ICEQ))
    label_VC.config(text="VC: {:.6f} V".format(VC))
    label_VCEQ.config(text="VCEQ: {:.6f} V".format(VCEQ))
    label_ro.config(text="ro: {:.6f} ohms".format(ro))
    label_re.config(text="re: {:.6f} ohms".format(re))
    label_rc.config(text="rc: {:.6f} ohms".format(rc))
    label_Zbase.config(text="Zbase: {:.6f} ohms".format(Zbase))
    label_Zin.config(text="Zin: {:.6f} ohms".format(Zin))
    label_Zout.config(text="Zout: {:.6f} ohms".format(Zout))
    label_Vin.config(text="Vin: {:.6f} Vp".format(Vin))
    label_Av.config(text="Av: {:.6f} V/V".format(Av))
    label_Vout.config(text="Vout: {:.6f} Vp".format(Vout))
    label_REop.config(text="REop: {:.6f} ohms".format(REop))
    label_Mpp.config(text="MPP: {:.6f} Vpp".format(Mpp))
    label_Ibias.config(text="Ibias: {:.6f} A".format(Ibias))
    label_IS.config(text="IS: {:.6f} A".format(IS))
    label_PD.config(text="PD: {:.6f} Watts".format(PD))
    label_PL.config(text="PL: {:.6f} Watts".format(PL))
    label_PS.config(text="PS: {:.6f} Watts".format(PS))
    label_Efficiency.config(text="Efficiency: {:.6f} %".format(Efficiency))
    label_VCEcutoff.config(text="VCEcutoff: {:.6f} V".format(VCEcutoff))
    label_ICsaturation.config(text="ICsaturation: {:.6f} A".format(ICsaturation))
    label_ACcutoff.config(text="ACcutoff: {:.6f} V".format(ACcutoff))
    label_ACsaturation.config(text="ACsaturation: {:.6f} A".format(ACsaturation))

########################################### Input values ######################################################
# Voltage at the Common Collector
label1 = tk.Label(root, text="VCC:")
label1.place(x=10, y=10)
entry1 = tk.Entry(root)
entry1.insert(0, "20")
entry1.place(x=80, y=10)

# Series Resistance
label2 = tk.Label(root, text="RS:") 
label2.place(x=10, y=40)
entry2 = tk.Entry(root)
entry2.insert(0, "8000")
entry2.place(x=80, y=40)

# Voltage Divider Resistance connected to VCC
label3 = tk.Label(root, text="R1:")
label3.place(x=10, y=70)
entry3 = tk.Entry(root)
entry3.insert(0, "10000000")
entry3.place(x=80, y=70)

# Voltage Divider Resistance connected to Ground
label4 = tk.Label(root, text="R2:")
label4.place(x=10, y=100)
entry4 = tk.Entry(root)
entry4.insert(0, "620000")
entry4.place(x=80, y=100)

# Swamped Emitter Resistance
label5 = tk.Label(root, text="RE1:")
label5.place(x=10, y=130)
entry5 = tk.Entry(root)
entry5.insert(0, "270")
entry5.place(x=80, y=130)

# Emitter Resistance
label6 = tk.Label(root, text="RE2:")
label6.place(x=10, y=160)
entry6 = tk.Entry(root)
entry6.insert(0, "430")
entry6.place(x=80, y=160)

# Collector Resistance
label7 = tk.Label(root, text="RC:")
label7.place(x=10, y=190)
entry7 = tk.Entry(root)
entry7.insert(0, "24000")
entry7.place(x=80, y=190)

# Load Resistance
label8 = tk.Label(root, text="RL:")
label8.place(x=10, y=220)
entry8 = tk.Entry(root)
entry8.insert(0, "2700")
entry8.place(x=80, y=220)

# Amplification Factor of the transistor
label_Transistor = tk.Label(root, text="Transistor")
label_Transistor.place(x=25, y=250)
label9 = tk.Label(root, text="Beta:")
label9.place(x=10, y=280)
entry9 = tk.Entry(root)
entry9.insert(0, "380")
entry9.place(x=80, y=280)

# Early Voltage of the Transistor
label10 = tk.Label(root, text="VA:")
label10.place(x=10, y=310)
entry10 = tk.Entry(root)
entry10.insert(0, "100")
entry10.place(x=80, y=310)

# Impedance of the signal source
label_SignalGen = tk.Label(root, text="Signal Generator")
label_SignalGen.place(x=25, y=340)
label11 = tk.Label(root, text="Zg:")
label11.place(x=10, y=370)
entry11 = tk.Entry(root)
entry11.insert(0, "50")
entry11.place(x=80, y=370)

# Amplitude of the signal source
label12 = tk.Label(root, text="Vs:")
label12.place(x=10, y=400)
entry12 = tk.Entry(root)
entry12.insert(0, "0.01")
entry12.place(x=80, y=400)

# Frequency of the signal source
label13 = tk.Label(root, text="Frequency:")
label13.place(x=10, y=430)
entry13 = tk.Entry(root)
entry13.insert(0, "1000")
entry13.place(x=80, y=430)

# Duration of the waveform
label14 = tk.Label(root, text="Duration:")
label14.place(x=10, y=460)
entry14 = tk.Entry(root)
entry14.insert(0, "0.002")
entry14.place(x=80, y=460)

# Calculate Button
button = tk.Button(root, text="Calculate", command=calculate)
button.place(x=10, y=490)

########################################### Output values ######################################################
# DC Output Labels
label_DC = tk.Label(root, text="DC Analysis")
label_DC.place(x=225, y=10)
label_VB = tk.Label(root, text="")
label_VB.place(x=200, y=40)
label_VE = tk.Label(root, text="")
label_VE.place(x=200, y=70)
label_ICEQ = tk.Label(root, text="")
label_ICEQ.place(x=200, y=100)
label_VC = tk.Label(root, text="")
label_VC.place(x=200, y=130)
label_VCEQ = tk.Label(root, text="")
label_VCEQ.place(x=200, y=160)

# AC Output Labels
label_AC = tk.Label(root, text="AC Analysis")
label_AC.place(x=225, y=190)
label_ro = tk.Label(root, text="")
label_ro.place(x=200, y=220)
label_re = tk.Label(root, text="")
label_re.place(x=200, y=250)
label_rc = tk.Label(root, text="")
label_rc.place(x=200, y=280)
label_Zbase = tk.Label(root, text="")
label_Zbase.place(x=200, y=310)
label_Zin = tk.Label(root, text="")
label_Zin.place(x=200, y=340)
label_Zout = tk.Label(root, text="")
label_Zout.place(x=200, y=370)
label_Vin = tk.Label(root, text="")
label_Vin.place(x=200, y=400)
label_Av = tk.Label(root, text="")
label_Av.place(x=200, y=430)
label_Vout = tk.Label(root, text="")
label_Vout.place(x=200, y=460)

# Optimizing Q-Point Label
label_Optimize = tk.Label(root, text="Optimizing Q-Point")
label_Optimize.place(x=225, y=490)
label_REop = tk.Label(root, text="")
label_REop.place(x=200, y=520)

# Maximum Output Swing (MPP) Label
label_MaxOut = tk.Label(root, text="Maximum Output Swing")
label_MaxOut.place(x=225, y=550)
label_Mpp = tk.Label(root, text="")
label_Mpp.place(x=200, y=580)

# Current Drain Labels
label_Current = tk.Label(root, text="Current Drain")
label_Current.place(x=225, y=610)
label_Ibias = tk.Label(root, text="")
label_Ibias.place(x=200, y=640)
label_IS = tk.Label(root, text="")
label_IS.place(x=200, y=680)

# Power and Efficiency Labels
label_Power = tk.Label(root, text="Power and Efficiency")
label_Power.place(x=225, y=710)
label_PD = tk.Label(root, text="")
label_PD.place(x=200, y=740)
label_PL = tk.Label(root, text="")
label_PL.place(x=200, y=770)
label_PS = tk.Label(root, text="")
label_PS.place(x=200, y=800)
label_Efficiency = tk.Label(root, text="")
label_Efficiency.place(x=200, y=830)

# DC Load Line Labels
label_DCLoadline = tk.Label(root, text="AC and DC Loadlines")
label_DCLoadline.place(x=10, y=520)
label_VCEcutoff= tk.Label(root, text="")
label_VCEcutoff.place(x=0, y=550)
label_ICsaturation = tk.Label(root, text="")
label_ICsaturation.place(x=0, y=580)

# AC Load Line Labels
label_ACcutoff= tk.Label(root, text="")
label_ACcutoff.place(x=0, y=610)
label_ACsaturation = tk.Label(root, text="")
label_ACsaturation.place(x=0, y=640)

root.mainloop()