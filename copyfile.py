import os
import subprocess
import sys
import usb.core
import usb.util


DELAY = 1000
DEFAULT_DELAY = 50
DESTINATION_KEYBOARD = "ch"


if ((len(sys.argv) < 2)):
    print "Usage : \"python copyfile.py source\""
    sys.exit(1)

if not os.path.isfile(sys.argv[1]):
    print "Error : " + sys.argv[1] + " not found"
    sys.exit(1)

toEncodePath = "duckyscript"
if os.path.isfile(toEncodePath):
    os.remove(toEncodePath)

fout = open(toEncodePath, 'w')
fout.write("DELAY " + str(DELAY) + "\n")
with open(sys.argv[1], 'r') as fin:
    for line in fin:
        fout.write("STRING " + line)
        fout.write("ENTER\n")
fout.close()
fin.close()
subprocess.call(['java', '-jar', 'Encoder/encoder.jar', '-i', toEncodePath, '-l', DESTINATION_KEYBOARD])
os.remove(toEncodePath)
print "Please copy/overwrite \"inject.bin\" file into the USB Drive, then unplug and replug it."
