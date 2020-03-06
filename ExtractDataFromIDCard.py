# https://fr.wikipedia.org/wiki/Carte_nationale_d%27identit%C3%A9_en_France
#!/usr/bin/env python3

import sys
import string
from datetime import datetime

def compute_checksum(code):
    result = 0
    i = -1
    factor = [7, 3, 1]
    
    for c in code:
        if c == '<':
            value = 0
            i += 1
        elif c in "0123456789":
            value = int(c)
            i += 1
        elif c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            value = ord(c) - 55
            i += 1
        result += value * factor[i%3]
        
    return result%10

data = None
# No data passed as an argument, then ask for input
if len(sys.argv) < 2:
    data = input("Please enter the data contained in the MRZ Border, should be 2 lines of 36 chars:\n")
else:
    data = sys.argv[1]
    

# Data length should be equal 72, if not, it's missing something
if len(data) != 72:
    print("You didn't enter all the data or you either entered too much data, please double check it.\n")
    sys.exit(1)

# Parse the data
# First line
header = data[:2]
country = data[2:5]
lastname = data[5:30]
administrationcode = data[30:36]

# Second line
# First part
emissiondate = data[36:40]
kindadept = data[40:43]
someid = data[43:48]
checksum = data[48]

# Second part
name = data[49:63]
birthdate = data[63:69]
checksum_1 = data[69]
gender = data[70]
ultimate_checksum = data[71]

# Do some processing on names
lastname = lastname.replace("<", " ")
lastname = lastname.strip()
name = name.replace("<<", " ")
name = name.replace("<", "-")
name = string.capwords(name)

# Replace M by Male and F by Female
if gender == 'M':
    gender = "Male"
else:
    gender = "Female"

# Convert the dates
if int(emissiondate[:2]) >= 88:
    emissiondate = datetime.strptime(emissiondate, '%y%m').strftime('%B 19%y')
else:
    emissiondate = datetime.strptime(emissiondate, '%y%m').strftime('%B 20%y')

birthdate = datetime.strptime(birthdate, '%y%m%d').strftime('%d %B %y')

print("Country: {}\nCard Owner:\n\tName:      {} {}\n\tBirthdate: {}\n\tGender:    {}\n".format(country, lastname, name, birthdate, gender))
print("Card Info:\n\tAdministration Code: {}\n\tEmission Date: {}\n\tMirror of 3 first characters of administration code: {}\n\tNumber related to request date and emission place: {}".format(administrationcode, emissiondate, kindadept, someid))

# Check checksums
# Compute and check first checksum
realchecksum = compute_checksum(data[36:48])
if realchecksum != int(checksum):
    print("/!\\ ERROR: Checksum at 13rd character of second line /!\\")
    print("This is most likely a fake ID card")
    print("Found {}, excepted {}".format(checksum, realchecksum))
    sys.exit(1)
    
realchecksum = compute_checksum(data[63:69])
if realchecksum != int(checksum_1):
    print("/!\\ ERROR: Checksum at 34th character of second line /!\\")
    print("This is most likely a fake ID card")
    print("Found {}, excepted {}".format(checksum_1, realchecksum))
    sys.exit(1)
    
realchecksum = compute_checksum(data[:71])
if realchecksum != int(ultimate_checksum):
    print("/!\\ ERROR: Checksum at last character of second line /!\\")
    print("This is most likely a fake ID card")
    print("Found {}, excepted {}".format(ultimate_checksum, realchecksum))
    sys.exit(1)


