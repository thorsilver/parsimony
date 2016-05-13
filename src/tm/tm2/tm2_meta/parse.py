import sys, re

# Written by Armin Rigo. Thank you Armin!

# Together with parse.py, converts a .tm2 file to a .c file (which will simulate much faster). Can be run with the command "python parse.py squaresaresmall.tm2 > tm.i && gcc -O2 tm.c"

r_header = re.compile(r"States: (\d+)$")
r_rule = re.compile(r"([A-Za-z0-9_.]+):"
                    r"\s+a -> ([A-Za-z0-9_.]+); ([LR-]); ([ab])"
                    r"\s+b -> ([A-Za-z0-9_.]+); ([LR-]); ([ab])")


def parse(filename):
    f = open(filename, 'r')
    match = r_header.match(f.readline())
    num_states = int(match.group(1))
    seen = set()
    seen_next = set()
    for (rulename, a_next, a_move, a_tape, b_next, b_move, b_tape
             ) in r_rule.findall(f.read()):
        seen.add(rulename)
        seen_next.add(a_next)
        seen_next.add(b_next)

        rulename = rulename.replace('.', '$')
        a_next = a_next.replace('.', '$')
        b_next = b_next.replace('.', '$')
        print '%s: s++;' % rulename
        if a_tape == 'a' and b_tape == 'b' and (a_next, a_move) == (b_next, b_move):
            if a_move == 'R':
                print 'p++;'
            elif a_move == 'L':
                print 'p--;'
            print 'goto %s;' % a_next
        else:
            print 'if(*p){'
            if b_tape == 'a':
                print '*p=0;'
            if b_move == 'R':
                print 'p++;'
            elif b_move == 'L':
                print 'p--;'
            print 'goto %s;' % b_next
            print '}else{'
            if a_tape == 'b':
                print '*p=1;'
            if a_move == 'R':
                print 'p++;'
            elif a_move == 'L':
                print 'p--;'
            print 'goto %s;' % a_next
            print '}'

    assert len(seen) == num_states
    seen.add('ERROR')
    seen.add('HALT')
    assert seen_next.issubset(seen), seen_next - seen


if __name__ == '__main__':
    parse(sys.argv[1])
