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
        'result': result,
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

            if not minBlanks or testBlanks['blankCount'] < minBlanks['blankCount']:
                minBlanks = testBlanks
                minBlanksList = []

            if testBlanks['blankCount'] == minBlanks['blankCount']:
                print([x, y])
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
    result = [['a', 'pa', 'b', 'pb']]
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


def main():

    start = 0
    end = 37

    pageList = range(start, end)

    template = lambda p: f"pages/impose_{p}.svg"
    blankValue = ''

    outputCSVFile = '../impose/impose.csv'

    # orderedPages = signatureBreaker(pageList, blankValue, 4, 8)

    orderedPages = minimalBlanksBreaker(pageList, blankValue)
    import json

    print(
        json.dumps(sliceDictList(
            orderedPages, ['result', 'blankCount', 'signatureSizes', 'signatureCount']),
                   sort_keys=True,
                   indent=4))
    # write_single_page_spread_data(orderedPages, outputCSVFile, template)


if __name__ == '__main__':
    main()