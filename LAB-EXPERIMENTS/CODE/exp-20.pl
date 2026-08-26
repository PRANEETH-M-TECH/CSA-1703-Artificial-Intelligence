% Experiment 20: Planets Database in Prolog

% Database Facts: planet(Name, Type, DistanceFromSun_AU, Moons).
planet('Mercury', 'Terrestrial', 0.39, 0).
planet('Venus', 'Terrestrial', 0.72, 0).
planet('Earth', 'Terrestrial', 1.00, 1).
planet('Mars', 'Terrestrial', 1.52, 2).
planet('Jupiter', 'Gas Giant', 5.20, 79).
planet('Saturn', 'Gas Giant', 9.58, 82).
planet('Uranus', 'Ice Giant', 19.22, 27).
planet('Neptune', 'Ice Giant', 30.05, 14).

% Rule: Find planets with moons greater than N
has_moons_greater_than(Planet, N) :-
    planet(Planet, _, _, Moons),
    Moons > N.

% Rule: Find planets by Type
planet_of_type(Planet, Type) :-
    planet(Planet, Type, _, _).

/* Sample Queries & Expected Results:
?- planet('Mars', Type, Distance, Moons).
   Type = 'Terrestrial', Distance = 1.52, Moons = 2.

?- planet_of_type(P, 'Gas Giant').
   P = 'Jupiter' ;
   P = 'Saturn'.

?- has_moons_greater_than(P, 50).
   P = 'Jupiter' ;
   P = 'Saturn'.
*/
