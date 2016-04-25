grammar Laconic;

// The grammar for the Laconic language.

prog: trueprog;
trueprog: (command)* EOF ;
command:  (funcdef | procdef | declare | nondefcommand)  ;

nondefprog: (nondefcommand)* ;
nondefcommand:  (funcproccall | whileloop | forloop | ifstate | ifelsestate | assign | returnstate | printstate)  ;

funcdef: 'func' funcprocbody ;
procdef: 'proc' funcprocbody ;

funcprocbody:  funcproccallbody  '{' nondefprog '}' ;

declare: (intdecl | listdecl | list2decl) ;

intdecl: 'int'  VAR ';' ;
listdecl: 'list'  VAR ';' ;
list2decl: 'list2'  VAR ';' ;

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
        |   BEGIN_LIST (intexpr ',')* intexpr END_LIST          // constlist DONE
        |   BEGIN_LIST END_LIST                     // emptylist DONE
        |   VAR                                     // listvar DONE
        ;
    
list2expr:
         |   list2expr OPERATOR_APPEND2 listexpr      // list2append DONE
         |   list2expr OPERATOR_CONCAT2 list2expr     // list2concat
         |   '(' list2expr ')'                       // DONE
         |   BEGIN_LIST2 (listexpr ',')* listexpr END_LIST2        // constlist2 DONE
         |   BEGIN_LIST2 BEGIN_LIST2                  // emptylist2 DONE
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
BEGIN_LIST: ('[');
END_LIST: (']');
BEGIN_LIST2: ':';
END_LIST2: ':';

COMMENT : '/*'.*?'*/' -> skip;
WS : [\t\n\r ]+ -> skip;
VAR     : [a-zA-Z_] [a-zA-Z0-9_]* ;
INT     : [0-9]+ ;

