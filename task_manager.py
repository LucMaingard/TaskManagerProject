import datetime
from datetime import datetime
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove
import os.path
from os import path
import time

#define functions 
#register new user
def reg_user(new_user, new_user_pw, pw_check):
    new_user = new_user
    new_user_pw = new_user_pw
    pw_check = pw_check

    #check if username already exists
    for item in login_info_list:
        if new_user in item:
            username_exists = True
            if username_exists == True:
                print("\nThere is already a user with this username!\nPlease choose another\n ")
                new_user = input("Choose a new username: ")
        else:
            username_exists = False

    #check pw's entered match
    while new_user_pw != pw_check:
        print("Passwords did not match")
        new_user_pw = input("Enter your password again: ")
        pw_check = input("Confirm password again: ")
    if new_user_pw == pw_check:
        with open("user.txt", "a") as f:
            f.write(new_user + ", " + new_user_pw + "\n")
            print("\nNew user has been added!\n")
            f.close()

def add_task(username):
    #check admin in signed in
    if username == "admin":
        user_assigned = input("Enter the username this asked is assigned to: ")
        task_title = input("Enter the title of the task: ")
        task_descript = input("Enter a description of the task: ")
        due_year = input("Enter the year this task is due: ")
        due_month = input("Enter the month this task is due: eg. [Jan] [Feb] ")
        due_day = input("Enter the day this task is due: ")
        due_date_str = due_day + " " + due_month + " " + due_year
        due_date = datetime.strptime(due_date_str, '%d %b %Y').date()
        date_assigned = datetime.today().date()
        completed = "No"
    else:
        print("\nYou are not authorised to perform this action")
        print("\nPlease log in as admin to perform this task:\n")
        exit()

        #write info to tasks
    with open("tasks.txt", "a") as f:
        f.write(f"\n{user_assigned}, {task_title}, {task_descript}, {date_assigned}, {due_date}, {completed}")
        print("The task has been added and assigned")
        
#create function for viewing all tasks
def view_all():
    with open("tasks.txt", "r") as f:
        for line in f:
            line_components = line.split(",")
            title = line_components[1]
            user = line_components[0]
            date_assigned = line_components[3]
            due_date = line_components[4]
            complete = line_components[-1]
            description = line_components[2]
            print(f"\nTask:\t\t\t{title}\nAssigned to:\t\t{user}\nDate assigned:\t\t{date_assigned}")
            print(f"Due date:\t\t{due_date}\nTask complete? \t\t{complete}Task description:\n\t{description}")

#create function for viewing signed in users tasks
def view_mine(username):
    i = 1
    with open("tasks.txt", "r+") as f:
        for line in f:
            line_components = line.split(",")

            #show all tasks with username same as logged in user
            if line_components[0] == username:
                title = line_components[1]
                user = line_components[0]
                date_assigned = line_components[3]
                due_date = line_components[4]
                complete = line_components[-1]
                description = line_components[2]
                print(f"\nTask [{i}]:\t\t\t{title}\nAssigned to:\t\t{user}\nDate assigned:\t\t{date_assigned}")
                print(f"Due date:\t\t{due_date}\nTask complete? \t\t{complete}\nTask description:\n\t{description}")
                i += 1

#define function to complete task
def complete_task(task_select):
    task_select = task_select
    task_select_space = " " + task_select 

    #make new temp file for rewriting changes
    fh, abs_path = mkstemp()
    with fdopen(fh, 'w') as new_file:
        with open("tasks.txt", "r") as old_file:
            for line in old_file:
                line_components = line.strip().strip(" ").split(",")

                #find task to complete by title and change no to yes
                if line_components[1] == task_select_space:
                    new_file.write(line.replace("No", "Yes"))
                else:
                    new_file.write(line) 
    
    #move new file to tasks.txt
    copymode("tasks.txt", abs_path)
    remove("tasks.txt")
    move(abs_path, "tasks.txt")

