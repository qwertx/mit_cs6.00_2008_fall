# 6.00 Problem Set 8
#
# Intelligent Course Advisor
#
# Name:
# Collaborators:
# Time:
#

import time

SUBJECT_FILENAME = "subjects.txt"
VALUE, WORK = 0, 1

#
# Problem 1: Building A Subject Dictionary
#
def loadSubjects(filename):
    """
    Returns a dictionary mapping subject name to (value, work), where the name
    is a string and the value and work are integers. The subject information is
    read from the file named by the string filename. Each line of the file
    contains a string of the form "name,value,work".

    returns: dictionary mapping subject name to (value, work)
    """

    # The following sample code reads lines from the specified file and prints
    # each one.
    inputFile = open(filename)
    Subjlib = {}
    for line in inputFile:
        eachline = line.strip()
        temp = eachline.split(',')
        Subjlib[temp[0]] = (int(temp[1]), int(temp[2]))
    return Subjlib

    # TODO: Instead of printing each line, modify the above to parse the name,
    # value, and work of each subject and create a dictionary mapping the name
    # to the (value, work).

def printSubjects(subjects):
    """
    Prints a string containing name, value, and work of each subject in
    the dictionary of subjects and total value and work of all subjects
    """
    totalVal, totalWork = 0,0
    if len(subjects) == 0:
        return 'Empty SubjectList'
    res = 'Course\tValue\tWork\n======\t====\t=====\n'
    subNames = subjects.keys()
    subNames.sort()
    for s in subNames:
        val = subjects[s][VALUE]
        work = subjects[s][WORK]
        res = res + s + '\t' + str(val) + '\t' + str(work) + '\n'
        totalVal += val
        totalWork += work
    res = res + '\nTotal Value:\t' + str(totalVal) +'\n'
    res = res + 'Total Work:\t' + str(totalWork) + '\n'
    print res

def cmpValue(subInfo1, subInfo2):
    """
    Returns True if value in (value, work) tuple subInfo1 is GREATER than
    value in (value, work) tuple in subInfo2
    """
    val1 = subInfo1[VALUE]
    val2 = subInfo2[VALUE]
    return  val1 > val2

def cmpWork(subInfo1, subInfo2):
    """
    Returns True if work in (value, work) tuple subInfo1 is LESS than than work
    in (value, work) tuple in subInfo2
    """
    work1 = subInfo1[WORK]
    work2 = subInfo2[WORK]
    return  work1 < work2

def cmpRatio(subInfo1, subInfo2):
    """
    Returns True if value/work in (value, work) tuple subInfo1 is 
    GREATER than value/work in (value, work) tuple in subInfo2
    """
    val1 = subInfo1[VALUE]
    val2 = subInfo2[VALUE]
    work1 = subInfo1[WORK]
    work2 = subInfo2[WORK]
    return float(val1) / work1 > float(val2) / work2

#
# Problem 2: Subject Selection By Greedy Optimization
#
def greedyAdvisor(subjects, maxWork, comparator):
    """
    Returns a dictionary mapping subject name to (value, work) which includes
    subjects selected by the algorithm, such that the total work of subjects in
    the dictionary is not greater than maxWork.  The subjects are chosen using
    a greedy algorithm.  The subjects dictionary should not be mutated.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    comparator: function taking two tuples and returning a bool
    returns: dictionary mapping subject name to (value, work)
    """
    def sort(ls, comparator):
        """
        Sorts the list of subjects' names in descendig order
        acording to the comparator.
        """
        for i in range(1, len(ls)):
            value = ls[i]
            j = i - 1
            done = False

            while not done:
                if comparator(subjects[value], subjects[ls[j]]):
                    ls[j+1] = ls[j]
                    j -= 1
                    if j < 0:
                        done = True
                else:
                    done = True
            ls[j+1] = value
                        
    schedule_list = subjects.keys()
    sort(schedule_list, comparator)
    recommended_list = {}
    courseLoad = 0
    done = False
    
    for course in schedule_list:
        if subjects[course][1] <= maxWork - courseLoad:
            recommended_list[course] = subjects[course]
            courseLoad += subjects[course][1]
    return recommended_list
    

