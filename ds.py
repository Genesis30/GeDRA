#!/usr/bin/python

#############################
#	Function "calculateRisk"
#		Given "data", calls the required function to compute the risk state of the
#		system, and returns it.
#############################
def calculateRisk(data):
	risk = computeRiskState(data[0], data[1], data[2], data[3], data[4], data[5], data[6])
	return risk

#############################
#	Function "computeRiskState"
#		Given all the parameters required to use the DST, calls the functions
#		required to compute risk index and risk distribution.
#############################
def computeRiskState(priority,AK, CK0, BK, RS0, priority_IDS, IDS_name):
#	Risk state = Risk Index [+] Risk Dristribution
		
	riskIndex = computeRiskIndex(AK, CK0, BK, RS0, priority_IDS, IDS_name)
	riskState = computeRiskDistribution(priority,riskIndex)
	return riskState

#############################
#	Function "computeRiskDistribution"
#		Given a riskIndex and the priority of the element in the system,
#		computes the actual risk of the element.
#############################
def computeRiskDistribution(priority, riskIndex):
#	Risk Distribution = Target Importance
#
#	medium = [0,0.5][0.5,0.8][0.8,1.0]
#	high = [0,0.4][0.4,0.7][0.7,1.0]

	if priority <= 3:
		if riskIndex <= 0.5:
			print 'Low risk: %s' % riskIndex
			return 0.3
		elif riskIndex <=0.8:
			print 'Medium risk: %s' % riskIndex
			return 0.6
		else:
			print 'High risk: %s' % riskIndex
			return 1.0
	else:
		if riskIndex <= 0.4:
			print 'Low risk: %s' % riskIndex
			return 0.3
		elif riskIndex <=0.7:
			print 'Medium risk: %s' % riskIndex
			return 0.6
		else:
			print 'High risk: %s' % riskIndex
			return 1.0

#############################
#	Function "computeRiskIndex"
#		Provided the correct parameters, calls the functions to calculate
#		the factors involved in risk calculations, and correlates them.
#############################
def computeRiskIndex(AK, CK0, BK, RS0, priority_IDS, IDS_name): 
#	Risk Index = Alert Amount [+] Alert Confidence [+] Alter Type Number
#					[+] Alert Severity [+] Alert Relevance Score
#
	if IDS_name == "snort":
		PIDS0 = 3
	else:
		PIDS0 = 1
	
	mu = calculateMu(AK, CK0, BK, RS0, priority_IDS)
	mk = calculateMk(mu,PIDS0)
	
	prob = mk[0][1] + mk[1][1] + mk[2][1] + mk[3][1] + mk[4][1]
	tmp = mk[0][0] + mk[1][0] + mk[2][0] + mk[3][0] + mk[4][0]
	
	conflict = tmp + prob
	result = prob/conflict
	return result

#############################
#	Function "calculateMk"
#		Factors involved in DST.
#############################
def calculateMk(mu, PIDS0):
	mk = [[0]*2 for i in range(5)]
	w = [0,0.1,0.2,0.3,0.4]

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
	
	#----------------
	alpha1 = 5
	alpha2 = 10
	alpha3 = 15
	#----------------
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

	#--------------
	lambda1 = 1
	lambda2 = 5
	lambda3 = 6
	#--------------
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
	PR0 = 4.0 - float(priority_IDS)
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

#############################
#	Dictionary used to store information related to the system.
#############################
alert_num_dict = { 'web_server': 0,
						'database_server': 0,
						'voip_server': 0,
						'router': 0,
						'switch': 0,
						'computer': 0,
						'firewall': 0,
						'printer': 0,
}

#############################
#	Function "calculateParams"
#		Given some information about the attack, computes it and
#		decides the factors to compute the risk index.
#############################
def calculateParams(params, affected_element, affected_element_relevance, attack_rating):
	IDS_name = 'snort'
	step, classification, priority_IDS, protocol, sourceIp, destinationIp = params[1],params[2],params[3],params[4],params[5],params[6]
	#priority_IDS = params

	alert_num_dict[affected_element] = alert_num_dict[affected_element]+1

	# AK : alert amount of an alert thread (not only attack strength but also attack confidence).
	# Calculate AK
	alert_number = alert_num_dict[affected_element]
	AK = alert_number * 3.0 + float(affected_element_relevance) + float(attack_rating)
	
	# CK0 : updated alert confidence [0,1] ; probability that an abnormal activity is a true attack. 
	# Calculate CK0
	if alert_number >=2:
		CK0 = 0.7
	else:
		CK0 = 0.5
	
	# BK : attack confident situation & severity of the corresponding intrusion.
	# Calculate BK
	BK = alert_number*2 + float(affected_element_relevance)
	
	# RS0 : likelihood of a sucessful intrusion. Updated alert in an alert thread. [0,1]
	# Calculate RS0
	if alert_number <=3:
		RS0 = CK0 + alert_number/10.0
	else:
		RS0 = 1.0

	data = [0.0 for i in range(7)]
	data[0], data[1], data[2], data[3], data[4], data[5], data[6] = affected_element_relevance, AK, CK0, BK, RS0, priority_IDS, IDS_name
	return data

	"""
	#computeRiskIndex(AK, CK0, BK, RS0, priority_IDS, IDS_name)
	#computeRiskIndex(12.0, 0.6, 6.0, 0.7, 3, "snort")

	computeRiskState(4,12.0, 0.6, 6.0, 0.7, 3, "snort")

	computeRiskState(4,15.0, 0.6, 10.0, 0.8, 3, "snort")

	computeRiskState(4,16.0, 0.6, 11.0, 0.9, 3, "snort")
	"""


"""
params = calculateParams(3, 'web_server', 5, 4)
ads = calculateRisk(params)
print ads
params = calculateParams(3, 'web_server', 5, 4)

params = calculateParams(3, 'web_server', 5, 4)

ads = calculateRisk(params)
print ads
"""
