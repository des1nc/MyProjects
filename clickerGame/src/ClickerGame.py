from tkinter import *
#Author AmUkSpace
f = open('results.txt') #Run to save statistics
n = float(f.readline())
z = float(f.readline())
count = float(f.readline())
f.close()



tk = Tk()
tk.title('ClickerGame By AmUkSpace')
tk.geometry("1500x800")

def plus():
    global n
    n = round((n+z),3)
    label1['text'] = str(n) + '$'

def nsbros():
    global n
    global z
    global count
    n=0
    z = 0.1
    count = 0.4
    label1['text'] = str(n) + '$'
    label2['text'] = 'Per click: ' + str(round(z, 3)) + '$'
    label3['text'] = 'Upgrade cost: ' + str(round(count, 3)) + '$'

def dopclick():
    global n
    global z
    global count
    if n >= count:
        n = round((n - count),3)
        z = z + z/4
        count = z * 4
    label1['text'] = str(n) + '$'
    label2['text'] = 'За клик: ' + str(round(z,3)) + '$'
    label3['text'] = 'Стоимость улучшения: ' + str(round(count, 3)) + '$'


label1 = Label(tk, text=str(round(n,3))+'$', font=('Helvetica 100'))
label1.pack()

label2 = Label(tk, text='За клик: '+str(round(z,3))+'$', font=('Helvetica 30'))
label2.pack()
label3 = Label(tk, text='Стоимость улучшения: '+str(round(count,3))+'$', font=('Helvetica 30'))
label3.pack()

btn1 = Button(text="Клик", background="#000", foreground="#fff",
             padx="60", pady="30", font="Helvetica 50", command=plus)

btn1.pack()
label4 = Label(tk, text='', font=('Helvetica 30'))
label4.pack()
btn3 = Button(text="Improvement", background="#000", foreground="#fff",
             padx="60", pady="10", font="Helvetica 25", command=dopclick)
btn3.pack()
label5 = Label(tk, text='', font=('Helvetica 30'))
label5.pack()
btn2 = Button(text="Reset", background="#000", foreground="#fff",
             padx="20", pady="8", font="16", command=nsbros)
btn2.pack()

mainloop()
f = open('results.txt', "w")
f.write(str(n) + '\n')
f.write(str(z) + '\n')
f.write(str(count) + '\n')
f.close()