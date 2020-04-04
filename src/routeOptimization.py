import utilities, logging, data, optModel


if __name__ == '__main__':

    try:

        solution = {}
        utilities.logger(logging)
        logging.info("------------\n")

        inputData = data.InputData()
        inputData.getDemandsForTheRun()

        while inputData.keepRunning:
            solution = optModel.buildAndSolveOptimizationModel(inputData, solution)
            inputData.getDemandsForTheRun()

        utilities.writeOutputToCsv(solution)
        logging.info("\n----------------------------------------------\n")



    except Exception as e:

        logging.exception('Optimization program failed')
        logging.info("\n----------------------------------------------\n")
