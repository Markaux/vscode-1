import logging

class thelogger:
    
    def __init__(self, logfile):
        # write in log file
        logging.basicConfig(filename=logfile, level=logging.INFO)

    def managelog(self):
        
        # create logger
        logger = logging.getLogger(' ***  Hey ... ***')
        logger.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

        # 'application' code
        logger.debug('debug message')
        logger.info('info message')
        logger.warning('warn message')
        logger.error('error message')
        logger.critical('critical message')

pathFolder = "C:\\Users\\celerierma\\OneDrive - Groupe BPCE\\00-PROJETS\\04-PBI\\RIFA\\WorkInProgress"
logfile = pathFolder + '\\logs\\sendtorifa.log'
thelogger(logfile).managelog()