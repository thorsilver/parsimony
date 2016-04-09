import os
import sys

# Transforms a TMD directory in your tmd_dirs directory
# (parsimony/src/tmd/tmd_dirs/)
# into a single-tape, 2-symbol parsimonious Turing machine in your tm2_files directory
# (parsimony/src/tm/tm2/tm2_files)
# whose behavior is the same.

# Before compiling your TMD directory, if you wrote it by hand,
# it is highly recommended that you debug it using tmd_interpreter.py!

# IMPORTANT: This program will only run correctly if you are IN the tmd_meta 
# directory when you call it! 

dirName = sys.argv[1]

print "Generating the initializer TM..."
os.system("python initializer.py " + dirName)

print "Generating the programmer TM..."
os.system("python programmer.py " + dirName)

print "Generating the processor TM..."
os.system("python processor.py " + dirName)

print "Converting the initializer TM to a 2-symbol TM..."
os.chdir("../../tm/tm4/tm4_meta/")
os.system("python tm4_to_tm2_converter.py " + dirName + "_init")
os.system("rm ../tm4_files/" + dirName + "_init.tm4")

print "Converting the printer TM to a 2-symbol TM..."
#os.system("python ../../tm/tm4/tm4_meta/tm4_to_tm2_converter.py " + dirName + "_proc")
os.system("python tm4_to_tm2_converter.py " + dirName + "_proc")
os.system("rm ../tm4_files/" + dirName + "_proc.tm4")

print "Melding the initializer TM and the programmer TM..."
os.chdir("../../tm2/tm2_meta/")
#os.system("python ../../tm/tm2/tm2_meta/tmmelder.py " + dirName + "_init " + \
#    dirName + "_prog " + dirName + "_initprog")
os.system("python tmmelder.py " + dirName + "_init " + \
    dirName + "_prog " + dirName + "_initprog")
os.system("rm ../tm2_files/" + dirName + "_init.tm2")
os.system("rm ../tm2_files/" + dirName + "_prog.tm2")

print "Melding the code-generating TMs with the processor TM..."
os.system("python tmmelder.py " + dirName + "_initprog " + dirName + "_proc " + \
    dirName + "_unpruned")
os.system("rm ../tm2_files/" + dirName + "_initprog.tm2")
os.system("rm ../tm2_files/" + dirName + "_proc.tm2")    

print "Pruning the final TM..."
os.system("python pruner.py " + dirName + "_unpruned " + dirName)
os.system("rm ../tm2_files/" + dirName + "_unpruned.tm2")

print "Compilation complete!"