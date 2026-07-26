% Experiment 32: Pattern Matching in Prolog

% Prolog matches structures and lists using unification.

% Pattern 1: Match head and tail of a list
match_head_tail([Head | Tail], Head, Tail).

% Pattern 2: Match specific tuple patterns point(X, Y)
match_point(point(X, Y), X, Y).

% Pattern 3: Match structured term student(Id, Name, Course)
match_student(student(Id, Name, Course), Id, Name, Course).

% Pattern 4: Check if two terms unify (pattern match)
match_terms(Term1, Term2) :-
    Term1 = Term2.

/* Sample Queries & Expected Results:
?- match_head_tail([10, 20, 30], Head, Tail).
   Head = 10, Tail = [20, 30].

?- match_point(point(5, 12), X, Y).
   X = 5, Y = 12.

?- match_terms(father(john, X), father(john, mary)).
   X = mary.
*/
