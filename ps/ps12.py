# 6.00 Problem Set 12
#
# Name:
# Collaborators:
# Time:

import numpy
import random
import pylab
import copy

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """    

#
# PROBLEM 1
#

class SimpleVirus(object):
    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb
        
    def doesClear(self):
        """
        Stochastically determines whether this virus is cleared from the
        patient's body at a time step. 

        returns: Using a random number generator (random.random()), this method
        returns True with probability self.clearProb and otherwise returns
        False.
        """
        x = random.random()
        if x <= self.clearProb:
            return True
        else:
            return False
    
    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the SimplePatient and
        Patient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """
        prob = self.maxBirthProb * (1 - popDensity)
        x = random.random()
        if x <= prob:
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        else:
            return False

class SimplePatient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """
    
    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)
        
        maxPop: the  maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.maxPop = maxPop

    def getTotalPop(self):
        """
        Gets the current total virus population. 

        returns: The total virus population (an integer)
        """
        return len(self.viruses)

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:

        - Determine whether each virus particle survives and updates the list
          of virus particles accordingly.

        - The current population density is calculated. This population density
          value is used until the next call to update() 

        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient.                    

        returns: the total virus population at the end of the update (an
        integer)
        """
        # clear and update list
        clrcount = 0
        for i in range(len(self.viruses)):
            x = self.viruses[i].doesClear()
            if x == True:
                self.viruses[i] = 0
                clrcount += 1
        for j in range(clrcount):
            self.viruses.remove(0)
                
        # calculate population density
        popDensity = len(self.viruses) / float(self.maxPop)
        
        # reproduce and update list
        baby = []
        for virus in self.viruses:
            new = virus.reproduce(popDensity)
            if new != False:
                baby.append(new)
        self.viruses += baby
        
        return len(self.viruses)

#
# PROBLEM 2
#

def problem2():
    """
    Run the simulation and plot the graph for problem 2 (no drugs are used,
    viruses do not have any drug resistance).    

    Instantiates a patient, runs a simulation for 300 timesteps, and plots the
    total virus population as a function of time.    
    """
    v = SimpleVirus(0.1, 0.05)
    vs = []
    for i in range(100):
        vs.append(v)
    p = SimplePatient(vs, 1000)
    totalpop = [100]
    for time in range(300):
        newpop = p.update()
        totalpop.append(newpop)
    
    pylab.figure()
    xAxis = pylab.arange(0, 301)
    yAxis = totalpop
    pylab.plot(xAxis, yAxis)
    pylab.title('Virus grow with no drug use')
    pylab.xlabel('Time in hours')
    pylab.ylabel('Virus population')
    pylab.show()
    
    
#
# PROBLEM 3
#

