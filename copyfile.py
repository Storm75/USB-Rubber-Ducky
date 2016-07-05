import getpass
import os
import shutil
import subprocess
import sys

DEVICE = "/dev/sdc1"
DELAY = 200
DEFAULT_DELAY = 50
DESTINATION_KEYBOARD = "ch"
DRIVE_NAME = "DUCKYDRIVE"

if os.environ.has_key('SUDO_USER'):
    DRIVE_PATH = "/media/" + os.environ['SUDO_USER'] + "/" + DRIVE_NAME
else:
    DRIVE_PATH = "/media/" + getpass.getuser() + "/" + DRIVE_NAME 

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
getpass.getuser()

try:
    shutil.copy("inject.bin", DRIVE_PATH + "/inject.bin")
except IOError:
    try:
        shutil.rmtree(DRIVE_PATH)
        os.makedirs(DRIVE_PATH)
    except:
        pass
    os.system("mount -t auto " + DEVICE + " " + DRIVE_PATH)
    shutil.copy("inject.bin", DRIVE_PATH + "/inject.bin")

os.remove("inject.bin")
os.system("umount -l " + DRIVE_PATH)
#shutil.rmtree(DRIVE_PATH)
#os.makedirs(DRIVE_PATH)
#os.system("sudo mount /dev/sdb1 " + DRIVE_PATH)
print "Ready, replug USB drive for pasting."
sys.exit(0)

