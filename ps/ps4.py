def nestEggFixed(salary, save, growthRate, years):
    YearEnd = 0
    RTFund = []
    while(years > 0):
        YearEnd = YearEnd * (1 + 0.01 * growthRate) + salary * save * 0.01
        RTFund.append(int(YearEnd))
        years -= 1
    RTFund.reverse()
    return RTFund

def nestEggVariable(salary, save, growthRates):
    years = len(growthRates)
    YearEnd = 0
    RTFund = []
    CurrentYear = 1
    while(years > 0):
        YearEnd = YearEnd * (1 + 0.01 * growthRates[CurrentYear - 1]) + salary * save * 0.01
        RTFund.append(int(YearEnd))
        CurrentYear += 1
        years -= 1
    return RTFund

def postRetirement(savings, growthRates, expenses):
    years = len(growthRates)
    YearEnd = savings
    CurrentYear = 1
    SavingsLeft = []
    while(years > 0):
        YearEnd = YearEnd * (1 + 0.01 * growthRates[CurrentYear - 1]) - expenses
        SavingsLeft.append(int(YearEnd))
        CurrentYear += 1
        years -= 1
    return SavingsLeft

def findMaxExpenses(salary, save, preRetireGrowthRates, postRetireGrowthRates, epsilon):
    #preRetire
    Savings = nestEggVariable(salary, save, preRetireGrowthRates)
    SavingAtRetire = Savings[-1]
    #afterRetire
    MinExp = 0
    MaxExp = SavingAtRetire + epsilon
    expenses = (MinExp + MaxExp) / 2
    print "Current estimate: ", expenses
    SavingsLeft = postRetirement(SavingAtRetire, postRetireGrowthRates, expenses)[-1]
    count = 0
    while(abs(SavingsLeft) > epsilon and count <= 500):
        if SavingsLeft > epsilon:
            MinExp = expenses
        elif SavingsLeft < -epsilon:
            MaxExp = expenses
        expenses = (MinExp + MaxExp) / 2
        print "Current estimate: ", expenses
        SavingsLeft = postRetirement(SavingAtRetire, postRetireGrowthRates, expenses)[-1]
        count += 1
    if count > 500:
        print "Error, epsilon too small."
    else:
        return expenses

def testNestEggFixed():
    RTFund = nestEggFixed(50000,5,3,20)
    print RTFund

def testNestEggVariable():
    RTFund = nestEggVariable(50000, 5,[5, 6, 11, 4, 12, 6])
    print RTFund

def testPostRetirement():
    SavingsLeft = postRetirement(50000, [1,3,2,-10,-5,14], 5000)
    print SavingsLeft
    SavingsLeft = postRetirement(50000, [1,3,2,-10,-5,14], 20000)
    print SavingsLeft

def testFindMaxExpenses():
    expenses = findMaxExpenses(50000, 5,[5, 6, 11, 4, 12, 6],[1,3,2,-10,-5,14],10)
    print expenses
    expenses = findMaxExpenses(50000, 5,[5, 6, 11, 4, 12, 6],[1],100)
    print expenses
    
        
