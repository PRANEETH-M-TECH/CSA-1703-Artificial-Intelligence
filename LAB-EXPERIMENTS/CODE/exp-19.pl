% Experiment 19: Student-Teacher-Subject Code Database in Prolog

% Database Facts:
% student(StudentName, SubjectCode).
student('Rahul', 'CS101').
student('Priya', 'CS102').
student('Amit', 'CS101').
student('Sneha', 'CS103').

% teacher(TeacherName, SubjectCode).
teacher('Dr. Sharma', 'CS101').
teacher('Prof. Verma', 'CS102').
teacher('Dr. Gupta', 'CS103').

% subject(SubjectCode, SubjectName).
subject('CS101', 'Artificial Intelligence').
subject('CS102', 'Data Structures').
subject('CS103', 'Database Management Systems').

% Rule: Find teacher of a student
student_teacher(Student, Teacher) :-
    student(Student, SubCode),
    teacher(Teacher, SubCode).

% Rule: Find subject name studied by a student
student_subject_name(Student, SubName) :-
    student(Student, SubCode),
    subject(SubCode, SubName).

/* Sample Queries & Expected Results:
?- student_teacher('Rahul', Teacher).
   Teacher = 'Dr. Sharma'.

?- student_subject_name('Priya', Subject).
   Subject = 'Data Structures'.

?- student(Student, 'CS101').
   Student = 'Rahul' ;
   Student = 'Amit'.
*/
