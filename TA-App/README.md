# TA-App
Software Engineering Fall 2018 Project, Sprint 2

# Web Page Usage
## Minor Commands
    login - To login. Usage: login username password
    logout - To logout. Usage: logout
    help - To get a small print out of a command. Usage help command or just help

## Major Commands
    Strucured as such:
    $ <Command> <Action> <Fields/Args>
    
    Fields and args can go in any order.
    Use the code arg to combine dept, cnum, and snum. Not all are needed but if you have a cnum you must have a dept and if you have a snum you must have a cnum. EX: code=CS-361-401 (code=dept-cnum-snum)
    
    Major Commands:
      Course  
      Section  
      User  
    
    Actions:
      add - Adds what you give it
      delete - Deletes a specific one
      edit - To edit a specific one
      view - Leave blank to view all
     
    Course Fields:
        Required Fields (except for when viewing all):
            dept - The department (will be set as the first part when using code=)
            cnum - The course number (will be set as the second part when using code=)
            
        Optional Fields:
            name - The course name (can have spaces EX: name=Software Engineering)
            description - The course description (can have spaces desc=A really fun course) 
            snum - The section number (will be set as the third part when useing code=)
            instructor - The username of the instructor
            
    Section Fields:
        Required Fields (except for when viewing all):
            dept - The department (will be set as the first part when using code=)
            cnum - The course number (will be set as the second part when using code=)
            snum - The section number (will be set as the third part when useing code=)
            
        Optional Fields
            instructor - The username of the instructor (must be a TA)
            type - The type of section (Discussion, Lab, Other)
            days - The days the section is on
            room - The room that that the section is in
            time - The time that the section is
            
    User Fields:
        Required Fields (except for when viewing all):
            username - The username
            password - The password
            role - The role of the user. Must be either TA, Instructor, Administrator, or Supervisor
            
        Optional Fields:
            address - The address of the user 
            phone_number - The phone number of the user
            email - The email address of the user

### Examples

    Department(dept) and course number(cnum) are required field to add a course
      
    $ Course add dept=CS cnum=351
    $ Course add dept=CS cnum=351 snum=802
    $ Course add dept=CS cnum=351 snum=802 ins=Rock
    $ Course add code=CS-351-802 ins=Rock
    
    $ User add user=Foo 
    $ User add user=Foo password=abc123 
    $ User add user=Foo password=abc123 role=TA
    
    $ Section add dept=CS cnum=351 snum=802
    $ Section add dept=CS cnum=351 snum=802 ins=Rock
    