class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """    
    
    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.
        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        
        clearProb: Maximum clearance probability (a float between 0-1).
        
        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'grimpex',False}, means that this virus
        particle is resistant to neither guttagonol nor grimpex.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.        
        """
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb
        self.resistances = resistances
        self.mutProb = mutProb
        
    def getResistance(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in Patient to determine how many virus
        particles have resistance to a drug.        

        drug: the drug (a string).

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        return self.resistances[drug]
        
    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient class.

        If the virus particle is not resistant to any drug in activeDrugs,
        then it does not reproduce. Otherwise, the virus particle reproduces
        with probability:       
        
        self.maxBirthProb * (1 - popDensity).                       
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). 

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.        

        For example, if a virus particle is resistant to guttagonol but not
        grimpex, and `self.mutProb` is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90% 
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        grimpex and a 90% chance that the offspring will not be resistant to
        grimpex.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population        

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings). 
        
        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.         
        """
        # check drug resistance
        for drug in activeDrugs:
            if self.resistances[drug] == False:
                return False
        # if reproduce  
        prob = self.maxBirthProb * (1 - popDensity)
        x = random.random()
        if x <= prob:
            # if mutate
            babyResists = copy.deepcopy(self.resistances)
            for drug in babyResists.keys():
                p = random.random()
                if p < self.mutProb:
                    babyResists[drug] = not babyResists[drug]
            return ResistantVirus(self.maxBirthProb, self.clearProb, babyResists, self.mutProb)
        else:
            return False
            
class Patient(SimplePatient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """
    
    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).               

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)
        
        maxPop: the  maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.maxPop = maxPop
        self.drugUse = []
        
    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the 
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: list of drugs being administered to a patient is updated
        """
        if newDrug not in self.drugUse:
            self.drugUse.append(newDrug)

    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """
        return self.drugUse
        
    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in 
        drugResist.        

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'grimpex'])

        returns: the population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        count = 0
        for virus in self.viruses:
            flag = True
            for drug in drugResist:
                if virus.resistances[drug] == False:
                    flag = False
                    break
            if flag:
                count += 1
        return count

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of 
          virus particles accordingly
          
        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient. 
          The listof drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces. 

        returns: the total virus population at the end of the update (an
        integer)
        """
        # clear and update list
        clrcount = 0
        for i in range(len(self.viruses)):
            x = self.viruses[i].doesClear()
            if x == True:
                self.viruses[i] = 0
                clrcount += 1
        for j in range(clrcount):
            self.viruses.remove(0)
                
        # calculate population density
        popDensity = len(self.viruses) / float(self.maxPop)
        
        # reproduce and update list
        baby = []
        for virus in self.viruses:
            new = virus.reproduce(popDensity, self.drugUse)
            if new != False:
                baby.append(new)
        self.viruses += baby
        
        return len(self.viruses)

#
# PROBLEM 4
#

def runsim1(time):
    v = ResistantVirus(0.1, 0.05, {'guttagonol':False}, 0.005)
    vs = []
    for i in range(100):
        vs.append(v)
    p = Patient(vs, 1000)
    totalpop = [100]
    resist = [0]
    for time1 in range(time):
        newpop = p.update()
        totalpop.append(newpop)
        res = p.getResistPop(['guttagonol'])
        resist.append(res)
    #add drug now
    p.addPrescription('guttagonol')
    for time2 in range(150):
        newpop = p.update()
        totalpop.append(newpop)
        res = p.getResistPop(['guttagonol'])
        resist.append(res)
    return resist, totalpop

def problem4():
    """
    Runs simulations and plots graphs for problem 4.

    Instantiates a patient, runs a simulation for 150 timesteps, adds
    guttagonol, and runs the simulation for an additional 150 timesteps.

    total virus population vs. time  and guttagonol-resistant virus population
    vs. time are plotted
    """
    resist, totalpop = runsim1(150)   
    pylab.figure()
    xAxis = pylab.arange(0, 301)
    y1 = totalpop
    y2 = resist
    pylab.plot(xAxis, y1)
    pylab.plot(xAxis, y2)
    pylab.title('Virus grow with one drug use')
    pylab.xlabel('Time in hours')
    pylab.ylabel('Virus population')
    pylab.show()
   
#
# PROBLEM 5
#
        
def problem5(time):
    """
    Runs simulations and make histograms for problem 5.

    Runs multiple simulations to show the relationship between delayed treatment
    and patient outcome.

    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).    
    """
    finalpop = []
    for i in range(50):
        resist, totalpop = runsim1(time) # replaced by 300, 150, 75, 0
        finalpop.append(totalpop[-1])
    finalpop = sorted(finalpop)
    pylab.figure()
    pylab.hist(finalpop, bins = 10)
    pylab.title('Delaying treatment time 300')
    pylab.xlabel('Final virus pop')
    pylab.ylabel('Times')
    pylab.show()

#
# PROBLEM 6
#
def runsim2(time):
    v = ResistantVirus(0.1, 0.05, {'guttagonol':False, 'grimpex':False}, 0.005)
    vs = []
    for i in range(100):
        vs.append(v)
    p = Patient(vs, 1000)
    totalpop = [100]
    resist_gu = [0]
    resist_gr = [0]
    resist_both = [0]
    for time1 in range(150):
        newpop = p.update()
        totalpop.append(newpop)
        res_gu = p.getResistPop(['guttagonol'])
        res_gr = p.getResistPop(['grimpex'])
        res_both = p.getResistPop(['guttagonol', 'grimpex'])
        resist_gu.append(res_gu)
        resist_gr.append(res_gr)
        resist_both.append(res_both)
    # add drug now
    p.addPrescription('guttagonol')
    for time2 in range(time):
        newpop = p.update()
        totalpop.append(newpop)
        res_gu = p.getResistPop(['guttagonol'])
        res_gr = p.getResistPop(['grimpex'])
        res_both = p.getResistPop(['guttagonol', 'grimpex'])
        resist_gu.append(res_gu)
        resist_gr.append(res_gr)
        resist_both.append(res_both)
    # add a second drug
    p.addPrescription('grimpex')
    for time3 in range(150):
        newpop = p.update()
        totalpop.append(newpop)
        res_gu = p.getResistPop(['guttagonol'])
        res_gr = p.getResistPop(['grimpex'])
        res_both = p.getResistPop(['guttagonol', 'grimpex'])
        resist_gu.append(res_gu)
        resist_gr.append(res_gr)
        resist_both.append(res_both)
    return resist_gu, resist_gr, resist_both, totalpop
    

def problem6(time):
    """
    Runs simulations and make histograms for problem 6.

    Runs multiple simulations to show the relationship between administration
    of multiple drugs and patient outcome.
    
    Histograms of final total virus populations are displayed for lag times of
    150, 75, 0 timesteps between adding drugs (followed by an additional 150
    timesteps of simulation).
    """
    finalpop = []
    for i in range(30):
        resist_gu, resist_gr, resist_both, totalpop = runsim2(time) # replaced by 300, 150, 75, 0
        finalpop.append(totalpop[-1])
    finalpop = sorted(finalpop)
    pylab.figure()
    pylab.hist(finalpop, bins = 10)
    pylab.title('Wait some time before applying a second drug')
    pylab.xlabel('Final virus pop')
    pylab.ylabel('Times')
    pylab.show()

#
# PROBLEM 7
#
     
def problem7(time):
    """
    Run simulations and plot graphs examining the relationship between
    administration of multiple drugs and patient outcome.

    Plots of total and drug-resistant viruses vs. time are made for a
    simulation with a 300 time step delay between administering the 2 drugs and
    a simulations for which drugs are administered simultaneously.        
    """
    resist_gu, resist_gr, resist_both, totalpop = runsim2(time) # 300 and 0
    pylab.figure()
    xAxis = pylab.arange(0, 301+time)
    y1 = totalpop
    y2 = resist_gu
    y3 = resist_gr
    y4 = resist_both
    pylab.plot(xAxis, y1)
    pylab.plot(xAxis, y2)
    pylab.plot(xAxis, y3)
    pylab.plot(xAxis, y4)
    pylab.title('Virus population with two drugs')
    pylab.xlabel('Time in hours')
    pylab.ylabel('Virus population')
    pylab.show()
