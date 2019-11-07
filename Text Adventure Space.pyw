from tkinter import *
import tkinter.messagebox
import shelve
from time import sleep

GUI = Tk()
GUI.wm_title("Control Panel")
GUI.columnconfigure(1, weight=1)
GUI.rowconfigure(1, weight=1)
GUI.columnconfigure(2,weight=0)


#Terminal
CommandConsole = Frame(GUI,relief="sunken",borderwidth=10)
CommandConsole.grid(column=1,row=1,rowspan=4,sticky="NESW")
CommandConsole.columnconfigure(1,weight=1)
CommandConsole.rowconfigure(1, weight=1)


Terminal = Text(CommandConsole,state="disabled",background ="black",foreground="white",wrap="word")
Terminal.grid(column=0,columnspan=3,row=0,rowspan=2,sticky="NESW")

Scrollbar = Scrollbar(CommandConsole)
Scrollbar.grid(column=1,row=0,rowspan=2,sticky="NES")

Terminal.config(yscrollcommand=Scrollbar.set)

Scrollbar.config(command=Terminal.yview)


#Drill Controls
DrillControls = Frame(GUI,relief="sunk",borderwidth=10)
DrillControls.grid(column=2,row=1,sticky="NESW")
DrillControls.columnconfigure(2, weight=3)
DrillControls.rowconfigure(1, weight=2)

Label(DrillControls,text="Drill Controls",font=("Times", 10,"bold")).pack()
Label(DrillControls,text="Lazer Drill Power (%)").pack()

Lazer_power = Scale(DrillControls, from_=0, to=110,state="normal",troughcolor="orange",tickinterval=10)
Lazer_power.pack(expand=True,fill=BOTH)

Lazer_power.set(100)
Lazer_power.config(state="disabled")

Scan_Asteroid = Button(DrillControls, text ="Scan Asteriod",state="disabled")
Scan_Asteroid.pack()

#Station controls
StationControls = Frame(GUI,relief="sunk",borderwidth=10)
StationControls.grid(column=2,row=3,sticky="NESW")
DrillControls.columnconfigure(1, weight=3)
DrillControls.rowconfigure(1, weight=2)

Label(StationControls,text="Station Controls",font=("Times", 10,"bold")).pack(expand=True,fill=X)

Open_Docking_Clamps = Button(StationControls, text =" Open Docking Clamps",state="disabled")
Open_Docking_Clamps.pack(expand=True,fill=X)

Release_Asteroid = Button(StationControls, text ="      Release Asteroid      ",state="disabled")
Release_Asteroid.pack(expand=True,fill=X)

Disconnect = Button(StationControls, text ="Disconnect from Station",command=GUI.destroy)
Disconnect.pack()



tag_num = 0
x = 0


class User():

    def __init__(self):
        
        
        Terminal.config(state="normal") #so we can edit
        Terminal.insert(END,"Enter Username:") #insert text
        Terminal.tag_add("Tag "+str(tag_num),"end -2c linestart",END) #add tag
        Terminal.tag_config("Tag "+str(tag_num),foreground="yellow") #change tag-text colour
        
        GUI.update()

        Terminal.insert(END,"\n")
        
        self.Username = StringVar()

        E = Entry(Terminal,textvariable=self.Username)
        Terminal.window_create(END, window=E)

        Terminal.insert(END,"\n\n")
        
        
        for option in [("Sign up",self.create_user),("Login",self.find_user)]:
            B = Button(Terminal,text=option[0],command=option[1])
            Terminal.window_create(END, window=B) #insert button
            Terminal.insert(END,"\t")

        
        Terminal.insert(END,"\n")
        Terminal.config(state="disabled") #make text non change able


    def create_user(self):
        self.name = self.Username.get()
        self.Done_This = False

        if self.name:
            user_data = shelve.open(self.name)#open user data
            user_data['progress'] = [] #create progress file
            self.progress = user_data['progress']
            user_data.close()

        
        
            Terminal.config(state="normal") #so we can edit
            Terminal.delete('1.0', END)#delete everything
            Terminal.config(state="disabled") #so the user can't edit        

            Story.Start()#start game

        else:
            tkinter.messagebox.showwarning("Invalid user name","Must enter username")
            

    def find_user(self):
         
        self.name = self.Username.get()
        self.Done_This = True

        
        if self.name:
            
            try:
                user_data = shelve.open(self.name)#open user data
                self.progress = user_data["progress"]
                user_data.close()
            except:
                tkinter.messagebox.showwarning("Invalid user name","We can't find this user: " + self.name)
            else:
                
                Terminal.config(state="normal") #so we can edit
                Terminal.delete('1.0', END)#delete everything
                Terminal.config(state="disabled") #so the user can't edit

                Story.Start() #start game
        else:
            tkinter.messagebox.showwarning("Invalid user name","Must enter username")



    def add_to_progress(self,string):

        user_data = shelve.open(str(self.name))#open user data
            
            
        self.progress = user_data['progress']
        self.progress.append(string)#add to progress

        ordered_progress = []
        for choice in self.progress:
            if choice not in ordered_progress:
              ordered_progress.append(choice)
            else:
                #print(choice)
                pass

        
        self.progress = ordered_progress

        
        user_data['progress'] = self.progress
        
        user_data.close()

        #print(self.progress)




