from tkinter import Tk,Label,Frame,Entry,Button,messagebox,filedialog
from tkinter.ttk import Combobox
import sqlite3
import time
import os,shutil
from PIL import Image,ImageTk
import random
import project_tables as pt
import project_mail
import captchageneratormodule as capc
from tkinter import ttk

#-----image collection--------
#left side images and index
images_coll=['images/banklogo.png','images/bankblue.png','images/banksilver.png','images/bankworker.png']
current_index=0
#right side images and index
images_coll2=['images/bankblue.png','images/banksilver.png','images/bankworker.png','images/banklogo.png']
current_index2=0

#----tkinter----------------------
root=Tk()                       #creating tk object and naming it root
root.state("zoomed")            #zoomed in full screen window
root.config(bg="navy")   #setting color of program window
root.title("Bank project")      #setting the title of program

root.resizable(width=False,height=False)  #minimize button removed

#functions
#create captcha using random library(combination of random int into char, and random int)
def generate_captcha():
    captcha=[] #captcha list to store captcha
    for i in range(3):
        #generates character after converting random int into char
        c=chr(random.randint(65,90))
        #appends the character generated into captcha list
        captcha.append(c)
        #generatese random int between 0 and 9
        n=random.randint(0,9)
        #appends the int into captcha list after converting it to string
        captcha.append(str(n))
        #shuffles the captcha generated
        random.shuffle(captcha)
        
    #joins captcha in string format
    captcha=" ".join(captcha)
    
    return captcha
#generates new captcha again when refresh button is clicked
def refresh_captcha():
    #calls generate captcha function and stores its value in variable
    new_cap=generate_captcha()
    #changes the captcha label text value and inserts the variable
    captcha_label.config(text=new_cap)

#title page of the program 
title_lbl=Label(root,text="Banking Automation",font=('helvetica',34,'underline'),bg='navy',fg='whitesmoke')
title_lbl.pack()
#time display (displays current time and date)
today_lbl=Label(root,text=time.strftime("%A,%d %B %Y"),font=('helvetica',20),bg='navy',fg='whitesmoke')
today_lbl.pack(pady=10)
#left logo image changing
img = Image.open(images_coll[current_index]).resize((300, 180))
bitmapImageTk = ImageTk.PhotoImage(img, master=root)
logo_lbl = Label(root, image=bitmapImageTk)
logo_lbl.image = bitmapImageTk
logo_lbl.place(relx=0, rely=0)

#second image on right
img= Image.open(images_coll[current_index]).resize((300, 180))
bitmapImageTk = ImageTk.PhotoImage(img, master=root)
logo_lbl2 = Label(root, image=bitmapImageTk)
logo_lbl2.image = bitmapImageTk
logo_lbl2.place(relx=0.8, rely=0)


#footer (displayed at the bottom of the page)
footer_lbl=Label(root,text="Developed by: Nitish",font=('helvetica',20),bg="navy",fg='white')
footer_lbl.pack(side='bottom',pady=10)

#function to change image regularly on header
def change_image():
    #global var to change the image in left label
    global current_index, bitmapImageTk

    current_index = (current_index + 1) % len(images_coll)
    #rotates the index from beginning to end
    try:
        new_img = Image.open(images_coll[current_index]).resize((300, 180))
        bitmapImageTk = ImageTk.PhotoImage(new_img, master=root)
        logo_lbl.config(image=bitmapImageTk)
        logo_lbl.image = bitmapImageTk
        
    except Exception as e:
        print("Error loading image:", e)

    root.after(2000, change_image)


change_image()#first image change function call
#second function to change right side images
def change_image2():
    #gloabal var to change images in right side label
    global current_index2, bitmapImageTk

    current_index2 = (current_index2 + 1) % len(images_coll2)
    #rotates the index from beginning to end
    try:
        new_img = Image.open(images_coll2[current_index2]).resize((300, 180))
        bitmapImageTk = ImageTk.PhotoImage(new_img, master=root)
        logo_lbl2.config(image=bitmapImageTk)
        logo_lbl2.image = bitmapImageTk
        
    except Exception as e:
        print("Error loading image:", e)

    root.after(2000, change_image2)
change_image2()  # second image change function call
#code inside functions

