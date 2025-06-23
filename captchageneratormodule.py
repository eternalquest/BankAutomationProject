import random 

def generate_captcha():
    captcha=[] #captcha list to store captcha
    for i in range(6):
        #generates character after converting random int into char
        c=chr(random.randint(65,90))
        #appends the character generated into captcha list
        captcha.append(c)

        
    return captcha

def refresh_captcha():

    #calls generate captcha function and stores its value in variable
    new_cap=generate_captcha()
    #changes the captcha label text value and inserts the variable
    return new_cap

