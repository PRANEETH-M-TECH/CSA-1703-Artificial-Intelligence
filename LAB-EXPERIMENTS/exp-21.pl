% Experiment 21: Tower of Hanoi in Prolog

% move(N, Source, Target, Auxiliary)

% Base case: Move 1 disk directly from Source to Target
hanoi(1, Source, Target, _) :-
    write('Move disk 1 from '), write(Source), write(' to '), write(Target), nl.

% Recursive case: Move N-1 disks to Auxiliary, move Nth disk to Target, move N-1 disks from Auxiliary to Target
hanoi(N, Source, Target, Auxiliary) :-
    N > 1,
    N1 is N - 1,
    hanoi(N1, Source, Auxiliary, Target),
    write('Move disk '), write(N), write(' from '), write(Source), write(' to '), write(Target), nl,
    hanoi(N1, Auxiliary, Target, Source).

/* Sample Queries & Expected Results:
?- hanoi(3, 'Peg A', 'Peg C', 'Peg B').
   Move disk 1 from Peg A to Peg C
   Move disk 2 from Peg A to Peg B
   Move disk 1 from Peg C to Peg B
   Move disk 3 from Peg A to Peg C
   Move disk 1 from Peg B to Peg A
   Move disk 2 from Peg B to Peg C
   Move disk 1 from Peg A to Peg C
   true.
*/
