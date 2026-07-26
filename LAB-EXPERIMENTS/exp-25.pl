% Experiment 25: Monkey Banana Problem in Prolog

% State representation: state(MonkeyPosition, MonkeyOnBoxStatus, BoxPosition, HasBananaStatus)

% Legal Moves / Actions

% Move 1: Grasp banana (Monkey must be on box under middle where banana is)
move(state(middle, onbox, middle, hasnot),
     grasp,
     state(middle, onbox, middle, has)).

% Move 2: Climb box (Monkey and Box must be at the same location)
move(state(P, onfloor, P, H),
     climb,
     state(P, onbox, P, H)).

% Move 3: Push box from P1 to P2
move(state(P1, onfloor, P1, H),
     push(P1, P2),
     state(P2, onfloor, P2, H)).

% Move 4: Walk from P1 to P2
move(state(P1, onfloor, B, H),
     walk(P1, P2),
     state(P2, onfloor, B, H)).

% Solve / Can reach Goal
canget(state(_, _, _, has)).

canget(State1) :-
    move(State1, Action, State2),
    write('Action: '), write(Action), nl,
    canget(State2).

/* Sample Queries & Expected Results:
?- canget(state(door, onfloor, window, hasnot)).
   Action: walk(door, window)
   Action: push(window, middle)
   Action: climb
   Action: grasp
   true.
*/
