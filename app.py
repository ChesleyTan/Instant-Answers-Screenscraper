from flask import Flask, render_template, request
import google
import urllib2
from urllib2 import urlopen
from bs4 import BeautifulSoup
import filterNames
from collections import Counter
from socket import timeout
from ssl import SSLError

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/answer", methods=["GET"])
def answer():
    query = request.args.get('q')
    query_upper = query.upper()
    if query_upper.find("WHO") > -1:
        try:
            urls = [x for x in google.search(query, lang='en', num=10, start=0, stop=9, pause=1.0)]
        except urllib2.URLError:
            pass
        print "Got urls :)"
        pages = []
        retStr = ""
        topNames = Counter() 
        for url in urls[:10]:
            try:
                soup = BeautifulSoup(urlopen(url, timeout=1).read())
            except urllib2.URLError:
                continue
            except timeout:
                continue
            except SSLError:
                continue
            print "Got soup :)"
            pages.append(soup.get_text())
        len_pages = len(pages)
        for pageIndex in range(len_pages):
            NUM_RESULTS = 5
            names = filterNames.getFilteredInputList(pages[pageIndex]).most_common(NUM_RESULTS)
            retStr += "<table>"
            for index in range(len(names)):
                name = names[index][0]
                if not(name.upper() in query_upper):
                    if not(' ' in name):
                        for item in topNames:
                            parts = item.split(" ")
                            if len(parts) > 1:
                                if name in parts:
                                    topNames[item] += 1
                                    print "Increasing confidence of " + item + " with " + name
                    topNames[name] += len_pages - pageIndex + NUM_RESULTS - index 
                    retStr += "<tr><td>" + name + "</td><td>" + str(names[index][1]) + "</td></tr>"
            retStr += "</table><hr>"
        retStr = "<h1>The most common name was " + topNames.most_common(1)[0][0] + "</h1>" + retStr

        return retStr
    else:
        return "Query not supported"
    #return render_template("answer.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
