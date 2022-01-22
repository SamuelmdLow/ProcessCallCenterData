from main import initialize, createCSV

def aveDayProductivity(servers):
    sum = 0
    count = 0
    for server in servers:
        for day in server.days:
            count += 1
            sum += day.productivity
    aveProductivity = sum/count
    return aveProductivity

def ProductivityOverDay0(servers):
    data = []

    for server in servers:
        for day in server.days:
            if len(day.smallers) > 3:
                for call in day.smallers:
                    time = call.start-day.start
                    line = [time, call.callTime]
                    data.append(line)
    data.sort(key=first)
    return data

def ProductivityOverDay1(servers):
    data = []

    for server in servers:
        for day in server.days:
            if len(day.smallers) > 3:
                for call in day.smallers:
                    if day.end - call.end > 60*60*2:
                        time = call.start-day.start
                        line = [time, call.callTime]
                        data.append(line)
    data.sort(key=first)
    return data

def ProductivityOverDay2(servers):
    data = []

    for server in servers:
        for day in server.days:
            if len(day.smallers) > 3:
                last = day.end
                for call in day.smallers:
                    time = last - call.start
                    line = [time, call.callTime]
                    data.append(line)
    data.sort(key=first)
    return data

def ProductivityOverDay3(servers):
    data = []

    for server in servers:
        for day in server.days:
            if len(day.smallers) > 3:
                dayLength = day.end - day.start
                for call in day.smallers:
                    time = ((call.start - day.start)/dayLength) * 100
                    line = [time, call.callTime]
                    data.append(line)

    data.sort(key=first)
    return data

def ProductivityOverDay4(servers):
    data = []

    for server in servers:
        for day in server.days:
            if len(day.smallers) > 3:
                for call in day.smallers:
                    time = (call.start/3600) % 24
                    line = [time, call.callTime]
                    data.append(line)

    data.sort(key=first)
    return data


def ProductivityOverDay5(servers):
    data = []

    for server in servers:
        for day in server.days:
            if len(day.smallers) > 3:
                for call in day.smallers:
                    if call.start - day.start > 3600:
                        time = day.end - call.start
                        line = [time, call.callTime]
                        data.append(line)
    data.sort(key=first)
    return data


def aveDayLength():
    sum = 0
    count = 0
    for server in servers:
        for day in server.days:
            dayLength = (day.end - day.start)/3600
            sum += dayLength
            count += 1
    return sum/count

def calculateIntervals(data, intervalLength, min, ave, convert=True):
    cutOff = intervalLength

    newData = []
    interval = []
    for line in data:
        if line[0] < cutOff:
            interval.append(line[1])
        else:
            if len(interval) >= min:
                callTime = 0
                for call in interval:
                    callTime += call

                productivity = len(interval) / callTime
                time = cutOff - (intervalLength/2)
                if convert == True:
                    time = time/3600
                newData.append([time, productivity / ave])

            cutOff += intervalLength
            interval = []

    if len(interval) >= min:
        callTime = 0
        for call in interval:
            callTime += call
        productivity = len(interval) / callTime
        time = cutOff - (intervalLength/2)
        newData.append([time, productivity / ave])

    return newData

def seventhInterval(server):
    callTimes = []
    for server in servers:
        for day in server.days:
            for call in day.smallers:
                if day.end - (8*3600) < call.start < day.end - (7*3600):
                    time = (call.start/3600) % 24
                    callTimes.append(time)

    newData = []
    count = 0
    interval = 0.5
    cutOff = interval
    callTimes.sort()
    for time in callTimes:
        if time > cutOff:
            newData.append([cutOff, count])
            cutOff += interval
            count = 1
        else:
            count += 1

    return newData

def first(e):
    return e[0]

if __name__ == "__main__":

    min = 30

    servers = initialize()

    ave = aveDayProductivity(servers)
    #print(aveDayLength())
    print("started!")

    data = ProductivityOverDay2(servers)
    data = calculateIntervals(data, 3600, min, ave)
    createCSV(data, "overDay-2.csv")
    print("overDay-2 finished!")

    data = ProductivityOverDay5(servers)
    data = calculateIntervals(data, 3600, min, ave)
    createCSV(data, "overDay-5.csv")
    print("overDay-5 finished!")
    '''
    data = ProductivityOverDay0(servers)
    data = calculateIntervals(data, 3600, min, ave)
    createCSV(data, "overDay-0.csv")
    print("overDay-0 finished!")
    '''
    '''
    data = ProductivityOverDay1(servers)
    data = calculateIntervals(data, 3600, min, ave)
    createCSV(data, "overDay-1.csv")
    print("overDay-1 finished!")

    data = ProductivityOverDay2(servers)
    data = calculateIntervals(data, 3600, min, ave)
    createCSV(data, "overDay-2.csv")
    print("overDay-2 finished!")

    data = ProductivityOverDay3(servers)
    data = calculateIntervals(data, 10, min, ave, convert=False)
    createCSV(data, "overDay-3.csv")
    print("overDay-3 finished!")

    data = seventhInterval(servers)
    createCSV(data, "7int.csv")


    data = ProductivityOverDay4(servers)
    data = calculateIntervals(data, 1, min, ave, convert=False)
    createCSV(data, "overDay-4.csv")
    print("overDay-4 finished!")
    '''
    print("finished!")