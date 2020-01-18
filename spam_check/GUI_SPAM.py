from tkinter import *
import tkinter as tk
from functools import partial
from sklearn.externals import joblib

model=joblib.load('C:\\Users\\tusha\Desktop\Spam_check\model.pkl')
cv=joblib.load('C:\\Users\\tusha\Desktop\Spam_check\\vector.pkl')
encryp_window=None

def predictor(text):
    text=text.get("1.0",END)
    global model,encryp_window
    text_bag=cv.transform([text])
    opt=model.predict(text_bag)
    Label(encryp_window,text='I Think it is...',font=("verdana",7,"bold")).place(relx=0.1,rely=0.55)
    Label(encryp_window,text=opt[0],font=("verdana",11,"bold italic")).place(relx=0.1,rely=0.6)

def GUI():
    global encryp_window
    encryp_window=tk.Tk()
    encryp_window.geometry("450x600")
    encryp_window.title('SPAM DETECTION')
    encryp_window.configure(background='white')

    title=tk.Label(encryp_window,text='SPAM OR HAM',font={'verdana','100','italic bold'},bg='red',fg='white',bd=8,width=70)
    title.pack(fill=Y,side=TOP)
    encrypt_exit=tk.Button(encryp_window,text='EXIT',width=5,bd=5, height=1,bg="white",font=("verdana",11,"bold"),command=quit)
    encrypt_exit.place(relx=0.80,rely=0.0045)

    ##textbox for taking text to be encrypted
    tk.Label(encryp_window,text='ENTER TEXT BELOW').place(relx=0.1,rely=0.10)
    enc_text=Text(encryp_window,width=40,height=10)
    enc_text.place(relx=0.1,rely=0.15)

    ##button to start encryption
    but=Button(encryp_window,text='CHECK',command=partial(predictor,enc_text))
    but.place(relx=0.1,rely=0.45)

    ##
    encryp_window.mainloop()

if __name__=='__main__':
    GUI()
