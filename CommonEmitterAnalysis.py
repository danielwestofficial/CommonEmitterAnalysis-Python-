import numpy as np 
import matplotlib.pyplot as plt

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

    # Common Emitter DC and AC Analysis
    #

    # DC Analysis
    #A = Beta.*(RE1+RE2);
    #B = 10.*(1/((1/R1)+(1/R2)));
    #StiffDivider = A >= B;          %iDoes the circuit have a stiff voltage divider?
###############################################################################################################################################

# Determining if there is a stiff voltage divider 
# β • (RE1+RE2) ≥ 10 • (R1//R2) 
def StiffDivider(Beta, RE1, RE2, R1, R2):
    A = Beta * (RE1 + RE2)
    B = 10 * (1 / ((1/R1) + (1/R2)))
    StiffDivider = A >= B

    if StiffDivider == False:
        StiffDivider = 'True'
    print(StiffDivider)

    # DC Analysis
def DCAnalysis(VCC, Beta, RS, R1, R2, RE1, RE2, RC, RL):
    VB = VCC*(R2/(R2+R1))
    print(VB)
    VE = VB - 0.7
    print(VE)
    ICEQ = VE/(RE1+RE2)
    print(ICEQ)
    VC = VCC-(ICEQ*RC)
    print(VC)
    VCEQ = VC - VE
    print(VCEQ)
    return VE, ICEQ, VC, VCEQ

    # AC Analysis
def ACAnalysis(ICEQ, VCC, Beta, RS, R1, R2, RE1, RE2, RC, RL, Zg, Vs, VA, Frequency):
    ro = VA/ICEQ
    print(ro)
    re = .025/(ICEQ)
    print(re)
    rc = 1/((1/RC)+(1/RL))
    print(rc)
    Zbase = (RE1+re)*Beta
    print(Zbase)
    Zin = RS + (1/((1/R1)+(1/R2)+(1/(Beta*(RE1+re)))))
    print(Zin)
    Zout = 1/((1/RC)+(1/RL)+(1/ro))
    print(Zout)
    Vin = Vs*(Zin/(Zin+Zg+RS))
    print(Vin)
    Av = rc/(RE1+re)
    print(Av)
    Vout=Av*(Vin)
    print(Vout)
    return ro, re, rc, Zbase, Zin, Zout, Vin, Av, Vout

    # Optimizing Q-Point
def Qpoint(VE, rc):
    REop = VE*(RC+rc)/(VCC-VE)
    print(REop)
    return REop

    # Maximum Peak to Peak 
def MPP(VCEQ,ICEQ,rc):
    Mpp = min(2*(ICEQ * rc), 2*(VCEQ)) # Take the minimum of MPP1 and MPP2
    print(Mpp)
    return Mpp

    # Current Drain
def CurrentDrain(ICEQ):
    Ibias = VCC/(R1+R2)
    print(Ibias)
    IS = Ibias + ICEQ
    print(IS)
    return Ibias, IS

    # Power and Efficiency
def Power(VCEQ,ICEQ,IS):
    PD = VCEQ  * ICEQ
    print(PD)
    PL = (Mpp**2)/(8 * RL)
    print(PL)
    PS = VCC * IS
    print(PS)
    Efficiency = PL/PS * 100 
    print(Efficiency)
    return PD, PL, PS, Efficiency

    # Plotting Q-Point

    # DC Loadline
def DCLoadline(VE):
    VCEcutoff = VCC - VE
    print(f'VCEcutoff: {VCEcutoff} V')
    ICsaturation = (VCC-VE)/RC
    print(f'ICsaturation: {ICsaturation} A')
    return VCEcutoff, ICsaturation


    # AC Loadline
def ACLoadline(VCEQ,ICEQ,rc):
    ACcutoff = VCEQ + (ICEQ * rc)
    print(f'ACcutoff: {ACcutoff} A')
    ACsaturation = ICEQ + (VCEQ/rc)
    print(f'ACsaturation: {ACsaturation} A')
    return ACcutoff, ACsaturation

def Loadlineplot(VCEcutoff, ICsaturation, ACcutoff, ACsaturation):
    #VCEcutoff, ICsaturation = DCLoadline(VCEQ)
    xDC = np.linspace(0, VCEcutoff)
    yDC = np.linspace(ICsaturation, 0)
  
    #ACcutoff, ACsaturation = ACLoadline(VCEQ, ICEQ, rc)
    xAC = np.linspace(ACcutoff, 0)
    yAC = np.linspace(0, ACsaturation)

    # Plot DC and AC loadlines
    fig, ax = plt.subplots()
    ax.plot(xDC, yDC, 'b', label='DC Loadline')
    ax.plot(xAC, yAC, 'r', label='AC Loadline')
    ax.set_xlim([0, VCC])
    ax.set_ylim([0, VCC/rc])
    ax.set_xlabel('VCE (volts)')
    ax.set_ylabel('IC (amps)')
    ax.legend() 

    # Show plot
    plt.show()  

# Plot input and output waveforms
def Waveforms(Duration, Frequency, Vs, Vout):
    T1 = Duration
    fs1 = 50*Frequency
    Ts1 = 1/fs1
    t1 = np.arange(0, T1+Ts1, Ts1)
    a1 = Vs*np.sin(2*np.pi*Frequency*t1)
    a2 = -1*Vout*np.sin(2*np.pi*Frequency*t1)
    fig, ax = plt.subplots()
    ax.plot(t1, a1, t1, a2)
    ax.set_xlabel('Duration (seconds)')
    ax.set_ylabel('Magnitude (volts)')
    ax.legend(['Input', 'Output'])

    # Show plot
    plt.show()  

# User Inputs
VCC = float(input("VCC: "))
Beta = float(input("Beta: "))
RS = float(input("RS: "))
R1 = float(input("R1: "))
R2 = float(input("R2: "))
RE1 = float(input("RE1: "))
RE2 = float(input("RE2: "))
RC = float(input("RC: ")) 
RL = float(input("RL: "))
Zg = float(input("Zg: "))
Vs = float(input("Vs: "))
VA = float(input("VA: "))
Frequency = float(input("Frequency: "))
Duration = float(input("Duration: "))

#VCC = 20
#Beta = 380
#RS = 8200
#R1 = 10000000
#R2 = 620000
#RE1 = 270
#RE2 = 430
#RC = 24000
#RL = 2700
#Zg = 0
#Vs = .02
#VA = 100
#Frequency = 1000
#Duration = .002

# Call Functions
StiffDivider(Beta, RE1, RE2, R1, R2)

VE, ICEQ, VC, VCEQ = DCAnalysis(VCC, Beta, RS, R1, R2, RE1, RE2, RC, RL)

ro, re, rc, Zbase, Zin, Zout, Vin, Av, Vout = ACAnalysis(ICEQ, VCC, Beta, RS, R1, R2, RE1, RE2, RC, RL, Zg, Vs, VA, Frequency)

REop = Qpoint(VE, rc)

Mpp = MPP(VCEQ,ICEQ,rc)

Ibias, IS = CurrentDrain(ICEQ)

PD, PL, PS, Efficiency = Power(VCEQ,ICEQ,IS)

VCEcutoff, ICsaturation = DCLoadline(VE)

ACcutoff, ACsaturation = ACLoadline(VCEQ,ICEQ,rc)

Loadlineplot(VCEcutoff, ICsaturation, ACcutoff, ACsaturation)

Waveforms(Duration, Frequency, Vs, Vout)
