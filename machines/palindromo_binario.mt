Estados: q0,q1,q2,q3,q4,q5,qf
Alfabeto_entrada: 0,1
Alfabeto_cinta: 0,1,B,X,Y
Inicial: q0
Finales: qf
Blanco: B
Transiciones:
q0,0 -> q1,X,R
q0,1 -> q2,Y,R
q0,X -> q0,X,R
q0,Y -> q0,Y,R
q0,B -> qf,B,S

q1,0 -> q1,0,R
q1,1 -> q1,1,R
q1,X -> q1,X,R
q1,Y -> q1,Y,R
q1,B -> q3,B,L

q2,0 -> q2,0,R
q2,1 -> q2,1,R
q2,X -> q2,X,R
q2,Y -> q2,Y,R
q2,B -> q4,B,L

q3,X -> q3,X,L
q3,Y -> q3,Y,L
q3,0 -> q5,X,L
q3,B -> q0,B,R

q4,X -> q4,X,L
q4,Y -> q4,Y,L
q4,1 -> q5,Y,L
q4,B -> q0,B,R

q5,0 -> q5,0,L
q5,1 -> q5,1,L
q5,X -> q5,X,L
q5,Y -> q5,Y,L
q5,B -> q0,B,R