class Story():

    def __init__(self,user):

        self.user = user

    def display(self,string,front="<>{ ",end="\n",colour="white",time=False):
        global tag_num

        if self.user.Done_This:
            sleep(0)
        elif not isinstance(time,int):
            sleep(time)
        else:
            sleep(1)
            
        tag_num += 1 #So the tag is unique other wize you change all of the tags with the same name
        
        Terminal.config(state="normal") #so we can edit

        if front == "->{ " and not self.user.Done_This:
            Terminal.insert(END,front)
            for letter in string:
                
                Terminal.config(state="disabled")
                sleep(0.05)
                Terminal.config(state="normal")
                
                Terminal.insert(END,letter)
                Terminal.tag_add("Tag "+str(tag_num),"end -2c linestart",END) #add tag
                #print(tag_num,":",Terminal.index("end -2c linestart"),">",Terminal.get("end -2c linestart","end - 2c "),"<",Terminal.index("end - 2c"))
                Terminal.tag_config("Tag "+str(tag_num),foreground=colour) #change tag colour
                GUI.update()
                
            Terminal.insert(END,end)

        else:
                
            Terminal.insert(END,front+string+end) #insert text

        
        Terminal.tag_add("Tag "+str(tag_num),"end -2c linestart",END) #add tag
        #print(tag_num,":",Terminal.index("end -2c linestart"),">",Terminal.get("end -2c linestart","end - 2c "),"<",Terminal.index("end - 2c"))
        Terminal.tag_config("Tag "+str(tag_num),foreground=colour) #change tag colour
        Terminal.config(state="disabled") #make text non change able

        GUI.update()

        

        Terminal.see("end")

    
        

    def user_response(self,*options):
        global Buttons
        Buttons = []

        def reply_and_continue(option):
            

            self.remove_buttons()
            
            self.display(option[0],colour="green",front="<-{ ")

            
            self.user.add_to_progress(option[0])
            

            option[1]()

        Terminal.config(state="normal") #so we can edit

        

        for option in options:
            if option[0] in self.user.progress:
                self.user.Done_This = True
                
                self.display(option[0],colour="green",front="<-{ ")

                option[1]()

                break
                
            
            
        else:
            self.user.Done_This = False
            sleep(1)
            

            for option in options:
                B = Button(Terminal,text=option[0],command=lambda i=option: reply_and_continue(i))
                Buttons.append(B)
                Terminal.window_create(END, window=B) #insert button

        

            
        Terminal.insert(END,"\n")
        Terminal.config(state="disabled") #make text non change able

        GUI.update()

        Terminal.see("end")

        



    def remove_buttons(self):
        global Buttons
            
        Terminal.config(state="normal") #so we can edit
        for button in Buttons:
            try:
                Terminal.delete(button,END)
            except:
                pass
            
        if not self.user.Done_This:
            Terminal.insert(END,"\n")
        
        Terminal.config(state="disabled") #make text non change able

        GUI.update()

    def Start(self):

        self.inside_ship = False
        
        self.display("Making conection with Mining Station 634A")
        self.display("Establishing conection",end="")

        for x in range(3):
            self.display(".",front="",end="",time=1)

        self.display("Conection Established",front="")
        
        self.display("",front="")
        
        self.display("While you were away:")
        self.display("  > Scanners picked up unusual energy flucuations from the asteroids core")
        self.display("  > Leg 4 was damaged by space debris")
        self.display("  > A light spaceship parked near us and tried to contact you")

        self.display("",front="")

        self.display("Incoming Transmission from spaceship:")
        
        self.display("Hello",colour="cyan",front="->{ ")
        self.display("Anyone out there?",colour="cyan",front="->{ ")
        self.display("Is this Mining Station 634A?",colour="cyan",front="->{ ")

        
        self.user_response(("Afirmitive, Do you need help?",self.Turn_it_off),("Yes, this Mining Station 634A",self.Doing_The_Job),("Nope, sorry mate",self.Hardly_working))

    def Doing_The_Job(self):
        
        self.display("Ah, good",colour="cyan",front="->{ ")

        self.user_response(("Who is this please?",self.Introduction),("How can I help?",self.Turn_it_off),("What are you doing here?",self.Not_safe))
        

    def Hardly_working(self):

        self.display("What???",colour="cyan",front="->{ ")
        self.display("Are you messing with me?",colour="cyan",front="->{ ")
        self.display("This is serious",colour="cyan",front="->{ ")

        self.Turn_it_off()

    def Introduction(self):
        
        self.display("I am Dr James B. Qantus",colour="cyan",front="->{ ")
        self.display("from the University of Forian",colour="cyan",front="->{ ")
        self.display("on the planet Sanus",colour="cyan",front="->{ ")
        
        self.Turn_it_off()

    def Turn_it_off(self):
        self.display("You need to turn off your drill",colour="cyan",front="->{ ")
        self.user_response(("What, why?",self.Not_safe),("I need to call my Manager",self.calling_the_boss),("Ok right away",self.Turn_off_the_drill))
        
        

    def Not_safe(self):

        self.display("I can't tell you here.",colour="cyan",front="->{ ")
        self.display("It's not safe.",colour="cyan",front="->{ ")
        self.display("I fear my communications are being recorded",colour="cyan",front="->{ ")

        self.three_options()

    def calling_the_boss(self):

        self.display("There isn't enough time",colour="cyan",front="->{ ")
        self.three_options()

    def three_options(self):
        self.display("Turn off your drill.",colour="cyan",front="->{ ")
        self.display("   or   ",colour="cyan",front="->{ ")
        self.display("Let me dock my ship",colour="cyan",front="->{ ")

        
        if "What, why?" in self.user.progress:
            self.display("so I can tell you in person",colour="cyan",front="->{ ")

        self.user_response(("I'll turn off the drill",self.Turn_off_the_drill),("I'm going to call my Manager",self.the_boss),("I'll open the docking clamps",self.openthedockingclamps))

    def the_boss(self):

        self.display("There is no time",colour="cyan",front="->{ ")
        
        self.display("Contacting DSMC HQ {46537943633764-63}",end="")

        for x in range(3):
            self.display(".",front="",end="",time=1)

        self.display("Connected",front="")

        self.display("I've already contacted him and...",colour="cyan",front="->{ ")

        self.display("What is it!?!?",colour="red",front="->{ ")
        self.display("You better not be wasting my time!",colour="red",front="->{ ")

        if "Who is this please?" in self.user.progress:
            formal_explanation = "A doctor called James Qantus wants me to turn off the drill"
        else:
            formal_explanation = "A man in a spaceship wants me to turn off the drill"

        self.user_response((formal_explanation,self.dont_turn_it_off),("Some crazy guy wants me to turn off the drill",self.dont_turn_it_off),("Errr... Bye",self.three_options_2))

    def dont_turn_it_off(self):
        self.display("Don't turn off that drill!!!",colour="red",front="->{ ")
        self.display("That drill makes the company money",colour="red",front="->{ ")
        self.display("If you turn it off I will personally fire you",colour="red",front="->{ ")
        self.display("Ignore that stupid doctor, I've already told him we won't turn off the drill",colour="red",front="->{ ")
        self.display("Goodbye!",colour="red",front="->{ ")

        self.three_options_2()

    def three_options_2(self):
        
        self.display("Connection lost with DSMC HQ {46537943633764-63}")

        self.display("Told you",colour="cyan",front="->{ ")
        self.display("Now let me come inside so I can tell you why you should turn it off",colour="cyan",front="->{ ")
        self.display("   or   ",colour="cyan",front="->{ ")
        self.display("Turn the drill off because it's the right thing to do",colour="cyan",front="->{ ")

        self.user_response(("I'll turn off the drill",self.Turn_off_the_drill),("Goodbye Doctor",self.goodbye),("I'll open the docking clamps",self.openthedockingclamps))

    def goodbye(self):
        self.display("Wait no...",colour="cyan",front="->{ ")
        self.display("Conection Lost")

        self.display("The spaceship is starting up",time=2)
        self.display("The spaceship is flying away")

        self.game_over()
        
        

    def Turn_off_the_drill(self):

        self.display("@@@@@@@@")

        DrillControls.config(relief="raise")
        GUI.update()

        def Nothing(power):
            pass
        
        def Lazer_power_change(power):

            
            if Lazer_power.get() == 110 and not "wrong way" in self.user.progress:
                Lazer_power.config(state="disabled",command=Nothing,troughcolor="red")
                DrillControls.config(relief="sunk");GUI.update()
                self.user.add_to_progress("wrong way")
                self.wrong_way()
                    
            elif Lazer_power.get() == 0 and not "phew" in self.user.progress:
                Lazer_power.config(state="disabled",command=Nothing,troughcolor="grey")
                DrillControls.config(relief="sunk");GUI.update()
                self.user.add_to_progress("phew")
                self.phew()
                
            else:
                pass

        

        Lazer_power.config(command=Lazer_power_change)

        Lazer_power.config(state="normal")

        #Make sure this is in revevse order

        
            
        if "wrong way" in self.user.progress and Lazer_power.get() == 100:
            Lazer_power.set(110)
            Lazer_power.config(state="disabled",command=Nothing,troughcolor="red")
            DrillControls.config(relief="sunk")
            GUI.update()
            self.wrong_way()

        elif "phew" in self.user.progress:
            Lazer_power.set(0)
            Lazer_power.config(state="disabled",command=Nothing,troughcolor="grey")
            DrillControls.config(relief="sunk")
            GUI.update()
            self.phew()
            
        else:
            self.user.Done_This = False
            


    def phew(self):
        
        
        
        self.display("Ah,thank you",colour="cyan",front="->{ ")
        self.display("Sorry to make you do that",colour="cyan",front="->{ ")
        self.display("I'm sure your boss will be very angry at you",colour="cyan",front="->{ ")

        if not self.inside_ship:

            self.display("Do you mind letting me inside so I can do some scans on the Asteroid",colour="cyan",front="->{ ")
            self.display("and tell you why we needed to turn it off",colour="cyan",front="->{ ")

            self.user_response(("Sure",self.openthedockingclamps),("Why do you need to come inside to scan?",self.why),("I can't let you inside",self.youcantcomein))

        else:
            self.display("Now that drill is off. We should run some scans",colour="cyan",front="->{ ")
            self.scans()
        

    def wrong_way(self):
        global Lazer_power
        Lazer_power.set(110)
        
        
        self.display("Whatt diidd youu ddoo?",colour="cyan",front="->{ ")
        self.display("Lazer at maximum capicity",colour="red")
        self.display("You are going to destroy it",colour="cyan",front="->{ ")
        self.display("Flux Capicater overheating",colour="red")
        self.display("Turn it off!!!",colour="cyan",front="->{ ")
        self.display("Energy siginals fr£$^&)*ide the Asteroid increasing",colour="red")
        self.display("Power Outr(*&$%^& imminent",colour="red")

        
        self.user_response(("I'll turn it off",self.Turn_off_the_drill),("How do you turn this thing off???",self.How_do_you),("No",self.self_destruct))

    def How_do_you(self):
        
        self.display("Move the slider up!!!",colour="cyan",front="->{ ")
        self.display("It's too late!!!",colour="cyan",front="->{ ")
        self.display("How did you get this job?!?!",colour="cyan",front="->{ ")
        
        self.explode()

    def self_destruct(self):
        self.display("Why would you do this?",colour="cyan",front="->{ ")
        self.display("You mad man!!!",colour="cyan",front="->{ ")

        self.explode()

    def explode(self):

        if self.inside_ship:
            self.display("I'm getting out of here",colour="cyan",front="->{ ")
        else:
            self.display("Conection lost with spaceship")
        
        self.display("Lazer stablizer damage detected",colour="red")

        self.display("Leg 4 damage detected",colour="red")
        self.display("Airlock compromised",colour="red")
        self.display("Leg 2 damage detected",colour="red")

        
        if self.inside_ship:
            self.display("Opening air lock")
            self.display("Ship presure compromised")
            self.display("Aaaaaaaahhhhhhhhhhhhhhhh",colour="cyan",front="->{ ")
            self.display("Connection to James B. Quantus lost",colour="cyan",front="->{ ")
            self.display("Shuting air lock")
            
        else:
            self.display("The spaceship starting up")

        self.display("Leg 5 damage detected",colour="red")
        self.display("Leg 1 damage detected",colour="red")

        if not self.inside_ship:
            self.display("The spaceship is flying away")
        
            
        self.display("Leg 6 damage detected",colour="red")
        self.display("Leg 3 damage detected",colour="red")

        
        self.display("Bridge damage detected",colour="red")


        self.display("Conection lost with DSMC HQ")
        self.display("Conection lost with Mining Station 634A")
        
        self.game_over()



    def why(self):

        self.display("Good question",colour="cyan",front="->{ ")
        self.display("My ships scanners are not as good as the ones in your Mining Station",colour="cyan",front="->{ ")
        self.display("Your station already has probes inside the Asteroid as well",colour="cyan",front="->{ ")

        self.user_response(("I will let you come inside",self.openthedockingclamps),("You can come inside but I'll be watching you,always watching",self.openthedockingclamps),("I can't let you inside",self.youcantcomein))

    def youcantcomein(self):
        
        self.display("What? , Why?",colour="cyan",front="->{ ")

        self.user_response(("The boss won't allow it",self.justletmein),("I don't trust you",self.justletmein),("I don't like you",self.justletmein))

    def justletmein(self):

        if "The boss won't allow it" in self.user.progress:
            self.display("I talked to your boss on the phone. He's crazy.",colour="cyan",front="->{ ")

            if "phew" in self.user.progress:
                self.display("plus he wouldn't let you turn off the drill either",colour="cyan",front="->{ ")

        elif "I don't trust you" in self.user.progress:
            self.display("What reason do I have to lie?",colour="cyan",front="->{ ")

        elif "I don't like you" in self.user.progress:
            self.display("We should put aside are diffrences for the greater good?",colour="cyan",front="->{ ")

        else:
            self.display("Whaaat? , That's stupid.",colour="cyan",front="->{ ")

        self.display("Just let me in",colour="cyan",front="->{ ")

        self.user_response(("Fine!!!",self.openthedockingclamps),("No!",self.goodbye),("Go away!!!",self.goodbye))


    def openthedockingclamps(self):
        global Open_Docking_Clamps
        

        def open_clamps():

            Open_Docking_Clamps.config(state="disabled")
            StationControls.config(relief="sunk")
            GUI.update()

            self.display("Spaceship starting up")
            self.display("Spaceship moving closer")
            
            self.display("Spaceship in docking position")

            self.display("Okay, I'm ready",colour="cyan",front="->{ ")

            if not self.user.Done_This:
                Open_Docking_Clamps.config(text="Close Docking Clamps",command=close_clamps,state="normal")
                StationControls.config(relief="raise")
                GUI.update()
            else:
                close_clamps()

        def close_clamps():
            
            Open_Docking_Clamps.config(state="disabled")
            StationControls.config(relief="sunk")
            GUI.update()


            self.display("Docking Succesful")

            self.display("Ok,I'm coming over",colour="cyan",front="->{ ")
            self.display("I will disconnect my ships VTS and rejoin to your Mining Stations one",colour="cyan",front="->{ ")
            self.display("See you soon",colour="cyan",front="->{ ")

            self.display("Disconnected from spaceship")
            
            self.display("Depressurising  airlock")
            self.display("Opening airlock")

            self.display("Connecting to James B. Qantus's space suit")

            self.display("I'm inside",colour="cyan",front="->{ ")

            self.inside_ship = True
            
            self.display("Closing airlock")
            self.display("Pressurising  airlock")
            self.display("Opening Door")


            self.display("I can't wait to get out of this spacesuit",colour="cyan",front="->{ ")

            self.display("Now that we are speaking through a closed communications system, I can tell you why I what is inside the Asteroid",colour="cyan",front="->{ ")
            
            

            if "I'll turn off the drill" in self.user.progress or "Ok right away" in self.user.progress:
                self.display("and why I wanted you to turn off the drill so badly.",colour="cyan",front="->{ ")
                self.put_the_drill_back_on()
            else:
                self.display("and why I want you to turn off the drill so badly.",colour="cyan",front="->{ ")
                self.story()

        
            
             

        self.display("Urgh, thanks",colour="cyan",front="->{ ")
        self.display("You won't regret this",colour="cyan",front="->{ ")

        self.display("@@@@@@@@")




        if not self.user.Done_This:
            Open_Docking_Clamps.config(state="normal",command=open_clamps)
            StationControls.config(relief="raise")
            GUI.update()
        else:
            open_clamps()

    def put_the_drill_back_on(self):

        self.display("Incoming call from DSMC HQ {46537943633764-63}")

        self.display("Sounds like your boss is angry",colour="cyan",front="->{ ")
        self.display("While you talk to him I will set up my stuff",colour="cyan",front="->{ ")
        
        self.display("Conected to DSMC HQ {46537943633764-63}")

        if "the_boss" in self.user.progress:
            self.display("I told you to turn off that drill!",colour="red",front="->{ ")
        else:
            self.display("why the hell did you turn off the drill!!!",colour="red",front="->{ ")


        self.display("Turn that drill back on immediatly!",colour="red",front="->{ ")
        self.display("or you're fired!",colour="red",front="->{ ")

        self.display("So whats your answer. Are you going to turn that drill back on?",colour="red",front="->{ ")

                    
        self.user_response(("Yes Sir",self.disconnect),("Um...",self.disconnect),("No, Fire me!",self.disconnect))

    def disconnect(self):

        if "Yes Sir" in self.user.progress:
            self.display("That's what I like to hear",colour="red",front="->{ ")
            self.display("Turn it off the...",colour="red",front="->{ ")
        elif "Um..." in self.user.progress:
            self.display("WHAT DO YOU MEAN ummm.... TURN ON THAT DRILL RIGHT...",colour="red",front="->{ ")
        elif "No, Fire me!":
            self.display("WHAT, HOW DARE YOU. I WILL...",colour="red",front="->{ ")
        else:
            self.display("...What...",colour="red",front="->{ ")

        self.display("Unexpectantly Disconected to DSMC HQ {46537943633764-63}")

        self.display("Sorry that guy was annoying me",colour="cyan",front="->{ ")

        self.display("It's time I told you the story",colour="cyan",front="->{ ")

        self.story()

        

    def story(self):

        if "story" not in self.user.progress:
            self.user.add_to_progress("story")

        self.display("I was on a research station orbiting on the other side of this gas giant",colour="cyan",front="->{ ")

        self.display("While investigating the affect of gravity on certain gases for a project",colour="cyan",front="->{ ")

        self.display("My team and I saw a boulder fly out of the planet and start obiting",colour="cyan",front="->{ ")

        self.display("We had tracked down the rock and investigated it",colour="cyan",front="->{ ")

        self.display("After lot of tests we realised it was no ordinary boulder",colour="cyan",front="->{ ")

        self.display("It was like an egg or a cocoon of some sort.",colour="cyan",front="->{ ")

        self.display("A thick casing protecting an undiscovered alien species",colour="cyan",front="->{ ")

        self.display("My team and I were extremely excited to discover a new species.",colour="cyan",front="->{ ")

        self.display("Especially one of the first species to inhabit a gas planet",colour="cyan",front="->{ ")

        self.display("The problem was that the thing inside the rock was growing incredably slowly",colour="cyan",front="->{ ")

        self.display("We estimated it would take about a million years for it to grow to full size",colour="cyan",front="->{ ")

        self.display("We knew we needed to find an older specimen to present to the university",colour="cyan",front="->{ ")

        self.display("My friend had the good idea to monitor Deep Space Mining stations",colour="cyan",front="->{ ")

        self.display("And see if we could find any readings that matched our own",colour="cyan",front="->{ ")

        self.display("Which would signify another lifeform deep inside the rock ",colour="cyan",front="->{ ")

        self.display("So we hacked into your companies database to find the signals that matched",colour="cyan",front="->{ ")

        self.display("And your station came up",colour="cyan",front="->{ ")

        self.display("I quickly embarked on our fastest ship to confirm our theory.",colour="cyan",front="->{ ")

        self.display("That inside your asteroid is a ancient unknown alien lifeform",colour="cyan",front="->{ ")

        self.display("So that's why I'm here",colour="cyan",front="->{ ")

        self.display("To confirm the alien lifeform's presence",colour="cyan",front="->{ ")

        self.display("And protect the alien lifeform from your lazer drill",colour="cyan",front="->{ ")
        

        self.user_response(("Wow!, That's amazing",self.story_reaction),("So what now",self.story_reaction),("Cool story bro!",self.story_reaction))


    def story_reaction(self):

        
        if "Wow!,That's amazing" in self.user.progress or "Cool story bro!" in self.user.progress:
            self.display("Thanks",colour="cyan",front="->{ ")

        if Lazer_power.get() == 100:
            self.display("We now have to turn off the drill",colour="cyan",front="->{ ")
            self.Turn_off_the_drill()   
        else:
            self.scans()


    def scans(self):

        self.display("So I have connected my computer to your console.",colour="cyan",front="->{ ")
        self.display("But you need to do a scan for me to get the results",colour="cyan",front="->{ ")
        
        def scan():

            if not "scan" in self.user.progress:
                self.user.add_to_progress("scan")
            
            Scan_Asteroid.config(state="disabled")
            DrillControls.config(relief="sunk");GUI.update()
            self.display("Getting the readings in now",colour="cyan",front="->{ ")
            self.display("Well looks like we were right, This asteroid is definitely hollow",colour="cyan",front="->{ ")
            self.display("You can see where the rock changes into the egg shell coocon substance",colour="cyan",front="->{ ")
            self.display("The hollow bit is where the thing has eaten it's food",colour="cyan",front="->{ ")
            self.display("And I think this one is much bigger and older than the one we found",colour="cyan",front="->{ ")
            self.display("Probably only got a few thousand years to go",colour="cyan",front="->{ ")


            self.unexpected_vistor()


        DrillControls.config(relief="raise");GUI.update()

        Scan_Asteroid.config(state="normal",command=scan)
        self.display("@@@@@@")

        if "scan" in self.user.progress:
            scan()
        else:
            self.user.Done_This = False
            
            
            
    def unexpected_vistor(self):

        self.display("Large Spaceship emerging from hyperspace and 3 others")
        self.display("Spaceship Connecting")
        self.display("Spaceship Connected")
        
        self.display("Is this Mining Station 634A?",colour="crimson",front="->{ ")

        self.user_response(("Afirmitive ... Do you need help ... sir?",self.under_arrest),("Yes ... this Mining Station 634A",self.under_arrest),("Nope ... sorry ,mate",self.under_arrest))

    def under_arrest(self):

        if "Nope ... sorry ,mate" in self.user.progress:
            self.display("Hmm",colour="crimson",front="->{ ")

        self.display("You are hiding a traitor to the IFoP",colour="crimson",front="->{ ")
        self.display("Hand him over immediately",colour="crimson",front="->{ ")


        self.user_response(("...okay",self.under_arrest_reaction),("What traitor? There isn't anyone on this station",self.under_arrest_reaction),("Never!",self.under_arrest_reaction))

    def under_arrest_reaction(self):

        if "...okay" in self.user.progress:
            self.display("Thank you for your coropation",colour="crimson",front="->{ ")
            self.display("What!",colour="cyan",front="->{ ")
            self.display("Please hand over control of your station to us",colour="crimson",front="->{ ")
            self.display("You can't do this.",colour="cyan",front="->{ ")
            self.display("What about the alien.",colour="cyan",front="->{ ")
            
        elif "What traitor? There isn't anyone on this station" in self.user.progress:
            self.display("Oh, really!",colour="crimson",front="->{ ")
            self.display("Then who's Ship is that docked to your station",colour="crimson",front="->{ ")
            self.display("Don't lie to us!",colour="crimson",front="->{ ")
            self.display("We scanned your station and dectected a lifeform",colour="crimson",front="->{ ")
            self.display("If you do not hand over the traitor we will obliterate your station",colour="crimson",front="->{ ")
            self.display("Well,thanks for trying",colour="cyan",front="->{ ")

        elif "Never!" in self.user.progress:
            self.display("If you do not hand over the traitor we will obliterate your station",colour="crimson",front="->{ ")


        if "...okay" in self.user.progress:
            self.user_response(("I will now hand over control of the station",self.surrender),("I was only buying time, cut communcations",self.cut_communications),("Aplogises, I cannnot do that",self.cut_communications))
        else:
            self.user_response(("Let's Attack",self.cut_communications),("Quick, run!",self.cut_communications),("I surrender!",self.surrender))

    def surrender(self):

        self.display("Ah, good choice",colour="crimson",front="->{ ")
        self.display("What, Don't surrender",colour="cyan",front="->{ ")
        self.display("Handover control? (Y/N)")
        self.display("Please",colour="cyan",front="->{ ")
        self.display("Y",colour="green",front="<-{ ")
        self.display("Handing control over to IFoP Command Spaceship")
        self.display("Thank you for your service",colour="crimson",front="->{ ")
        self.display("Conection lost with Mining Station 634A")

        self.game_over()


    def cut_communications(self):
        self.display("What!",colour="crimson",front="->{ ")
        self.display("Connection to IFoP Command Spaceship lost")

        self.display("Thanks for not handing me over",colour="cyan",front="->{ ")

        if "Let's Attack" in self.user.progress:
            self.display("But I don't think we can attack them",colour="cyan",front="->{ ")
            self.display("1. We don't have any weapons or shields",colour="cyan",front="->{ ")
            self.display("2. They have lots of weapons and powerful shields",colour="cyan",front="->{ ")
            self.display("3. They will oblitorate us due to points one and two",colour="cyan",front="->{ ")

        self.display("What are we going to do?",colour="cyan",front="->{ ")


        self.user_response(("Let's use the Mining Lazor to attack them",self.attack),("You should run away",self.run_away),("We should release the alien!",self.release_the_beast))


        
    def attack(self):

        self.display("Ooh,That's an intresting idea",colour="cyan",front="->{ ")

        self.display("But how would it work?",colour="cyan",front="->{ ")

        self.display("I guess we would have to point the mining lazor at them",colour="cyan",front="->{ ")

        self.display("We would need to release the asteroid",colour="cyan",front="->{ ")
        self.display("And we could use my ship still clamped in to point the station in the correct direction",colour="cyan",front="->{ ")

        self.display("I will connect to my spaceship and turn it on remotely. You release the asteroid",colour="cyan",front="->{ ")

        self.release()

    def run_away(self):

        self.display("Ah, I wish I could.",colour="cyan",front="->{ ")
        self.display("But I'am afraid that they would just catch me before I left this sector",colour="cyan",front="->{ ")
        self.display("Unless...",colour="cyan",front="->{ ")
        self.display("We create a distraction",colour="cyan",front="->{ ")

        self.user_response(("Let's use the Mining Lazor to distract them",self.attack),("You could hack them",self.hack_them),("We could release the alien!",self.release_the_beast))

     
    def hack_them(self):

        self.display("I can't just 'Hack Them'",colour="cyan",front="->{ ")

        self.display("It takes weeks to prepare to hack somthing",colour="cyan",front="->{ ")

        self.display("It takes weeks to prepare to hack somthing",colour="cyan",front="->{ ")

        self.display("You clearly don't understand how hacking works",colour="cyan",front="->{ ")

        self.display("Why don't we release the lifeform?",colour="cyan",front="->{ ")

        self.release_the_beast()

        
    def release_the_beast(self):

        self.display("Hmm... It is highly unscientific though",colour="cyan",front="->{ ")
        self.display("Releasing an unknown lifeform from its egg before it's ready",colour="cyan",front="->{ ")
        self.display("But I don't want the IFoP getting their hands on it either",colour="cyan",front="->{ ")
        self.display("And it's are only chance",colour="cyan",front="->{ ")
        self.display("Lets do it!",colour="cyan",front="->{ ")

        self.display("First we would need to wake the alien up",colour="cyan",front="->{ ")
        self.display("I could probably do that by switching the lazer power store to the scans power store",colour="cyan",front="->{ ")
        self.display("Then run a scan which could distrupt anything",colour="cyan",front="->{ ")

        self.display("You have probably broken away most of rock with the lazer already",colour="cyan",front="->{ ")
        self.display("so It shouldn't be hard to break out of the rock",colour="cyan",front="->{ ")

        self.display("Lets's wake it up!",colour="cyan",front="->{ ")

        self.wake_up()


    def wake_up(self):

        self.display("So I have connected lazer power store to the scans power store.",colour="cyan",front="->{ ")
        self.display("You need to do a scan for me to wake it up",colour="cyan",front="->{ ")
        
        def scan():

            if not "wake up" in self.user.progress:
                self.user.add_to_progress("wake up")
            
            Scan_Asteroid.config(state="disabled")
            DrillControls.config(relief="sunk");GUI.update()
            
            self.display("Getting some readings in now",colour="cyan",front="->{ ")
            self.display("Ship unsteady")
            self.display("It's waking up",colour="cyan",front="->{ ")
            self.display("What did you do?",colour="crimson",front="->{ ")
            
            self.display("I think I can see it",colour="cyan",front="->{ ")
            self.display("It's free!",colour="cyan",front="->{ ")
            
            self.display("What is that thing?",colour="crimson",front="->{ ")

            self.display("It's looks like it has wings",colour="cyan",front="->{ ")
            self.display("and scales",colour="cyan",front="->{ ")

            self.display("IS THAT A GODDAM DRAGON!!!",colour="crimson",front="->{ ")

            self.display("It's magnificent!",colour="cyan",front="->{ ")

            self.display("I should probably use this optiunity to excape!",colour="cyan",front="->{ ")

            self.leaving()


        DrillControls.config(relief="raise");GUI.update()

        Scan_Asteroid.config(state="normal",command=scan)
        self.display("@@@@@@")

        if "wake up" in self.user.progress:
            scan()
        else:
            self.user.Done_This = False
            


    def release(self):

        def released():

            self.display("Releasing asteroid")
            
            
            StationControls.config(relief="sunk")
            Release_Asteroid.config(state="disabled",text="       Secure asteroid       ")
            GUI.update()

            self.positioning()


        StationControls.config(relief="raise")
        Release_Asteroid.config(state="normal",command=released)
        GUI.update()
        
        self.display("@@@@@@")

        if "release" in self.user.progress:
            released()
        else:
            self.user.Done_This = False
            self.user.add_to_progress("release")

    def positioning(self):

        self.display("Ah good we're free",colour="cyan",front="->{ ")

        self.display("I've connected to my ship",colour="cyan",front="->{ ")
        self.display("Hold on",colour="cyan",front="->{ ")

        self.display("Ship tilting",colour="red")
        self.display("5> from original postion",colour="red")
        self.display("10> from original postion",colour="red")
        self.display("25> from original postion",colour="red")
        self.display("30> from original postion",colour="red")
        self.display("45> from original postion",colour="red")
        self.display("85> from original postion",colour="red")
        self.display("100> from original postion",colour="red")
        self.display("Oops bit over",colour="cyan",front="->{ ")
        self.display("95> from original postion",colour="red")

        self.display("In position!",colour="cyan",front="->{ ")
        self.display("Fire it up!",colour="cyan",front="->{ ")
        
        self.user.add_to_progress("In position")
        
        self.Turn_on_the_drill()


    def Turn_on_the_drill(self):

        self.display("@@@@@@@@")

        DrillControls.config(relief="raise")
        GUI.update()

        def Nothing(power):
            pass
        
        def Lazer_power_change(power):
            
            if Lazer_power.get() == 110 and not "boom" in self.user.progress:
                Lazer_power.config(state="disabled",command=Nothing,troughcolor="red")
                DrillControls.config(relief="sunk");GUI.update()
                self.user.add_to_progress("boom")
                self.boom()
                

        

        Lazer_power.config(command=Lazer_power_change)

        Lazer_power.config(state="normal")

        

        if "boom" in self.user.progress and Lazer_power.get() == 0:
            Lazer_power.set(110)
            Lazer_power.config(state="disabled",command=Nothing,troughcolor="red")
            DrillControls.config(relief="sunk")
            GUI.update()
            self.boom()
            
        else:
            self.user.Done_This = False

    def boom(self):

        self.user.add_to_progress("boom")

        self.display("Oh wow!. That's really effective",colour="cyan",front="->{ ")
        self.display("It's burning straight through the hull",colour="cyan",front="->{ ")
        self.display("If it keeps going it will it the nucleur reactor",colour="cyan",front="->{ ")
        self.display("Oh no. The reactor",colour="cyan",front="->{ ")

        self.display("Large Energy readings detected",colour="red")

        self.display("Leg 5 damage detected",colour="red")
        self.display("Leg 1 damage detected",colour="red")

        self.display("Mining Lazor damage dectected",colour="red")
        
        self.display("Leg 4 damage detected",colour="red")
        self.display("Leg 2 damage detected",colour="red")

        self.display("Leg 6 damage detected",colour="red")
        self.display("Leg 3 damage detected",colour="red")
        self.display("Mining Lazor damage dectected",colour="red")
        self.display("Mining Lazor disabled",colour="red")

        self.display("Oh my. What have we done",colour="cyan",front="->{ ")

        self.display("An entire IFoP fleet wiped out",colour="cyan",front="->{ ")

        self.display("By us",colour="cyan",front="->{ ")


        self.user_response(("They were trying to kill us",self.destruction_reaction),("They desevered it",self.destruction_reaction),("Mhm",self.destruction_reaction))


    def destruction_reaction(self):

        if "Mhm" not in self.user.progress:
            self.display("I guess you're right",colour="cyan",front="->{ ")

        self.display("Hey look",colour="cyan",front="->{ ")
        self.display("The asteriod is being pulled back down to the planet",colour="cyan",front="->{ ")

        self.display("The crust should break up upon entry",colour="cyan",front="->{ ")

        self.display("Maybe that is part of the natural lifecycle of the lifeform",colour="cyan",front="->{ ")

        self.display("Pity my team won't get to see this",colour="cyan",front="->{ ")

        self.display("My Team!",colour="cyan",front="->{ ")
        
        self.display("I need to go to them",colour="cyan",front="->{ ")

        self.display("If IFop thought I was a traitor, My team may be in danger!",colour="cyan",front="->{ ")

        self.display("I need to go",colour="cyan",front="->{ ")

        self.leaving()



    def leaving(self):

        self.display("Opening Door")

        self.display("Disconnected from spaceship",time=2)

        self.display("Closing Door")

        self.display("Closing airlock")

        self.display("Depressurising  airlock")
        
        self.display("Opening airlock",time=2)

        self.inside_ship = False

        self.display("Connecting to James B. Qantus's space ship")

        self.display("Closing airlock",time=2)


        self.display("Open the clamps",colour="cyan",front="->{ ")
                
        
        def open_clamps():

            Open_Docking_Clamps.config(state="disabled")
            StationControls.config(relief="sunk")
            GUI.update()

            self.display("Spaceship starting up",time=2)
                
            self.display("Spaceship disingaged",time=2)
            
            self.display("Spaceship moving away",time=2)

            self.display("Goodbye",colour="cyan",front="->{ ")

            if "wake up" in self.user.progress:
                self.display("Out here I can see it in all it's entirety",colour="cyan",front="->{ ")
                self.display("It looks like it is going back down to the planet",colour="cyan",front="->{ ")
                self.display("I will need to go back and tell my team about all of this",colour="cyan",front="->{ ")
                self.display("I also better go before the IFoP comes to it's senses",colour="cyan",front="->{ ")
                self.display("Thanks for helping free the lifeform",colour="cyan",front="->{ ")
                
                
            else:
                self.display("Thanks for helping me and saving my life",colour="cyan",front="->{ ")


                
            self.display("Spaceship jumped to hyperspace")

            
            self.game_over()
        


        Open_Docking_Clamps.config(state="normal",command=open_clamps)
        StationControls.config(relief="raised")
        GUI.update()

        if "Bye" in self.user.progress:
            open_clamps()
        else:
            self.user.Done_This = False
            self.user.add_to_progress("Bye")

        

    def unfinished(self):

        self.display("Sorry, this part of the story isn't finished yet",colour="yellow")
                    
        self.retry()

    def game_over(self):

        if "boom" in self.user.progress:
            ending = "WEAPON OF MASS DESTRUCTION"
        elif "I will now hand over control of the station" or "I surrender!" in self.user.progress:
            ending = "I SURRENDER"
        elif "story" and "No" in self.user.progress:
            ending = "BETRAYAL!"
        elif "How do you turn this thing off???" in self.user.progress:
            ending = "HOW DID YOU GET THIS JOB!"
        elif "Goodbye Doctor" or "Go away!!!" or "No!" in self.user.progress:
            ending = "REJECTED!"
        elif "No" in self.user.progress:
            ending = "MAD MAN!"
        else:
            ending = "BORING"

        self.display("You got the " + ending + " Ending",colour="yellow")
        
        self.display("GAME OVER",front="\n    ",colour="red")
        self.display("\n",front="")

        print(self.user.progress)


        self.retry()

        

    def retry(self):

        self.display("Would you like to go back?",colour="yellow")

        B = Button(Terminal,text="Go back one",command=lambda: self.go_back())
        Buttons.append(B)
        Terminal.window_create(END, window=B) #insert button

        S = Spinbox(Terminal,from_=2,to=100,width=2,borderwidth=4)

        B = Button(Terminal,text="Go back [",command=lambda: self.go_back(number=int(S.get())))
        Buttons.append(B)
        Terminal.window_create(END, window=B) #insert button

        Terminal.window_create(END, window=S)



        B = Button(Terminal,text="Quit",command=lambda:GUI.destroy())
        Buttons.append(B)
        Terminal.window_create(END, window=B) #insert button

        

            
        Terminal.insert(END,"\n")
        Terminal.config(state="disabled") #make text non change able

        GUI.update()

        Terminal.see("end")

    def go_back(self,number=1):
        global Lazer_power

        print(self.user.progress)
        self.user.progress = self.user.progress[:-(number)]
        

        user_data = shelve.open(self.user.name)#open user data
        user_data['progress'] = self.user.progress
        
        user_data.close()

        Terminal.config(state="normal") #so we can edit
        Terminal.delete('1.0', END)#delete everything
        Terminal.config(state="disabled") #so the user can't edit


        if "phew" in self.user.progress:
            Lazer_power.set(0)
        elif "wrong_way" in self.user.progress:
            Lazer_power.set(110)
        else:
            Lazer_power.set(100)


        self.user.Done_This = True
        
        self.Start()
        
        

def setup():
    global User,Story
    
    User = User()

    try:
        Story = Story(User)
    except _tkinter.TclError:
        print("!")


GUI.after(1,setup)
mainloop()



