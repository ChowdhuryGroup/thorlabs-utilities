# -*- coding: utf-8 -*-
"""
GUI Melles Griot Nanomotion II
UPDATED: 02-07-2020

 M easurement
 A cquisition
'N
 D ata
 O rganization to
 R eplace
 L abVIEW
 A pplications

"""
import MellesGriot_nanomotionii as mg # import Python library for the desired instrument
import tkinter as tk # Python's standard GUI package
from types import MethodType

#%%
def end(): # what to do when you press "Close"
    m.quit()
    m.destroy()
    return

def maketkvar(var): # function to automatically assign proper TK variable to an input
     if type(var)==str:
        tkvar=tk.StringVar()
     elif type(var)==int:
        tkvar=tk.IntVar()
     elif type(var)==float:
        tkvar=tk.DoubleVar()
     elif type(var)==bool:
        tkvar=tk.BooleanVar()
     else:
        print('THIS FUNCTION WILL NOT WORK!')
        tkvar=var  
     return tkvar

class labelvalupd: # a class to create a GUI row with the format: [Label][Value Display][PostLabel][Update Button]
   
    def __init__(self,frame,label,valinit,editable,frow,fcol,postlabel,importcmd,*args):
        
        self.frame=tk.Frame(frame)
        self.frame.grid(row=frow,column=fcol)
        if editable==False:
            self.state='readonly'
            bname='Update'
            self.valupdB=tk.Button(self.frame,text=bname,command=self.updcmd)
            
        else:
            self.state='normal'
            bname='Set'
            self.valupdB=tk.Button(self.frame,text=bname,command=self.setcmd)
            
        self.importcmd=importcmd
        self.args=args
        self.margs=list(args)+[None]
        tk.Label(self.frame,text=str(label)).grid(row=0,column=0)
        self.value=maketkvar(valinit)          
        self.value.set(valinit)
        self.valdisplay=tk.Entry(self.frame,textvariable=self.value,state=self.state)
        self.valdisplay.grid(row=0,column=1)
        tk.Label(self.frame,textvariable=postlabel).grid(row=0,column=2)
        self.valupdB.grid(row=0,column=3)
        
        return 
    
    def updcmd(self):
        a,b=self.importcmd(*self.args)
        self.value.set(b)
        return
    
    def setcmd(self):
        lastelm=len(self.margs)-1
        self.margs[lastelm]=self.valdisplay.get()
        self.importcmd(*self.margs)
        return

class advbutton: # a class to create a GUI row with the format: [Action Button][Value Display][PostLabel] with option for just showing the button
   
    def __init__(self,frame,label,solobutton,valinit,frow,fcol,postlabel,importcmd,*args):
        self.frame=tk.Frame(frame)
        self.frame.grid(row=frow,column=fcol)
        self.importcmd=importcmd
        self.solob=solobutton
        self.args=args
        self.margs=list(args)+[None]
        self.cmdb=tk.Button(self.frame,text=str(label),command=self.setcmd)
        self.cmdb.grid(row=0,column=0)
        self.value=maketkvar(valinit)          
        self.value.set(valinit)
            
        if self.solob==False:   
            self.valdisplay=tk.Entry(self.frame,textvariable=self.value)
            self.valdisplay.grid(row=0,column=1)
            tk.Label(self.frame,textvariable=postlabel).grid(row=0,column=2)
            
        return 
    
    def setcmd(self):
        if self.solob==True:
            self.importcmd(*self.args)
        else:
            lastelm=len(self.margs)-1
            self.margs[lastelm]=self.valdisplay.get()
            self.importcmd(*self.margs)
            
        return
    
class genradbuttonupd: # a class to create a GUI radiobutton with custom size for selection
   
    def __init__(self,frame,label,valinit,labrow,labcol,importcmd,*args,**kwargs):
        self.frame=tk.LabelFrame(frame,text=label,bd=4)
        self.frame.grid(row=labrow,column=labcol)
        self.margs=list(args)+[None] # convert 'args' from a tuple to a list so that we can change elements and add an element to store the variable controlled by the widget     
        self.kwargs=kwargs
        self.importcmd=importcmd
        self.output=tk.StringVar()
        self.var=maketkvar(valinit)          
        self.var.set(valinit)
           
        self.radb=[None]*len(self.kwargs.keys()) # create empty list for radio buttons
        i=0   # set index for list
        for key, kvalue in self.kwargs.items(): # populate list
            
            self.radb[i]=tk.Radiobutton(self.frame, text= str(key), variable=self.var,value=kvalue, command=self.setcmd)
            self.radb[i].grid(row=i,column=0)
            i=i+1
        self.output.set(list(self.kwargs.keys())[list(self.kwargs.values()).index(valinit)])        
        return 
    def setcmd(self):
        lastelm=len(self.margs)-1
        self.margs[lastelm]=self.var.get() # store widget variable in 'args' list
        self.importcmd(*self.margs) # send arguments to imported command
        self.output.set(list(self.kwargs.keys())[list(self.kwargs.values()).index(self.var.get())])
        return

