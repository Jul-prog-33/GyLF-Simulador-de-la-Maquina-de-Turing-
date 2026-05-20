Estados: q0,q1,q2,q3,qf
Alfabeto_entrada: 1
Alfabeto_cinta: 1,B,X,Y
Inicial: q0
Finales: qf
Blanco: B
Transiciones:
q0,1 -> q1,X,R
q0,X -> q0,X,R
q0,Y -> q0,Y,R
q0,B -> q3,B,L
q1,1 -> q1,1,R
q1,X -> q1,X,R
q1,Y -> q1,Y,R
q1,B -> q2,Y,L
q2,1 -> q2,1,L
q2,X -> q0,X,R
q2,Y -> q2,Y,L
q3,X -> q3,1,L
q3,Y -> q3,1,L
q3,1 -> q3,1,L
q3,B -> qf,B,S