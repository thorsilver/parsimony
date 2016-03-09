import os
import sys

# Transforms a Laconic program in your laconic_files directory
# (parsimony/src/laconic/laconic_files/)
# into a 2-symbol Turing machine in your tm2_files directory
# (parsimony/src/tm/tm2/tm2_files/)
# whose behavior is the same. Print statements are ignored.

# Before compiling your Laconic program, it is highly
# recommended that you debug it using laconic_interpreter.py!

name = sys.argv[1]

os.system("python laconic_to_tmd_compiler.py " + name)

os.chdir("../../tmd/tmd_meta")
os.system("python tmd_to_2s_tm_compiler.py " + name)