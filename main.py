from pathlib import Path
import math

def convertToCSV(filename):
    file = open(filename, "r")
    content = file.read()
    csv = content.replace("	", ",")
    file.close()

    file = open(file.name.replace(".txt", ".csv"), "w")
    file.write(csv)
    file.close()

# convertToCSV("january.txt")

def readCSV(filename):
    file = open(filename, "r")
    content = file.readlines()
    content.pop(0)
    file.close()

    data = []
    for line in content:
        data.append(line.split(","))
    return data

class call:
    def __init__(self, line):
        self.server     = line[16]
        self.time       = line[13]
        self.start      = SecsSinceJ0(line)
        self.end        = self.start + int(line[15])
        self.callTime   = (int(line[11]) + int(line[15]))/3600
        self.date       = self.getDate(line)
        self.productivity = 1/self.callTime

    def getDate(self,line):
        date = line[5]
        while len(date) != 6:
            date = "0"+date
        month   = date[2:4]
        day     = date[4:6]

        return day + "/" + month

class Server:
    def __init__(self, call):
        self.name = call.server
        self.days  = []
        self.weeks = []
        self.calls = [call]
    def getAveWeekPro(self):
        count = 0
        sum = 0
        for week in self.weeks:
            sum += week.productivity
            count += 1
        return sum/count

    def addCall(self, call):
        self.calls.append(call)

    def getDays(self):
        #self.days = self.getContainer2(self.calls, 60*60*5.5)
        self.days = self.getContainer2(self.calls, 60 * 60 * 5)

    def getWeeks(self):
        self.getDays()
        #self.weeks = self.getContainer2(self.days, 60*60*18)
        self.weeks = self.getContainer2(self.days, 60 * 60 * 30)

    def getContainer(self, smallers, gap):
        all = []
        new = container()
        first = smallers[0].start
        for small in smallers:
            if small.start != None:
                if small.start - first < (gap):
                    new.add(small)
                else:
                    all.append(new)
                    new = container()
                    new.add(small)
                    first = small.start
        all.append(new)

        return all

    def getContainer2(self, smallers, gap):
        all = []
        new = container()
        last = smallers[0].end
        for small in smallers:
            if small.start != None:
                if small.start - last < (gap):
                    new.add(small)
                    last = small.end
                else:
                    all.append(new)
                    new = container()
                    new.add(small)
                    last = small.end
        all.append(new)

        return all
def dt(e):
    return e.time

class container:
    def __init__(self):
        self.start  = None
        self.end    = None
        self.date   = None
        self.smallers  = []
        self.productivity = 0
        self.callTime = 0
    def add(self, small):
        if self.start == None:
            self.start = small.start
            self.date  = small.date
        self.smallers.append(small)
        self.callTime += small.callTime
        self.productivity = len(self.smallers)/self.callTime
        self.end = small.end

def buildServers(data):
    serverNames = []
    servers = []
    for line in data:
        if "NO_SERVER\n" not in line:
            if int(line[15]) > 5:
                newCall = call(line)
                if newCall.server in serverNames:
                    index = serverNames.index(newCall.server)
                    servers[index].addCall(newCall)
                else:
                    if newCall.server != "NO_SERVER":
                        serverNames.append(newCall.server)
                        servers.append(Server(newCall))

    for server in servers:
        server.getDays()
        server.getWeeks()

    return servers


def ProductivityOverWeek(servers):
    data = []

    for server in servers:
        ave = server.getAveWeekPro()
        for week in server.weeks:
            dayNumber = 0
            days = len(week.smallers)
            for day in week.smallers:
                line = [dayNumber, days, day.productivity/ave]
                data.append(line)
                dayNumber += 1

    return data

def hoursOnDay(servers):
    data = []

    for server in servers:
        for week in server.weeks:
            worked = None
            for day in week.smallers:
                if worked == None:
                    worked = day.end - day.start
                else:
                    line = [worked, day.productivity]
                    data.append(line)
                    worked = day.end - day.start

    return data

def serverCalls(servers):
    data = []

    for server in servers:
        for week in server.weeks:
            for day in week.smallers:
                for call in day.smallers:
                    data.append([call.date, call.start])

    return data

def SecsSinceJ0(line):
    try:
        date = line[5] #yymmdd
        time = line[13].split(":") #hh:mm:ss

        yearDif     = (int(date[0:2]) - 99) * 356 * 24 * 60 * 60
        month       = int(date[2:4])
        monthDif    = 0

        daysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        for i in range(month -1):
            monthDif = monthDif + (daysInMonth[i] * 24 * 60 * 60)

        dayDif      = int(date[4:6]) * 24 * 60 * 60
        hourDif     = int(time[0]) * 60 * 60
        minuteDif   = int(time[1]) * 60
        secondDif   = int(time[2])

        difference = yearDif + monthDif + dayDif + hourDif + minuteDif + secondDif
        return difference

    except:
        return None

