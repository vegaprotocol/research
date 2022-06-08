from typing import Any
import numpy as np
from scipy.stats import norm

class LogNormal:
    '''
    Log-normal risk model
    '''

    def __init__(self, mu:float, sigma:float, lambd:float, tau:float) -> Any:
        if (tau < 0 or sigma <= 0 or lambd < 0.0 or lambd > 1.0):
            raise ValueError(
                "Time and volatility parameter should be strictly +ve and lambd must be between 0 and 1. ")
        self.mu = mu
        self.sigma = sigma
        self.lambd = lambd
        self.tau = tau

    def RiskFactorLong(self) -> float:
        sigmaBar = np.sqrt(self.tau) * self.sigma 
        muBar=(self.mu - 0.5*self.sigma*self.sigma) * self.tau
        quantileForLambda = norm.ppf(self.lambd)
        logNormalEs = -(1/self.lambd)*np.exp(muBar*sigmaBar*sigmaBar*0.5) * norm.cdf(quantileForLambda-sigmaBar)
        return logNormalEs + 1.0

    def RiskFactorShort(self) -> float:
        sigmaBar = np.sqrt(self.tau) * self.sigma 
        muBar=(self.mu - 0.5*self.sigma*self.sigma) * self.tau
        quantileForOneMinusLambda = norm.ppf(1.0 - self.lambd)
        negativeLogNormalEs = (1/self.lambd)*np.exp(muBar*sigmaBar*sigmaBar*0.5) * (1.0 - norm.cdf(quantileForOneMinusLambda-sigmaBar))
        return negativeLogNormalEs - 1.0

    def ProbOfTrading(self, mid: float, level: float) -> float:
        transLevel = (np.log(level/mid) - (self.mu - 0.5*self.sigma*self.sigma)*self.tau) / (self.sigma*np.sqrt(self.tau))
        if (mid < level):
            return 1.0 - norm.cdf(transLevel)
        else:
            return norm.cdf(transLevel)