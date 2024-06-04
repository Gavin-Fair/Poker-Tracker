import csv
from matplotlib import pyplot as plt
from datetime import datetime

career = []


def main(hasRan):
    # only running startup tasks if @main has not ran
    if not hasRan:
        try:
            with open('cache.txt'):
                readSavedCSV()
        except FileNotFoundError:
            open('cache.txt', 'x')

    try:
        print(
            f'1. Read CSV file\n'
            f'2. Create new CSV file\n'
            f'3. Add session to existing CSV file\n'
            f'4. Print career data\n'
            f'5. Plot data\n'
            f'6. Delete Session\n'
            f'7. Exit'
        )

        option = int(input())
        while 0 > option or option > 7:
            print(f'Your answer must be a number 1-7\n'
                  f'1. Read CSV file\n'
                  f'2. Create new CSV file\n'
                  f'3. Add session to existing CSV file\n'
                  f'4. Print career data\n'
                  f'5. Plot data\n'
                  f'6. Delete Session\n'
                  f'7. Exit')
            option = int(input())
    except ValueError:
        print('Your answer must be a number 1-7')
        main(True)

    match option:
        case 1:
            prepCSV()
        case 2:
            createNewCSV()
        case 3:
            addSession()
        case 4:
            printCareer()
        case 5:
            plotData()
        case 6:
            delData()
        case 7:
            print('Goodbye...')


def delData():
    print('Select which game session you want to delete (type the game ID below')
    # Displaying all possible games to delete
    for i in range(len(career)):
        print(f'ID: {i + 1} | Date: {career[i][0]} ')

    inp = int(input())

    while 0 > inp >= len(career):
        print(f'Input must be a number between 1-{len(career)}')
        inp = int(input())
    inp -= 1
    date = career.pop(inp)[0]
    # retrieving cached csv file
    with open('cache.txt', 'r') as cache:
        file = cache.readline()
    # saving all lines in csv file to @lines
    with open(file, 'r') as f:
        lines = f.readlines()
    # deleting all lines
    open(file, 'w').close()
    # re-writing all lines except for the deleted one
    with open(file, 'w') as f:
        for line in lines:
            if not line[0:8] == date:
                f.write(line)

    print('The data you selected has been deleted, returning to menu')
    main(True)


def prepCSV():
    # this is to ensure the user has properly formatted the csv file
    print(f'To properly read the CSV file please have it in the following format:\n'
          f'Date(mm/dd/yy), Initial Stack in USD, Final Stack in USD, '
          f' Small Blind, Big Blind, Ante, Session Length (HH:MM), any notes\n'
          f'  01/12/23,             250,                 0,'
          f'                 1,         2,       0,           02:01,          sad :(\n')
    print(f'If your file is formatted correctly enter \'1\' to continue or \'2\' to go back to main menu:')
    option = int(input())
    if option == 1:
        readCSV()
    if option == 2:
        main(True)
    while not option == 1 and not option == 2:
        print('please either type ')
        option = int(input())
        if option == 2:
            main(True)
        if option == 1:
            readCSV()


def readCSV():
    print('Caution reading a new CSV will replace the old CSV in cache')
    print("Input CSV name (example.csv): ")
    file = input()
    # if the user did not add '.csv' we append it to @file
    if not file.__contains__('.csv'):
        file += '.csv'
    # clearing old cache to ensure old csv file is still cached
    open('cache.txt', 'w').close()
    # writing new csv file to cache
    with open('cache.txt', 'w') as cache:
        cache.write(file)
    try:
        career.clear()
        with open(file) as f:
            csvFile = csv.reader(f)
            for row in csvFile:
                date = row[0]
                stackSize = float(row[1])
                finalStackSize = float(row[2])
                smallBlind = float(row[3])
                bigBlind = float(row[4])
                ante = float(row[5])
                sessionLength = row[6]
                game = [date, stackSize, finalStackSize, smallBlind, bigBlind, ante, sessionLength]
                data = processData(game)
                insertData(data)
        print('Finished processing data returning to main menu')
        main(True)

    except FileNotFoundError:
        print('File not found, please try a different file name or ensure file is in right directory')
        readCSV()


def processData(game):
    profit = float(game[2] - game[1])
    hours = float(game[6][:2])
    minutes = float(game[6][3:])
    totalMin = hours * 60 + minutes
    data = [game[0], game[1], game[2], game[3], game[4], game[5], profit, totalMin]
    return data


