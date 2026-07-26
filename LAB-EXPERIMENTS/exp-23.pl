% Experiment 23: Family Tree in Prolog

% Parent Relationships: parent(Parent, Child)
parent(john, mary).
parent(john, tom).
parent(mary, ann).
parent(mary, bob).
parent(tom, lisa).

% Gender Facts
male(john).
male(tom).
male(bob).
female(mary).
female(ann).
female(lisa).

% Rules
father(X, Y) :- parent(X, Y), male(X).
mother(X, Y) :- parent(X, Y), female(X).

grandparent(X, Y) :- parent(X, Z), parent(Z, Y).
grandfather(X, Y) :- grandparent(X, Y), male(X).
grandmother(X, Y) :- grandparent(X, Y), female(X).

sibling(X, Y) :- parent(Z, X), parent(Z, Y), X \= Y.
brother(X, Y) :- sibling(X, Y), male(X).
sister(X, Y) :- sibling(X, Y), female(X).

/* Sample Queries & Expected Results:
?- father(john, Child).
   Child = mary ;
   Child = tom.

?- grandparent(john, GrandChild).
   GrandChild = ann ;
   GrandChild = bob ;
   GrandChild = lisa.

?- sibling(ann, Sibling).
   Sibling = bob.
*/
