% Experiment 26: Fruit and its Color using Backtracking in Prolog

% Facts: fruit(FruitName, Color)
fruit(apple, red).
fruit(apple, green).
fruit(banana, yellow).
fruit(grape, purple).
fruit(grape, green).
fruit(mango, yellow).
fruit(mango, green).
fruit(strawberry, red).
fruit(orange, orange).

% Find fruit by color using Prolog's built-in backtracking engine
get_fruit_by_color(Color, Fruit) :-
    fruit(Fruit, Color).

% Find color of a specific fruit
get_color_by_fruit(Fruit, Color) :-
    fruit(Fruit, Color).

/* Sample Queries & Expected Results:
?- get_fruit_by_color(yellow, Fruit).
   Fruit = banana ;
   Fruit = mango.

?- get_fruit_by_color(green, Fruit).
   Fruit = apple ;
   Fruit = grape ;
   Fruit = mango.

?- get_color_by_fruit(apple, Color).
   Color = red ;
   Color = green.
*/
