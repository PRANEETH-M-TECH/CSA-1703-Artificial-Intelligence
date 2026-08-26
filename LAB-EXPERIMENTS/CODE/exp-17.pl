% Experiment 17: Sum of integers from 1 to N in Prolog

% Base case: Sum of 1 to 0 is 0
sum_1_to_n(0, 0).

% Recursive case: Sum(N) = N + Sum(N-1)
sum_1_to_n(N, Sum) :-
    N > 0,
    N1 is N - 1,
    sum_1_to_n(N1, Sum1),
    Sum is N + Sum1.

/* Sample Queries & Expected Results:
?- sum_1_to_n(5, Result).
   Result = 15.

?- sum_1_to_n(10, Result).
   Result = 55.
*/
