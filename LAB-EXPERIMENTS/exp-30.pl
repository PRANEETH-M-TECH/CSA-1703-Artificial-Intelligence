% Experiment 30: Backward Chaining Reasoning Engine in Prolog

% Base Knowledge Base Facts
fact(mammal(dog)).
fact(has_hair(dog)).
fact(gives_milk(dog)).
fact(mammal(cat)).
fact(has_hair(cat)).

% Rules for Backward Chaining: rule(Goal, ListOfSubgoals)
rule(carnivore(X), [mammal(X), eats_meat(X)]).
rule(mammal(X), [has_hair(X)]).
rule(mammal(X), [gives_milk(X)]).
rule(pet(X), [mammal(X)]).

% Backward Chaining Proof Engine: prove(Goal)
prove(Goal) :-
    fact(Goal),
    write('Fact confirmed: '), write(Goal), nl.

prove(Goal) :-
    rule(Goal, SubGoals),
    write('Attempting to prove subgoals for: '), write(Goal), nl,
    prove_all(SubGoals).

prove_all([]).
prove_all([G|Rest]) :-
    prove(G),
    prove_all(Rest).

/* Sample Queries & Expected Results:
?- prove(pet(dog)).
   Attempting to prove subgoals for: pet(dog)
   Attempting to prove subgoals for: mammal(dog)
   Fact confirmed: has_hair(dog)
   true.

?- prove(mammal(cat)).
   Fact confirmed: mammal(cat)
   true.
*/
