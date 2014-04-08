#!/usr/bin/python

def computeRiskState(*kwargs):
#	Risk state = Risk Index [+] Risk Dristribution
	riskDistribution = computeRiskDistribution()
	riskIndex = computeRiskIndex(kwargs)
	riskState = riskDistribution + riskIndex
	return riskState

def computeRiskDistribution():
#	Risk Distribution = Target Importance
#
	pass

def computeRiskIndex(AK, CK0, BK, RS0, priority_IDS, IDS_name): 
#	Risk Index = Alert Amount [+] Alert Confidence [+] Alter Type Number
#					[+] Alert Severity [+] Alert Relevance Score
#
	if IDS_name == "Snort":
		PIDS0 = 3
	else:
		PIDS0 = 1
	
	mu = calculateMu(AK, CK0, BK, RS0, priority_IDS)
	mk = calculateMk(mu)

	#_______________Mass function________________

	# mass_q(Vj) = (mu qj) / (sum [i=1,2] muq i) + 1 - wq*PIDS0

	# mass(V) = coso == RiskIndex


def calculateMk(mu):
	mk = [[0]*2 for i in range(5)]

	for i in range(5):
		for j in range(2):
			if j == 0:
				mk[i][j] = mu[i][j] / ( mu[i][j] + mu[i][j+1] + 1 - w[i] * PIDS0)
			else:
				mk[i][j] = mu[i][j] / ( mu[i][j] + mu[i][j-1] + 1 - w[i] * PIDS0)

	return mk

#############################
#	Function "calculateMu"
#		Given the parameters of the system, it will return the factors of risk/no risk
#
#		AK : alert amount of an alert thread (not only attack strength but also attack confidence).
#
#		CK0 : updated alert confidence [0,1] ; probability that an abnormal activity is a true attack. 
#
#		BK : attack confident situation & severity of the corresponding intrusion.
#
#		RS0 : likelihood of a sucessful intrusion. Updated alert in an alert thread. [0,1]
#
#############################

def calculateMu(AK, CK0, BK, RS0, priority_IDS):
	# alpha1 [5,15]  ; alpha2 [10,20]  ; alpha3 [15,30]
	mu = [[0.0]*2 for i in range(5)]
	w = [0.0]*5

	if AK <= alpha2:
		mu[0][0] = float((alpha2-AK) / alpha2)
	else:
		mu[0][0] = 0.0

	if alpha1 >= AK:
		mu[0][1] = 0.0
	elif alpha3 < AK:
		mu[0][1] = 1.0	
	else:
		mu[0][1] = float((AK - alpha1) / (alpha3 - alpha1))
	

	# CK0 [0,1]
	mu[1][0] = 1.0 - CK0
	mu[1][1] = float(CK0)

	# lambda1 [1,5] ; lambda2 [5,9] ; lambda3 [6,10]

	if BK <= lambda2:
		mu[2][0] = float((lambda2 - BK) / lambda2)
	else:
		mu[2][0] = 0.0

	if lambda1 >= BK:
		mu[2][1] = 0.0
	elif lambda3 < BK:
		mu[2][1] = 1.0
	else: 
		mu[2][1] = float((BK - lambda1) / (lambda3 - lambda1))


	# phi = 3 ; PR0 = 4 - priority_IDS
	PR0 = 4.0 - priority_IDS
	phi = 3.0

	if PR0 <= phi:
		mu[3][0] = float((phi - PR0) / phi)
		mu[3][1] = float(PR0 / phi)
	else:
		mu[3][0] = 0.0
		mu[3][1] = 1.0

	# RS0 relevance score

	mu[4][0] = 1.0 - RS0
	mu[4][1] = float(RS0)

	return mu