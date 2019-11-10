# Predict for example n

# n[0] is the longitude
# n[1] is the latitude

# 0 is blue state
# 1 is red state
def predict(n):
	if n[0] > -80.305106:
		if n[1] > 36.453576:
			return 0
		else:
			return 0
	else:
		if n[1] > 37.669007:
			return 0
		else:
			return 1