class logwindow: # create a multiline window to log info NOT FINISHED
    def __init__(self,frame,label,header,frow,fcol,width,length,readcommand,*args):
        self.frame=tk.Frame(frame)
        self.frame.grid(row=frow,column=fcol)
        tk.Label(self.frame,text=label).grid(row=0,column=0)
        self.readout=tk.Text(self.frame,state='normal')
        self.readout.grid(row=2,column=0,columnspan=4)
        
        
        return
    
#%%-- take instrument library and add a tk widget for COM control
def setcomport(self): # command to set COM port
        self.setcmd(self,self.var.get())    
        return
    
def comwidget(self): # tk widget
        self.valdisplay=tk.Spinbox(self.frame,from_=1,to=9,textvariable=self.var,width=5)
        self.valdisplay.grid(row=0,column=1)
        self.cmdb=tk.Button(self.frame,text='Set COM port',command=self.setcomport)
        self.cmdb.grid(row=0,column=0)
        return

def cinstrument(importlib,frame,name,setcmd,setarg,frow,fcol,**attr): # function to add previous methods to instrument library
        setattr(importlib,'setcmd',setcmd)
        setattr(importlib,'var',maketkvar(setarg))
        importlib.var.set(setarg)
        setattr(importlib,'frame',tk.LabelFrame(frame,text=name))
        importlib.setcomport=MethodType(setcomport,importlib)
        importlib.comwidget=MethodType(comwidget,importlib)
        importlib.comwidget()
        
        importlib.frame.grid(row=frow,column=fcol)
        
        for key, value in attr.items():
          setattr(importlib,key,value)
        return


    
#%%-- make GUI window and setup instrument
      
m=tk.Tk()
m.title('MANDORLA_template')
#icon=tk.PhotoImage(file='mandorlaicon_v2.png')  
#m.iconphoto(False,icon)
rowNum=10;
colNum=5;
ntxt=tk.StringVar() # no text for some postlabels
ntxt.set('')
buttonw=15

mot=mg.motor()
motargs=dict(motornum=1,)
cinstrument(mot,m,'MG Nanomover',mg.motor.comset,5,0,0,**motargs)
#%%
#-- status and exit frame
statfr=tk.Frame(m)
statfr.grid(row=1,column=3)

strplhld='-------------------------' # string placeholder for initialization

cinfo=labelvalupd(statfr,'Controller ID:',strplhld,False,1,1,ntxt,mot.controlID)
cstat=labelvalupd(statfr,'Controller Status:',strplhld,False,3,1,ntxt,mot.checkstat)
cstat.valdisplay.config(width=30)
motstat=labelvalupd(statfr,'Motor Status:',strplhld,False,3,5,ntxt,mot.readstat,mot.motornum)
motstat.valdisplay.config(width=30)

stop=tk.Button(statfr,text='EXIT', width=buttonw, fg='red',command=end)
stop.grid(row=1,column=5)

motreset=advbutton(statfr,'Reset Motor',True,'',3,7,ntxt,mot.reset,mot.motornum)
#motnum=genradbuttonupd(statfr,'Motor #',1,1,5,mot.)
#-- motor settings frame
motsetfr=tk.Frame(m)
motsetfr.grid(row=5,column=4)
udict=dict(cm='CM',mm='MM',um='MI',nm='NM')
motunits=genradbuttonupd(motsetfr,'Motor Units','MM',7,1,mot.setunits,1,**udict)
leftlim=labelvalupd(motsetfr, 'Retract Limit',0,True,3,1,ntxt,mot.setleftabs,mot.motornum)
leftlim.valdisplay.config(width=5)
rightlim=labelvalupd(motsetfr, 'Extend Limit',0,True,5,1,ntxt,mot.setleftabs,mot.motornum)
rightlim.valdisplay.config(width=5)
motspeed=labelvalupd(motsetfr,'Motor Speed',2.5,True,1,1,ntxt,mot.setspeed,mot.motornum)
motspeed.valdisplay.config(width=5)

#-- motor move and position frame
motfr=tk.Frame(m)
motfr.grid(row=3,column=3)
motpos=labelvalupd(motfr,'Current Position:',strplhld,False,1,1,motunits.output,mot.rposition,mot.motornum)

motstop=advbutton(motfr,'STOP MOTOR',True,'',5,8,ntxt,mot.stop,mot.motornum)
motstop.cmdb.config(fg='white',bg='red',width=buttonw)
motpark=advbutton(motfr,'Park Motor',True,'',3,8,ntxt,mot.park,mot.motornum)
motpark.cmdb.config(bg='yellow',width=buttonw)
motunpark=advbutton(motfr,'Unpark Motor',True,'',1,8,ntxt,mot.unpark,mot.motornum)
motunpark.cmdb.config(bg='light green',width=buttonw)

move=advbutton(motfr,'Move',False,0,1,5,motunits.output,mot.move,mot.motornum)
move.cmdb.config(width=10)
move.valdisplay.config(width=5)
moveto=advbutton(motfr,'Move To',False,0,3,5,motunits.output,mot.moveto,mot.motornum)
moveto.cmdb.config(width=10)
moveto.valdisplay.config(width=5)
#-- position history frame
#poslog=logwindow(motfr,'Position Log',8,0,5,5,motor.rposition,1)
#-- motor position graphic



m.mainloop() # runs GUI window continuously
