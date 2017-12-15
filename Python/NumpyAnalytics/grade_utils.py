# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 23:50:44 2017

@author: cfalter
"""
from decimal import Decimal

def letterGrade(score):
    ''' given a numerical score, returns the corresponding letter grade
    Parameters:
    score - in string format
    
    Returns:
    letter grade in string format (e.g., 'A-')
    '''
    score = Decimal(score)
    if score >= 93.0: 
        return 'A'
    elif score >= 90.0: 
        return 'A-'
    elif score >= 86.0:
        return 'B+'
    elif score >= 83.0:
        return 'B'
    elif score >= 80.0:
        return 'B-'
    elif score >= 76.0:
        return 'C+'
    elif score >= 73.0:
        return 'C'
    elif score >= 70.0:
        return 'C-'
    elif score >= 66.0:
        return 'D+'
    elif score >= 63.0:
        return 'D'
    elif score >= 60.0:
        return 'D-'
    else:
        return 'F'


