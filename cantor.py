from tkinter import *
import requests
import json 
from PIL import ImageTk, Image
from requests.models import codes

root = Tk()
root.title("Cantor")
#root.geometry("650x450")
root.iconbitmap("favicon.ico")
root.resizable(False, False)

currencies = []
mids = []
codes = []


#--------- DATABASE ---------#
try:
   api_request = requests.get("http://api.nbp.pl/api/exchangerates/tables/A/")
   api = json.loads(api_request.content)
   with open("data.json", "w") as f:
      json.dump(api, f)
except:
   f = open("data.json")
   api = json.load(f)

for i in range(len(api[0]["rates"])):
   currencies.append(api[0]["rates"][i]["currency"])
   mids.append(api[0]["rates"][i]["mid"])
   codes.append(api[0]["rates"][i]["code"])

currencies.append("złoty")
mids.append(1)
codes.append("PLN")
d1 = dict(zip(currencies, mids))
d2 = dict(zip(currencies, codes))



#--------- CALCULATIONS ---------#
def run():
   v = round(float(value.get()), 2)
   c1 = choice1.get()
   c2 = choice2.get()
   m1 = d1[c1]
   m2 = d1[c2]
   k = m1/m2
   r = k*v

   V.set(v)
   R.set(round(r, 2))
   K.set(round(k, 4))

   abbr1.set(d2[choice1.get()])
   abbr2.set(d2[choice2.get()])
   


#--------- INFO ---------#
def finfo(): 
   info = Toplevel()
   info.resizable(False, False)
   info.title("Cantor - Information")
   info.iconbitmap("favicon.ico")
   txt = Label(info, font=7, justify=LEFT, text = "O PROGRAMIE\n\nProgram pobiera aktualne kursy walut ze strony\nNarodowego Banku Polskiego. Jeśli urządzenie\nnie ma dostępu do internetu, użyte zostaną\nkursy walut ściągnięte podczas ostatniego\nuruchomienia programu.")
   txt.pack()
   binfo = Button(info, text="OK", padx=5, borderwidth=3, command=info.destroy)
   binfo.pack(side=BOTTOM, pady=5)


#--------- REVERSE ---------#
def reverse():
   c1 = choice1.get()
   c2 = choice2.get()
   choice1.set(c2)
   choice2.set(c1)


#--------- MENU ---------#
menubar = Menu(root)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Start", command=run)
filemenu.add_command(label="Reverse", command=reverse)
filemenu.add_command(label="Quit", command=quit)
menubar.add_cascade(label="File", menu=filemenu)

infomenu = Menu(menubar, tearoff=0)
infomenu.add_command(label="Show info", command=finfo)
menubar.add_cascade(label="Info", menu=infomenu)



#--------- FRAMES ---------#
frame1 = LabelFrame(root, text="Choose currencies", padx=10, pady=20)
frame1.grid(row=0, column=0, padx=10, pady=10, columnspan=3)
frame2 = LabelFrame(root, text="Enter value", padx=10, pady=20)
frame2.grid(row=1, column=0, padx=10, pady=10, sticky="W")
frame3 = LabelFrame(root, text="Result", padx=10, pady=20)
frame3.grid(row=1, column=2, padx=10, pady=10, sticky="E")
frame4 = LabelFrame(root, text="Currency rate", padx=10, pady=20)
frame4.grid(row=1, column=1, padx=10, pady=10)
frame5 = LabelFrame(root, borderwidth=0)
frame5.grid(row=2, column=2, padx=5, sticky="E")


#--------- FILLING 1st FRAME ---------#
choice1 = StringVar()
choice2 = StringVar()
choice1.set("euro")
choice2.set("euro")
list1 = OptionMenu(frame1, choice1, *currencies)
list1.config(width=28, height=2, font=9)
list1.grid(row=0, column=0)
list2 = OptionMenu(frame1, choice2, *currencies)
list2.config(width=28, height=2, font=9)
list2.grid(row=0, column=2)
arrow_image = ImageTk.PhotoImage(Image.open("arrow.png").resize((100,40)))
arrow = Button(frame1, image=arrow_image, borderwidth=0, command=run)
arrow.grid(row=0, column=1, ipadx=10)


#--------- FILLING 2sd FRAME ---------#
V = DoubleVar()
value = Entry(frame2, textvariable=V, justify=CENTER, font=15, width=20)
value.grid(row=0, column=0)
abbr1 = StringVar()
abbr1.set((d2[choice1.get()]))
label1 = Label(frame2, textvariable=abbr1, borderwidth=4, relief="ridge", width=5)
label1.grid(row=0, column=1, padx=5)


#--------- FILLING 3rd FRAME ---------#
R = DoubleVar()
result = Label(frame3, textvariable=R, justify=CENTER, font=15, width=20)
result.grid(row=0, column=0)
abbr2 = StringVar()
abbr2.set((d2[choice2.get()]))
label2 = Label(frame3, textvariable=abbr2, borderwidth=4, relief="ridge", width=5)
label2.grid(row=0, column=1, padx=5)


#--------- FILLING 4th FRAME ---------#
K = DoubleVar()
label3 = Label(frame4, textvariable=K, font=15, width=10)
label3.grid(row=0, column=0)


#--------- BUTTONS ---------#
b1 = Button(frame5, text="Start", relief="groove", command=run)
b1.grid(row=0, column=0, padx=5, pady=10, sticky="E")
b2 = Button(frame5, text="Info", relief="groove", command=finfo)
b2.grid(row=0, column=2, padx=5, pady=10, sticky="E")
b3 = Button(frame5, text="Quit", relief="groove", command=quit)
b3.grid(row=0, column=3, padx=5, pady=10, sticky="E")
b4 = Button(frame5, text="Reverse", relief="groove", command=reverse)
b4.grid(row=0, column=1, padx=5, pady=10, sticky="E")


root.config(menu=menubar)
root.mainloop()