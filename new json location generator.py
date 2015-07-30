#YRS random longitude lattidude generator
#Angus goody
#29/07/15

"""
Program to generate longitude and lattitude data based in England
also generates magnitude then can export to txt file

version alpha 2.1

new features
--------------------------

*preset countrys available
*Custom longitude and latitude
*More efficient code

"""
#import files needed in program
import random
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import  asksaveasfilename
from tkinter import *
import time

#sets up GUI window
master=Tk()
master.geometry("300x300")

#positions all the labels on screen
Label(master,text="Longitude:").grid(row=0,column=0)
Label(master,text="Latitude:").grid(row=1,column=0)
Label(master,text="# of results:   ").grid(row=2,column=0)
Label(master,text="Export name:").grid(row=3,column=0)
Label(master,text="Magnitude inc").grid(row=4,column=0)
Label(master,text="Messages      ").grid(row=5,column=0)
e1=Entry(master)
e1.grid(row=2,column=1)

e2=Entry(master)
e2.grid(row=3,column=1)

e3=Entry(master)
e3.grid(row=4,column=1)
#Entrys that handle custom longitude and lattitude
long=Entry(master,width=9)
lat=Entry(master,width=9)
long.grid(row=0,column=1)
lat.grid(row=1,column=1)


#inserts defaults into entrys based in birmingham
long.insert(END,52.662828)
lat.insert(END,-0.747835)
e3.insert(END,0.05)
#Lalbel that displays warning messages 
v=StringVar()
messages=Label(master,text="",textvariable=v).grid(row=5,column=1)
temp=Entry(master)
adr=Entry(master)

amount=random.randint(0,500)
e1.insert(END,amount)
e2.insert(END,"locations.txt")

track=[]
global loaded
loaded=False
def rand():
    addMag=e3.get()
    try:
        addMag=float(addMag)
    except:
        v.set("Not integer")
    else:
        del track [:]
        number=e1.get()
        try:
            number=int(number)
        except:
            v.set("Error when converting to integer")
        else:
            v.set(" ")
            track.append("{\"Locations\":[")
            track.append("\n")
            count=0
            mg=2
            ov=0
            mini=1
            #Main for loop that generates data for whatever user requests
            for x in range(0,number):
                count=count+1
                if count > 5 and ov < 150 :
                    ov=ov+1
                    count=0
                    mg=mg+addMag
                    mini=mini+addMag
                
                range1=long.get()
                range3=lat.get()
                range1=float(range1)
                range3=float(range3)
                Long=range1
                Lat=range3
                diff=0.1
                diff2=0.2
                fix1 =Long-diff
                fix2 =Long+diff
                num=random.uniform(fix1,fix2)
                fix1=Lat-diff2
                fix2=Lat+diff2
                num2=random.uniform(fix1,fix2)

                """
                track.append("     \"Magnitude\",(")
                
                track.append(mag)
                track.append("),")
                track.append("\n")
                track.append("     }")
                track.append("\n")
                """
                #adds to array in a json format for our database
                """
     {"point":new GLatLng(52.65228551322338,-0.6582179951695124),
     "Magnitude",(1.5),
     """
                #Adds the magnitude
                mag=random.uniform(mini,mg)
                mag=round(mag,1)
                track.append("     {")
                track.append("\n")
                track.append("        \"ACL\": { \n")
                track.append("              \"*\": { \n")
                track.append("                   \"read\": true \n")
                track.append("            }\n")
                track.append("        },\n")
                track.append("        \"Magnitude\": ")
                track.append(mag)
                track.append(",")
                track.append("\n")
                track.append("        \"createdAt\": ")
                nowTime=time.localtime()
                dateString=str(nowTime.tm_year)+"-"+str(nowTime.tm_mon)+"-"+str(nowTime.tm_mday)+"T"
                dateString=dateString+str(nowTime.tm_hour)+":"+str(nowTime.tm_min)+":"+str(nowTime.tm_sec)+".0Z"
                track.append("\"")
                track.append(dateString)
                track.append("\"")
                track.append(",")
                track.append("\n")
                track.append("        \"location\": { ")
                track.append("\n")
                track.append("            \"__type\": \"GeoPoint\",")
                track.append("\n")
                track.append("            \"latitude\": ")
                track.append(num2)
                track.append(", \n")
                track.append("            \"longitude\": ")
                track.append(num)
                track.append("\n")
                track.append("        },\n")
                track.append("        \"objectId\": ")
                track.append("\"ajhsakjd\"")#change to variable after test
                track.append(",")
                track.append("\n")
                track.append("        \"updatedAt\": ")
                track.append("\"")
                track.append(dateString)
                track.append("\"")
                track.append("\n")
                track.append("     }")
                if x != number-1:
                    track.append(",")
                track.append("\n")
                """
                track.append(num)
                track.append(",")
                track.append(num2)
                track.append(")")
                track.append(",")
                track.append("\n")
                """

                
            #Loop complete
            track.append("]}")
                             
            v.set("Generation complete")

            
            
def export():
    if loaded == True:
        file=adr.get()
        name=e2.get()
        name=str(name)
        if name.endswith(".txt") == False and name.endswith(".json") == False:
            v.set("Please use .txt or .json")
        else:
            temp.delete(0,END)
            temp.insert(END,file)
            temp.insert(END,"\ ")
            temp.insert(END,name)
            over=temp.get()
            over=str(over)
            
            #attemppts to open the directory file
            try:
                file=open(over,"w")
            except:  
               v.set("Directory error")
            else:
                for x in track:
                    x=str(x)
                    file.write(x)
                file.close()

                v.set("Export complete")
                print("Exported to",over)
    else:
        v.set("Please load export")
    
       
def browse():  
    directory=filedialog.askdirectory()
    if directory != "":
        adr.delete(0,END)
        adr.insert(END,directory)
        global loaded
        loaded=True
        v.set("Ready to export data")

#non button function        
def rename(nam):
    e2.delete(0,END)
    e2.insert(END,nam)

def country(longi,lati,name): #fucntion for prebuilt countrys longitude first then lattitude   
    long.delete(0,END)
    long.insert(END,longi)
    lat.delete(0,END)
    lat.insert(END,lati)
    rename(name)
    
#prebuilt countrys stored as functions that pass parameters to country function to reduce code size
    
def rush(): #Russia
    country(62.436242, 94.271690,"Russia locations.txt")
def can(): #Canada
    country(59.806251, -112.095496,"Canada locations.txt")
def africa(): #Africa
    country(13.728184, 20.218545,"Africa locations.txt")    
def china(): #Greenland
    country(34.987889, 103.666807,"China.txt")
def birming(): #Birmingham
    country(52.485377, -1.893179,"Birmingham.txt")
    
ran=Button(master,text="Generate",command=rand)
ran.grid(row=2,column=2)
br=Button(master,text="Browse    ",command=browse)
br.grid(row=3,column=2)
ex=Button(master,text="Export     ",command=export)
ex.grid(row=4,column=2)

#Buttons
Button(master,text="Russia     ",command=rush,bg="lightblue").grid(row=5,column=2)
Button(master,text="Canada  ",command=can,bg="magenta").grid(row=6,column=2)
Button(master,text="Africa     ",command=africa,bg="tomato").grid(row=7,column=2)
Button(master,text="China     ",command=china,bg="snow").grid(row=8,column=2)
Button(master,text="Birming  ",command=birming,bg="orange").grid(row=9,column=2)
#main return loop
master.mainloop()

