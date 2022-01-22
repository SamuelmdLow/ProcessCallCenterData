from main import initialize, createCSV, first


def hoursOnDay(servers):
    data = []

    for server in servers:
        for week in server.weeks:
            worked = None
            for day in week.smallers:
                if worked == None:
                    worked = day.end - day.start
                    lastProductivity = day.productivity
                else:
                    line = [worked, day.productivity/lastProductivity]
                    data.append(line)
                    worked = day.end - day.start
                    lastProductivity = day.productivity
    return data

def calculateIntervals(data, intervalLength, min, ave, convert=True):
    cutOff = intervalLength

    newData = []
    interval = []
    for line in data:
        if line[0] < cutOff:
            interval.append(line[1])
        else:
            if len(interval) >= min:
                sum = 0
                for productivity in interval:
                    sum += productivity

                productivity = sum/len(interval)
                time = cutOff - (intervalLength/2)
                if convert == True:
                    time = time/3600
                newData.append([time, productivity / ave])

            cutOff += intervalLength
            interval = []

    if len(interval) >= min:
        sum = 0
        for productivity in interval:
            sum += productivity

        productivity = sum / len(interval)
        time = cutOff - (intervalLength / 2)
        if convert == True:
            time = time / 3600
        newData.append([time, productivity / ave])

    return newData

def aveDayProductivity(servers):
    sum = 0
    count = 0
    for server in servers:
        for day in server.days:
            count += 1
            sum += day.productivity
    aveProductivity = sum/count
    return aveProductivity

if __name__ == "__main__":

    min = 30

    servers = initialize()
    ave = aveDayProductivity(servers)
    print(ave)
    filename = "hoursOnDay"
    print(filename + " started!")
    data = hoursOnDay(servers)
    data.sort(key=first)
    data = calculateIntervals(data, 3600, min, 1)
    createCSV(data, filename + ".csv")
    print(filename + " finished!")