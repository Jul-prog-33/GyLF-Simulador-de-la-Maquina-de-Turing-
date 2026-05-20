Estados: q0,q1,q2,qf
Alfabeto_entrada: 0,1
Alfabeto_cinta: 0,1,B,X,Y
Inicial: q0
Finales: qf
Blanco: B
Transiciones:
q0,0 -> q1,X,R
q0,X -> q0,X,R
q0,Y -> q0,Y,R
q0,B -> qf,B,S
q1,0 -> q1,0,R
q1,X -> q1,X,R
q1,Y -> q1,Y,R
q1,1 -> q2,Y,L
q2,0 -> q2,0,L
q2,X -> q2,X,L
q2,Y -> q2,Y,L
q2,B -> q0,B,R