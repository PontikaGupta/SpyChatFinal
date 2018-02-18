#Details of spy imported from spy_details file
from spy_details import spy
from spy_details import Spy,ChatMessage,friends, chats
from steganography.steganography import Steganography
import csv



#Welcome message
print"Hello!!"
print"Welcome to Spychat"
print"Let's get started"


#List for storing old and new status
status_messages = ["i'm in gym","sleeping","Busy","At work"]
friends = []
new_chat = []

#Function defines to load friends
def load_friends():
    with open('friends.csv', 'rb') as friends_data:
        reader = list(csv.reader(friends_data))

        for row in reader[1:]:
            if row:
                name = row[0]
                age = row[1]
                rating = row[2]
                online = row[3]
                spy = Spy(name, age, rating, online)
                friends.append(spy)


# Defining  load chat function to load the chat when application starts
def load_chats():
    with open('chats.csv', 'rb') as chats_data:
        reader = list(csv.reader(chats_data))

        for row in reader[1:]:
            if row:
                time = row[0]
                sender=row[1]
                message_sent_to =row[2]
                text = row[3]
                sent_by_me = row[4]
                chats.append(new_chat)

load_friends()

#Function define for Current or old status update
def add_status(current_status_message):

    # Checks the old status
    if current_status_message != None:
        print "Your current status message is: " + current_status_message
    else:
         print"\nYou don't have any status currently!"


    status = raw_input("Do you want to select from old stauts? Y or N   ")
    if len(status) >=1:

        if status.upper() == 'Y':
            serial_no = 1

            for old_status in status_messages:
                print "%d . %s " % (serial_no, old_status)
                serial_no = serial_no + 1
            user_selection = input("Which one do you want to select ::   ")
            if len(status_messages) >= user_selection:
                new_status = status_messages[user_selection - 1]
            else:
                print "invalid selection"
            return new_status

        elif status.upper() == "N":
            new_status = raw_input("Enter your new status::")
            if len(new_status) > 1:
                status_messages.append(new_status)
            else:
                 print("Please enter something atleast...")
            return new_status

        else:
            print "invalid entry"


    else:
        set_status = 'No status'
        return set_status

#Function define ro qdd new freind
def add_freind():
    new_friend =Spy("",0,0.0,True)
    new_friend.name = raw_input("What is the name of friend ? ")
    new_friend.salutation = raw_input("What should we call you ? (Mr. or Ms.) ")
    new_friend.name=new_friend.salutation + " " + new_friend.name
    new_friend.age = input("What is the age of friend ? ")
    new_friend.rating=input("What is your rating ? ")

    if len(new_friend.name)>=3 and 50>=new_friend.age and new_friend.rating>=spy.rating:
        friends.append(new_friend)
        print "friend is added"
        with open('friends.csv', 'a') as friends_data:
            writer = csv.writer(friends_data)
            writer.writerow([new_friend.name, new_friend.age, new_friend.rating, new_friend.is_online])
    else:
        print "Freind cannot be added"
    return len(friends)
#Function define for select new freind
def select_a_friend():
    serial_no = 1
    for friend in friends:
        print  str(serial_no)+" "+friend.name
        serial_no = serial_no +  1
    user_selected_friend=input("Select your friend:: ")
    user_index= user_selected_friend -1
    return user_index

#Function defines for send the secret message
def send_message():
    user_index=select_a_friend()
    original_image=raw_input("What is the name of your image ? ")
    text=raw_input("What is your secret message ? ")
    output_path=raw_input("Enter the name of your secret message image  with extension :: ")
    Steganography.encode(original_image,output_path,text)
    new_chat= ChatMessage(text,True)
    with open('chats.csv', 'ab') as chats_data:
        write = csv.writer(chats_data)
        write.writerow([spy.name, friends[user_index].name, new_chat.message, new_chat.time, new_chat.sent_by_me])

    friends[user_index].chats.append(new_chat)
    print "your  message encrypted successfully..."
    print "The  encrypted message is saved in  "+ output_path +" image . "


#Function Defines for Sending  help message
def send_help_message():
     friend_choice = select_a_friend()
     text = raw_input("Enter the Rescue message for your friend")
     new_chat = ChatMessage(text,False)
     friends[friend_choice].chats.append(new_chat)


