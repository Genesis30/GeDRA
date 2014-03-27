#!/usr/bin/python

# 

def calculaMu(): 
	
	# alpha1 [5,15]  ; alpha2 [10,20]  ; alpha3 [15,30]

	if AK <= alpha2:
		mu11 = (alpha2-AK) / alpha2
	else:
		mu11 = 0

	if alpha1 >= AK:
		mu21 = 0
	elif alpha3 < AK:
		mu21 = 1	
	else:
		mu21 = (AK - alpha1) / (alpha3 - alpha1)
	

	# CK0 [0,1]
	mu21 = 1 - CK0
	mu22 = CK0

	# lambda1 [1,5] ; lambda2 [5,9] ; lambda3 [6,10]

	if BK <= lambda2:
		mu31 = (lambda2 - BK) / lambda2
	else:
		mu31 = 0

	if lambda1 >= BK:
		mu32 = 0
	elif lambda3 < BK:
		mu32 = 1
	else: 
		mu32 = (BK - lambda1) / (lambda3 - lambda1)


	# phi = 3 ; PR0 = 4 - priority_IDS
	PR0 = 4 - priority_IDS
	phi = 3

	if PR0 <= phi:
		mu41 = (phi - PR0) / phi
		mu42 = PR0 / phi
	else:
		mu41 = 0
		mu42 = 1

	# RS0 relevance score

	mu51 = 1 - RS0
	mu52 = RS0

	# _______________Mass function________________

	mass_q(Vj) = (mu qj) / (sum [i=1,2] muq i) + 1 - wq*PIDS0

	mass(V) = coso == RiskIndex


def calculaCosos():