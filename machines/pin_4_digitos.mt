Estados: q0,q1,q2,q3,q4,qf
Alfabeto_entrada: 0,1,2,3,4,5,6,7,8,9
Alfabeto_cinta: 0,1,2,3,4,5,6,7,8,9,B
Inicial: q0
Finales: qf
Blanco: B
Transiciones:
q0,0 -> q1,0,R
q0,1 -> q1,1,R
q0,2 -> q1,2,R
q0,3 -> q1,3,R
q0,4 -> q1,4,R
q0,5 -> q1,5,R
q0,6 -> q1,6,R
q0,7 -> q1,7,R
q0,8 -> q1,8,R
q0,9 -> q1,9,R
q1,0 -> q2,0,R
q1,1 -> q2,1,R
q1,2 -> q2,2,R
q1,3 -> q2,3,R
q1,4 -> q2,4,R
q1,5 -> q2,5,R
q1,6 -> q2,6,R
q1,7 -> q2,7,R
q1,8 -> q2,8,R
q1,9 -> q2,9,R
q2,0 -> q3,0,R
q2,1 -> q3,1,R
q2,2 -> q3,2,R
q2,3 -> q3,3,R
q2,4 -> q3,4,R
q2,5 -> q3,5,R
q2,6 -> q3,6,R
q2,7 -> q3,7,R
q2,8 -> q3,8,R
q2,9 -> q3,9,R
q3,0 -> q4,0,R
q3,1 -> q4,1,R
q3,2 -> q4,2,R
q3,3 -> q4,3,R
q3,4 -> q4,4,R
q3,5 -> q4,5,R
q3,6 -> q4,6,R
q3,7 -> q4,7,R
q3,8 -> q4,8,R
q3,9 -> q4,9,R
q4,B -> qf,B,S