#Function defines  for reading the secret meassage
def read_message():

    sender = select_a_friend()
    output_path = raw_input("What is the name of the file you want to decode? ")

    try:
        #To decryept  the message
        secret_text = Steganography.decode(output_path)
        print ("Your secret message is:")
        print (secret_text)

        new_text = (secret_text.upper()).split()

        # To check the help or emergency message
        if 'SOS' in new_text or 'SAVE ME'in new_text or 'HELP ME' in new_text or 'ALERT' in new_text :
            print "Plzzz help me!!!!"
            print "Select the friend to send a helping message.\n"
            send_help_message()
            print "Message sent successfully to your frined...."
            new_chat = ChatMessage(secret_text, False)
            friends[sender].chats.append(new_chat)


        else:
            new_chat = ChatMessage(secret_text, False)
            friends[sender].chats.append(new_chat)
            print "Your secret message has been saved.\n"

    # No secret message
    except TypeError:
        print "\n Sorry! There is no secret message in the image"



#Function define for read the chat history
def read_chat_history():
    friend_choice = select_a_friend()

    print '\n'

    for chat in friends[friend_choice].chats:
        if chat.sent_by_me:
            print " Chatting Time" + str(chat.time.strftime("%d %B %Y %A %H : %M")) + ","
            print " Sender : You  "
            print "Message : " +str(chat.message)

        else:
             print str(chat.time.strftime("%d %B %Y %A %H : %M"))+ ","
             print str(friends[friend_choice].name) + " : "
             print str(chat.message)


#Function defines for removing the friend
def remove_friend():
    friend_choice = select_a_friend()
    del friends[friend_choice]
    print ("Friend has been removed !")
    return len(friends)




#Function defines for menu and status
def start_chat(spy_name,spy_age,spy_rating):
    current_status_message = None

    #for creating menu
    show_menu = True
    while show_menu:
        menu_choice=input("\n What do you want to do? \n 1. Add a status update\n 2. Add new freind \n 3. Send a message\n 4. Read a  message \n 5. Read chats  \n 6. Remove a friend \n 0. Exit \n   ")

        # For adding new status
        if (menu_choice == 1):
            current_status_message = add_status(current_status_message)

            if len(current_status_message) >= 1:
                if current_status_message == 'No status':
                    print "You didn't select the status correctly"
                else:
                    print "Your status has set to   %s" % (current_status_message.upper())
            else:
                print "You didn't select the status correctly"

        elif menu_choice==2:
            no_of_frnds=add_freind()
            print "You have " +str(no_of_frnds) + " friend . "
        elif menu_choice==3:
             send_message()
        elif menu_choice==4:
            read_message()
        elif menu_choice==5:
            read_chat_history()
        elif menu_choice==6:
             no_of_frnds=remove_friend()
             print "You hsve " +str(no_of_frnds) + "friends"
        elif menu_choice == 0:
            show_menu = False
        else:
            print "Invalid Choice"


#For  checking the existing user
spy_exist=raw_input("Are you existing Spy? Y or N :: ")

if spy_exist.upper() == "Y":
    print "We already have your details..."
    start_chat(spy.name, spy.age, spy.rating)

elif spy_exist.upper() == "N":


   # For New Spy Profile
   spy.name=raw_input("What is your spy name?\n")

   if len(spy.name)>=2:

        print"Welcome " + spy.name.title() + ", Glad to meet you. "
        spy.salutation=raw_input("What should we call you (Mr. or Ms.)?\n")

        if (spy.salutation)>0:

            spy.name= spy.salutation.capitalize() + ". " + spy.name.title()
            print"Alright " +spy.name + " . I'd like to know a little bit more about..."
            spy.age=input("Enter Your Age :: ")

            if spy.age > 12 and spy.age < 50:

                print "Your age is fine to be a spy..."
                spy.rating=input("Enter Your Rating :: ")

                if spy.rating>=5:
                    print "Great Spy"
                elif spy.rating>=4.5 and spy.rating<5:
                    print "Good Spy"
                elif spy.rating>=3.5 and spy.rating<4.5:
                    print "Average Spy"
                else:
                    print "Bad Spy"

                #For checking Spy's online status
                spy_is_online=True
                print "Authentication Complete. Welcome  %s  Age:  %d  And Rating of: %.2f Proud to have you on board" %(spy.name,spy.age ,spy.rating )
                start_chat(spy.name,spy.age,spy.rating)

            else:
                print "Your age is not fine to be a spy..."
        else:
            print"Invalid Salutation..."
   else:
        print"Invalid name!! please enter a 3 letters name atleast..."
else:
       print "Wrong Input..."