#--------------Main Screen Function-----------------
def main_screen():

    #hide password/Show password
    def toggle_password():
        if pass_entry.cget('show')=='':
            pass_entry.config(show='*')
            toggle_btn.config(text='show password')
        else:
            pass_entry.config(show='')
            toggle_btn.config(text='Hide')
    
    #login function
    
    def login():
        #getting data from user
        uacn=Accn_number_entry.get()
        upass=pass_entry.get()
        ucap=cap_entry.get()
        utype=user_combo.get()
        actual_captcha=captcha_label.cget('text')
        actual_captcha=actual_captcha.replace(" ","")

        if utype=="Admin":
            if uacn=="0" and upass=="admin":
                if ucap==actual_captcha:
                    messagebox.showinfo("Welcome")
                    frm.destroy()
                    admin_screen()
                else:
                    messagebox.showerror('Login',"Invalid captcha")
            else:
                messagebox.showerror('Login',"invalid Login Accn/Pass/Type")
        elif utype=='User':
            if ucap==actual_captcha:
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query="select * from accounts where accounts_no=? and accounts_pass=?"
                curobj.execute(query,(uacn,upass))

                tup=curobj.fetchone()
                conobj.close()
                if tup==None:
                    messagebox.showerror("user login","Invalid credentials")
                else:
                    frm.destroy()
                    user_screen(uacn)

            else:
                messagebox.showerror("Login","invalid captcha")          
        else:
            messagebox.showerror("login","Kindly select valid user type")
    #forgot password function
    def forgot():
        frm.destroy()
        forgot_screen()

    

    #creating a global var to update captcha using refresh button
    global captcha_label  #needed to  update the text later
    #------frame inside main screen----------
    frm=Frame(root)    #create a Frame object called frm with root
    frm.configure(bg='#3B82F6') #sets frame color
    frm.place(relx=0,rely=.2,relwidth=1,relheight=.74) #sets frame position
    
    #--------user type enter  row------------
    #user type text label
    label_usertype=Label(frm,text="User Type",font=('arial',25),bg='#3B82F6',borderwidth=2, relief="raised")
    label_usertype.place(relx=0.28,rely=0.05)
    #combobox to let user select one option out of two
    user_combo=Combobox(frm,values=['Admin','User','---------Select------------'],font=('Arial',25),state='readonly')
    #sets the default option at index value 2
    user_combo.current(2)
    user_combo.place(relx=0.4,rely=0.05)

    #-----------Account_number row------------

    #account number text label
    Accn_number_label=Label(frm,text="AC Num",font=('arial',25),bg='#3B82F6',borderwidth=2, relief="raised")
    Accn_number_label.place(relx=0.28,rely=0.2)
    #takes user account number as input
    Accn_number_entry=Entry(frm,font=('Arial',25),bd=5,bg='lightblue')
    Accn_number_entry.place(relx=0.4,rely=0.2)
    #keeps the cursor on account number by default
    Accn_number_entry.focus()

    #-------------password row-----------
    #password label 
    pass_label=Label(frm,text="Password",font=('arial',25),bg='#3B82F6',borderwidth=2, relief="raised")
    pass_label.place(relx=0.28,rely=0.3)
    #place to enter password 
    pass_entry=Entry(frm,font=('Arial',25),bd=5,show='*',bg='lightblue')
    pass_entry.place(relx=0.4,rely=0.3)
    toggle_btn=Button(root,text='show password',command=toggle_password,width=12)
    toggle_btn.place(relx=0.58,rely=0.49)
    #----------captcha row------

    #captcha label 
    cap_text_label=Label(frm,text="Captcha",font=('arial',25),bg='#3B82F6',borderwidth=2, relief="raised")
    cap_text_label.place(relx=0.3,rely=0.6)
    #actual 6 character captcha
    captcha_label=Label(frm,text=generate_captcha(),font=('arial',25))
    captcha_label.place(relx=0.4,rely=0.47)
    #takes input from user to match captcha
    cap_entry=Entry(frm,font=('Arial',25),bd=5,bg='lightblue')
    cap_entry.place(relx=0.4,rely=0.6)


    #refresh captcha button (uses refresh captcha function)
    captcha_btn=Button(frm,text='Refresh',font=('arial',17),command=refresh_captcha)
    captcha_btn.place(relx=0.53,rely=0.47)

    #login button(button for login)
    login_btn=Button(frm,text="Login",font=('arial',24),command=login)
    login_btn.place(relx=0.42,rely=0.72)
    #reset button(for password reset)
    reset_btn=Button(frm,text="Reset",font=('arial',24),command=main_screen)
    reset_btn.place(relx=0.5,rely=0.72)
    #forgot password button(button for forgot password)
    forgot_pass_btn=Button(frm,text="Forgot Password",font=('arial',24),command=forgot_screen)
    forgot_pass_btn.place(relx=0.41,rely=0.85)


#----------------------Admin module-----------------


