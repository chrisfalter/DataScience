# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 23:52:30 2017

@author: cfalter
"""
from grade_utils import letterGrade
import numpy as np

COLS_Homework = np.arange(0,6)
COLS_Labs = np.arange(6,17)
COLS_FinalProject = np.arange(17,18)
COLS_MidTerm1 = np.arange(18,19)
COLS_Quizzes = np.arange(19,28)
COLS_MidTerm2 = np.arange(28,29)

Weight_Labs = 0.30
Weight_Homework = 0.20
Weight_Quizzes = 0.15 * 10 # multiply quiz scores by 10 bc/they have a max of 10, not 100
Weight_Midterm1 = 0.10
Weight_Midterm2 = 0.15
Weight_FinalProject = 0.10

def calc_weights(weights, cols, group_weight):
    group = weights[cols]
    sum_group = sum(group)
    return group_weight * group / sum_group
    
def shaped(a):
    ''' 
    returns an array of shape (n,1) from an array of shape (n,)
    '''
    return a[:,np.newaxis]

def main():
    # load the grades from disk
    gradebook = np.load("./Grades.npy")

    # create views of the gradebook
    weights = gradebook[0,1:] # first row, except for 0,0
    student_ids = gradebook[1:,0] # first column, except for 0,0
    student_ids = np.array([str(x) for x in student_ids])
    scores = gradebook[1:,1:]

    # out-of-range values are treated as zeros 
    scores = np.where(np.logical_or(scores < 0, scores > 102), 0, scores)

    # refine the array of weights so they sum to 1.0, based on the weight of groups
    # and weights within groups
    w_homework = calc_weights(weights, COLS_Homework, Weight_Homework)
    w_labs = calc_weights(weights, COLS_Labs, Weight_Labs)
    w_final_project = calc_weights(weights, COLS_FinalProject, Weight_FinalProject)
    w_midterm1 = calc_weights(weights, COLS_MidTerm1, Weight_Midterm1)
    w_quizzes = calc_weights(weights, COLS_Quizzes, Weight_Quizzes)
    w_midterm2 = calc_weights(weights, COLS_MidTerm2, Weight_Midterm2)
    weights = np.concatenate((w_homework, w_labs, w_final_project, w_midterm1, w_quizzes, w_midterm2))    

    # Result 1: Final score + letter grade of each student
    final_scores = np.sum(weights * scores, axis = 1)
    final_scores_str = np.array(["{0:.2f}".format(x) for x in final_scores])
    grades = np.array([letterGrade(s) for s in final_scores])
    finalGrades = np.concatenate(
        (shaped(student_ids), shaped(final_scores_str), shaped(grades)),
        axis = 1)
    np.save("FinalGrades", finalGrades) # saved as an array of strings

    # Result 2: Average final score + letter grade across all students
    avg_finalGrade = np.mean(final_scores)
    avg_letterGrade = letterGrade(avg_finalGrade)
    averageGrades = np.array(["{0:.2f}".format(avg_finalGrade), avg_letterGrade])
    np.save("AverageGrades", averageGrades)

    # Result 3: Average score of each assignment
    assignmentAvgs = np.mean(scores, axis = 0)
    np.save("AverageAssig", assignmentAvgs)

    # Result 4: Average score of each assignment group
    aa = assignmentAvgs # view to make code more terse
    groupAvgs = np.array([
        np.mean(aa[COLS_Labs]),
        np.mean(aa[COLS_Homework]),
        np.mean(aa[COLS_Quizzes]),
        np.mean(aa[COLS_MidTerm1]),
        np.mean(aa[COLS_MidTerm2]),
        np.mean(aa[COLS_FinalProject])])
    np.save("AverageGroup", groupAvgs)


if __name__ == '__main__':
    main()