def rollingAverageDay2(data, interval, reach, required, ave):
    newData = []
    timePoint = data[0][0]
    start = 0
    last = data[-1][0]

    while timePoint < last - reach:

        MaxDateTime = reach + timePoint

        tested = start
        count = 0
        sum = 0
        while True:
            if data[tested][0] <= timePoint:
                start = start + 1
            else:
                if data[tested][0] <= MaxDateTime:
                    count = count + 1
                    sum = sum + data[tested][1]
                else:
                    break
            tested = tested + 1
            if tested >= len(data):
                break

        if count >= required:
            average = count/sum
            newDataLine = [(timePoint+(reach/2))/(60*60), average/ave]
            newData.append(newDataLine)

        timePoint = interval + timePoint
    return newData

def rollingAverageDay(data, interval, reach, required):
    newData = []
    timePoint = data[0][0]
    start = 0
    last = data[-1][0]

    while timePoint < last - reach:

        MaxDateTime = reach + timePoint

        tested = start
        count = 0
        sum = 0
        while True:
            if data[tested][0] <= timePoint:
                start = start + 1
            else:
                if data[tested][0] <= MaxDateTime:
                    count = count + 1
                    sum = sum + data[tested][1]
                else:
                    break
            tested = tested + 1
            if tested >= len(data):
                break

        if count >= required:
            average = sum/count
            newDataLine = [(timePoint+(reach/2))/(60*60), average]
            #newDataLine = [convertSecondsTOTimeFormat(timePoint), average]
            newData.append(newDataLine)

        timePoint = interval + timePoint
    return newData

def averageWeek(data, required):
    newData = []
    point = 0
    sums = []
    counts = []
    for line in data:
        day = line[0]
        days = line[1]
        #if day == 5:
            #print(line[3].smallers[0].server)
            #print(str(line[3].date) + " " + str(round(line[2])))
            #x = [i.time for i in line[3].smallers]
            #print(x)

        if point == day:
            while len(sums) < days:
                sums.append(0)
                counts.append(0)

            counts[days - 1] += 1
            sums[days - 1] += line[2]
        else:
            averages = []

            for i in range(len(sums)):
                if counts[i] >= required:
                    averages.append(sums[i]/counts[i])
                else:
                    averages.append(None)

            newData.append([point+1] + averages)

            point = day
            counts = []
            sums = []
            while len(sums) < days:
                sums.append(0)
                counts.append(0)
            counts[days - 1] = 1
            sums[days - 1] = line[2]

    averages = []
    for i in range(len(sums)):
        if counts[i] >= required:
            averages.append(sums[i] / counts[i])
        else:
            averages.append(None)

    newData.append([point+1] + averages)

    return newData

def restDays(server):
    data = []

    for server in servers:
        end = None
        ave = server.getAveWeekPro()
        for week in server.weeks:
            if end == None:
                end = week.end
            else:
                gap = round((week.start - end)/(60*60*24))
                data.append([gap, week.productivity/ave])
                end = week.end

    return data

def averageRestDays(data, required):
    newData = []

    point = data[0][0]
    count = 0
    sum = 0
    for line in data:
        if line[0] == point:
            count   += 1
            sum     += line[1]
        else:
            if count >= required:
                average = sum/count
                newData.append([point,average])

            point = line[0]
            count = 1
            sum = line[1]
    if count >= required:
        average = sum / count
        newData.append([point, average])

    return newData

def sortByTime(data):
    newData = []
    for line in data:
        time = SecsSinceJ0(line)
        line.append(time)
        newData.append(line)

    newData.sort(key=MyFunc)

    return newData

def MyFunc(e):
    try:
        value = int(e[-1])
        return value
    except:
        return -1

def createCSV(data, filename):
    file = open(filename, "w")
    for line in data:
        line = [str(x) for x in line]
        savedLine = ",".join(line).replace("\n","") + "\n"
        file.write(savedLine)

    file.close()

def cleanData(data, min):
    newData = []
    for line in data:
        line = [x.replace("\n", "") for x in line]
        try:
            if "NO_SERVER" not in line and len(line) == 17 and int(line[15]) >= min:
                newData.append(line)
        except:
            pass
    return newData

def first(e):
    return e[0]

required = 5

def initialize():
    data = []

    p = Path(r'original data').glob('**/*')
    directory = [file for file in p]
    for file in directory:
        if "csv" in file.name:
            print("opening " + file.name + "...")
            data = data + readCSV(file)
    # data = readCSV("original data\\february.csv")
    print("cleaning data...")
    data = cleanData(data, 10)
    print("sorting data...")
    data = sortByTime(data)
    print("processing data...")
    servers = buildServers(data)
    return servers
'''
filename = "hoursOnDay"
print(filename + " started!")
data = hoursOnDay(servers)
data.sort(key=first)
data = rollingAverageDay(data, 300, 60*60*1, 30)
createCSV(data, filename + ".csv")
print(filename + " finished!")

filename = "restdays"
print(filename + " started!")
data = restDays(servers)
data.sort(key=first)
data = averageRestDays(data, 10)
createCSV(data, filename + ".csv")
print(filename + " finished!")

filename = "overWeek"
print(filename + " started!")
data = ProductivityOverWeek(servers)
data.sort(key=first)
data = averageWeek(data, 30)
createCSV(data, filename + ".csv")
print(filename + " finished!")
'''
