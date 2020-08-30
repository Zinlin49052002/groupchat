from tkinter import * 
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from PIL import Image,ImageTk

bg = "#333333"
fg = "#ffffff"
wtf = True
class LoginFrame(Frame):
    def __init__(self,parent):
        self.parent = parent
        super().__init__(parent)
        self.config(width=600,height=800,relief=FLAT,highlightcolor = bg, highlightbackground = bg, highlightthickness = 2, borderwidth = 2)
        self.loginLabel = Label(self,text="Login",fg=fg,bg=bg)
        self.loginLabel.grid(row=0,column=0,columnspan=2,ipadx=20,pady=(10,30))
        self.signupLabel = Label(self,text="Signup",fg=bg)
        self.signupLabel.grid(row=0,column=2,columnspan=2,ipadx=20,pady=(10,30))
        self.signupLabel.bind("<1>",self.toSignup)

        Label(self,text="Username",fg=bg).grid(row=1,column=0,columnspan=2,padx=20,pady=(0,20))
        self.usernameEnt = Entry(self,relief=FLAT,highlightcolor = bg, highlightbackground = bg, highlightthickness = 1, borderwidth =2)
        self.usernameEnt.grid(row=1,column=2,columnspan=2,pady=(0,20),padx=(0,10))

        Label(self,text="Password",fg=bg).grid(row=2,column=0,columnspan=2,padx=20,pady=(0,20))
        self.passwordEnt = Entry(self,relief=FLAT,show="*",highlightcolor = bg, highlightbackground = bg, highlightthickness = 1, borderwidth =2)
        self.passwordEnt.grid(row=2,column=2,columnspan=2,pady=(0,30),padx=(0,10))

        self.loginBtn = Label(self, text = "Login", relief = "flat", bg = bg, fg = fg)
        self.loginBtn.grid(row=3,column=1,columnspan=2,pady=(0,30),padx=(30,10),ipadx=20)
        self.loginBtn.bind('<1>',self.login)
        
        Label(self,text="Whisper..",font=("Pacifico",20),fg="teal").grid(row=4,column=1,columnspan=2,pady=(0,30))
    def login(self,e):
        username = self.usernameEnt.get()
        password = self.passwordEnt.get()
        data = self.parent.login(username,password)
        if data[-1]:
            self.parent.connectServer(data[0])
            self.pack_forget()
            HomeFrame(self.parent,data[0],data[1],data[2]).pack(pady=(40,0))
        else:
            mb.showerror(title="Whisper",message=data[0])
    def toSignup(self,e):
        self.pack_forget()
        SignupFrame(self.parent).pack(pady=(40,0))
