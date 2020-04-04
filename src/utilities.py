import csv, logging


def getDemandsFromCsv():

    with open("../input/demandData.csv") as csvFile:
        data = list(csv.reader(csvFile))

    ORDER_COLUMN = 0
    LOCATION_COLUMN = 1
    DEMAND_QTY_COLUMN = 2


    demandData = {}
    demandLocationData = {}
    for row in range(1, len(data)):
        demandData[data[row][ORDER_COLUMN]] = round(float(data[row][DEMAND_QTY_COLUMN]))
        demandLocationData[data[row][ORDER_COLUMN]] = data[row][LOCATION_COLUMN]

    return demandData, demandLocationData





def getTravelMatrixFromCsv():

    with open("../input/travelMatrix.csv") as csvfile:
        data = list(csv.reader(csvfile))

    locationList = data[0][1:]

    travelMatrix = {}
    for i,fromLoc in enumerate(locationList):
        travelMatrix[fromLoc] = {}
        for j, toLoc in enumerate(locationList):
            travelMatrix[fromLoc][toLoc] = float(data[i+1][j+1])

    return travelMatrix





def logger(logging):
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(asctime)s %(process)d %(message)s',
                        filename='../output/OptimizerLog.log', filemode='a')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    logging.getLogger().addHandler(console)




def writeLpFile(model, iteration):

    logging.debug("Writing lp file")
    model.writeLP('../output/vehicleRouting_'+str(iteration)+'.lp')
    logging.info("lp file written")



def printOutputFromSolver(assignVars):
    for sourceDestinationTuple in assignVars:
        if assignVars[sourceDestinationTuple].value() > 0.5:
            logging.info("Assign --- Source: "+str(sourceDestinationTuple[0])+" | Destination: "+str(sourceDestinationTuple[1]))




def createRouteString(inputData, assignVars, fromOrder, routeString, kpis, ordersServed):

    for toOrder in inputData.demands:

        if toOrder in ordersServed or fromOrder == toOrder:
            continue

        if assignVars[(fromOrder, toOrder)].value() > 0.5:
            routeString += " --> " + str(toOrder) + "(" + str(inputData.demands[toOrder]) + ")"
            kpis['totalQtyDelivered'] += inputData.demands[toOrder]
            kpis['totalCost'] += inputData.travelMatrix[inputData.demandLocation[fromOrder]][inputData.demandLocation[toOrder]] * inputData.costPerKm

            if inputData.demandLocation[toOrder] != inputData.depot:
                ordersServed.add(toOrder)
                routeString, kpis = createRouteString(inputData, assignVars, toOrder, routeString, kpis, ordersServed)
                return routeString, kpis

    return routeString, kpis





def storeSolution(assignVars, solution, inputData):

    solution[inputData.iteration] = {'routes': [], 'totalQtyDelivered': [], 'totalCost': []}

    ordersServed = set()
    for _ in range(inputData.numOfVehicles):
        kpis = {'totalQtyDelivered': 0, 'totalCost': 0}
        routeString, kpis = createRouteString(inputData, assignVars, inputData.depot, inputData.depot, kpis, ordersServed)
        if kpis['totalQtyDelivered'] == 0:
            continue
        solution[inputData.iteration]['routes'].append(routeString)
        solution[inputData.iteration]['totalQtyDelivered'].append(kpis['totalQtyDelivered'])
        solution[inputData.iteration]['totalCost'].append(kpis['totalCost'])

    return solution





def writeOutputToCsv(solution):

    with open("../output/routes.csv", "w", newline='') as file:
        dataWriter = csv.writer(file)
        dataWriter.writerow(['Route Optimization'])
        dataWriter.writerow([''])
        dataWriter.writerow(['Trip', 'TotalQtyDelivered', 'Route', 'TotalTravelCost'])

        tripCounter = 1
        for iteration in solution:
            for id in range(len(solution[iteration]['routes'])):
                dataWriter.writerow([tripCounter, solution[iteration]['totalQtyDelivered'][id], solution[iteration]['routes'][id], solution[iteration]['totalCost'][id]])
                tripCounter += 1