import time
import numpy
class MinMax:
    lahsaApplicants, splaApplicants, applicants = [], [], []
    splaSpecific = []
    lahsaSpecific = []
    common = []
    unselectedApplicants = []
    selectedApplicants = []
    newlySelectedSplaApplicants = []
    newlySelectedLahsaApplicants = []
    splaScore = 0
    lahsaScore = 0
    tempSplaScore = 0
    tempLahsaScore = 0
    futureSplaList = []
    futureLahsaList = []
    residualSplaScore = 0
    applicant = []
    flas = 0
    pScores = []
    qScores = []
    ct=0
    dict = {}

    class Applicant:
        def __init__(self, id, gender,age,pets,medical,car,license,schedule, isSelected):
            self.id = id
            self.gender = gender
            self.age = age
            self.pets = pets
            self.medical = medical
            self.car = car
            self.license = license
            self.schedule = schedule
            self.isSelected = isSelected
    class LAHSA:
        def __init__(self, beds):
            self.beds = beds
            self.remaining = [beds for i in range(7)]
            self.efficiency = 0
            self.remainingResources = beds * 7
    class SPLA:
        def __init__(self, slots):
            self.slots = slots
            self.remaining = [slots for i in range(7)]
            self.efficiency = 0
            self.remainingResources = slots * 7

    def __init__(self, inputFile):
        start_time = time.time()
        file = open(inputFile, "r")
        f = file.readlines()
        self.spla = self.SPLA(int(f.__getitem__(1)))
        self.lahsa= self.LAHSA(int(f.__getitem__(0)))
        chosenByLAHSA = int(f.__getitem__(2))
        lineNumber = 3

        for i in range(chosenByLAHSA):
            self.lahsaApplicants.append(f.__getitem__(lineNumber).strip())
            lineNumber+=1
        chosenBySPLA = int(f.__getitem__(lineNumber))
        lineNumber+=1

        for i in range(chosenBySPLA):
            self.splaApplicants.append(f.__getitem__(lineNumber).strip())
            lineNumber+=1
        numberOfApplicants = int(f.__getitem__(lineNumber))
        lineNumber+=1
        self.readAndAddApplicants(f, lineNumber, numberOfApplicants)
        # list of applicant objects that are selected both in SPLA and LAHSA
        self.selectedApplicants = [app for app in self.applicants if app.isSelected]
        # list of applicant objects that are selected by SPLA
        self.selectedBySPLA = [app for app in self.selectedApplicants if app.id in self.splaApplicants]
        # list of applicant objects that are selected by LAHSA
        self.selectedByLAHSA= [app for app in self.selectedApplicants if app.id in self.lahsaApplicants]

        # Segregating the applicants into different lists
        self.unselectedApplicants = [app for app in self.applicants if app.isSelected == False]
        #print("hai")
        # #print(j.id for j in self.selectedApplicants)
        # #print(self.selectedApplicants[0].id)
        # #print(self.selectedApplicants[1].id)
        #print(len(self.unselectedApplicants))
        for app in self.unselectedApplicants:
            if app.car and app.license and app.medical ==False and app.age > 17 and app.gender == "F" and app.pets == False:
                self.common.append(app)
            elif app.car and app.license and app.medical == False:
                self.splaSpecific.append(app)
            elif app.age > 17 and app.gender == "F" and app.pets == False:
                self.lahsaSpecific.append(app)
        self.calculateSelectedApplicantsScore()
        #print(self.spla.remaining)
        #print(self.spla.efficiency)
        #print(self.lahsa.remaining)
        #print(self.lahsa.efficiency)

        scores=[]
        scores.append(self.spla.efficiency)
        scores.append(self.lahsa.efficiency)
        self.pScores.append(scores[0])
        self.pScores.append(scores[1])
        self.qScores.append(scores[0])
        self.qScores.append(scores[1])
        self.flag = len(self.common+self.splaSpecific)
        self.check = len(self.common+self.splaSpecific)
        # print()
        l = self.splaGame(self.common + self.splaSpecific, scores[1], scores[0])
        print(l)
        # print(self.applicant)
        file = open("output.txt", "w+")
        self.applicant.sort()
        file.write(str(self.applicant[0]))
        print(self.ct)
        print("--- %s seconds ---" % (time.time() - start_time))
        # print(len(self.dict))
        # print(self.maxSpla)
        # print(self.maxLahsa)

    def readAndAddApplicants(self, f, lineNumber, numberOfApplicants):
        for i in range(numberOfApplicants):
            id = f.__getitem__(lineNumber)[:5]
            isSelected = True if (id in self.splaApplicants or id in self.lahsaApplicants) else False
            gender = f.__getitem__(lineNumber)[5:6]
            age = int(f.__getitem__(lineNumber)[6:9]) if f.__getitem__(lineNumber)[6:9][0] == "0" else int(f.__getitem__(lineNumber)[6:9])
            pets = False if f.__getitem__(lineNumber)[9:10] == "N" else True
            medical = False if f.__getitem__(lineNumber)[10:11] == "N" else True
            car = False if f.__getitem__(lineNumber)[11:12] == "N" else True
            license = False if f.__getitem__(lineNumber)[12:13] == "N" else True
            s = f.__getitem__(lineNumber)[13:].strip()
            schedule = []
            schedule.append(int(s[0]))
            schedule.append(int(s[1]))
            schedule.append(int(s[2]))
            schedule.append(int(s[3]))
            schedule.append(int(s[4]))
            schedule.append(int(s[5]))
            schedule.append(int(s[6]))
            self.applicants.append(self.Applicant(id, gender, age, pets, medical, car, license, schedule, isSelected))
            lineNumber += 1

    # calculate efficiency after the given selected applicants
    def calculateSelectedApplicantsScore(self):
        for app in self.selectedBySPLA:
            for i in range(len(app.schedule)):
                self.spla.remaining[i] =  self.spla.remaining[i] -  1 if app.schedule[i] == 1 else self.spla.remaining[i]
                self.spla.efficiency = self.spla.efficiency +1 if app.schedule[i] == 1 else self.spla.efficiency
                self.spla.remainingResources = self.spla.remainingResources - 1 if app.schedule[i] == 1 else self.spla.remainingResources
        for app in self.selectedByLAHSA:
            for i in range(len(app.schedule)):
                self.lahsa.remaining[i] =  self.lahsa.remaining[i] -  1 if app.schedule[i] == 1 else self.lahsa.remaining[i]
                self.lahsa.efficiency = self.lahsa.efficiency +1 if app.schedule[i] == 1 else self.lahsa.efficiency
                self.lahsa.remainingResources = self.lahsa.remainingResources - 1 if app.schedule[
                                                                                       i] == 1 else self.lahsa.remainingResources

    def splaGame(self, combList, lahsaScore, splaScore):
        if (len(combList) == 0):
            # scores[1] += self.newlySelectedLahsaApplicants[-1].schedule.count(1)
            score = self.residualRecursionForLahsa(self.lahsaSpecific, 0)
            for i in range(self.count):
                self.lahsa.remainingResources += sum(self.newlySelectedLahsaApplicants[-1].schedule)
                for k in range(len(self.newlySelectedLahsaApplicants[-1].schedule)):
                    if self.newlySelectedLahsaApplicants[-1].schedule[k] == 1:
                        self.lahsa.remaining[k] = self.lahsa.remaining[k] + 1
                self.newlySelectedLahsaApplicants = self.newlySelectedLahsaApplicants[0:-1]
                self.futureLahsaList = self.futureLahsaList[0:-1]
            self.count = 0
            lahsaScore = self.lahsa.beds * 7 - self.lahsa.remainingResources + score
            splaScore = (self.spla.slots*7) - self.spla.remainingResources
            self.ct += 1

            return lahsaScore, splaScore
        # if (len(combList) == 1):
        #     if self.spla.remainingResources <= 0:
        #         return scores
        #     if(~self.contradicts(combList[0], self.spla) and self.spla.remainingResources>0):
        #         if combList[0] in self.common:
        #             self.common = [i for i in self.common if i.id != combList[0].id]
        #         else:
        #             self.splaSpecific = [i for i in self.splaSpecific if i.id != combList[0].id]
        #         scores[0] += combList[0].schedule.count(1)
        #     return scores
        # self.applicant = combList[0].id
        # self.pScores[0] = scores[0]
        # self.pScores[1] = scores[1]
        maxSpla = 0
        otherScore = 0
        entered = False
        length = len(combList)
        possible = []
        for app in combList:
            # scores[0] = self.pScores[0]
            # scores[1] = self.pScores[1]
            if(self.contradicts(app, self.spla)==False):
                commonBoolaen = False
                entered = True
                if app in self.common:
                    commonBoolaen = True
                    self.common = [i for i in self.common if i.id!=app.id]
                else:
                    self.splaSpecific = [i for i in self.splaSpecific if i.id!=app.id]
                self.newlySelectedSplaApplicants.append(app)
                self.tempSplaScore += app.schedule.count(1)
                self.spla.remainingResources -= sum(app.schedule)
                self.futureSplaList.append(app.id)
                for k in range(len(app.schedule)):
                    if app.schedule[k] == 1:
                        self.spla.remaining[k] = self.spla.remaining[k] - 1
                # scores[0] += app.schedule.count(1)
                temp = maxSpla
                l1 = self.futureSplaList[:]
                l2 = self.futureLahsaList[:]
                l1.sort()
                l2.sort()
                key = ",".join(l1) +";"+ ",".join(l2)
                if key in self.dict:
                    a = int(self.dict[key].split(",")[0])
                    b = int(self.dict[key].split(",")[1])
                else :
                    a, b = self.lahsaGame(self.common + self.lahsaSpecific, lahsaScore, splaScore)
                    c = a
                    d = b
                    self.dict[key] = str(c) +"," + str(d)
                # if maxSpla == b:

                if b >= maxSpla:
                    if maxSpla < b:
                        possible = []
                        possible.append(app.id + "_" + str(a) + "_" + str(b))
                    if maxSpla == b:
                        possible.append(app.id + "_" + str(a) + "_" + str(b))

                    if(self.check == length and b>maxSpla):
                        self.applicant = []
                        self.applicant.append(app.id)
                    if (self.check == length and b == maxSpla):
                        self.applicant.append(app.id)

                    maxSpla = b
                    splaScore = b
                    lahsaScore = a
                    otherScore = a
                self.common.append(app) if commonBoolaen else self.splaSpecific.append(app)
                self.newlySelectedSplaApplicants = self.newlySelectedSplaApplicants[:-1]
                self.tempSplaScore -= app.schedule.count(1)
                self.spla.remainingResources += sum(app.schedule)
                self.futureSplaList = self.futureSplaList[:-1]
                for k in range(len(app.schedule)):
                    if app.schedule[k] == 1:
                        self.spla.remaining[k] = self.spla.remaining[k] + 1
                if (len(combList) == self.check):
                    print(app.id, b, a)
        if entered == False:
            score = self.residualRecursionForLahsa(self.common + self.lahsaSpecific, 0)
            for i in range(self.count):
                self.lahsa.remainingResources += sum(self.newlySelectedLahsaApplicants[-1].schedule)
                for k in range(len(self.newlySelectedLahsaApplicants[-1].schedule)):
                    if self.newlySelectedLahsaApplicants[-1].schedule[k] == 1:
                        self.lahsa.remaining[k] = self.lahsa.remaining[k] + 1
                self.newlySelectedLahsaApplicants = self.newlySelectedLahsaApplicants[0:-1]
                self.futureLahsaList = self.futureLahsaList[0:-1]
            self.count = 0
            lahsaScore = self.lahsa.beds * 7 - self.lahsa.remainingResources + score
            splaScore = (self.spla.slots* 7) - self.spla.remainingResources
            self.ct += 1
            return lahsaScore, splaScore
        if len(possible)>0:
            possible.sort()
            maxSpla=int(possible[0].split("_")[2])
            otherScore = int(possible[0].split("_")[1])
            return otherScore, maxSpla
        return otherScore, maxSpla



    def lahsaGame(self, combList, lahsaScore, splaScore):
        if(len(combList) == 0):
            score = self.residualRecursionForSpla(self.splaSpecific,0)
            for i in range(self.count):
                self.spla.remainingResources += sum(self.newlySelectedSplaApplicants[-1].schedule)
                for k in range(len(self.newlySelectedSplaApplicants[-1].schedule)):
                    if self.newlySelectedSplaApplicants[-1].schedule[k] == 1:
                        self.spla.remaining[k] = self.spla.remaining[k] + 1
                self.newlySelectedSplaApplicants = self.newlySelectedSplaApplicants[0:-1]
                self.futureSplaList = self.futureSplaList[0:-1]
            self.count = 0
            splaScore=self.spla.slots*7 - self.spla.remainingResources + score
            lahsaScore=(self.lahsa.beds*7) - self.lahsa.remainingResources
            self.ct += 1
            return lahsaScore, splaScore
        maxLahsa = 0
        otherScore = 0
        entered = False
        possible = []
        for app in combList:
            # scores[0] = self.pScores[0]
            # scores[1] = self.pScores[1]
            if (self.contradicts(app, self.lahsa)==False):
                entered = True
                commonBoolaen = False
                if app in self.common:
                    commonBoolaen = True
                    self.common = [i for i in self.common if i.id!=app.id]
                else:
                    self.lahsaSpecific = [i for i in self.lahsaSpecific if i.id!=app.id]
                self.newlySelectedLahsaApplicants.append(app)
                self.tempLahsaScore += app.schedule.count(1)
                self.lahsa.remainingResources -= sum(app.schedule)
                self.futureLahsaList.append(app.id)
                for k in range(len(app.schedule)):
                    if app.schedule[k] == 1:
                        self.lahsa.remaining[k] = self.lahsa.remaining[k] - 1
                l1 = self.futureSplaList[:]
                l2 = self.futureLahsaList[:]
                l1.sort()
                l2.sort()
                key = ",".join(l1) +";"+ ",".join(l2)
                if key in self.dict:
                    a = int(self.dict[key].split(",")[0])
                    b = int(self.dict[key].split(",")[1])
                else :
                    a, b = self.splaGame(self.common + self.splaSpecific, lahsaScore, splaScore)
                    c = a
                    d = b
                    self.dict[key] = str(c)+","+str(d)

                if maxLahsa <= a:
                    if maxLahsa == a:
                        possible.append(app.id + "_" + str(a) + "_" + str(b))
                    if maxLahsa < a:
                        possible = []
                        possible.append(app.id+"_"+str(a)+"_"+str(b))
                    maxLahsa = a
                    lahsaScore = a
                    splaScore = b
                    otherScore = b

                self.common.append(app) if commonBoolaen else self.lahsaSpecific.append(app)
                self.newlySelectedLahsaApplicants = self.newlySelectedLahsaApplicants[:-1]
                self.tempLahsaScore -= app.schedule.count(1)
                self.lahsa.remainingResources += sum(app.schedule)
                self.futureLahsaList = self.futureLahsaList[:-1]
                for k in range(len(app.schedule)):
                    if app.schedule[k] == 1:
                        self.lahsa.remaining[k] = self.lahsa.remaining[k] + 1

        if entered == False:
            score = self.residualRecursionForSpla(self.common + self.splaSpecific, 0)
            for i in range(self.count):
                self.spla.remainingResources += sum(self.newlySelectedSplaApplicants[-1].schedule)
                for k in range(len(self.newlySelectedSplaApplicants[-1].schedule)):
                    if self.newlySelectedSplaApplicants[-1].schedule[k] == 1:
                        self.spla.remaining[k] = self.spla.remaining[k] + 1
                self.newlySelectedSplaApplicants = self.newlySelectedSplaApplicants[0:-1]
                self.futureSplaList = self.futureSplaList[0:-1]
            self.count = 0
            splaScore = self.spla.slots * 7 - self.spla.remainingResources + score
            lahsaScore = (self.lahsa.beds * 7) - self.lahsa.remainingResources
            self.ct += 1
            return lahsaScore, splaScore
        if len(possible)>0:
            possible.sort()
            maxLahsa=int(possible[0].split("_")[1])
            otherScore = int(possible[0].split("_")[2])
            return maxLahsa, otherScore
        return maxLahsa, otherScore

    count = 0
    def residualRecursionForSpla(self,list, score):
        if len(list) == 0:
            return 0
        if len(list) == 1:
            if self.contradicts(list[0], self.spla)==False:
                self.newlySelectedSplaApplicants.append(list[0])
                score += list[0].schedule.count(1)
                self.spla.remainingResources -= sum(list[0].schedule)
                self.futureSplaList.append(list[0].id)
                for k in range(len(list[0].schedule)):
                    if list[0].schedule[k] == 1:
                        self.spla.remaining[k] = self.spla.remaining[k] - 1
                self.count+=1
                return score
            else:
                return 0
        l=list[:1]
        s1=self.residualRecursionForSpla(l, score)+self.residualRecursionForSpla(list[1:], score)
        for i in range(self.count):
            for k in range(len(self.newlySelectedSplaApplicants[-1].schedule)):
                if self.newlySelectedSplaApplicants[-1].schedule[k] == 1:
                    self.spla.remaining[k] = self.spla.remaining[k] + 1
            self.spla.remainingResources += sum(self.newlySelectedSplaApplicants[-1].schedule)
            self.newlySelectedSplaApplicants = self.newlySelectedSplaApplicants[0:-1]
            self.futureSplaList = self.futureSplaList[0:-1]
        self.count = 0
        s2=self.residualRecursionForSpla(list[1:], score)
        for i in range(self.count):
            for k in range(len(self.newlySelectedSplaApplicants[-1].schedule)):
                if self.newlySelectedSplaApplicants[-1].schedule[k] == 1:
                    self.spla.remaining[k] = self.spla.remaining[k] + 1
            self.spla.remainingResources += sum(self.newlySelectedSplaApplicants[-1].schedule)
            self.newlySelectedSplaApplicants = self.newlySelectedSplaApplicants[0:-1]
            self.futureSplaList = self.futureSplaList[0:-1]
        self.count = 0
        return max(s1, s2)

    def residualRecursionForLahsa(self,list, score):
        if len(list) == 0:
            return 0
        if len(list) == 1:
            if self.contradicts(list[0], self.lahsa)==False:
                self.newlySelectedLahsaApplicants.append(list[0])
                score += list[0].schedule.count(1)
                self.lahsa.remainingResources -= sum(list[0].schedule)
                self.futureLahsaList.append(list[0].id)
                for k in range(len(list[0].schedule)):
                    if list[0].schedule[k] == 1:
                        self.lahsa.remaining[k] = self.lahsa.remaining[k] - 1
                self.count+=1
                return score
            else:
                return 0
        l=list[:1]
        s1=self.residualRecursionForLahsa(l, score)+self.residualRecursionForLahsa(list[1:], score)
        for i in range(self.count):
            for k in range(len(self.newlySelectedLahsaApplicants[-1].schedule)):
                if self.newlySelectedLahsaApplicants[-1].schedule[k] == 1:
                    self.lahsa.remaining[k] = self.lahsa.remaining[k] + 1
            self.lahsa.remainingResources += sum(self.newlySelectedLahsaApplicants[-1].schedule)
            self.newlySelectedLahsaApplicants = self.newlySelectedLahsaApplicants[0:-1]
            self.futureLahsaList = self.futureLahsaList[0:-1]
        self.count = 0
        s2=self.residualRecursionForLahsa(list[1:], score)
        for i in range(self.count):
            for k in range(len(self.newlySelectedLahsaApplicants[-1].schedule)):
                if self.newlySelectedLahsaApplicants[-1].schedule[k] == 1:
                    self.lahsa.remaining[k] = self.lahsa.remaining[k] + 1
            self.lahsa.remainingResources += sum(self.newlySelectedLahsaApplicants[-1].schedule)
            self.newlySelectedLahsaApplicants = self.newlySelectedLahsaApplicants[0:-1]
            self.futureLahsaList = self.futureLahsaList[0:-1]
        self.count = 0
        return max(s1, s2)

    def contradicts(self, app, org):
        for i in range(len(app.schedule)):
            if app.schedule[i] == 1 and org.remaining[i] <= 0:
                return True
        return False


sol = MinMax("input.txt")