def bruteForceAdvisor(subjects, maxWork):
    """
    Returns a dictionary mapping subject name to (value, work), which
    represents the globally optimal selection of subjects using a brute force
    algorithm.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    returns: dictionary mapping subject name to (value, work)
    """
    nameList = subjects.keys()
    tupleList = subjects.values()
    bestSubset, bestSubsetValue = \
            bruteForceAdvisorHelper(tupleList, maxWork, 0, None, None, [], 0, 0)
    outputSubjects = {}
    for i in bestSubset:
        outputSubjects[nameList[i]] = tupleList[i]
    return outputSubjects

def bruteForceAdvisorHelper(subjects, maxWork, i, bestSubset, bestSubsetValue,
                            subset, subsetValue, subsetWork):
    # Hit the end of the list.
    if i >= len(subjects):
        if bestSubset == None or subsetValue > bestSubsetValue:
            # Found a new best.
            return subset[:], subsetValue
        else:
            # Keep the current best.
            return bestSubset, bestSubsetValue
    else:
        s = subjects[i]
        # Try including subjects[i] in the current working subset.
        if subsetWork + s[WORK] <= maxWork:
            subset.append(i)
            bestSubset, bestSubsetValue = bruteForceAdvisorHelper(subjects,
                    maxWork, i+1, bestSubset, bestSubsetValue, subset,
                    subsetValue + s[VALUE], subsetWork + s[WORK])
            subset.pop()
        bestSubset, bestSubsetValue = bruteForceAdvisorHelper(subjects,
                maxWork, i+1, bestSubset, bestSubsetValue, subset,
                subsetValue, subsetWork)
        return bestSubset, bestSubsetValue

#
# Problem 3: Subject Selection By Brute Force
#
def bruteForceTime():
    """
    Runs tests on bruteForceAdvisor and measures the time required to compute
    an answer.
    """
    subjects = loadSubjects(SUBJECT_FILENAME)
    maxWork = int(raw_input("Type in your max work: "))
    start_time = time.time()
    x = bruteForceAdvisor(subjects, maxWork)
    end_time = time.time()
    total_time = end_time - start_time
    print x
    print 'It took %0.2fs to get the result.' % total_time

# Problem 3 Observations
# ======================
#
# TODO: write here your observations regarding bruteForceTime's performance

#
# Problem 4: Subject Selection By Dynamic Programming
#
def dpAdvisor(subjects, maxWork):
    """
    Returns a dictionary mapping subject name to (value, work) that contains a
    set of subjects that provides the maximum value without exceeding maxWork.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    returns: dictionary mapping subject name to (value, work)
    """
    rec_dict = {}
    m = {}

    work_list = []
    value_list = []
    key_list = []

    for i in subjects:
        work_list.append(subjects[i][1])
        value_list.append(subjects[i][0])
        key_list.append(i)

    value, rec_list = dpAdvisorHelper(work_list, value_list, len(work_list)-1, maxWork, m)

    for each in rec_list:
        rec_dict[key_list[each]] = (value_list[each], work_list[each])
    return rec_dict

def dpAdvisorHelper(w, v, i, aW, m):
    try:
        return m[(i, aW)]
    except KeyError:
        if i == 0:
            if w[i] < aW:
                m[(i, aW)] = v[i], [i]
                return v[i], [i]
            else:
                m[(i, aW)] = 0, []
                return 0, []

        without_i, course_list = dpAdvisorHelper(w, v, i-1, aW, m)
        if w[i] > aW:
            m[(i, aW)] = without_i, course_list
            return without_i, course_list
        else:
            with_i, course_list_temp = dpAdvisorHelper(w, v, i-1, aW - w[i], m)
            with_i += v[i]
        if with_i > without_i:
            i_value = with_i
            course_list = [i] + course_list_temp
        else:
            i_value = without_i

        m[(i, aW)] = i_value, course_list
    return i_value, course_list       

###
# Problem 5: Performance Comparison
#
def dpTime():
    """
    Runs tests on dpAdvisor and measures the time required to compute an
    answer.
    """
    subjects = loadSubjects(SUBJECT_FILENAME)
    maxWork = int(raw_input("Type in your max work: "))
    start_time = time.time()
    final = dpAdvisor(subjects, maxWork)
    end_time = time.time()
    total_time = end_time - start_time
    print final
    print 'It took %0.2fs to get the result.' % total_time

# Problem 5 Observations
# ======================
#
# TODO: write here your observations regarding dpAdvisor's performance and
# how its performance compares to that of bruteForceAdvisor.
