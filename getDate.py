import re, scraper

r = scraper.scrape()
def findDate(r):
    listOfDates = re.findall("Jan|January|Feb|February|Mar|March|Apr|April|May|Jun|June|Jul|July|Aug|August|Sep|September|Oct|October|Nov|November|Dec|December", r)
    return listOfDates


def findTime(r):
    listOfTimes = re.findall("[0-9]{2}:[0-9]{2}", r)
    return listOfTimes

print "Times: " + str(findTime(r))
print "Dates: " + str(findDate(r))
