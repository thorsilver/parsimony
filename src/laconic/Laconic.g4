grammar Laconic;

prog: trueprog ;
trueprog: (command)* EOF ;
command:  (funcdef | procdef | declare | nondefcommand)  ;

nondefprog: (nondefcommand)* ;
nondefcommand:  (funcproccall | whileloop | forloop | ifstate | ifelsestate | assign | returnstate | printstate)  ;

funcdef: 'func' funcprocbody ;
procdef: 'proc' funcprocbody ;

funcprocbody:  funcproccallbody  '{' nondefprog '}' ;

declare: (intdecl | listdecl | list2decl) ;

intdecl: 'int'  VAR ('=' expr)? ';' ;
listdecl: 'list'  VAR ('=' expr)? ';' ;
list2decl: 'list2'  VAR ('=' expr)? ';' ;

funcproccall: funcproccallbody  ';' ;

funcproccallbody: VAR  '(' ( VAR  ',' )* VAR  ')' ;

whileloop: 'while'  '('  whileexpr  ')'  '{' whilenondefprog '}' ;

forloop: 'for'  '('  nondefcommand  ';'  expr  ';'  nondefcommand  ')'  '{' nondefprog '}' ;

ifstate: 'if'  '('  ifexpr  ')'  '{' ifnondefprog '}' ;

printstate: 'print' VAR ';' ;

ifelsestate: 'ifelse' '(' ifelseexpr ')' '{' ifelsenondefprog '}' '{' elsenondefprog '}' ;

ifelsenondefprog: nondefprog ;
elsenondefprog: nondefprog ;
ifnondefprog: nondefprog ; 
whilenondefprog: nondefprog ;

ifelseexpr: intexpr ;
ifexpr: intexpr ;
whileexpr: intexpr ;

expr: (intexpr | listexpr | list2expr) ;

assign: VAR  '='  expr  ';' ;

returnstate: ('return' | 'halt')  ';' ;



intexpr:   intexpr OPERATOR_MUL_DIV intexpr     // intop DONE 
    |   intexpr OPERATOR_ADD_SUB intexpr        // intop DONE 
    |   intexpr OPERATOR_COMPARE intexpr        // intop DONE
    |   intexpr OPERATOR_BOOLEAN intexpr        // intop DONE 
    |   listexpr OPERATOR_INDEX intexpr         // listindex DONE
    |   OPERATOR_NOT intexpr                    // intnot DONE 
    |   '(' intexpr ')'                         // DONE 
    |   OPERATOR_NEGATE intexpr                 // intneg DONE
    |   OPERATOR_LENGTH listexpr                // len DONE
    |   OPERATOR_LENGTH2 list2expr              // len2 DONE
    |   INT                                     // intint DONE 
    |   VAR                                     // intvar DONE 
    ;
    
listexpr:
    |   list2expr OPERATOR_INDEX2 intexpr       // list2index DONE
    |   listexpr OPERATOR_APPEND intexpr        // listappend DONE
    |   listexpr OPERATOR_CONCAT listexpr       // listconcat DONE
    |   '(' listexpr ')'                        // DONE
    |   '[' (intexpr ',')* intexpr ']'          // constlist DONE
    |   '[' ']'                                 // emptylist DONE
    |   VAR                                     // listvar DONE
    ;

    // This is a giant hack!! Ask Zach how to fix this ASAP!
    
list2expr:
    |   list2expr OPERATOR_APPEND2 listexpr      // list2append DONE
    |   list2expr OPERATOR_CONCAT2 list2expr     // list2concat
    |   '(' list2expr ')'                       // DONE
    |   ':' (listexpr ',')* listexpr ':'        // constlist2 DONE
    |   ':' ':'                                     // emptylist2 DONE
    |  VAR                                      // list2var DONE
    ;

OPERATOR_MUL_DIV: ('*' | '/' | '%') ;
OPERATOR_ADD_SUB: ('+' | '-') ;
OPERATOR_NEGATE: ('~') ;
OPERATOR_COMPARE: ('==' | '!=' | '>' | '<' | '>=' | '<=') ;
OPERATOR_BOOLEAN: ('&' | '|') ;
OPERATOR_NOT: ('!') ;
OPERATOR_APPEND: ('^') ;
OPERATOR_APPEND2: ('^*') ;
OPERATOR_CONCAT: ('||') ;
OPERATOR_CONCAT2: ('||*') ;
OPERATOR_INDEX: ('@') ;
OPERATOR_INDEX2: ('@*') ;
OPERATOR_LENGTH: ('#') ;
OPERATOR_LENGTH2: ('#*') ;

COMMENT : '/*'.*?'*/' -> skip;
WS : [\t\n\r ]+ -> skip;
VAR     : [a-zA-Z_] [a-zA-Z0-9_]* ;
INT     : [0-9]+ ;

