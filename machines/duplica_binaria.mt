Estados: q0,q1,q2,q3,q4,q5,q6,q7,q8,qf
Alfabeto_entrada: 0,1
Alfabeto_cinta: 0,1,#,B,X,Y
Inicial: q0
Finales: qf
Blanco: B
Transiciones:
q0,0 -> q1,X,R
q0,1 -> q2,Y,R
q0,X -> q0,X,R
q0,Y -> q0,Y,R
q0,# -> q5,#,L
q0,B -> qf,B,S
q1,0 -> q1,0,R
q1,1 -> q1,1,R
q1,X -> q1,X,R
q1,Y -> q1,Y,R
q1,# -> q7,#,R
q1,B -> q4,#,R
q2,0 -> q2,0,R
q2,1 -> q2,1,R
q2,X -> q2,X,R
q2,Y -> q2,Y,R
q2,# -> q8,#,R
q2,B -> q6,#,R
q3,0 -> q3,0,L
q3,1 -> q3,1,L
q3,X -> q3,X,L
q3,Y -> q3,Y,L
q3,# -> q3,#,L
q3,B -> q0,B,R
q4,B -> q3,0,L
q6,B -> q3,1,L
q7,0 -> q7,0,R
q7,1 -> q7,1,R
q7,X -> q7,X,R
q7,Y -> q7,Y,R
q7,# -> q7,#,R
q7,B -> q3,0,L
q8,0 -> q8,0,R
q8,1 -> q8,1,R
q8,X -> q8,X,R
q8,Y -> q8,Y,R
q8,# -> q8,#,R
q8,B -> q3,1,L
q5,0 -> q5,0,L
q5,1 -> q5,1,L
q5,X -> q5,0,L
q5,Y -> q5,1,L
q5,# -> q5,#,L
q5,B -> qf,B,S