def admin_screen():

    #admin font
    admin_font=('arial',15)
    #font inside admin panel buttons
    panel_font=('helvetica',20,'bold')
    #---------functions-------------
    #opens account frame
    def open_acn():
        #-----------Admin database function---------------
        def open_acn_db():
            uname=name_entry.get()
            uemail=email_entry.get()
            umob=mobile_entry.get()
            ugender=gender_entry.get()
            ubal=0.0
            uopendate=time.strftime("%A,%d %B %Y")
            upass=generate_captcha().replace(" ",'')

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='''insert into accounts 
                values  (null,?,?,?,?,?,?,?)
                '''
            curobj.execute(query,(uname,upass,uemail,umob,ugender,uopendate,ubal)) 

            conobj.commit()
            conobj.close()
            # After admin submits the form
            #import emailsystem module
            
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
        
            #getting user id from accounts table in db
            curobj.execute(f"select accounts_no from accounts where accounts_email=?",(uemail,))
            uacno=curobj.fetchone()[0]
            #getting user password from the accounts table in db
            curobj.execute(f"select accounts_pass from accounts where accounts_email=?",(uemail,))
            epass=curobj.fetchone()[0]
            conobj.close()

            try:
                #calling the function inside emailsystem module 
                project_mail.send_mail_for_openacn(uemail,uacno,uname,upass,uopendate)
                msg=f"Account opened with ACN {uacno} and mail sent to {uemail},kindly check spam also"
                messagebox.showinfo('Open Account',msg)
            except Exception as msg:
                messagebox.showerror("Open Account",msg)
            
            #display message after account creation
            messagebox.showinfo("Open Account","Account opened successfully")
            print("acn created")
        
        def reset():
            name_entry.delete(0,"end")
            email_entry.delete(0,"end")
            mobile_entry.delete(0,"end")
            gender_entry.current(3)
            name_entry.focus()


        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.15,rely=.2,relwidth=.7,relheight=.6)

        title_lbl=Label(ifrm,text="This is Open Account screen",bg='white',font=panel_font,fg='purple')
        title_lbl.pack()

        #account form
        name_Label=Label(ifrm,text="Name",font=panel_font)
        name_Label.place(relx=0.1,rely=0.2)

        name_entry=Entry(ifrm,font=panel_font,bd=5,bg='lightblue')
        name_entry.place(relx=0.2,rely=0.2)
        
        email_Label=Label(ifrm,text="Email",font=panel_font)
        email_Label.place(relx=0.1,rely=0.4)
        
        email_entry=Entry(ifrm,font=panel_font,bd=5,bg='lightblue')
        email_entry.place(relx=0.2,rely=0.4)

        mobile_Label=Label(ifrm,text="Mobile",font=panel_font)
        mobile_Label.place(relx=0.5,rely=0.2)

        mobile_entry=Entry(ifrm,font=panel_font,bd=5,bg='lightblue')
        mobile_entry.place(relx=0.6,rely=0.2)
        
        gender_Label=Label(ifrm,text="Gender",font=panel_font)
        gender_Label.place(relx=0.5,rely=0.4)
        
        gender_entry=Combobox(ifrm,values=['male','female','others','---------Select------------'],font=panel_font,state='readonly')
        gender_entry.current(3)
        gender_entry.place(relx=0.6,rely=0.4)
        
        open_acc_btn=Button(ifrm,text='Open Account',font=('arial',18),bg='lightgreen',command=open_acn_db)
        open_acc_btn.place(relx=0.5,rely=0.65)

        reset_btn=Button(ifrm,text='Reset',font=('arial',18),bg='whitesmoke',command=reset)
        reset_btn.place(relx=0.7,rely=0.65)

    #----------opens  account delete frame-----------
    def delete_acn():
        #otp in delete acn
        def send_otp():
            uacn=Acn_entry.get()
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select * from accounts where accounts_no=?'
            curobj.execute(query,(uacn,))

            tup=curobj.fetchone()
            conobj.close()
            if tup==None:
                messagebox.showerror("Delete account",'Record not found')
            else:
                otp=str(random.randint(1000,9999))
                project_mail.send_otp_del(tup[3],tup[1],otp)
                messagebox.showinfo("Delete account","Otp sent to registered mail")

                otp_entry=Entry(ifrm,font=panel_font)
                otp_entry.place(relx=.4,rely=.7)
                def verify():
                    uotp=otp_entry.get()
                    if uotp==otp:
                        resp=messagebox.askyesno("Delete Account",f'Do you want to delete this account?')
                        if not resp:
                            frm.destroy()
                            admin_screen()
                            return
                        conobj=sqlite3.connect(database='bank.sqlite')
                        curobj=conobj.cursor()
                        query='delete from accounts where accounts_no=?'
                        curobj.execute(query,(uacn,))
                        conobj.commit()
                        conobj.close()
                        messagebox.showinfo("Delete Account","Account deleted")
                        frm.destroy()
                        admin_screen()
                    else:
                        messagebox.showerror("Delete Account","Incorrect OTP")
                verify_btn=Button(ifrm,text='Verify',font=panel_font,command=verify)
                verify_btn.place(relx=.7,rely=.7)
        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.15,rely=.2,relwidth=.7,relheight=.6)

        title_lbl=Label(ifrm,text="This is Delete Account screen",bg='white',font=panel_font,fg='purple')
        title_lbl.pack()

        Acn_Label=Label(ifrm,text="Acn",font=panel_font,width=5)
        Acn_Label.place(relx=0.3,rely=0.3)

        Acn_entry=Entry(ifrm,font=panel_font,bd=5,bg='lightblue')
        Acn_entry.place(relx=0.4,rely=0.3)

        send_otp_btn=Button(ifrm,text='Send Otp',font=('arial',15),command=send_otp)
        send_otp_btn.place(relx=0.4,rely=0.5)
    #open account details view frame
    def view_acn():

        #functions
        def view_details():
            uacn=Acn_entry.get()
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select * from accounts where accounts_no=?'
            curobj.execute(query,(uacn,))

            tup=curobj.fetchone()
            conobj.close()
            if tup==None:
                messagebox.showerror("View account",'Record not found')
            else:
                ifrm.destroy()
                gen_frame()
                name_label_x=.3
                tup_label_x=.5
                font_view=('arial',20)

                acndetails_label=Label(ifrm,text="Account Details",font=('arial',25))
                acndetails_label.place(relx=name_label_x,rely=.2)

                name_text_label=Label(ifrm,text="Name:",font=font_view)
                name_text_label.place(relx=name_label_x,rely=.4)
                name_label=Label(ifrm,text=tup[1],font=font_view)
                name_label.place(relx=tup_label_x,rely=.4)

                email_text_label=Label(ifrm,text="Email:",font=font_view)
                email_text_label.place(relx=name_label_x,rely=.5)
                email_label=Label(ifrm,text=tup[3],font=font_view)
                email_label.place(relx=tup_label_x,rely=.5)
                
                mobile_text_label=Label(ifrm,text="Mobile:",font=font_view)
                mobile_text_label.place(relx=name_label_x,rely=.6)
                mobile_label=Label(ifrm,text=tup[4],font=font_view)
                mobile_label.place(relx=tup_label_x,rely=.6)
                
                gender_text_label=Label(ifrm,text="Gender:",font=font_view)
                gender_text_label.place(relx=name_label_x,rely=.7)
                gender_label=Label(ifrm,text=tup[5],font=font_view)
                gender_label.place(relx=tup_label_x,rely=.7)

                acnopen_text_label=Label(ifrm,text="Acn OpenDate:",font=font_view)
                acnopen_text_label.place(relx=name_label_x,rely=.8)
                acnopen_label=Label(ifrm,text=tup[6],font=font_view)
                acnopen_label.place(relx=tup_label_x,rely=.8)

                #back button
                back_btn=Button(ifrm,text="back",font=('arial',15),command=view_acn)
                back_btn.place(relx=.8,rely=.2)
        #frame
        def gen_frame():
            global ifrm
            ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
            ifrm.configure(bg='white')
            ifrm.place(relx=.15,rely=.2,relwidth=.7,relheight=.6)
        gen_frame()
        title_lbl=Label(ifrm,text="This is View account screen",bg='white',font=panel_font,fg='purple')
        title_lbl.pack()

        Acn_Label=Label(ifrm,text="Acn",font=panel_font,width=5)
        Acn_Label.place(relx=0.3,rely=0.2)

        Acn_entry=Entry(ifrm,font=panel_font,bd=5,bg='lightblue')
        Acn_entry.place(relx=0.4,rely=0.2)

        view_btn=Button(ifrm,text='View',font=('arial',15),command=view_details)
        view_btn.place(relx=0.7,rely=0.2)
    #logs out of the admin account
    def logout():
        resp=messagebox.askyesno("logout","Do you want to logout?")
        if resp:
            frm.destroy()#destroys the current frame
            main_screen()#loads back to main screen with login signup
    
    #----------frame inside admin screen---------------
    frm=Frame(root)    #create a Frame object called frm with root
    frm.configure(bg='#3B82F6') #sets frame color
    frm.place(relx=0,rely=.2,relwidth=1,relheight=.74) 

    welcome_lbl=Label(frm,text="welcome,Admin",font=('helvetica',20),bg='navy',fg='white')
    welcome_lbl.place(relx=0.1,rely=0.03)

    openacc_btn=Button(frm,text='Open Account',font=admin_font,bg='yellow',command=open_acn)
    openacc_btn.place(relx=.3,rely=0.03)

    deleteacc_btn=Button(frm,text='Delete Account',font=admin_font,bg='orange',command=delete_acn)
    deleteacc_btn.place(relx=.4,rely=0.03)

    viewacc_btn=Button(frm,text='View Account',font=admin_font,bg='lightgreen',command=view_acn)
    viewacc_btn.place(relx=.5,rely=0.03)

    logout_btn=Button(frm,text='Logout',font=admin_font,bg='red',command=logout)
    logout_btn.place(relx=.6,rely=0.03)
