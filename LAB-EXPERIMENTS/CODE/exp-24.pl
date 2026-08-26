% Experiment 24: Dieting System Based on Disease in Prolog

% Diet recommendations based on medical condition
recommend_diet(diabetes, ['Oats', 'Leafy Greens', 'Whole Grains', 'Fish'], ['Sugar', 'White Bread', 'Soda']).
recommend_diet(hypertension, ['Bananas', 'Spinach', 'Garlic', 'Low-fat Yogurt'], ['Excess Salt', 'Fried Food', 'Caffeine']).
recommend_diet(anemia, ['Spinach', 'Beans', 'Red Meat', 'Pomegranate'], ['Tea during meals', 'Coffee', 'Calcium supplements with Iron']).
recommend_diet(obesity, ['Salads', 'Green Tea', 'Sprouts', 'Fruits'], ['Fast Food', 'Sugary Beverages', 'Butter']).
recommend_diet(hyperthyroidism, ['Berries', 'Broccoli', 'Eggs', 'Nuts'], ['Iodized Salt', 'Excess Soy']).

% Predicate to get foods to eat
food_to_eat(Disease, FoodsToEat) :-
    recommend_diet(Disease, FoodsToEat, _).

% Predicate to get foods to avoid
food_to_avoid(Disease, FoodsToAvoid) :-
    recommend_diet(Disease, _, FoodsToAvoid).

/* Sample Queries & Expected Results:
?- food_to_eat(diabetes, EatList).
   EatList = ['Oats', 'Leafy Greens', 'Whole Grains', 'Fish'].

?- food_to_avoid(hypertension, AvoidList).
   AvoidList = ['Excess Salt', 'Fried Food', 'Caffeine'].

?- recommend_diet(anemia, Eat, Avoid).
   Eat = ['Spinach', 'Beans', 'Red Meat', 'Pomegranate'],
   Avoid = ['Tea during meals', 'Coffee', 'Calcium supplements with Iron'].
*/