def readSavedCSV():
    career.clear()
    with open('cache.txt', 'r') as cache:
        file = cache.readline()
        with open(file) as f:
            csvFile = csv.reader(f)
            for row in csvFile:
                date = row[0]
                stackSize = float(row[1])
                finalStackSize = float(row[2])
                smallBlind = float(row[3])
                bigBlind = float(row[4])
                ante = float(row[5])
                sessionLength = row[6]
                game = [date, stackSize, finalStackSize, smallBlind, bigBlind, ante, sessionLength]
                data = processData(game)
                # inserting data into ascending order by date of game
                insertData(data)


def createNewCSV():
    print('Caution reading a new CSV will replace the old CSV in cache')
    print('What do you want the name of the CSV to be? (example.csv)')
    file = input()
    try:
        if not file.__contains__('.csv'):
            file += '.csv'
        open('cache.txt', 'w').close()
        with open('cache.txt', 'w') as cache:
            cache.write(file)
        open(file, 'x')
        print(f'{file} was added to your directory, bringing you back to the main menu')
        main(True)
    except FileExistsError:
        print(f'{file} was already found in this directory, please rename your new file\n')
        createNewCSV()


def addSession():
    print('Please input the following values')
    try:

        date = input('date (mm/dd/yy): ')
        while not len(date) == 8:
            print('Make sure date is in (mm/dd/yy) format if month is 1 type \'01\'')
            date = input('date (mm/dd/yy): ')

        stackSize = float(input('Stack Size: '))
        finalStackSize = float(input('Final Stack Size: '))
        smallBlind = float(input('Small Blind: '))
        bigBlind = float(input('Big Blind: '))
        ante = float(input('Ante: '))

        sessionLength = input('Session Length (HH:MM): ')
        while not len(sessionLength) == 5:
            print('Make sure session length is in (HH:MM) format if hour is 1 type \'01\'')
            sessionLength = input('Session Length (HH:MM): ')

        with open('cache.txt', 'r') as cache:
            file = cache.readline()

        with open(file, 'r') as f:
            lines = f.readlines()
        # re-writing all data and adding new data
        open(file, 'w').close()
        with open(file, 'w') as f:
            for line in lines:
                f.write(line)
            f.write(f'{date},{stackSize},{finalStackSize},{smallBlind},{bigBlind},{ante},{sessionLength}\n')
        game = [date, stackSize, finalStackSize, smallBlind, bigBlind, ante, sessionLength]
        data = processData(game)
        insertData(data)
        print('Your data was logged, returning to the main menu')
        main(True)

    except ValueError:
        print('Please ensure your input matches implied data type')
        addSession()


def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%m/%d/%y")
    d2 = datetime.strptime(d2, "%m/%d/%y")
    return (d2 - d1).days


def insertData(data):
    index = len(career)
    # loops through @career until it finds date that it larger than the new data's
    for i in range(len(career)):
        if days_between(data[0], career[i][0]) > 0:
            index = i
            break
    # if it loops through the entire list and @data is the largest it adds it to the end of @career
    if index == len(career):
        career.append(data)
    else:
        # otherwise @data is inserted at the index where the current date is larger than the @data date
        career.insert(index, data)


def printCareer():
    totalHoursPlayed = 0
    totalProfit = 0
    games = 0
    for game in career:
        games += 1
        print(f'{game[0]},\n'
              f'Blinds: {round(game[3], 2)}/{round(game[4], 2)}({round(game[5], 2)})'
              f'   Buy In: {round(game[1], 2)}   Final Stack: {round(game[2], 2)}   Profit: {round(game[6],2)}'
              f'\nHours Played: {round(game[7] / 60, 2)}')
        print(f'----------------------------------------------------------------------------')
        totalHoursPlayed += round(game[7] / 60, 2)
        totalProfit += game[6]
    print(f'\nTotal Profit          : {totalProfit}\n'
          f'Average Profit        : {round(totalProfit / games, 2)}\n'
          f'Total Hours Logged    : {round(totalHoursPlayed, 2)}\n'
          f'Average Hours Played  : {round(totalHoursPlayed / games, 2)}')
    print('\n')
    main(True)


def plotData():
    profits = []
    dates = []
    totProf = 0
    # tracking a running profit counter
    for game in career:
        totProf += game[6]
        profits.append(totProf)
        dates.append(game[0])
    if len(profits) < 2:
        print('Must have at least 2 games logged to plot data, returning to menu')
        main(True)
    plt.plot(dates, profits)
    plt.xticks(rotation=45)
    plt.ylabel('Total Profit')
    plt.show()
    main(True)


if __name__ == '__main__':
    main(False)