#define function to change duedate of task
def date_change(task_select):

    #create variable to id the task chosen
    task_select = task_select
    task_select_space = " " + task_select 

    #get new inputs
    year = input("Enter the year this task is due: ")
    month = input("Enter the month this task is due: ")
    day = input("Enter the day this task is due: ")
    due_date_str = day + " " + month + " " + year
    due_date_new = datetime.strptime(due_date_str, '%d %b %Y').date()

    #create temp new file to reite lines to with changed info
    fh, abs_path = mkstemp()
    with fdopen(fh, 'w') as new_file:
        with open("tasks.txt", "r") as old_file:
            for line in old_file:
                line_components = line.strip().strip(" ").split(",")
                
                #check the task is incomplete
                if line_components[-1] == "Yes":
                    print("\n******   This task has already been completed and cannot be edited   *******\n")
                    break
                
                #get line for editing
                elif line_components[1] == task_select_space and line_components[-1] == "No":
                    new_file.write(line.replace(line_components[4], str(due_date_new)))

                else:
                    #write the other lines unchanged
                    new_file.write(line)

    #move new file to tasks.txt
    copymode("tasks.txt", abs_path)
    remove("tasks.txt")
    move(abs_path, "tasks.txt")
    print(f"\nYou successfully updated the duedate of task: {task_select}")

#function to display user_choice message
def user_action():
    if username == "admin":
        print("\nPlease select one of the following options:\n")
        print("r\t-\tregister user\na\t-\tadd task\nva\t-\tview all tasks\nvm\t-\tview my tasks\ngr\t-\tgenerate reports\nds\t-\tdisplay statistics\ne\t-\texit\n")
        user_choice = input("What would you like to do? ")
        return user_choice
    else:
        print("\nPlease select one of the following options:\n")
        print("r\t-\tregister user\na\t-\tadd task\nva\t-\tview all tasks\nvm\t-\tview my tasks\ngr\t-\tgenerate reports\ne\t-\texit\n")
        user_choice = input("What would you like to do? ")
        return user_choice

#define function to locate and return index of username in login_info_list for pw check
def deep_index(lst, w):
    return [(i, sub.index(w)) for (i, sub) in enumerate(lst) if w in sub]

#define function for generating reports 
def generate_reports(username):

    line_count = 0
    user_line_count = 0
    user_completed_count = 0
    completed_count = 0
    overdue = 0
    user_overdue = 0

    with open("tasks.txt", "r") as f:
        for line in f:
            
            #strip and split line into components
            line_comp = line.strip().split(",")
            line_count += 1
            
            #if completed add to comp count else check if due date is before todays date, it not add count to overdue
            if line_comp[-1] == "Yes":
                completed_count += 1
            else:
                due_date = line_comp[4].strip()
                due_date_conv = datetime.strptime(due_date, "%d %b %Y").date()
                if due_date_conv < datetime.today().date():
                    overdue += 1

    total_uncompleted_tasks = line_count - completed_count
    percent_total_incomp = round((((line_count - completed_count)/line_count)*100), 0)
    percent_total_overdue = round(((overdue/line_count)*100), 0)

    #open and write report
    with open("task_overview.txt​", "w") as f:
        f.write(f"The total tasks:\t\t\t{line_count}\n")
        f.write(f"The total completed tasks:\t\t{completed_count}\n")
        f.write(f"The total uncompleted tasks: \t\t{total_uncompleted_tasks}\n")
        f.write(f"The total overdue tasks:\t\t{overdue}\n")
        f.write(f"The percentage incomplete tasks: \t{percent_total_incomp}\n")
        f.write(f"The percentage overdue tasks: \t\t{percent_total_overdue}\n")

    #open tasks.txt to read and create user_overview.txt  
    with open("tasks.txt", "r+") as f:
        for line in f:
            line_components = line.strip().split(",")

            #show all tasks with username same as logged in user
            if line_components[0] == username:
                user_line_count += 1

                #increase count of users completed tasks
                if line_comp[-1] == "Yes":
                    user_completed_count += 1
                else:
                    due_date = line_comp[4].strip()
                    due_date_conv = datetime.strptime(due_date, "%d %b %Y").date()
                    if due_date_conv < datetime.today().date():
                        user_overdue += 1

    
    percent_user_tasks = round(((user_line_count/user_line_count)*100), 2)
    percent_user_comp = round(((user_completed_count/user_line_count)*100), 2)
    percent_user_uncomp = round((((user_line_count - user_completed_count)/user_line_count)*100), 2)

    #open and write report
    with open("user_overview.txt​", "w") as f:
        f.write(f"The total tasks for username:\t\t\t\t\t{username}: {user_line_count}\n")
        f.write(f"The percentage of tasks assigned to username: \t\t\t{username}: {percent_user_tasks}\n")
        f.write(f"The percentage of completed tasks assigned to username:\t\t{username}: {percent_user_comp}\n")
        f.write(f"The percentage of uncompleted tasks assigned to username:\t{username}: {percent_user_uncomp}\n") 

