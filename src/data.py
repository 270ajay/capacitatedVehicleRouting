import utilities, logging


class InputData:

    def __init__(self):

        logging.info("Reading inputData")

        self.minDeliveryAmount = 30
        self.minDeliveryPercentage = 0.1

        self.travelMatrix = utilities.getTravelMatrixFromCsv()
        self.remainingDemands, self.demandLocation = utilities.getDemandsFromCsv()
        self.depot = 'Warehouse'
        self.demands = {self.depot : 0}
        self.demandLocation[self.depot] = self.depot


        self.vehicleCapacity = 100
        self.costPerKm = 10
        self.keepRunning = False

        self.numOfVehicles = 10
        self.iteration = 0
        self.timeLimitForSolver = 2
        self.writeLpFile = True


        logging.debug("Input data read and stored in objects")




    def getDemandsForTheRun(self):

        self.keepRunning = False
        for order in self.remainingDemands:

            if order in self.demands and self.remainingDemands[order] == 0:
                del self.demands[order]

            elif self.remainingDemands[order] >= self.minDeliveryAmount:
                self.demands[order] = max(self.minDeliveryAmount, round(self.minDeliveryPercentage * self.remainingDemands[order]))

            elif self.remainingDemands[order] > 0:
                 self.demands[order] = self.remainingDemands[order]



            if order in self.demands and self.demands[order] > 0:
                self.keepRunning = True
                self.remainingDemands[order] -= self.demands[order]

        self.iteration += 1