% Experiment 22: Bird Flying System with Queries in Prolog

% Facts: Categories of birds
bird(eagle).
bird(sparrow).
bird(pigeon).
bird(penguin).
bird(ostrich).

% Facts: Exception birds that cannot fly
cannot_fly(penguin).
cannot_fly(ostrich).

% Rule: A bird can fly if it is a bird and NOT an exception
can_fly(X) :-
    bird(X),
    \+ cannot_fly(X).

/* Sample Queries & Expected Results:
?- can_fly(eagle).
   true.

?- can_fly(penguin).
   false.

?- can_fly(X).
   X = eagle ;
   X = sparrow ;
   X = pigeon.
*/
