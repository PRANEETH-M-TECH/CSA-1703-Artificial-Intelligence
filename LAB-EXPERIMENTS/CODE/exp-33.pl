% Experiment 33: Find the number of vowels in a list of characters in Prolog

% Vowel predicate
is_vowel(a).
is_vowel(e).
is_vowel(i).
is_vowel(o).
is_vowel(u).
is_vowel('A').
is_vowel('E').
is_vowel('I').
is_vowel('O').
is_vowel('U').

% Count vowels in a character list
% Base case: Empty list has 0 vowels
count_vowels([], 0).

% Recursive case 1: Head is a vowel
count_vowels([H|T], Count) :-
    is_vowel(H),
    count_vowels(T, TailCount),
    Count is TailCount + 1.

% Recursive case 2: Head is NOT a vowel
count_vowels([H|T], Count) :-
    \+ is_vowel(H),
    count_vowels(T, Count).

% Helper: Count vowels in an atom/string
count_vowels_in_string(Atom, Count) :-
    atom_chars(Atom, CharList),
    count_vowels(CharList, Count).

/* Sample Queries & Expected Results:
?- count_vowels([a, r, t, i, f, i, c, i, a, l], Count).
   Count = 5.

?- count_vowels_in_string('prolog', Count).
   Count = 2.
*/