#function to display statistics
def stats(username):  
    #if file exists print lines in file 
    print("\n\n-----TASK OVERVIEW-----\n\n")
    with open("task_overview.txt​", "r") as f:
        for line in f:
            strip_line = line.strip()
            print(strip_line)
            
    #if tasks_overview exisit - so will user_overview
    print(f"\n\n-----USER TASK OVERVIEW-----\n\nuser: \t{username}\n")
    with open("user_overview.txt​") as f:
        for line in f:
            strip_line = line.strip()
            print(strip_line)

#function to check if files exist
def check_file_exisit():
    check_task = os.path.exists('./task_overview.txt​')
    if check_task == False:
        username_rep = input("Enter the username for report on: ")
        generate_reports(username_rep)
        stats(username_rep)
    else:
        return check_task

#get login details from user
username = input("Enter your username: ")
pw = input("Enter your password: ")
correct_credentials = False
login_info_list = []
username_in_list = False
username_exists = False

#open user.txt file to check login credentials
with open("user.txt", "r") as f:

#check the user name is valid, then check pw 
    for line in f:

        #split and replace unwanted characters for login info
        login_info = line.replace("\n", "").replace(" ", "").split(",")
        login_info_list.append(login_info)

#while username is not valid
while not username_in_list:
    for item in login_info_list:            #check lists (username and pw pairs) in login_info_list
        if username in item:                #if username found in list, get its index, and matching pw index
            user_info_index = deep_index(login_info_list, username)
            username_index = user_info_index[0][0]
            pw_match = login_info_list[username_index][1]
            username_in_list = True
    #require username reentry if incorrect
    if username_in_list == False: 
        print("The username you entered was not valid, please re-enter: \n")
        username = input("Enter your username: ")

#check if pw entered matches stored pw
while pw != pw_match:
    pw = input("The password you entered was incorrect: ")

#print successful message and change correct_credentials = True
print("\nYour login was successful! :)\n")
correct_credentials = True

#if login credentials true get user choice
if correct_credentials == True:
    user_choice = user_action()

#check userchoice and get user credentials for new user. if passwords match create new user
#exit loop when user_choice = e
while user_choice != "e":
    if user_choice == "r":
        new_user = input("Enter the new users username: ")
        new_user_pw = input("Enter your password: ")
        pw_check = input("Confirm password: ")
        reg_user(new_user, new_user_pw, pw_check)
        user_choice = user_action()

    #call add task func to add new task to task.txt
    elif user_choice == "a":
        add_task(username)
        user_choice = user_action()

    #call view all function to show functions
    elif user_choice == "va":
        view_all()
        user_choice = user_action()

    #call view_mine function and ask if user want to edit
    elif user_choice == "vm":
        view_mine(username)
        
        #ask user if they want to edit/complete task and print accompanying messages
        task_select = input("\nEnter the title of the task you would like to edit. ([-1] to return to main menu): \n")
        #if user selects -1 the main menu returns 
        if task_select == "-1":
            user_choice = user_action() 

        else: #task_select != "-1":
            print("\nWould you like to edit or complete a task?\n")
            print("c\t\t-\t\tcomplete task\ned\t\t-\t\tedit task\n")
            edit_complete = input("Edit or complete? [ed] [c]: ")

        #depending on user input call functions to edit or complete 
        if edit_complete == "ed":
            date_change(task_select)
            user_choice = user_action()

        elif edit_complete == "c":
            complete_task(task_select)
            user_choice = user_action()
    
    #generate reports if user selects gr
    elif user_choice == "gr":
        username_rep = input("Enter the username for report on: ")
        generate_reports(username_rep)
        user_choice = user_action()

    #display stats from user report
    elif user_choice == "ds":
        check_task = check_file_exisit()
        if check_task == True:
            stats(username)
            user_choice = user_action()
            break

    else:
        print("You did not select a valid option, please re-select\n")
        user_choice = user_action()

#if user selects e exit
if user_choice == "e":
    print("\nHave a nice day :)\n") 
