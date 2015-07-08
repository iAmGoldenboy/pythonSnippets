__author__ = 'Miklas Njor (iAmGoldenboy) http://miklasnjor.com - Feel free to use this script and hack away'

from collections import Counter
from statistics import median
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer


def sortByKey1(item):
    # http://www.pythoncentral.io/how-to-sort-a-list-tuple-or-object-with-sorted-in-python/
    return item[1]



def removeStopwordsKeepString(stringToRemoveStopwordsFrom, stopwordLanguage = 'danish'):
    """ Takes a string or list and removes all the stopwords in the string (or list) from the chosen language.
    :param stringToRemoveStopwordsFrom: The string or list to remove stopwords from.
    :param language: the stopword's langauge - defaults to danish.
    :return: string that has had all stopwords from the chosen language removed.
    """

    # if object is a list, convert to string
    if isinstance(stringToRemoveStopwordsFrom, list):
        joinedList = ''
        joinedList += " ".join(stringToRemoveStopwordsFrom)
        stringToRemoveStopwordsFrom = joinedList

    listOfStopwords = stopwords.words(stopwordLanguage)

    stringWithoutStopWords = ""

    for token in stringToRemoveStopwordsFrom.split():
        if token not in listOfStopwords:
            stringWithoutStopWords += "{} ".format(token)

    return stringWithoutStopWords



def tokenizeRemovePunctuation(stringToClean):
    """ Removes all punctuation and splits the tokens. http://stackoverflow.com/a/15555162
    Depends on from nltk.tokenize import RegexpTokenizer
    :param stringToClean: a string object.
    :return: a list of tokens (and no punctuation)
    """

    tokenizer = RegexpTokenizer(r'\w+')
    tokenisedList = tokenizer.tokenize(stringToClean)

    return tokenisedList





def returnThirdQuartileAnnotations(annotationsList):
    """ Returns the annotations in the third quartile of all the annotations (i.e. keywords)
    Depends on minMaxMedianParts(), extractsFromCounter(), Counter() (from collections)
    :param annotationsList: a list of annotations
    :return: foundQuartile (with counts, foundQuartileRaw (without count)
    """

    numberslist = []
    foundQuartile = []
    foundQuartileRaw = []

    # for each annotation in the list, add the count of the annotation
    # to the list using the functions extractFromCounter()
    for annotations in extractFromCounter(Counter(annotationsList)):

        # add the count to the list
        numberslist.append(annotations[1])


    # compute the third quartile using the functions minMaxMedianInParts
    third = minMaxMedianInParts(numberslist)[4]

    # for each annotation in the list, add the count of the annotation
    # to the list using the functions extractFromCounter() if annotation is in 3rd quartile
    for newAnnotations in extractFromCounter(Counter(annotationsList)):

        if newAnnotations[1] >= third and newAnnotations[1]:

            foundQuartile.append(newAnnotations)
            foundQuartileRaw.append(newAnnotations[0])

    return foundQuartile, foundQuartileRaw



def returnCounterQuartiles(listKeywords):
    """ Finds and returns the float of 1st, 2nd and 3rd quartiles of a list of keywords
    :param listKeywords:
    :return: 1st, 2nd, 3rd quartiles.
    """
    countedKeywords = Counter(listKeywords)
    keywordCounts = []

    # loop through each keywords and it's count and add only the counts to the list
    for items in countedKeywords.items():
        keywordCounts.append(items[1])

    # get 1st, 2nd, 3rd medians (quartiles) from the list of keywordCounts
    medians = minMaxMedianInParts(sorted(keywordCounts))


    return medians[3], medians[2], medians[4]




