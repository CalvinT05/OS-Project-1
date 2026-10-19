Session 1

Goals:
- Create and clone repository
- Download and push boilerplate code from project description
- Create driver, logger, and encryption files
- Define classes and functions based on project description

# 10/18/2026 2:35pm
I am going over the project description and rubric. I am to create a program with multiple concurrent processes. It is supposed to encrypt/decrypt a string using the Vigenere algorithm and allow the user to set the key used for the algorithm. Additionally, the users inputs need to be saved and be able to be selected and every action needs to be logged. The program can be divded into 3 sections: the driver, encryption, and the logger.

# 10/18/2026 2:58pm
I am going to start by creating the GitHub repository and cloning it locally. I also downloaded and unzipped the python_process.zip file and see that it contains an example of how to set up the processes and use the I/O pipes. I think I will try to implement the functions first before worrying about the processes. Before that, I need to plan out the classes and functions.

# 10/18/2026 3:55pm
For defining classes and functions, I started with the easiest first. For the logger, I needed a function to format the message and turn it into a log entry. For the encryption, I needed a encrypt and decypt function, a service class that parses a command and runs corresponding functions. For the driver, it needs to start/stop the logger and encryption client processes and send and recieve messages via pipes, have a history class to store, print, and select the user inputs, read commands and run the corresponding functions.

Session 2

Goals:
- Code the Vigenere encryption and decryption algorithms
- Code the logger functionality
- Implement input validation
- Test the encrypt/decrypt and logger functions with unit tests
- Implement the messaging system in each process

# 10/18/2026 4:21pm
I was thinking about how the cpu.py and mem.py example maps onto this project. The driver is like cpu.py, since it starts a child process, writes commands, and reads replies. The encryption program is like mem.py, since it loops on stdin and answers each command, but the logger only receives. I decided to keep the cipher as functions separate from the class that stores the passkey, so I can test it with unit tests. I am starting with vigenere_encrypt and vigenere_decrypt now.

# 10/18/2026 5:42pm
I finished both cipher functions. Each letter gets shifted by the matching key letter, and the key wraps around using the index mod the key length. I checked them with example in the project description and it matched. I then wrote the EncryptionService class with a handle function that splits a command line into the command and its argument. Started writing unit tests and got an AttributeError, no attribute 'svc'. I had named my setup method create_instance, but unittest only runs one named setUp. Renaming it fixed the error. In the logger, format_entry crashed because I used import datetime, which gives the module and not the class, so datetime.now() doesn't exist. Switched to from datetime import datetime and gave the now parameter a default so the tests can pass in a fixed time.

# 10/18/2026 6:59pm
I realized the lines read from stdin end in a newline, so the message "PASS HELLO" was giving the argument "HELLO\n", which failed the alpha only check. Added strip() before splitting in both the logger and the encryption service. I also changed my error message to ERROR Password not set so it matches the example in the project description. Wrote main for both programs, with a flush after every printed response so the driver won't hang waiting on a reply.

Session 3

Goals:
- Code the driver file
- Implement concurrent processes
- Implement inter process communication with pipes
- Priority: get the program and password + exit commands running (with logging)

# 10/18/2026 8:31pm
Since the last session I have been thinking about the pipe part, since it is the piece I understand least. The driver writes a command and then blocks on readline until the child answers, so the child has to flush every response or both sides wait forever. That is why I want one line out for every line in from the encryption program. I was also wondering if the processes actually run in parallel. They are separate processes, but the driver and the encryption program take turns because of the blocking read. Only the logger can really overlap, since the driver never waits for it. I am starting on the driver file now.

# 10/18/2026 9:12pm
I wrote the LoggerClient and EncryptionClient classes with Popen. I changed both to launch the real scripts and pass the log file name to the logger. Also, I found two missing sets of parentheses, flush and select, so the methods were never actually called. Then got a Popen __del__ error and an IndexError from logger.py, which means the logger was started without a log file argument. I traced the file name through main, Driver, and LoggerClient and fixed it. The password command now works end to end, and the log file shows START, COMMAND, RESULT, and EXIT lines in the order they happened.

Session 4

Goals:
- Implement the encrypt/decrypt and history with logging
- Test all commands with various cases
- Debug pipes (I/O flushing issues)
- Clean up the user interface
- Clean up code

# 10/18/2026 9:46pm
I have been rereading the project description, mostly the history section. For the history, I would like password, encrypt, and decrypt to each have their own, so I need to decide whether that is okay. It actually says the entered password is not stored in history, so it does not make sense to do so. I also want to make sure shutdown is clean, meaning QUIT goes to both children and the driver waits on them before exiting, because that is what the project is really testing. I am now starting on encrypt, decrypt, and history now.

# 10/18/2026 10:34pm
I implemented encrypt, decrypt, and history. I added letters-only validation in the driver so bad input like "Hello World!" is rejected before it reaches the encryption program. I then tested all the commands, including invalid input, an unknown command, a bad history number, and closing input early. I also wrapped the main loop so ctrl-c or a closed input still sends QUIT to both child processes and logs the exit. Remaining cleanup: log invalid history selections, and decide whether passwords should be kept in history, since the spec says they shouldn't.