import gmail

def send_mail_for_openacn(to_mail,uacno,uname,upass,udate):
    con=gmail.GMail('nitishpokhriyal1@gmail.com','szpz mbwa tfhy tgun')
    sub="Account Opened with ABC Bank"
    body=f"""Dear {uname},
        Your account has been opened successfully with ABC Bank and details are
        ACN = {uacno}
        Pass = {upass}
        Open date = {udate}

        Kindly change your password when you login first time
        Thanks
        ABC Bank
        Noida"""
    msg=gmail.Message(to=to_mail,subject=sub,text=body)
    con.send(msg)
    

def send_otp(to_mail,uname,uotp):
    con=gmail.GMail('nitishpokhriyal1@gmail.com','szpz mbwa tfhy tgun')
    sub="OTP password recovery"
    body=f"""Dear {uname},
    Your OTP to get password = {uotp}
   
    Kindly verify this otp to application 
    Thanks
    ABC Bank
    Noida
    """
    msg=gmail.Message(to=to_mail,subject=sub,text=body)
    con.send(msg)

def send_otp_del(to_mail,uname,uotp):
    con=gmail.GMail('nitishpokhriyal1@gmail.com','szpz mbwa tfhy tgun')
    sub="Account Deletion OTP"
    body=f"""Dear {uname},
    Your OTP to get password = {uotp}
   
    Kindly verify this otp to application for account deletion.
    Thanks
    ABC Bank
    Noida
    """
    msg=gmail.Message(to=to_mail,subject=sub,text=body)
    con.send(msg)