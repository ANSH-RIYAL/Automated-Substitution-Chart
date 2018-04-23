import os
import time
import random

def subsier(substitution_preferance_table,substitute_teachers_available_in_that_period):

    '''gives the names of the teachers having the maximum number of free periods
        that day on the condition that they are also free in that particular period
        it is a condition checking boolean variable.'''

    cond_var=False
    available_teachers=[]
    subsi_order = sorted(substitution_preferance_table.values())[::-1]

    for i in subsi_order:
        for k in substitute_teachers_available_in_that_period:
            if substitution_preferance_table[k]==i: #checks if the teacher has i no. of free periods, i is in descending order
                available_teachers.append(k)
                cond_var=True
        if cond_var:
            return available_teachers   #stop the function as soon as all teachers having the maximum number of free periods are returned
    return available_teachers       #gives back an empty list in case no teacher is available for taking a substitution in that period

class Substitution:

    def printer(self, num):

        '''Printing starts here!
       subsi_temp: maintains a temporary list for each teacher so that the data is always read to print
       self.substitution_table: dictionary that maintains all the final substitution data.
        '''
        #print self.substitution_table
        name = "Subsis"+str(num)+".csv"
        obj = open(name,'w')
        obj.write(' '+','+str(0)+','+str(1)+','+str(2)+','+str(3)+','+str(4)+','+str(5)+','+str(6)+','+str(7)+','+str(8)+'\n')
        for teacher_name, substitution in self.substitution_table.iteritems():

            subsi_temp = [[teacher_name], [], [], [], [], [], [], [], [], []]
            for j in range(len(substitution)):

                for x in range(0,9):

                    if substitution[j][2] == x:
                        subsi_temp[x+1].append([substitution[j][0],substitution[j][1]])
                        break

            obj.write(str(teacher_name)+',')

            for final in range(1,10):
                if len(subsi_temp[final]) == 1:
                    obj.write(str(subsi_temp[final][0][0])+' '+str(subsi_temp[final][0][1]+',')) #writes the substitution according to the periods
                else:
                    obj.write(' '+',')
            obj.write('\n')

        obj.close()

    def subsier_main(self):

        for i in range(9):
            if len(self.empty_classes[i]) != 0: #works only if there are classes which require substitution
                temp_list=[]
                for j in range(len(self.empty_classes[i])):

                    temp_free = subsier(self.substitution_preferance_table,self.substitute_teachers_available[i])
                    if temp_list!=[]:
                        for p in temp_list:
                            if p in temp_free:
                                temp_free.remove(p)
                    if len(temp_free)!=0:
                        randomnum = random.randint(0,len(temp_free)-1)
                        chosen_teacher = temp_free[randomnum] #selects a teacher randomly from the most free teachers
                        del temp_free[randomnum]
                        self.substitution_preferance_table[chosen_teacher] -= 1
                        temp_list.append(chosen_teacher)
                    else:                   #in case no teacher is available in a particular period
                        chosen_teacher="NA"

                    if self.periodwise_absentees[i][j] in self.substitution_table:
                        self.substitution_table[self.periodwise_absentees[i][j]].append([self.empty_classes[i][j],chosen_teacher,i])
                    else:
                        self.substitution_table[self.periodwise_absentees[i][j]] = []
                        self.substitution_table[self.periodwise_absentees[i][j]].append([self.empty_classes[i][j],chosen_teacher,i])


    def read(self, num):

        '''function definitions'''

        self.substitution_table = {}
        self.substitution_preferance_table = {}
        self.empty_classes = [ [] , [] , [] , [] , [] , [] , [] , [] , []]
        self.absent_teachers_list = []
        self.periodwise_absentees = [ [] , [] , [] , [] , [] , [] , [] , [] , [] ]
        self.substitute_teachers_available = [ [] , [] , [] , [] , [] , [] , [] , [] , []]

        '''Read function reads the data and manipulated it for computer use'''

        name = 'Teacherslist'+str(num)+".csv"
        f = open("Timetables.csv" , 'r')
        g = open(name,'r')
        alldata = f.readlines()
        day = time.localtime()[6]

        while True:

            temp_attendance = g.readline().split(',')
            busy=0
            for i in range(1,len(alldata),7):
                temp2 = alldata[i-1].split(',')
                check = temp2[0]
                #print check
                if check in temp_attendance[0]:
                    temp_time_table = alldata[i+day].split(',')
                    break
            try:
                if temp_attendance[1] == 'P' or temp_attendance[1] == 'p':
                    for i in range(1,6):
                        if temp_time_table[i] == 'NIL' or temp_time_table[i] == 'NIL\n' :
                            if temp_attendance[0] in self.substitution_preferance_table:
                                self.substitution_preferance_table[temp_attendance[0]] += 1
                            else:
                                self.substitution_preferance_table[temp_attendance[0]] = 1
                            if busy==2:
                                self.substitution_preferance_table[temp_attendance[0]] -= 1
                                busy=0
                            self.substitute_teachers_available[i-1].append(temp_attendance[0])
                        else:
                            busy += 1
                elif temp_attendance[1] == 'SL' or temp_attendance[1] == 'sl' or temp_attendance[1] == 'Sl\n' or temp_attendance[1] == "SL":
                    for i in range(1,3):
                        if temp_time_table[i] != 'NIL' and temp_time_table[i] != 'NIL\n':
                            self.periodwise_absentees[i-1].append(temp_attendance[0])
                            self.empty_classes[i-1].append(temp_time_table[i])
                    for i in range(3,6):
                        if temp_time_table[i] == 'NIL' or temp_time_table[i] == 'NIL\n' :
                            if temp_attendance[0] in self.substitution_preferance_table:
                                self.substitution_preferance_table[temp_attendance[0]] += 1
                            else:
                                self.substitution_preferance_table[temp_attendance[0]] = 1
                            if busy==2:
                                self.substitution_preferance_table[temp_attendance[0]] -= 1
                                busy=0
                            self.substitute_teachers_available[i-1].append(temp_attendance[0])
                        else:
                            busy += 1

                else:
                    self.absent_teachers_list.append(temp_attendance[0])
                    for i in range(1,6):
                        if temp_time_table[i] != 'NIL' and temp_time_table[i] != 'NIL\n':
                            self.periodwise_absentees[i-1].append(temp_attendance[0])
                            self.empty_classes[i-1].append(temp_time_table[i])

                if temp_attendance[2] == 'P\n' or temp_attendance[2] == 'p\n':
                    for i in range(6,10):
                        if temp_time_table[i] == 'NIL' or temp_time_table[i] == 'NIL\n':
                            if temp_attendance[0] in self.substitution_preferance_table:
                                self.substitution_preferance_table[temp_attendance[0]] += 1
                            else:
                                self.substitution_preferance_table[temp_attendance[0]] = 1
                            if busy==2:
                                self.substitution_preferance_table[temp_attendance[0]] -= 1
                                busy=0
                            self.substitute_teachers_available[i-1].append(temp_attendance[0])
                        else:
                            busy += 1
                elif temp_attendance[2] == 'SL\n' or temp_attendance[2] == 'sl\n' or temp_attendance[2] == 'Sl\n' or temp_attendance == 'SL':
                    for i in range(6,8):
                        if temp_time_table[i] == 'NIL' or temp_time_table[i] == 'NIL\n':
                            if temp_attendance[0] in self.substitution_preferance_table:
                                self.substitution_preferance_table[temp_attendance[0]] += 1
                            else:
                                self.substitution_preferance_table[temp_attendance[0]] = 1
                            if busy==2:
                                self.substitution_preferance_table[temp_attendance[0]] -= 1
                                busy=0
                            self.substitute_teachers_available[i-1].append(temp_attendance[0])
                        else:
                            busy += 1
                    self.absent_teachers_list.append(temp_attendance[0])
                    for i in range(8,10):
                        if temp_time_table[i] != 'NIL' and temp_time_table[i] != 'NIL\n':
                            self.periodwise_absentees[i-1].append(temp_attendance[0])
                            self.empty_classes[i-1].append(temp_time_table[i])

                else:
                    self.absent_teachers_list.append(temp_attendance[0])
                    for i in range(6,10):
                        if temp_time_table[i] != 'NIL' and temp_time_table[i] != 'NIL\n':
                            self.periodwise_absentees[i-1].append(temp_attendance[0])
                            self.empty_classes[i-1].append(temp_time_table[i])
            except:
                break

            '''creates list of teachers and records when they are present and when they are not
                and when they are free and when they are not. Basically, manipulates the whole data around.'''

        self.absent_teachers_list = list(set(self.absent_teachers_list)) #so that teachers are not repeated when we are printing

        for i in range (len(self.empty_classes)): #manages the situation where a certain class has an optional period and multiple teachers are absent
            self.empty_classes[i] = list(set(self.empty_classes[i]))

        for i in range(len(self.empty_classes[-1])):
            if '\n' in self.empty_classes[-1][i]:
                self.empty_classes[-1][i]=self.empty_classes[-1][i][0:self.empty_classes[-1][i].index('\n')] #prevents the last teacher from going to a new lne during output.

        for i  in range(len(self.substitution_preferance_table)):
            if 'HOD' in self.substitution_preferance_table.keys()[i]:
                self.substitution_preferance_table[self.substitution_preferance_table.keys()[i]] -= 4 #reduces the preference that will be given to HODs
        f.close()
        g.close()
    def refresh(self):

        #Refresh function would keep the file ready to mark the absentees when it is opened next time!

        f = open("Teacherslist.csv",'r')
        g = open("temp_attendance.csv",'w')
        mainfile = f.readlines()

        for i in range(len(mainfile)):
            t = mainfile[i].split(',')
            t[1] = 'P'
            t[2] = 'P'
            g.write(','.join(t))

        f.close()
        g.close()
        os.remove("Teacherslist.csv")
        os.rename("temp_attendance.csv","Teacherslist.csv")

