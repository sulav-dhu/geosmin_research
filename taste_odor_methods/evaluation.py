"""Probability scoring functions used in the research project.

The functions take arrays supplied by the caller. No predictions or outcomes
from the study are included.
"""
import numpy as np
from scipy.stats import beta
from sklearn.metrics import average_precision_score, roc_auc_score, brier_score_loss, log_loss
from sklearn.linear_model import LogisticRegression
def metrics(y,p):
    y=np.asarray(y,dtype=int);p=np.asarray(p,dtype=float)
    n=len(y)
    if n==0:return {"n":0,"positive_days":0,"prevalence":np.nan,"average_precision":np.nan,"roc_auc":np.nan,"brier":np.nan,"log_loss":np.nan,"calibration_intercept":np.nan,"calibration_slope":np.nan}
    both=len(np.unique(y))==2
    out={"n":n,"positive_days":int(y.sum()),"prevalence":y.mean(),"average_precision":average_precision_score(y,p) if y.sum()>0 else np.nan,"roc_auc":roc_auc_score(y,p) if both else np.nan,"brier":brier_score_loss(y,p),"log_loss":log_loss(y,np.clip(p,1e-8,1-1e-8),labels=[0,1]),"calibration_intercept":np.nan,"calibration_slope":np.nan}
    if both and len(np.unique(p))>2 and y.sum()>=10 and (1-y).sum()>=10:
        logits=np.log(np.clip(p,1e-6,1-1e-6)/(1-np.clip(p,1e-6,1-1e-6)))
        fit=LogisticRegression(C=1e6).fit(logits[:,None],y)
        out.update(calibration_intercept=fit.intercept_[0],calibration_slope=fit.coef_[0,0])
    return out

def exact_interval(k,n):
    if not n:return np.nan,np.nan
    return (float(beta.ppf(.025,k,n-k+1)) if k else 0.,float(beta.ppf(.975,k+1,n-k)) if k<n else 1.)