class SignupFrame(Frame):
    def __init__(self,parent):
        self.parent = parent
        super().__init__(parent)
        self.filepath = 'user.png'
        self.config(width=600,height=800,relief=FLAT,highlightcolor = bg, highlightbackground = bg, highlightthickness = 2, borderwidth = 2)
        self.loginLabel = Label(self,text="Login",fg=bg)
        self.loginLabel.grid(row=0,column=0,columnspan=2,ipadx=20,pady=(10,20))
        self.loginLabel.bind('<1>',self.toLoginin)
        self.signupLabel = Label(self,text="Signup",fg=fg,bg=bg)
        self.signupLabel.grid(row=0,column=2,columnspan=2,ipadx=20,pady=(10,20))

        Label(self,text="Profile",fg=bg).grid(row=1,column=0,columnspan=2,padx=20,pady=(0,20))
        self.profile = Label(self, text = "Add Image", relief = "flat", bg = bg, fg = fg)
        self.profile.grid(row=1,column=2,columnspan=2,pady=(0,20),ipadx=32,padx=(0,10))
        self.profile.bind("<1>",self.browseImage)

        Label(self,text="Username",fg=bg).grid(row=2,column=0,columnspan=2,padx=20,pady=(0,20))
        self.usernameEnt = Entry(self,relief=FLAT,highlightcolor = bg, highlightbackground = bg, highlightthickness = 1, borderwidth =2)
        self.usernameEnt.grid(row=2,column=2,columnspan=2,pady=(0,20),padx=(0,10))

        Label(self,text="Password",fg=bg).grid(row=3,column=0,columnspan=2,padx=20,pady=(0,20))
        self.passwordEnt = Entry(self,relief=FLAT,show="*",highlightcolor = bg, highlightbackground = bg, highlightthickness = 1, borderwidth =2)
        self.passwordEnt.grid(row=3,column=2,columnspan=2,pady=(0,20),padx=(0,10))

        Label(self,text="Re-password",fg=bg).grid(row=4,column=0,columnspan=2,padx=15,pady=(0,20))
        self.repasswordEnt = Entry(self,relief=FLAT,show="*",highlightcolor = bg, highlightbackground = bg, highlightthickness = 1, borderwidth =2)
        self.repasswordEnt.grid(row=4,column=2,columnspan=2,pady=(0,20),padx=(0,10))

        Label(self,text="Email",fg=bg).grid(row=5,column=0,columnspan=2,padx=20,pady=(0,20))
        self.emailEnt = Entry(self,relief=FLAT,highlightcolor = bg, highlightbackground = bg, highlightthickness = 1, borderwidth =2)
        self.emailEnt.grid(row=5,column=2,columnspan=2,pady=(0,30),padx=(0,10))

        self.signupbtn = Label(self, text = "Submit", relief = "flat", bg = bg, fg = fg)
        self.signupbtn.grid(row=6,column=1,columnspan=2,pady=(0,30),padx=(30,10),ipadx=20)
        self.signupbtn.bind("<1>",self.signup)

        Label(self,text="Whisper..",font=("Pacifico",20),fg="teal").grid(row=7,column=1,columnspan=2,pady=(0,30))
    def signup(self,e):
        username = self.usernameEnt.get()
        password = self.passwordEnt.get()
        repassword = self.repasswordEnt.get()
        email = self.emailEnt.get()
        filepath = self.filepath
        msg = self.parent.signup(username,password,repassword,email,filepath)
        if msg:
            mb.showerror(title="Signup Error!",message=msg)
        else:
            mb.showinfo(title="Whisper",message="Signup Successful!")
            self.toLoginin(e)

    def toLoginin(self,e):
        self.pack_forget()
        LoginFrame(self.parent).pack(pady=(40,0))
    
    def browseImage(self,e):
        self.filepath = fd.askopenfilename()
class user(Frame):
    def __init__(self, parent, username,profile,owner):
        self.parent = parent
        self.username= username
        self.profile = profile
        super().__init__(parent, cursor = 'hand2')  
        f = open('temp_profile.png', 'wb')
        f.write(self.profile)
        f.close()
        # self.pp_img = PhotoImage(file = 'temp_profile.png')
        self.img = Image.open(r'temp_profile.png')
        if owner:
            self.new = self.img.resize((60,60))
        else:
            self.new = self.img.resize((40,40))    
            self.bind("<1>",lambda event,name = self.username: self.click(event,name))
        self.pp_img = ImageTk.PhotoImage(self.new)
        Label(self, image = self.pp_img).grid(row=0,column=0)
        self.name = Label(self, text = self.username)
        self.name.grid(row=0,column=1)
        self.bind("<Enter>",self.lightUp)
        self.bind("<Leave>",self.lightOut)
        
    def lightUp(self,e):
        self.name.config(fg="teal")
    def lightOut(self,e):
        self.name.config(fg=bg)
    def click(self,e,username):
        print(username)
        global wtf
        print(e)
        print("Hello-----------------")
        if wtf:
            self.parent.pack_forget()
            ChatFrame(self.parent,username).grid(column=2,row=0,columnspan=4,rowspan=6)
            wtf = False
        else :
            self.grid_forget()
            ChatFrame(self.parent,username).grid(column=2,row=0,columnspan=4,rowspan=6)
    
