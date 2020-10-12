import yaml
import os
import glob
import json
import datetime

CWD_PATH = os.path.dirname(os.path.realpath(__file__))
CONF_PATH = os.path.join(CWD_PATH, '../config/')
DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'

NOWTIME = datetime.datetime.now()
RUNTIME_AS_STRING = NOWTIME.strftime(DATETIME_FORMAT)


def load_yaml_config(configFilePath):
    yaml_config = None
    with open(configFilePath, 'r') as account_stream:
        if account_stream != "":  # To prevent failure on empty file
            try:
                yaml_config = yaml.safe_load(account_stream)
            except yaml.YAMLError as exc:
                print(exc)
                raise
    return yaml_config


def _produceVersionInfo(domainsDict):
    """
    return the versionInfo output
    """
    versionInfo = []
    ticketAPIDict = {}
    ticketAPIDict['ID'] = 'TicketApi'
    ticketAPIDict['modifiedDate'] = RUNTIME_AS_STRING
    versionInfo.append(ticketAPIDict)
    cmsDict = {}
    cmsDict['ID'] = 'CMS'
    cmsDict['modifiedDate'] = RUNTIME_AS_STRING
    versionInfo.append(cmsDict)
    return versionInfo


def _produceGetDomains(domainsDict):
    """
    return the complete getdomains output
    """
    getDomains = []
    for domain in domainsDict:
        responseSection = {}
        responseSection['ID'] = domain
        responseSection['modifiedDate'] = RUNTIME_AS_STRING
        responseSection['Domains'] = domainsDict[domain]
        getDomains.append(responseSection)
    return getDomains


def _produceGetDomain(domainsDict, targetDomain):
    """
    return the getdomain output for both ticketAPI and CMS
    """
    getDomains = []
    for domain in domainsDict:
        if targetDomain == domain:
            responseSection = {}
            responseSection['ID'] = domain
            responseSection['modifiedDate'] = RUNTIME_AS_STRING
            responseSection['Domains'] = domainsDict[domain]
            getDomains.append(responseSection)
    return getDomains


def writeOutput(output, fileType):
    """
    output is json so write it out prettified to a file named {fileType}.json
    """
    if not os.path.isdir(os.path.join(CONF_PATH, '../output')):
        os.mkdir(os.path.join(CONF_PATH, '../output'))
    if not os.path.isdir(os.path.join(CONF_PATH, '../output', 'api')):
        os.mkdir(os.path.join(CONF_PATH, '../output', 'api'))
    if not os.path.isdir(os.path.join(CONF_PATH, '../output/api', 'application')):
        os.mkdir(os.path.join(CONF_PATH, '../output/api', 'application'))
    outputfile = os.path.join(CONF_PATH, '../output', '{0}.json'.format(fileType))
    data_file = open(outputfile, 'w')
    data_file.write(json.dumps(output, indent=2))
    data_file.close()


def loadConfigData():
    domainsDict = {}
    success = True
    errorList = []
    for filename in glob.iglob(os.path.join(CONF_PATH, '**/*.yml'), recursive=True):
        try:
            domainsDict.update(load_yaml_config(filename))
        except Exception as e:
            success = False
            errorList.append("Unable to process file {0}, Error: {1}".format(filename, str(e)))
            continue
    return success, domainsDict, errorList


def main():
    success, domainsDict, errorList = loadConfigData()
    if success:
        versionInfo = _produceVersionInfo(domainsDict)
        getDomains = _produceGetDomains(domainsDict)
        getDomainTicket = _produceGetDomain(domainsDict, 'ticketApi')
        getDomainCMS = _produceGetDomain(domainsDict, 'CMS')
        writeOutput(versionInfo, 'api/versioninfo')
        writeOutput(getDomains, 'api/getdomains')
        writeOutput(getDomainTicket, 'api/application/TicketApi')
        writeOutput(getDomainCMS, 'api/application/CMS')
    else:
        print(errorList)


if __name__ == "__main__":
    main()