#-----------forgot password screen-------------------
def forgot_screen():
    
    #functions
    def back():
        frm.destroy()
        main_screen()

    #captcha refresh
    def cap_refresh(): #refreshes the forgot screen captcha
        global forgot_captcha
        forgot_captcha="".join(capc.refresh_captcha())
        captcha_Label.config(text=forgot_captcha)

    #function for sending otp
    def send_otp():
        uacn=Acn_entry.get()
        uemail=email_entry.get()
        ucaptcha=captcha_entry.get()
        if ucaptcha!=forgot_captcha.replace(" ",""):
            messagebox.showerror('forgot password',"invalid captcha")
            return 
        #email and uacn authentication
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query="select * from accounts where accounts_no=? and accounts_email=?"
        curobj.execute(query,(uacn,uemail))

        tup=curobj.fetchone()
        conobj.close() #connection object closed
        if tup==None:
            messagebox.showerror("Forgot password","Record not found")
        else:
            #otp generation
            otp=str(random.randint(1000,9999))
            project_mail.send_otp(uemail,tup[1],otp)
            messagebox.showinfo("Forgot pass",'Otp sent to the registered email id')

            #taking otp from user
            otp_entry=Entry(frm,font=("arial",20),bd=5)
            otp_entry.place(relx=.44,rely=.5)
            #verifying function for otp
            def verify():
                uotp=otp_entry.get()
                if otp==uotp:
                    messagebox.showinfo("Forgot password",f"your pass={tup[2]}")
                else:
                    messagebox.showerror("Forgot password","Incorrect OTP")

            verify_btn=Button(frm,command=verify,text="verify",font=('Arial',15,'bold'),bd=5)
            verify_btn.place(relx=.59,rely=.6)                    
                

    #frame
    frm=Frame(root)    #create a Frame object called frm with root
    frm.configure(bg='#3B82F6') #sets frame color
    frm.place(relx=0,rely=.2,relwidth=1,relheight=.74) #sets frame position
    #font variable
    main_font=('arial',20,'bold')
    back_btn=Button(frm,text="back",font=main_font,command=back)
    back_btn.place(relx=.9,rely=.04)
    

    #user interface of forgot screen
    Acn_Label=Label(frm,text="ACN",font=main_font)
    Acn_Label.place(relx=0.34,rely=0.2)

    Acn_entry=Entry(frm,font=main_font,bd=5,bg='lightblue')
    Acn_entry.place(relx=0.44,rely=0.2)

    email_Label=Label(frm,text="Email",font=main_font)
    email_Label.place(relx=0.34,rely=0.3)
    
    email_entry=Entry(frm,font=main_font,bd=5,bg='lightblue')
    email_entry.place(relx=0.44,rely=0.3)
    #captcha label
    forgot_captcha="".join(capc.generate_captcha())
    captcha_Label=Label(frm,text=forgot_captcha,font=main_font)
    captcha_Label.place(relx=0.5,rely=0.5)
    #captcha text lab
    captchatext_Label=Label(frm,text="Captcha",font=main_font)
    captchatext_Label.place(relx=0.34,rely=0.5)
    #refresh button


    catpcha_refresh_btn=Button(frm,text="refresh",command=cap_refresh,font=('arial',15))
    catpcha_refresh_btn.place(relx=.63,rely=.5)

    captcha_entry=Entry(frm,font=main_font,bd=5,bg='lightblue')
    captcha_entry.place(relx=0.44,rely=0.6)

    Send_btn=Button(frm,text='send otp',font=main_font,bg='green',command=send_otp)
    Send_btn.place(relx=0.44,rely=0.7)

    reset_btn=Button(frm,text='reset',font=main_font,bg='green')
    reset_btn.place(relx=0.56,rely=0.7)

    #Submit_btn=Button(frm,text='submit',font=main_font,bg='green')
    #Submit_btn.place(relx=0.5,rely=0.7)


