import numpy as np
import utils


class DecisionStumpEquality:

    def __init__(self):
        pass


    def fit(self, X, y):
        N, D = X.shape

        # Get an array with the number of 0's, number of 1's, etc.
        count = np.bincount(y)    
        
        # Get the index of the largest value in count.  
        # Thus, y_mode is the mode (most popular value) of y
        y_mode = np.argmax(count) 

        self.splitSat = y_mode
        self.splitNot = None
        self.splitVariable = None
        self.splitValue = None

        # If all the labels are the same, no need to split further
        if np.unique(y).size <= 1:
            return

        minError = np.sum(y != y_mode)

        # Loop over features looking for the best split
        X = np.round(X)

        for d in range(D):
            for n in range(N):
                # Choose value to equate to
                value = X[n, d]

                # Find most likely class for each split
                y_sat = utils.mode(y[X[:,d] == value])
                y_not = utils.mode(y[X[:,d] != value])

                # Make predictions
                y_pred = y_sat * np.ones(N)
                y_pred[X[:, d] != value] = y_not

                # Compute error
                errors = np.sum(y_pred != y)

                # Compare to minimum error so far
                if errors < minError:
                    # This is the lowest error, store this value
                    minError = errors
                    self.splitVariable = d
                    self.splitValue = value
                    self.splitSat = y_sat
                    self.splitNot = y_not

    def predict(self, X):

        M, D = X.shape
        X = np.round(X)

        if self.splitVariable is None:
            return self.splitSat * np.ones(M)

        yhat = np.zeros(M)

        for m in range(M):
            if X[m, self.splitVariable] == self.splitValue:
                yhat[m] = self.splitSat
            else:
                yhat[m] = self.splitNot

        return yhat





class DecisionStumpErrorRate:

    def __init__(self):
        pass

    # Copied and then modified from DecisionStumpEquality.fit
    def fit(self, X, y):
        # X is N by D, N rows and D columns
        N, D = X.shape

        # Get an array with the number of 0's, number of 1's, etc.
        # count = occurrence of each unique label
        count = np.bincount(y)
        
        # Get the index of the largest value in count.
        # Thus, y_mode is the mode (most popular value) of y
        y_mode = np.argmax(count)

        # Initialize prediction to y_mode
        self.splitSat = y_mode
        self.splitNot = None
        # Feature we split on
        self.splitVariable = None
        # Threshold we split with
        self.splitValue = None

        # If all the labels are the same, no need to split further
        # Always predict y_mode
        if np.unique(y).size <= 1:
            return

        # Initialize minError as number of times we predict wrong if we always predict y_mode
        # This is computing the error if using "baseline" rule, number of times y_i does not equal most common value
        minError = np.sum(y != y_mode)

        # Loop over features looking for the best split
        # No need to round as we are doing a threshold-based split
        # For feature d of D features
        for d in range(D):
            # For example n of N examples
            for n in range(N):
                # Choose value to equate to
                # This is a threshold
                value = X[n, d]

                # Find most likely class for each split
                # Change from equality-based split to threshold-based split
                # Set y_sat to most common label of examples satisfying rule
                y_sat = utils.mode(y[X[:,d] > value])
                # Set y_not to most common label of examples not satisfying rule
                y_not = utils.mode(y[X[:,d] <= value])

                # Make predictions
                y_pred = y_sat * np.ones(N)
                y_pred[X[:, d] <= value] = y_not

                # Compute error
                errors = np.sum(y_pred != y)

                # Compare to minimum error so far
                if errors < minError:
                    # This is the lowest error, store this value
                    minError = errors
                    self.splitVariable = d
                    self.splitValue = value
                    self.splitSat = y_sat
                    self.splitNot = y_not

    # Copied and then modified from DecisionStumpEquality.predict
    def predict(self, X):
        # X is M by D, M rows and D columns
        M, D = X.shape
        # No need to round as we are doing a threshold-based split

        # If there was no need to split due to only having one unique label, always predict splitSat (which is the mode, which will always be correct in this case)
        if self.splitVariable is None:
            return self.splitSat * np.ones(M)

        yhat = np.zeros(M)

        # For each example m of M examples
        for m in range(M):
            # Change from equality-based split to threshold-based split
            # If satisfies split rule of decision stump
            if X[m, self.splitVariable] > self.splitValue:
                # Predict splitSat
                yhat[m] = self.splitSat
            else:
                # Predict splitNot
                yhat[m] = self.splitNot

        return yhat