class HomeFrame(Frame):
    def __init__(self,parent,username,email,profile):
        self.parent = parent
        super().__init__(parent)
        self.config(width=800,height=450,relief=FLAT,highlightcolor = bg, highlightbackground = bg, highlightthickness = 2, borderwidth = 2)
        # self.grid_propagate(0)
        Label(self,text="Whisper..",font=("Pacifico",20),fg="teal").grid(row=0,column=0,sticky="W",padx=(0,15))
        user(self,username,profile,True).grid(row=1,column=0,columnspan=2,sticky="W",pady=(0,15))
        # NavFrame(self).grid(row=2,column = 0,columnspan=2,rowspan=4)
        self.friendList = Frame(self)
        self.cv = Canvas(self.friendList,width=100)
        self.sbar = Scrollbar(self.friendList,command=self.cv.yview)
        self.cv.config(yscrollcommand = self.sbar.set)
        self.f = Frame(self.cv)
        self.cv.create_window((0,0), window = self.f)
        
        self.cv.pack(side = 'left',fill='both')
        self.sbar.pack(side = 'right', fill = 'y')
        self.parent.bind("<Configure>", lambda e: self.cv.config(scrollregion = self.cv.bbox('all')))
        self.friendList.grid(row=2,column = 0,columnspan=2,rowspan=3)

        for i in self.parent.getAllUser():
            if i[0]==username:
                continue
            else:
                user(self.f,i[0],i[1],False).pack(side="top")
        Welcome(self,username).grid(column=2,row=0,columnspan=4,rowspan=6)
class Welcome(Frame):
    def __init__(self,parent,username):
        self.parent = parent
        super().__init__(parent)
        self.config(width=700,height=450,relief=FLAT,highlightcolor = bg, highlightbackground = bg, highlightthickness = 1, borderwidth = 1)
        self.pack_propagate(0)
        Label(self,text=f"Welcome {username}!",font=("Pacifico",24),fg="teal").pack(side="top",anchor='e')
        Label(self,text="Help Center With AI -").pack(side="top",anchor="e")
        Label(self,text="Messages are Encrypted -").pack(side="top",anchor="e")
        Label(self,text="Messages will not be stored in our database -").pack(side="top",anchor="e")
        Label(self,text="Contact Us",font=("Pacifico",22),fg="teal").pack(side="bottom",anchor="w")
        Label(self,text="- kz3@enterprise.com").pack(side="bottom",anchor="w")
        Label(self,text="- whisperXkz3.com").pack(side="bottom",anchor="w")
        Label(self,text="- Developed By KZ3").pack(side="bottom",anchor="w")
        

class ChatFrame(Frame):
    def __init__(self,parent,toUsername):
        self.parent = parent
        self.toUsername = toUsername
        super().__init__(parent)
        self.config(width=700,height=450,relief=FLAT,highlightcolor = bg, highlightbackground = bg, highlightthickness = 1, borderwidth = 1)
        self.grid_propagate(0)
        Label(self,text=self.toUsername,font=15).grid(row=0,column=0,columnspan=3)
        self.chatF = Frame(self,bg= "blue")
        self.cv = Canvas(self.chatF,bg = "green")
        self.sbar = Scrollbar(self.chatF,command=self.cv.yview)
        self.cv.config(yscrollcommand = self.sbar.set)
        self.innerChatF = Frame(self.cv,bg="red")
        self.cv.create_window((0,0), window = self.innerChatF)
        self.cv.pack(side = 'left',fill='both',expand=True)
        self.sbar.pack(side = 'right', fill = 'y')
        self.parent.bind("<Configure>", lambda e: self.cv.config(scrollregion = self.cv.bbox('all')))
        self.chatF.grid(row=1,column=0,columnspan=3,rowspan=3)
