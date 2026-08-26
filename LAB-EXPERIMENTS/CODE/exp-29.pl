% Experiment 29: Forward Chaining Reasoning Engine in Prolog

% Initial Known Facts in Working Memory
:- dynamic fact/1.

fact(croaks).
fact(eat_flies).
fact(has_stripes).
fact(yellow_color).

% Forward Chaining Rules:
% If croaks AND eat_flies -> frog
% If frog -> green
% If yellow_color AND has_stripes -> tiger

infer :-
    rule(IF, THEN),
    all_known(IF),
    \+ fact(THEN),
    asserta(fact(THEN)),
    write('Derived New Fact: '), write(THEN), nl,
    infer.
infer :-
    write('Forward Chaining Complete. No more new facts can be derived.'), nl.

all_known([]).
all_known([H|T]) :-
    fact(H),
    all_known(T).

% Rules Representation: rule(PremisesList, Conclusion)
rule([croaks, eat_flies], frog).
rule([frog], green_colored).
rule([yellow_color, has_stripes], tiger).

/* Sample Queries & Expected Results:
?- infer.
   Derived New Fact: frog
   Derived New Fact: green_colored
   Derived New Fact: tiger
   Forward Chaining Complete. No more new facts can be derived.
   true.

?- fact(frog).
   true.
*/
