import os
import sys

# Transforms a Laconic program in your laconic_files directory
# (parsimony/src/laconic/laconic_files/)
# into a TMD directory in your tmd_dirs directory
# (parsimony/src/tmd/tmd_dirs/)
# whose behavior is the same. Print statements are ignored.

# Before compiling your Laconic program, it is highly
# recommended that you debug it using laconic_interpreter.py!

def pront(x):
    print x

try:
    fileName = sys.argv[1]
except:
    raise Exception("Usage: python laconic_to_tmd_compiler [Laconic file name without extension]")

try:
    assert os.path.exists("../laconic_files/" + fileName + ".lac")
except:
    raise Exception("Error: file parsimony/src/laconic/laconic_files/" + fileName + ".lac not found.")

dirName = "../../tmd/tmd_dirs/" + fileName

if not os.path.exists(dirName + "/"):
    os.system("mkdir " + dirName)

print "Compiling..."
os.system("python compiler_helper.py ../laconic_files/" + fileName + ".lac")
print "Importing dependencies..."
os.system("python importer.py " + dirName)
print "Done!"