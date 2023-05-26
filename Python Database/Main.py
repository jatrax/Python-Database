import mysql.connector
from tkinter import *
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="sys"
)

mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS myTable (PERSONAL_ID INT AUTO_INCREMENT,FULL_NAME varchar(64) NOT NULL,DEPARTMENT varchar(64),SALARY DECIMAL(8,2),BORN_DATE DATE,LAST_UPDATE DATETIME,EMAIL VARCHAR(255),PHONE VARCHAR(20),PRIMARY KEY (PERSONAL_ID));")
mycursor.execute("select * from myTable")
datas = []
id_list = []

def update_list():
    if not(data_list.size() == 0):
        for i in range(0,int(data_list.size())):
            data_list.delete(0,END)
    datas = mycursor.fetchall()
    data = 0
    for i in id_list:
        id_list.pop(0)
    for i in datas:
        id_list.append((data,i[0]))
        data += 1
        ttt = "ID: "
        if i[0] < 10:
            ttt += "  "
        if i[0] < 100:
            ttt += "  "
        ttt += str(i[0])+"  LAST UPDATE : "+str(i[5])+"       Name:"+str(i[1])
        data_list.insert("end",ttt)

def delete_employee():
    selection = data_list.curselection()[0]
    if not(selection):
        return
    for i,j in id_list:
        if selection == i:
            id = j
    mycursor.execute("DELETE FROM myTable WHERE PERSONAL_ID = %s", (id,))
    mydb.commit()
    mycursor.execute("select * from myTable")
    update_list()

def update_employee():
    selection = data_list.curselection()[0]
    if not(selection):
        return
    for i,j in id_list:
        if selection == i:
            id = j
    fname = name_entry.get()
    depart = department_entry.get()
    salary = salary_entry.get()
    born = date_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    sql = "UPDATE myTable SET FULL_NAME = %s, DEPARTMENT = %s, SALARY = %s, BORN_DATE = %s, LAST_UPDATE = NOW() , EMAIL = %s , PHONE = %s WHERE PERSONAL_ID = %s"
    val = (fname, depart, salary, born, email, phone, id)
    mycursor.nextset()
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.execute("select * from myTable")
    update_list()


def add_employee():
    data1 = name_entry.get()
    data2 = department_entry.get()
    data3 = date_entry.get()
    data4 = salary_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    if data1 and data2 and data3 and data4 and email and phone:
        pass
    else:
        return
    mycursor.execute('INSERT INTO MYTABLE (FULL_NAME, DEPARTMENT, BORN_DATE, SALARY, EMAIL, PHONE, LAST_UPDATE) VALUES (%s, %s, %s, %s, %s, %s, NOW())', (data1, data2, data3, data4, email, phone))
    mydb.commit()
    mycursor.execute("select * from mytable")
    update_list()

def show():
    mycursor.execute("select * from mytable")
    datas = mycursor.fetchall()
    selection = data_list.curselection()[0]
    temp = list()
    for i,j in id_list:
        if selection == i:
            id = j
    for i in datas:
        if id == i[0]:
            mydata = i
    name_entry.delete(0,END)
    name_entry.insert(0,mydata[1])
    date_entry.delete(0,END)
    date_entry.insert(0,mydata[4])
    department_entry.delete(0,END)
    department_entry.insert(0,mydata[2])
    salary_entry.delete(0,END)
    salary_entry.insert(0,mydata[3])
    email_entry.delete(0, END)
    email_entry.insert(0, mydata[6])
    phone_entry.delete(0, END)
    phone_entry.insert(0, mydata[7])
        
    mycursor.nextset()
    mycursor.execute("select * from mytable")
    mycursor.nextset()

    
root = Tk()
search = Entry(root,font=("Arial",25),width=32,bg="#1d1d1d",foreground="white")

def search_f():
    d = search.get()
    mycursor.execute("select * from myTable where FULL_NAME LIKE '"+str(d)+"%'")
    update_list()

search.bind("<KeyRelease>", lambda event: search_f())


root.geometry("800x900")
root.config(bg="#223322")
root.resizable(False,False)

photo = PhotoImage(file = 'icon.png')
root.wm_iconphoto(False, photo)

data_list = Listbox(root,foreground="white",font=("Arial",14),exportselection=False)
data_list.config(height=20,width=71,bg="#2b2b2b")
data_list.pack(pady=10)
data_list.bind("<<ListboxSelect>>", lambda event: show())

Label(root,text="SEARCH BY NAME",bg="#2b2b2b",foreground="white").pack()
search.pack(side=TOP)

if not(mycursor.fetchall()):
    mycursor.nextset()
    mycursor.execute('INSERT INTO MYTABLE (FULL_NAME, DEPARTMENT, BORN_DATE, SALARY, EMAIL, PHONE, LAST_UPDATE) VALUES (%s, %s, %s, %s, %s, %s, NOW())', ("Example Name", "Example Department", "2000-12-30", 1500, "example@example.com", "0555 555 55 55"))
    mydb.commit()
mycursor.execute("select * from mytable")
update_list()

frame1 = Frame(root)
frame1.pack(pady=10)
name = Entry()

button_delete= Button(frame1,text="DELETE",font=("Arial",25),command=delete_employee)
button_update = Button(frame1,text="UPDATE",font=("Arial",25),command=update_employee)
button_add = Button(frame1,text="ADD",font=("Arial",25),command=add_employee)
button_delete.grid(column=0,row=0)
button_update.grid(column=1,row=0)
button_add.grid(column=3,row=0)

name_label = Label(frame1, text="Full Name:",font=("Arial",20))
name_label.grid(row=1, column=0)

name_entry = Entry(frame1,font=("Arial",25))
name_entry.grid(row=1, column=1)

date_label = Label(frame1, text="Born Date:",font=("Arial",20))
date_label.grid(row=2, column=0)

date_entry = Entry(frame1,font=("Arial",25))
date_entry.grid(row=2, column=1)

salary_label = Label(frame1, text="Salary:",font=("Arial",20))
salary_label.grid(row=3, column=0)

salary_entry = Entry(frame1,font=("Arial",25))
salary_entry.grid(row=3, column=1)

department_label = Label(frame1, text="Department:",font=("Arial",20))
department_label.grid(row=4, column=0)

department_entry = Entry(frame1,font=("Arial",25))
department_entry.grid(row=4, column=1)

phone_label = Label(frame1, text="Phone:",font=("Arial",20))
phone_label.grid(row=5, column=0)

phone_entry = Entry(frame1,font=("Arial",25))
phone_entry.grid(row=5, column=1)

email_label = Label(frame1, text="Email:",font=("Arial",20))
email_label.grid(row=6, column=0)

email_entry = Entry(frame1,font=("Arial",25))
email_entry.grid(row=6, column=1)

root.mainloop()