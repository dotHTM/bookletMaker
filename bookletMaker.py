#!/usr/bin/env python3
# bookletMaker.py

import math
import csv


def sliceDict(someDict, keylist):
    result = {}
    for k in someDict:
        if k in keylist:
            result[k] = someDict[k]
    return result


def sliceDictList(someDictList, keylist):
    return list(map(lambda x: sliceDict(x, keylist), someDictList))


def signatureBreaker(sequence, blankValue, maxsheets, minSheets=None):
    if minSheets == None:
        minSheets = maxsheets
    if maxsheets < minSheets:
        s = [maxsheets, minSheets]
        s.reverse()
        [maxsheets, minSheets] = s

    maxPages = maxsheets * 4
    ssc = 0

    result = []
    rapp_sb = lambda subseq: result.append(signatureBuilder(
        subseq, blankValue))

    wcSignature = []
    for i in sequence:
        ssc += 1
        wcSignature.append(i)
        if ssc % maxPages == 0:
            rapp_sb(wcSignature)
            wcSignature = []

    while 0 < len(wcSignature) and len(wcSignature) < minSheets * 4:
        wcSignature.append(blankValue)

    rapp_sb(wcSignature)

    flat_result = []
    for x in result:
        flat_result.extend(x)

    blankCount = len(list(filter(lambda x: x == blankValue, flat_result)))

    return {
        'signatures': result,
        'flat_result': flat_result,
        'blankCount': blankCount,
        'signatureCount': len(result),
        'signatureSizes': list(map(lambda x: int(len(x) / 4), result))
    }


def minimalBlanksBreaker(sequence, blankValue, maxsheets=6, minSheets=2):
    if minSheets == None:
        minSheets = maxsheets
    if maxsheets < minSheets:
        s = [maxsheets, minSheets]
        s.reverse()
        [maxsheets, minSheets] = s

    minBlanks = None
    minBlanksList = []
    xl = list(range(minSheets, maxsheets))
    xl.reverse()
    for x in xl:
        yl = list(range(minSheets, x))
        yl.reverse()
        for y in yl:
            testBlanks = signatureBreaker(sequence, blankValue, x, minSheets=y)

            if not minBlanks or testBlanks['blankCount'] < minBlanks[
                    'blankCount']:
                minBlanks = testBlanks
                minBlanksList = []

            if testBlanks['blankCount'] == minBlanks['blankCount']:
                DEBUG.msg([x, y])
                minBlanksList.append(testBlanks)

    return minBlanksList


def signatureBuilder(sequence, blankValue):
    start = 0
    length = len(sequence)
    missingLength = math.ceil(length / 4) * 4 - length
    turnAroundIndex = math.ceil(length / 4) * 2

    for x in range(0, missingLength):
        sequence.append(blankValue)

    pages = []
    walk = 0
    direction = 1
    for i in sequence:
        if direction == 1 and walk < turnAroundIndex:
            walk += 1
            pages.append([i])
        else:
            direction = -1
            walk += -1
            pages[walk].append(i)

    walk = 0
    for i in pages:
        walk += 1
        if walk % 2 == 1:
            i.reverse()

    printablePages = []
    for p in pages:
        for i in p:
            if i == blankValue:
                printablePages.append(blankValue)
            else:
                printablePages.append(i)

    return printablePages


def write_single_page_spread_data(orderedPages,
                                  filename,
                                  template=lambda x: x):
    flatPages = orderedPages['flat_result']
    result = [['imageA', 'pageNumbA', 'imageB', 'pageNumbB']]
    row = []

    for somePage in flatPages:
        row.append(template(somePage))
        row.append(somePage)
        if len(row) >= 4:
            result.append(row)
            row = []

    with open(f'{filename}', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile,
                            delimiter=',',
                            quotechar='"',
                            quoting=csv.QUOTE_MINIMAL)
        for r in result:
            writer.writerow(r)


def dict_breakLines(inputDict):
    result = []
    for x in inputDict:
        result.append(f'  {x} : {inputDict[x]}')
    return "\n".join(result)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#                                  88
#                                  ""
#
#    88,dPYba,,adPYba,  ,adPPYYba, 88 8b,dPPYba,
#    88P'   "88"    "8a ""     `Y8 88 88P'   `"8a
#    88      88      88 ,adPPPPP88 88 88       88
#    88      88      88 88,    ,88 88 88       88
#    88      88      88 `"8bbdP"Y8 88 88       88
#
#


class BoolMsg():
    def __init__(self, value):
        self.value = value

    def msg(self, message):
        if self.value:
            print(message)

    def set(self, newValue):
        self.value = newValue

    def get(self):
        return self.value


DEBUG = BoolMsg(False)
VERBOSE = BoolMsg(False)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description=
        'Order pages for booklet signatures and optionally generate data file for merge with a layout application.'
    )

    parser.add_argument(
        'pages',
        metavar='<page>',
        type=str,
        nargs='*',
        help='Pages for ordering. Can be integers, file names, or file paths.')

    parser.add_argument(
        '--out-csv',
        '-o',
        metavar='<path to output file>',
        dest='outputPath',
        action='store',
        type=str,
        help=
        'Output a CSV file in the four-column format: imageA,pageNumbA,imageB,pageNumbB'
    )

    parser.add_argument(
        '--prefix',
        metavar="<substring>",
        action="store",
        type=str,
        default='',
        help="The prefix for the filename. Usually path and file prefix.")
    parser.add_argument(
        '--suffix',
        metavar="<substring>",
        action="store",
        type=str,
        default='',
        help="The suffix for the filename. Usually file extention.")

    parser.add_argument('--optimize',
                        action='store_true',
                        help='Optimize signatures for minimal blank page insertions.')
    parser.add_argument('--print',
                        '-p',
                        action='store_true',
                        help='Print object of result')

    parser.add_argument('--debug',
                        '-d',
                        dest='debug',
                        action='store_true',
                        help='Enable Debugging messages.')
    parser.add_argument('--verbose',
                        '-v',
                        dest='verbose',
                        action='store_true',
                        help='Enable Debugging messages.')

    args = parser.parse_args()

    DEBUG.set(args.debug)
    VERBOSE.set(args.verbose)

    template = lambda p: f"{args.prefix}{p}{args.suffix}"
    blankValue = ''
    
    DEBUG.msg({
        'DEBUG': DEBUG.get(),
        'VERBOSE': VERBOSE.get(),
        'prefix': args.prefix,
        'suffix': args.suffix,
        'print': args.print,
        'pages': args.pages,
        'outputPath': args.outputPath,
        'template' : template("{#}"),

    })

    def errorHelp(message):
        print(f"ERROR: {message}")
        parser.print_help()
        exit(2)

    solution = None
    
    if args.optimize:
        solution = minimalBlanksBreaker(args.pages, '')[0]
    else:
        solution = signatureBreaker(args.pages, '', 4, 8)

    if args.print:
        print(solution)
    
    if args.outputPath:
        write_single_page_spread_data(solution, args.outputPath, template)


if __name__ == '__main__':
    main()