"""
A helper function that computes the entropy of the 
discrete distribution p (stored in a 1D numpy array).
The elements of p should add up to 1.
This function ensures lim p-->0 of p log(p) = 0
which is mathematically true (you can show this with l'Hopital's rule), 
but numerically results in NaN because log(0) returns -Inf.
"""
def entropy(p):
    plogp = 0*p # initialize full of zeros
    plogp[p>0] = p[p>0]*np.log(p[p>0]) # only do the computation when p>0
    return -np.sum(plogp)
    
# This is not required, but one way to simplify the code is
# to have this class inherit from DecisionStumpErrorRate.
# Which methods (init, fit, predict) do you need to overwrite?

# Only need to overwrite fit as init and predict are the same as DecisionStumpErrorRate
class DecisionStumpInfoGain(DecisionStumpErrorRate):
    
    # Copied and then modified from DecisionStumpErrorRate.fit
    def fit(self, X, y):
        # X is N by D, N rows and D columns
        N, D = X.shape

        # Get an array with the number of 0's, number of 1's, etc.
        # count = occurrence of each unique label
        count = np.bincount(y)
        
        # Get the index of the largest value in count.
        # Thus, y_mode is the mode (most popular value) of y
        y_mode = np.argmax(count)

        # Initialize prediction to y_mode
        self.splitSat = y_mode
        self.splitNot = None
        # Feature we split on
        self.splitVariable = None
        # Threshold we split with
        self.splitValue = None
    
        # Initialize info gain to 0, this is the baseline rule ("do nothing")
        maxInfoGain = 0
        # Get an array with the probabilities of the occurrence of each unique label
        p = count/np.sum(count)
        # Find entropy of labels before split
        preSplitEntropy = entropy(p)

        # If all the labels are the same, no need to split further
        # Always predict y_mode
        if np.unique(y).size <= 1:
            return

        # Loop over features looking for the best split to maximize info gain
        # For feature d of D features
        for d in range(D):
            # For example n of N examples
            for n in range(N):
                # Choose value to equate to
                # This is a threshold
                value = X[n, d]

                examples_satisfying_rule = X[:,d] > value
                # Calculate number of examples satisfying rule / number of examples to get probability of "yes" side
                y_prob = np.sum(examples_satisfying_rule) / N
                # Calculate probability of "no" side
                n_prob = 1 - y_prob

                # Count number of labels satisfying rule
                y_labels = y[examples_satisfying_rule]
                y_count = np.bincount(y_labels, minlength = len(count))
                # Calculate number of labels not satisfying rule
                n_count = count - y_count

                # Calculate entropy of labels for examples satisfying rule
                y_p = y_count / np.sum(y_count)
                y_entropy = entropy(y_p)

                # Calculate entropy of labels for examples not satisfying rule
                n_p = n_count / np.sum(n_count)
                n_entropy = entropy(n_p)

                # Calculate info gain from split
                splitInfoGain = preSplitEntropy - (y_prob * y_entropy) - (n_prob * n_entropy)

                # Store split if info gain is greater than best found so far
                if splitInfoGain > maxInfoGain:
                    self.splitSat = np.argmax(y_count)
                    self.splitNot = np.argmax(n_count)
                    self.splitVariable = d
                    self.splitValue = value
                    # Update new best info gain found so far
                    maxInfoGain = splitInfoGain
