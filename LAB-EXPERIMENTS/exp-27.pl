% Experiment 27: Best First Search Algorithm in Prolog

% Graph connections: edge(Node1, Node2, Cost)
edge(a, b, 3).
edge(a, c, 2).
edge(b, d, 4).
edge(b, e, 1).
edge(c, f, 5).
edge(e, goal, 2).
edge(d, goal, 6).

% Heuristic values: h(Node, EstimatedCostToGoal)
h(a, 5).
h(b, 3).
h(c, 4).
h(d, 6).
h(e, 2).
h(f, 5).
h(goal, 0).

% Best First Search entry point
best_first_search(Start, Goal, Path) :-
    h(Start, H),
    bfs_queue([[h(H, Start)]], Goal, RevPath),
    reverse(RevPath, Path).

% Base case: Goal reached
bfs_queue([[h(_, Goal)|Path]|_], Goal, [Goal|Path]).

% Step: Expand node with lowest heuristic value
bfs_queue([[h(_, Node)|Path]|Rest], Goal, FinalPath) :-
    findall([h(H, Next), Node|Path],
            (edge(Node, Next, _), \+ member(Next, Path), h(Next, H)),
            NewPaths),
    append(Rest, NewPaths, AllPaths),
    sort(AllPaths, SortedPaths), % Sort by heuristic h(N)
    bfs_queue(SortedPaths, Goal, FinalPath).

/* Sample Queries & Expected Results:
?- best_first_search(a, goal, Path).
   Path = [a, b, e, goal].
*/
