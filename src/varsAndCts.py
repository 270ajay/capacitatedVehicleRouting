import pulp, logging
'''https://arxiv.org/pdf/1606.01935.pdf - page 3, 4'''



#######################################################################################################################
###########################################      CONSTANTS BELOW      #################################################
#######################################################################################################################



ASSIGN_VAR = "Assign"
SUBTOUR_ELIM_VAR = "SubtourELim"
EACH_ORDER_ONCE_CT = "EachOrderOnceCt"
MAX_NUM_OF_ROUTES_CT = "MaxNumOfRoutesCt"
CORRECT_FLOW_CT = "CorrectFlowCt"
SUBTOUR_ELIM_CT = "SubtourElimCt"



#######################################################################################################################
####################################         VARIABLE FUNCTIONS BELOW      ############################################
#######################################################################################################################


def createAssignVehicleVars(model, inputData):

    assignVars = {}
    for fromOrder in inputData.demands:
        for toOrder in inputData.demands:

            if fromOrder == toOrder:
                continue

            varNameInLpFile = ASSIGN_VAR + "_" + str(fromOrder) + "_" + str(toOrder)
            variable = pulp.LpVariable(varNameInLpFile, lowBound=0, upBound=1, cat=pulp.LpBinary)
            assignVars[(fromOrder, toOrder)] = variable
            model.addVariable(variable)

    logging.info("Created assign variables")
    return assignVars





def createSubtourElimVars(model, inputData):

    subtourElimVars = {}
    for order in inputData.demands:

        varNameInLpFile = SUBTOUR_ELIM_VAR + "_" + str(order)
        if order == inputData.depot:
            variable = pulp.LpVariable(varNameInLpFile, lowBound=0, upBound=inputData.vehicleCapacity, cat=pulp.LpContinuous)
        else:
            variable = pulp.LpVariable(varNameInLpFile, lowBound=inputData.demands[order], upBound=inputData.vehicleCapacity, cat=pulp.LpContinuous)

        subtourElimVars[order] = variable
        model.addVariable(variable)

    logging.info("Created sub-tour elimination variables")
    return subtourElimVars




#######################################################################################################################
#######################################      OBJECTIVE FUNCTION BELOW      ############################################
#######################################################################################################################



def createObjectiveFunction(model, assignVars, inputData):

    coeffVarList = []
    for fromOrderToOrderTuple in assignVars:

        fromOrderLoc = inputData.demandLocation[fromOrderToOrderTuple[0]]
        toOrderLoc = inputData.demandLocation[fromOrderToOrderTuple[1]]

        coeffVarList += [float(inputData.travelMatrix[fromOrderLoc][toOrderLoc]) * float(inputData.costPerKm) \
                         * assignVars[fromOrderToOrderTuple]]

    model.setObjective(pulp.lpSum(coeffVarList))
    logging.info("Objective is set")






#######################################################################################################################
####################################      CONSTRAINT FUNCTIONS BELOW       ############################################
#######################################################################################################################





def createEachOrderOnceCt(model, assignVars, inputData):

    for fromOrder in inputData.demands:
        if fromOrder == inputData.depot:
            continue

        coeffVarList = []
        for toOrder in inputData.demands:
            if fromOrder == toOrder:
                continue

            coeffVarList += [assignVars[(fromOrder, toOrder)]]

        model += pulp.lpSum(coeffVarList) == 1, EACH_ORDER_ONCE_CT + "_" + str(fromOrder)

    logging.info("Each order visit only once constraints added")





def createUpperBoundOnMaxNumberOfRoutesCt(model, assignVars, inputData):

    for fromOrder in inputData.demands:
        if fromOrder == inputData.depot:

            coeffVarList = []
            for toOrder in inputData.demands:
                if fromOrder == toOrder:
                    continue

                coeffVarList += [assignVars[(fromOrder, toOrder)]]

            model += pulp.lpSum(coeffVarList) <= inputData.numOfVehicles, MAX_NUM_OF_ROUTES_CT + "_" + str(fromOrder)
            break

    logging.info("Upper bound on max number of routes constraint added")





def createCtForCorrectFlow(model, assignVars, inputData):

    for fromOrder in inputData.demands:
        if fromOrder == inputData.depot:
            continue

        coeffVarList = []
        for toOrder in inputData.demands:
            if fromOrder == toOrder:
                continue

            coeffVarList += [assignVars[(toOrder, fromOrder)] - assignVars[(fromOrder, toOrder)]]

        model += pulp.lpSum(coeffVarList) == 0, CORRECT_FLOW_CT + "_" + str(fromOrder)

    logging.info("Correct flow constraints added")





def createSubtourElimCt(model, assignVars, subtourElimVars, inputData):

    for fromOrder in inputData.demands:
        for toOrder in inputData.demands:

            if fromOrder == toOrder:
                continue

            if toOrder == inputData.depot:
                continue

            coeffVarList = [subtourElimVars[fromOrder] - subtourElimVars[toOrder]
                      + (inputData.demands[toOrder] * assignVars[(fromOrder,toOrder)])
                      + (inputData.vehicleCapacity * assignVars[(fromOrder,toOrder)])]
            model += pulp.lpSum(coeffVarList) <= inputData.vehicleCapacity, SUBTOUR_ELIM_CT + "_" + fromOrder + "_" + toOrder

    logging.info("Subtour elimination constraints added")