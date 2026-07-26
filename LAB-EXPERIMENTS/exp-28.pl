% Experiment 28: Medical Diagnosis Expert System in Prolog

% Rules for diagnosing diseases based on symptoms
symptom(fever).
symptom(cough).
symptom(headache).
symptom(runny_nose).
symptom(sore_throat).

% Disease Rules
hypothesis(flu) :-
    symptom(fever),
    symptom(cough),
    symptom(headache),
    symptom(runny_nose).

hypothesis(common_cold) :-
    symptom(cough),
    symptom(runny_nose),
    symptom(sore_throat).

hypothesis(strep_throat) :-
    symptom(fever),
    symptom(sore_throat).

hypothesis(migraine) :-
    symptom(headache),
    \+ symptom(fever).

% Entry point for diagnosis query
diagnose(Disease) :-
    hypothesis(Disease), !.
diagnose(unknown_condition).

/* Sample Queries & Expected Results:
?- hypothesis(flu).
   true.

?- diagnose(Disease).
   Disease = flu.
*/