def divide():
    mainfile = open("Teacherslist.csv", 'r')
    alldata = mainfile.readlines()
    group1 = open("Teacherslist1.csv", "w")
    group2 = open("Teacherslist2.csv", "w")
    group3 = open("Teacherslist3.csv", "w")
    for i in alldata:
        tmp = i.split(',')
        if tmp[-1] == '1\n':
            group1.write(','.join(tmp[:3]) + '\n')
        elif tmp[-1] == '2\n':
            group2.write(','.join(tmp[:3]) + '\n')
        elif tmp[-1] == '3\n':
            group3.write(','.join(tmp[:3]) + '\n')

    mainfile.close()
    group2.close()
    group3.close()
    group1.close()

def combine():
    os.remove("Teacherslist1.csv")
    os.remove("Teacherslist2.csv")
    os.remove("Teacherslist3.csv")

    mainsubsi = open("Subsis.csv", "w")
    subsi1 = open("Subsis1.csv", "r")
    subsi2 = open("Subsis2.csv", "r")
    subsi3 = open("Subsis3.csv", "r")

    alldata1 = subsi1.readlines()
    alldata2 = subsi2.readlines()
    alldata3 = subsi3.readlines()

    mainsubsi.write(",,,,,Amity International School Mayur Vihar\n")
    mainsubsi.write(alldata1[0])
    mainsubsi.write(",,,,,Junior School\n")
    mainsubsi.writelines(alldata1[1:])
    mainsubsi.write(",,,,,Middle School\n")
    mainsubsi.writelines(alldata2[1:])
    mainsubsi.write(",,,,,Senior School\n")
    mainsubsi.writelines(alldata3[1:])

    subsi1.close()
    subsi2.close()
    subsi3.close()

    os.remove("Subsis1.csv")
    os.remove("Subsis2.csv")
    os.remove("Subsis3.csv")

divide()
classobj = Substitution()
for i in range(1, 4):
    classobj.read(i)
    classobj.subsier_main()
    classobj.printer(i)
combine()

if raw_input("Refresh?[Y/N]\t").upper() == 'Y':
    classobj.refresh() 