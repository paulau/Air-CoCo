#!/usr/bin/python
# -*- coding: UTF-8 -*-

# This script is to visualize Data of: 
# 1) Temperature sensor inside downstares
# 2) Temperature sensor outside
# 3) State of ventilation (logical variable 0 or 1)
# 4) State of Wind-rain automatic.

# usage: 
# cd ... 
# python visu.py /home/pi/Steuerung-Monitoring/data/  kk002_2019_03_22_00_00.txt


import sys, os, datetime
from ReadSplitFile import ReadSplitFileN
from datetime import timedelta


#expath = os.path.split(os.path.abspath(os.path.realpath(sys.argv[0])))[0]
#datapath = '/home/pi/Steuerung-Monitoring/data/'
#fname = 'kk002_2019_03_22_00_00.txt'
#excommand  = 'python ' + expath + '/visu.py' +  ' ' + datapath + ' ' + fname
#print(excommand)

import matplotlib as mpl
window = False
if (not window):
	mpl.use('Agg')
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

fa = 5

args = sys.argv
ipath = str(args[1])
ifilesteuerout = ipath + str(args[2])

outf = ifilesteuerout[0:-3]	
outf = outf + "png"	
#outf = "auswertung.png"

y1min = 0
y1max = 40



colorOutside="#0000FF" #
colorInside='#00FF00' # 
colorInsideUp='#00FFFF' # 

# control Data
tr, Values = ReadSplitFileN(ifilesteuerout, 4) #
Tin = Values[0]
Tout = Values[1]
WindRainState = Values[2]
VentillatorState = Values[3]

#print (VentillatorState)

#CleanControlData(tr, Tin, RHin, Tout, RHout, VentillatorState)


Now = datetime.datetime.today()
		
fig = plt.figure() #,  dpi=300 # "Temperatur Und Feuchtigkeit")

d2 = tr[-1]
d1 = tr[0]

#delta = d2 - d1
myFmt = mdates.DateFormatter('%d.%m.%Y %H:%M')   # '%d.%m.%Y %H:%M'  


#d1 = datetime.datetime.strptime('26.06.2017 07:00', '%d.%m.%Y %H:%M') #  %H:%M
#d2 = datetime.datetime.strptime('28.06.2017 07:00', '%d.%m.%Y %H:%M') #  %H:%M

	
ax1 = fig.add_subplot(211)
ax1.set_xlabel('t')
ax1.set_ylabel(u'T, °C')

line2 = ax1.plot(tr, Tout, '.', color=colorOutside, markersize=5, label=u'draußen')  # markerfacecolor='#FFFFFF', markeredgecolor='#FFFF00', 
line1 = ax1.plot(tr, Tin, '.', color=colorInside, markersize=7, label=u'innen, unten') 

ax1.set_ylim([y1min, y1max])	
#plt.figtext(-0.2, 0.93, "Updated: "  + Now.strftime("%d.%m.%Y %H:%M") )

#ax1.set_ylim([10., 22.0])	
#ld1 = "09-06-16/16:00:00"
#ld2 = "10-06-16/16:00:00"
#d1 = datetime.datetime.strptime(ld1, '%d-%m-%y/%H:%M:%S') #    
#d2 = datetime.datetime.strptime(ld2, '%d-%m-%y/%H:%M:%S') #    

ax1.xaxis.set_major_formatter(myFmt)
plt.grid()	
plt.gcf().autofmt_xdate()

ax1r1 = ax1.twinx()	
line5 = ax1r1.plot(tr, VentillatorState, '.', color='r', markersize=3, label=u'Lüftungsanlagezustand') 
ax1r1.set_yticks([0.0, 0.5, 1.0])
ax1r1.set_ylim([0.1, 1.1])	

print(d1)
print(d2)

ax1r1.set_xlim([d1, d2])	

## inverse logic
#i = 0
#for val in WindRainState:
#	v = float(val)
#	if (v<0.1):
#		WindRainState[i] = 0.95
#	else:
#		WindRainState[i] = 0.0	
#	i = i + 1	

line7 = ax1r1.plot(tr, WindRainState, '.', color='#FFA500', markersize=10, label=u'Regen oder Wind')
lns = line1 + line2
lns = lns + line5 + line7 # + line4
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc='upper center', bbox_to_anchor=(0.5, 1.25), ncol=5, prop={'size':10}, fontsize=12, markerscale=2)		

plt.savefig(outf, dpi=300, bbox_inches='tight', pad_inches=0) # save temperatures
if (window):
	plt.show()
else:
	plt.close()
