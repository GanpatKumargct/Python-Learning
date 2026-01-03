
# 3
#
import pyjokes as pp;


print(pp.get_joke())

import pyttsx3
engine = pyttsx3.init()

# For Mac, If you face error related to "pyobjc" when running the `init()` method :
# Install 9.0.1 version of pyobjc : "pip install pyobjc>=9.0.1"

engine.say("hey im a abhimanyu sing, a 3rd year student")
engine.runAndWait()



# 4
import os

# specify the directory (use "." for current directory)
directory = "/"

# get the list of files and folders
contents = os.listdir(directory)

# print them
print("Contents of the directory:")
for item in contents:
    print(item)
