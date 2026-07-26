% Experiment 18: Database with Name and Date of Birth (DOB) in Prolog

% Database Records: person(Name, Day, Month, Year).
person('Alice', 15, 'January', 2000).
person('Bob', 22, 'March', 1998).
person('Charlie', 10, 'July', 2002).
person('Diana', 5, 'December', 1999).
person('Evan', 15, 'January', 2001).

% Query helper to get full DOB string for a person
get_dob(Name, DOB) :-
    person(Name, Day, Month, Year),
    DOB = (Day, Month, Year).

% Query helper to find people born in a specific month
born_in_month(Name, Month) :-
    person(Name, _, Month, _).

% Query helper to find people born in a specific year
born_in_year(Name, Year) :-
    person(Name, _, _, Year).

/* Sample Queries & Expected Results:
?- person('Alice', Day, Month, Year).
   Day = 15, Month = 'January', Year = 2000.

?- born_in_month(Name, 'January').
   Name = 'Alice' ;
   Name = 'Evan'.

?- born_in_year(Name, 1998).
   Name = 'Bob'.
*/
