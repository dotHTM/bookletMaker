#!/usr/bin/env python3
# bookletMaker.py

import math
import csv
import json


def sliceDict(someDict, keylist):
    result = {}
    for k in someDict:
        if k in keylist:
            result[k] = someDict[k]
    return result


def sliceDictList(someDictList, keylist):
    return list(map(lambda x: sliceDict(x, keylist), someDictList))


def flatten_listList(listList):
    tmp = []
    for x in listList:
        tmp.extend(x)
    return tmp


def sliceDict(inputDict, indexList):
    tmp = {}
    for i in indexList:
        if i in inputDict:
            tmp[i] = inputDict[i]
        else:
            tmp[i] = None
    return tmp


def signatureBreaker(
    sequence,
    blankValue,
    maxSheets,
    minSheets=None,
    startNumber=1,
):
    if minSheets == None:
        minSheets = maxSheets
    if maxSheets < minSheets:
        s = [maxSheets, minSheets]
        s.reverse()
        [maxSheets, minSheets] = s

    maxPages = maxSheets * 4
    pagesAppended = 0
    sn_offset = pagesAppended

    signatures = []
    rapp_sb = lambda r, subseq, startNumber: r.append(
        signatureBuilder(subseq, blankValue, startNumber))

    wcSignature = []
    for i in sequence:
        wcSignature.append(i)
        pagesAppended += 1
        if pagesAppended % maxPages == 0:
            rapp_sb(signatures, wcSignature, startNumber + sn_offset)
            wcSignature = []
            sn_offset = pagesAppended

    while 0 < len(wcSignature) and len(wcSignature) < minSheets * 4:
        wcSignature.append(page(blankValue, ''))
        pagesAppended += 1

    if 0 < len(wcSignature):
        rapp_sb(signatures, wcSignature, startNumber + sn_offset)

    flat_signatures = flatten_listList(signatures)

    blankCount = len(
        list(filter(lambda x: x['page'] == blankValue, flat_signatures)))

    return {
        'signatures': signatures,
        'flat_signatures': flat_signatures,
        'blankCount': blankCount,
        'signatureCount': len(signatures),
        'signatureSizes': list(map(lambda x: int(len(x) / 4), signatures))
    }


def minimalBlanksBreaker(sequence,
                         blankValue,
                         maxSheets=6,
                         minSheets=2,
                         startNumber=1):
    if minSheets == None:
        minSheets = maxSheets
    if maxSheets < minSheets:
        s = [maxSheets, minSheets]
        s.reverse()
        [maxSheets, minSheets] = s

    minBlanks = None
    minBlanksList = []
    seenSizes = {}
    xl = list(range(minSheets, maxSheets))
    xl.reverse()
    for x in xl:
        yl = list(range(minSheets, x))
        yl.reverse()
        for y in yl:
            testBlanks = signatureBreaker(sequence,
                                          blankValue,
                                          x,
                                          minSheets=y,
                                          startNumber=startNumber)

            if not minBlanks or testBlanks['blankCount'] < minBlanks[
                    'blankCount']:
                minBlanks = testBlanks
                minBlanksList = []
                seenSizes = {}

            if testBlanks['blankCount'] == minBlanks['blankCount']:
                DEBUG.msg([x, y])
                sizeStr = str(testBlanks['signatureSizes'])
                if not sizeStr in seenSizes:
                    minBlanksList.append(testBlanks)
                    seenSizes[sizeStr] = 1

    for mb in minBlanksList:
        VERBOSE.msg(
            json.dumps(sliceDict(mb, [
                'blankCount',
                'signatureCount',
                'signatureSizes',
            ]),
                       indent=2))

    return minBlanksList


def signatureBuilder(sequence, blankValue, startNumber):
    start = 0
    length = len(sequence)
    missingLength = math.ceil(length / 4) * 4 - length
    turnAroundIndex = math.ceil(length / 4) * 2

    for x in range(0, missingLength):
        sequence.append(page(blankValue, ''))

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
    flatPages = orderedPages['flat_signatures']
    result = [['imageA', 'pageNumbA', 'imageB', 'pageNumbB']]
    row = []

    for somePage in flatPages:
        if 'page' in somePage and 'number' in somePage:
            row.append(template(somePage['page']))
            row.append(somePage['number'])

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


def page(value, number):
    return {'page': value, 'number': number}


def numberNaiveSequence(inputList, startNumber=1):
    step = startNumber
    r = []
    for e in inputList:
        r.append(page(e, step))
        step += 1
    return r


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

    parser.add_argument('--signature-size',
                        '-s',
                        '--smax',
                        metavar="<integer>",
                        action="store",
                        dest="signatureSize",
                        type=int,
                        help="Maximum size of the signatures.")

    parser.add_argument(
        '--signature-size-min',
        '--smin',
        metavar="<integer>",
        action="store",
        dest="signatureMinSize",
        type=int,
        help=
        "Minimum size of the signatures. If not defined, will be the same as the maximum size."
    )

    parser.add_argument(
        '--start-number',
        '--sn',
        metavar="<integer>",
        action="store",
        dest="startNumber",
        type=int,
        default=1,
        help=
        "The number the first page image should be numbered with. Default is 1."
    )

    parser.add_argument(
        '--minimal-blanks',
        action='store_true',
        dest='minimalBlanks',
        default=False,
        help=
        'Optimize signatures for minimal blank page insertions. Overides maximum and minimum signature size values.'
    )

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

    # args.startNumber

    DEBUG.msg({
        'DEBUG': DEBUG.get(),
        'VERBOSE': VERBOSE.get(),
        'prefix': args.prefix,
        'suffix': args.suffix,
        'startNumber': args.startNumber,
        'print': args.print,
        'pages': args.pages,
        'outputPath': args.outputPath,
        'template': template("{#}"),
    })

    def errorHelp(message):
        print(f"ERROR: {message}")
        parser.print_help()
        exit(2)

    solution = None

    pagesNumbered = numberNaiveSequence(args.pages, args.startNumber)

    if args.minimalBlanks:
        solution = minimalBlanksBreaker(pagesNumbered, '')[0]
    elif args.signatureSize:
        if args.signatureMinSize:
            solution = signatureBreaker(pagesNumbered, '', args.signatureSize,
                                        args.signatureMinSize)
        else:
            solution = signatureBreaker(pagesNumbered, '', args.signatureSize,
                                        args.signatureSize)
    else:
        solution = signatureBreaker(pagesNumbered, '', 2, 4)

    if args.print:
        print(solution)

    if args.outputPath:
        write_single_page_spread_data(solution, args.outputPath, template)


if __name__ == '__main__':
    main()