def splitIntoQuartile(lowercaseKeywords):
    """
    :param lowercaseKeywords: a list of lowercase keywords (strings, NO integers!)
    :return: a list of lists with keywords and their count from each quartile (1st, 2nd, 3rd)
    """

    # get the quartile for counts of annotations (1st, 2nd, 3rd)
    quartiles = returnCounterQuartiles(sorted(lowercaseKeywords, reverse=True))

    # create lists
    firstQuart = []
    secondQuart = []
    thirdQuart = []

    # take the count of items in the list
    tagsCounterList = convertCounterToList(lowercaseKeywords)

    # for items in the tagsCounterList, add them to the quartile bags.
    for token in tagsCounterList:

        # third quartile, very popular
        if token[1] >= quartiles[2]:
            thirdQuart.append([token[0], token[1]])

        # second quartile, fairly popular NOTE BETWEEN! Important, so that it wont interfere with 1st or 3rd quartile
        elif token[1] < quartiles[2] and token[1] >= quartiles[1]:
            secondQuart.append([token[0], token[1]])

        # first quartile - obviously always minimum 1
        elif token[1] <= quartiles[1]:
            firstQuart.append([token[0], token[1]])

        else:
            pass
            # print(token) # leaving here just in case for debugging, so it prints like an alert if stuff goes south!


    return firstQuart, secondQuart, thirdQuart



def getCounterQuartiles(listKeys):

    countedAnnos = Counter(listKeys)
    countsNumbers = []
    for items in countedAnnos.items():
        countsNumbers.append(items[1])

    # print(sorted(countsNumbers))
    medians = minMaxMedianInParts(sorted(countsNumbers))

    return medians[3], medians[2], medians[4]




def extractFromCounter(counterItems):
    """ Extracts items from a Counter object in descending order. Basically converts Counter Dict to a List
    Depends on sortByKey1, and Counter from collections
    :param counterItems: The items to count and extract the count from.
    :return: extracedList (a list of counts, with the item and count: [ ["wordOne", 4], ["chapstick", 3] , ["Giant Eggs", 1]]
    """

    extractedList = []

    for items, parts in sorted(counterItems.items(), key=sortByKey1, reverse=True):

        extractedList.append([items, parts])

    return extractedList


def convertCounterToList(listOfTags):
    """ Extracts items from a list
    :param listOfTags: Tags to find counts and make into list
    :return: a sorted list
    """

    countedConvertedTags = []

    countsList = Counter(listOfTags)

    [countedConvertedTags.append([items[0], items[1]]) for items in countsList.items()]

    return sorted(countedConvertedTags, key=sortByKey1, reverse=True)



def minMaxMedianInParts(listToMinMaxMedian):
    """ Returns list with min, mix, median, 1st and 3rd median
    :param listToMinMaxMedian: The list of items to find the five number summary from
    :return: List with min, mix, median, 1st and 3rd median
    """


    if len(listToMinMaxMedian) > 1:

        minimum = min(listToMinMaxMedian)
        maximum = max(listToMinMaxMedian)
        secondQuart = round(median(listToMinMaxMedian), 3)
        firstQuart = round(median(median1st3rd(listToMinMaxMedian)[0]), 3)
        thirdQuart = round(median(median1st3rd(listToMinMaxMedian)[1]), 3)

    else:
        minimum = min(listToMinMaxMedian)
        maximum = max(listToMinMaxMedian)
        secondQuart = 0.0
        firstQuart = 0.0
        thirdQuart = 0.0

    return minimum, maximum, secondQuart, firstQuart, thirdQuart




def median1st3rd(listTomediate):
    """ Find the first and Third median from a list
    :param listTomediate: List
    :return: FirstQuartile and SecondQuartile
    """
    sortedAge = sorted(listTomediate)
    arrayLength = round(len(sortedAge)/2)

    firstHalf = sortedAge[0:arrayLength]
    lastHalf = sortedAge[arrayLength:]

    return firstHalf, lastHalf



somelist = ['banan', 'banan','banan', 'banan','banan', 'banan', 'aber', 'aber', 'aber', 'spiser', 'spiser', 'spiser', 'spiser', 'spiser', 'spiser', 'spiser', 'spiser', 'spiser', 'spiser', 'spiser', 'koket', 'koket', 'koket', 'koket', 'koket', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'træet', 'træet', 'træet', 'træet', 'træet', 'træet', 'mens', 'mens', 'mens', 'de', 'de', 'de', 'de', 'de', 'de', 'de', 'de', 'de', 'de', 'de', 'de', 'de', 'de', 'de', 'de', 'de', 'de', ]

print(splitIntoQuartile(somelist))