#------------user module------------------
def user_screen(uacn=None):
    #functions 
    #ROUNDING OFF THE AMOUNTS IN STMTS TABLE
    def round_upstmts():
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        curobj.execute("update stmts set stmts_update_bal=round(stmts_update_bal,2)")
        conobj.commit()
        conobj.close()
    def round_accounts():
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        curobj.execute("update accounts set accounts_bal=round(accounts_bal,2)")
        conobj.commit()
        conobj.close()
    
    #function to get details of user
    def get_details():
        conobj=sqlite3.connect("bank.sqlite")
        curobj=conobj.cursor()

        query="select * from accounts where accounts_no=?"
        curobj.execute(query,(uacn,))
        tup=curobj.fetchone()
        conobj.close()
        return tup
    #update picture

    def update_picture():
        path=filedialog.askopenfilename()
        if not path:
             messagebox.showerror("Error", "No file selected.")
             return
        shutil.copy(path,f"images/{uacn}.png")
        
        profile_img=Image.open(f"images/{uacn}.png").resize((150,120))
        bitmap_profile_img=ImageTk.PhotoImage(profile_img,master=root)
        logo_lbl.image=bitmap_profile_img
        logo_lbl.configure(image=bitmap_profile_img  )


    def logout():
        resp=messagebox.showerror("logout","Do you want to logout?")
        if resp:
            frm.destroy()#destroys the current frame
            main_screen()#loads back to main screen with login signup
    
                 
    def check_details():
        
        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.15,rely=.2,relwidth=.8,relheight=.7)

        title_lbl=Label(ifrm,text="This is Check Details screen",bg='white',font=panel_font,fg='purple')
        title_lbl.pack()

        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query="select * from accounts where accounts_no=?"
        curobj.execute(query,(uacn))
        tup=curobj.fetchone()
        conobj.close()
        if tup==None:
            messagebox.showerror("View account",'Record not found')
        else:
            name_label_x=.3
            tup_label_x=.5
            font_view=('arial',20)

            acndetails_label=Label(ifrm,text="Account Details",font=('arial',25))
            acndetails_label.place(relx=name_label_x,rely=.2)

            acn_text_label=Label(ifrm,text="ACN:",font=font_view)
            acn_text_label.place(relx=name_label_x,rely=.4)
            acn_label=Label(ifrm,text=tup[0],font=font_view)
            acn_label.place(relx=tup_label_x,rely=.4)

            bal_text_label=Label(ifrm,text="Available balance:",font=font_view)
            bal_text_label.place(relx=name_label_x,rely=.5)
            bal_label=Label(ifrm,text=round(tup[7],2),font=font_view)
            bal_label.place(relx=tup_label_x,rely=.5)

            email_text_label=Label(ifrm,text="Email:",font=font_view)
            email_text_label.place(relx=name_label_x,rely=.6)
            email_label=Label(ifrm,text=tup[3],font=font_view)
            email_label.place(relx=tup_label_x,rely=.6)
                
            mobile_text_label=Label(ifrm,text="Mobile:",font=font_view)
            mobile_text_label.place(relx=name_label_x,rely=.7)
            mobile_label=Label(ifrm,text=tup[4],font=font_view)
            mobile_label.place(relx=tup_label_x,rely=.7)
                
            

            acnopen_text_label=Label(ifrm,text="Acn OpenDate:",font=font_view)
            acnopen_text_label.place(relx=name_label_x,rely=.8)
            acnopen_label=Label(ifrm,text=tup[6],font=font_view)
            acnopen_label.place(relx=tup_label_x,rely=.8)
        
        

    def deposit():
        def deposit_fn():
            uamt=float(amount_entry.get().strip())
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query="update accounts set accounts_bal=accounts_bal+? where accounts_no=?"
            curobj.execute(query,(uamt,uacn))
            conobj.commit()
            conobj.close()

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query="select accounts_bal from accounts where accounts_no=?"
            curobj.execute(query,(uacn,))
            ubal=curobj.fetchone()[0]
            conobj.close()

            time_string=str(time.time())
            utxnid='txn'+time_string[:time_string.index('.')]
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query="insert into stmts values(?,?,?,?,?,?)"
            curobj.execute(query,(uacn,uamt,"CR.",time.strftime('%d-%m-%Y %r'),ubal,utxnid))
            conobj.commit()
            conobj.close()
            
            messagebox.showinfo("Deposit",f"{uamt} Amount Deposited")
            frm.destroy()
            user_screen(uacn)



        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.15,rely=.2,relwidth=.8,relheight=.7)

        title_lbl=Label(ifrm,text="This is Deposit screen",bg='white',font=panel_font,fg='purple')
        title_lbl.pack()

        amount_text_label=Label(ifrm,text="Amount",font=('arial',20))
        amount_text_label.place(relx=.2,rely=.2)
        amount_entry=Entry(ifrm,text='amount_label',font=('arial',20),border=5)
        amount_entry.place(relx=.4,rely=.2)

        deposit_btn=Button(ifrm,text='Deposit',font=('arial',15,'bold'),bg='green',command=deposit_fn)
        deposit_btn.place(relx=.55,rely=.4)
        #deposit function
        #deposit buttons

    

    def withdraw():

        def withdraw_fn():
            withdraw_amt=float(withdraw_entry.get().strip())
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query="select accounts_bal from accounts where accounts_no=?"
            curobj.execute(query,(uacn,))
            ubal=curobj.fetchone()[0]
            conobj.close()

            if ubal>=withdraw_amt:
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query="update accounts set accounts_bal=accounts_bal-? where accounts_no=?"
                curobj.execute(query,(withdraw_amt,uacn))
                conobj.commit()
                conobj.close()

                time_string=str(time.time())
                utxnid='txn'+time_string[:time_string.index('.')]
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query="insert into stmts values(?,?,?,?,?,?)"
                curobj.execute(query,(uacn,withdraw_amt,'DB',time.strftime("%d-%m-%Y %r"),ubal-withdraw_amt,utxnid))
                conobj.commit()
                conobj.close()

                messagebox.showinfo("withdraw",f"{withdraw_amt} amount withdrawn")
                frm.destroy()
                user_screen(uacn)
            else:
                messagebox.showerror("Withdraw","Insufficient Balance")
        
       
        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.15,rely=.2,relwidth=.8,relheight=.7)

        title_lbl=Label(ifrm,text="This is Withdraw screen",bg='white',font=panel_font,fg='purple')
        title_lbl.pack()

        withdraw_text_label=Label(ifrm,text="Withdraw",font=('arial',20))
        withdraw_text_label.place(relx=.2,rely=.2)
        withdraw_entry=Entry(ifrm,text='withdraw amount',font=('arial',20),border=5)
        withdraw_entry.place(relx=.4,rely=.2)

        withdraw_btn=Button(ifrm,text='Withdraw',font=('arial',15,'bold'),bg='green',command=withdraw_fn)
        withdraw_btn.place(relx=.55,rely=.4)
        

        

    def update():
        
        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.15,rely=.2,relwidth=.8,relheight=.7)


        title_lbl=Label(ifrm,text="This is Update screen",bg='white',font=panel_font,fg='purple')
        title_lbl.pack()

        #function to update user details
        def update_db():
            uname=name_entry.get()
            upass=pass_entry.get()
            uemail=email_entry.get()
            umob=mobile_entry.get()

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()

            query="update accounts set accounts_name=?,accounts_pass=?,accounts_email=?,accounts_mob=?  where accounts_no=?"
            curobj.execute(query,(uname,upass,uemail,umob,uacn))
            conobj.commit()
            conobj.close()

            messagebox.showinfo("Update Details","Profile Updated")
            frm.destroy()
            user_screen(uacn)
        #database for user details fetching
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        curobj.execute('select * from accounts where accounts_no=?',(uacn,))
        tup=curobj.fetchone()
        conobj.close()
           

        #account form
        name_Label=Label(ifrm,text="Name",font=panel_font)
        name_Label.place(relx=0.1,rely=0.2)

        name_entry=Entry(ifrm,font=panel_font,bd=5,bg='lightblue')
        name_entry.place(relx=0.2,rely=0.2)
        name_entry.insert(0,tup[1])
        
        email_Label=Label(ifrm,text="Email",font=panel_font)
        email_Label.place(relx=0.1,rely=0.4)
        
        email_entry=Entry(ifrm,font=panel_font,bd=5,bg='lightblue')
        email_entry.place(relx=0.2,rely=0.4)
        email_entry.insert(0,tup[3])

        mobile_Label=Label(ifrm,text="Mobile",font=panel_font)
        mobile_Label.place(relx=0.5,rely=0.2)

        mobile_entry=Entry(ifrm,font=panel_font,bd=5,bg='lightblue')
        mobile_entry.place(relx=0.65,rely=0.2)
        mobile_entry.insert(0,tup[4])

        pass_Label=Label(ifrm,text="Password",font=panel_font)
        pass_Label.place(relx=0.5,rely=0.4)
        
        pass_entry=Entry(ifrm,font=panel_font,bd=5,bg='lightblue')
        pass_entry.place(relx=0.65,rely=0.4)
        pass_entry.insert(0,tup[2])
        
        
        
        update_btn=Button(ifrm,text='Update',font=('arial',18),bg='lightgreen',command=update_db)
        update_btn.place(relx=0.5,rely=0.65)
    
        

    def transfer():
        def transfer_fn():
            uamt=float(transfer_entry.get().strip())
            toacn=transferto_entry.get()

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query="select * from accounts where accounts_no=?"
            curobj.execute(query,(toacn,))
            to_tup=curobj.fetchone()
            conobj.close()
            if to_tup==None:
                messagebox.showerror("Transfer","Account doesn't exist")
                return
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query="select accounts_bal from accounts where accounts_no=?"
            curobj.execute(query,(uacn,))
            ubal=curobj.fetchone()[0]
            conobj.close()

            if ubal>=uamt:
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query_deduct='update accounts set accounts_bal=accounts_bal-? where accounts_no=?'
                query_credit='update accounts set accounts_bal=accounts_bal+? where accounts_no=?'
                
                curobj.execute(query_deduct,(uamt,uacn))
                curobj.execute(query_credit,(uamt,toacn))

                conobj.commit()
                conobj.close()

                time_string=str(time.time())
                utxniddb='txn_db'+time_string[:time_string.index('.')]
                utxnidcr='txn_cr'+time_string[:time_string.index('.')]

                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()

                query1='insert into stmts values(?,?,?,?,?,?)'
                
                curobj.execute(query1,(uacn,uamt,'DB.',time.strftime("%d-%m-%Y %r"),ubal-uamt,utxniddb))
                curobj.execute(query1,(toacn,uamt,'CR.',time.strftime("%d-%m-%Y %r"),ubal+uamt,utxnidcr))

                conobj.commit()
                conobj.close()

                messagebox.showinfo("Transfer",f"{uamt} Amount Transferred")
                frm.destroy()
                user_screen(uacn)
            else:
                messagebox.showerror("Transfer",f"Insufficient Balance {ubal}")


        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.15,rely=.2,relwidth=.8,relheight=.7)

        title_lbl=Label(ifrm,text="This is Transfer screen",bg='white',font=panel_font,fg='purple')
        title_lbl.pack()

        transfer_text_label=Label(ifrm,text="Amount",font=('arial',20))
        transfer_text_label.place(relx=.2,rely=.2)
        transfer_entry=Entry(ifrm,font=('arial',20),border=5)
        transfer_entry.place(relx=.4,rely=.2)

        transferto_text_label=Label(ifrm,text="To Acn",font=('arial',20))
        transferto_text_label.place(relx=.2,rely=.4)
        transferto_entry=Entry(ifrm,font=('arial',20),border=5)
        transferto_entry.place(relx=.4,rely=.4)

        transfer_btn=Button(ifrm,text='Transfer',font=('arial',15,'bold'),bg='green',command=transfer_fn)
        transfer_btn.place(relx=.6,rely=.7)
        
        
    
    def history():
        
        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.15,rely=.2,relwidth=.8,relheight=.7)

        title_lbl=Label(ifrm,text="This is History screen",bg='white',font=panel_font,fg='purple')
        title_lbl.pack()
        
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 15),rowheight=40)           # Row font
        style.configure("Treeview.Heading", font=("Arial", 20, "bold"))  # Header font
        table_headers=("Txn ID","Amount","Txn type","Updated Bal","Date")
        tree=ttk.Treeview(ifrm,columns=table_headers,show='headings')

        # Define tag styles for zebra striping
        tree.tag_configure("evenrow", background="#f2f2f2")  # Light gray
        tree.tag_configure("oddrow", background="white")     # White

        for col in table_headers:
            tree.heading(col,text=col)
            tree.column(col,anchor='center',width=200)

        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query="select stmts_txnid,stmts_amt,stmts_type,stmts_update_bal,stmts_date from stmts where stmts_acn=?"
        curobj.execute(query,(uacn,))
        data=curobj.fetchall()
        for index,row in enumerate(data):
            tag='evenrow' if index%2==0 else 'oddrow'
            tree.insert("","end",values=row,tags=(tag,))
        tree.pack(pady=10)
        conobj.close()                          
        
        
    #admin font
    admin_font=('arial',20)
    #font inside admin panel buttons
    panel_font=('helvetica',20,'bold')


    frm=Frame(root)    #create a Frame object called frm with root
    frm.configure(bg='#3B82F6') #sets frame color
    frm.place(relx=0,rely=.2,relwidth=1,relheight=.74) 

    round_upstmts()
    round_accounts()

    #image

    if os.path.exists(f"images/{uacn}.png"):
        path=f"images/{uacn}.png"
    else:
        path="images/userlogo.png"
    img=Image.open(path).resize((150,120))
    #converts the image into bitmap format
    bitmapImageTk3=ImageTk.PhotoImage(img,master=frm)
    #create label to display bitmap image 
    logo_lbl=Label(frm,image=bitmapImageTk3)
    logo_lbl.image = bitmapImageTk3
    logo_lbl.place(relx=0.01,rely=0.03)


    #labels
    welcome_lbl=Label(frm,text=F"welcome,{get_details()[1]}...",font=admin_font,bg='navy',fg='white')
    welcome_lbl.place(relx=0.2,rely=0.03)


    logout_btn=Button(frm,text='Logout',font=admin_font,bg='red',command=logout)
    logout_btn.place(relx=.8,rely=0.03)

    updateimg_btn=Button(frm,text='Update image',font=admin_font,bg='lightblue',width=10,command=update_picture)
    updateimg_btn.place(relx=.01,rely=0.2)

    check_btn=Button(frm,text='Check details',font=admin_font,bg='whitesmoke',width=10,command=check_details)
    check_btn.place(relx=.01,rely=0.3)

    deposit_btn=Button(frm,text='Deposit',font=admin_font,bg='lightblue',width=10,command=deposit)
    deposit_btn.place(relx=.01,rely=0.4)

    
    withdraw_btn=Button(frm,text='Withdraw',font=admin_font,bg='lightyellow',width=10,command=withdraw)
    withdraw_btn.place(relx=.01,rely=0.5)

    update_btn=Button(frm,text='Update',font=admin_font,bg='lightblue',width=10,command=update)
    update_btn.place(relx=.01,rely=0.6)

    transfer_btn=Button(frm,text='Transfer',font=admin_font,bg='whitesmoke',width=10,command=transfer)
    transfer_btn.place(relx=.01,rely=0.7)

    history_btn=Button(frm,text='History',font=admin_font,bg='lightblue',width=10,command=history)
    history_btn.place(relx=.01,rely=0.8)

    
    

#runs tkinter GUI
main_screen()       #main function
root.mainloop()     #starts the tkinter gui


