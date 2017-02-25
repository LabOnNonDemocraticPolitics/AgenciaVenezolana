# Theodore Chu
# February 20, 2017
# For the USC Lab on Non-Democratic Politics under the direction of Erin Baggott Carter and Brett Logan Carter
# Scrapes the Agencia Venezolana
# Prints all contenida (content) sections
# Use ISO-8859-1 Encoder to read the txt files

# from __future__ import division # this lets you divide numbers and get floating results
import math  # this lets you do math
import re  # this lets you make string replacements: 'hi there'.replace(' there') --> 'hi'
import os  # this lets you set system directories
import time  # this lets you slow down your scraper so you don't crash the website =/
import codecs  # symbols are annoying. this lets you replace them.
import random  # this lets you draw random numbers.
import datetime  # this lets you create a list of dates
from datetime import timedelta  # same
from selenium import webdriver  # the rest of these let you create your scraper
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

# set your working directory
writedir = 'C:\\Users\\Theodore\\Desktop\\Programming\\Scraping\\'


#prompt for start date
#prompt for end date
#name the file out
#load first date
#get the number of results
#go to the first page on the first date
#get all links from the first page on the first date
#go to each article from first page on first date. print to file
#repeat for all links on first date (for loop)
#repeat for all dates until the last date (for loop)

startTime = time.time()

url = "http://www.avn.info.ve/buscar?page=1&key="

class AgenciaVenezolana(object):
    def __init__(self):
        directory = input("Enter Directory: (ex: C:/Users/Theodore/Desktop/Programming/Scraping/). Press Enter for example:")
        if directory == "":
            directory = "C:/Users/Theodore/Desktop/Programming/Scraping/"

        """while True:
            try:
                print("Enter Start Date", end=". ")
                self.__startDate = self.getDate()
                print("Enter End Date", end=". ")
                self.__endDate = self.getDate()
                if self.__startDate > self.__endDate:
                    raise Exception("Start date must be less than end date.")
                break
            except Exception:
                print("Error. Start date must be less than end date.")
                pass"""

        fileOutName = input("Enter file out name. Please omit \".txt\" (ex: avs2016.txt):")
        self.__fileOut = open(directory + fileOutName + ".txt", "a")
        self.__fileOut2 = open(directory + fileOutName + "_utf-8.txt", "a")
        self.__pageCounter = 0
        queryInput = input("Insert search term (if none, enter \"none\"):")
        if queryInput == "" or queryInput == "none":
            queryInput = ""
        self.__query = queryInput.strip()
        self.__driver = webdriver.Firefox()

    # Dates are not needed, but they are here in case we find a way to use dates
    """def getDate(self):
        datebool = True
        while datebool:
            startdate = input("Year and Month only (ex: 20160105 for January 5, 2016):")
            try:
                date = datetime.datetime.strptime(startdate, "%Y%m%d")
                return date
            except Exception as e:
                print("An incorrect date was inputted. Please try again. Error message:\n", e)
                continue

    def getStartDate(self):
        return self.__startDate

    def getEndDate(self):
        return self.__endDate"""

    def loadFirstResultsPage(self):
        firstPage = "http://www.avn.info.ve/buscar?key=" + self.__query
        print("Search URL:", firstPage)
        self.__driver.get(firstPage)

    def getNumberOfResultsPages(self):
        resultsdiv = self.__driver.find_element_by_class_name('result.pull-left')
        #resultsText = resultsdiv.find_element_by_tag_name("p")
        results = resultsdiv.text
        print('Results:', results)
        results = results.split(' resultados')[0]
        results = results.split(' ')[(len(results.split(' ')) - 1)]
        results = int(results)
        resultPages = math.ceil(results / 15)
        print('Result pages:', resultPages)
        time.sleep(random.uniform(2, 10))
        return resultPages

    def goToNextResultsPage(self, numResultsPage):
        print("Page", (numResultsPage-1), "done")     # put at end of each page rather than beginning
        nextPage = "http://www.avn.info.ve/buscar?page=" + str(numResultsPage) + "&key=" + self.__query
        self.__driver.get(nextPage)
        print("Getting page", numResultsPage, "URL:", nextPage)
        time.sleep(random.uniform(2, 5))

    def getSubLinks(self):
        div = self.__driver.find_element_by_class_name("view-content")
        linkdata = div.find_elements_by_tag_name("h4")
        linksList = []
        for data in linkdata:
            try: # Some elements with tag "h2" don't have links. This gets past that
                link = data.find_element_by_css_selector("a").get_attribute("href")
                print(link)
                if "contenido" in link: # Agencia Venezolana does not allow changes in article type. This filters content only
                    linksList.append(link)

                time.sleep(random.uniform(1, 3))
            except Exception as e:
                print("Error in getting sublinks")
                print(e)
        print("Sublinks:", linksList)
        print("Loading sublinks done", end="\n\n")
        time.sleep(random.uniform(5, 10))
        return linksList

    def printFullPageText(self, linksList):  # I'm exploring different ways to write into the file: print(text, file=filename), f.write, utf-8
        for url in linksList:
            try:
                print(url)
                print(url, file=self.__fileOut)
                print(url.encode("utf-8"), file=self.__fileOut2)
                self.__driver.get(url)
                time.sleep(random.uniform(1, 10))

                # Print Title
                titleData = self.__driver.find_element_by_class_name("titulo")
                title = titleData.text
                print(title)
                print(title, file=self.__fileOut)
                titleUTF = title.encode("utf-8")
                print(titleUTF, file=self.__fileOut2)

                # Date
                dateData = self.__driver.find_element_by_class_name("fecha-hora")
                dateText = dateData.text
                print(dateText)
                print(dateText, file=self.__fileOut)
                dateUTF = dateText.encode("utf-8")
                print(dateUTF, file=self.__fileOut2)

                # Author
                authorData = self.__driver.find_element_by_class_name("autor")
                authorText = authorData.text
                print(authorText)
                print(authorText, file=self.__fileOut)
                authorUTF = authorText.encode("utf-8")
                print(authorUTF, file=self.__fileOut2)

                # Print the story in the article
                content = self.__driver.find_element_by_class_name("contenido")
                storydata = content.find_elements_by_tag_name("p")
                for story in storydata:
                    storyText = story.text
                    print(storyText)
                    print(storyText, file=self.__fileOut)
                    storyTextUTF = storyText.encode("utf-8")
                    print(storyTextUTF, file=self.__fileOut2)
                self.__pageCounter += 1
                print("Article", self.__pageCounter, "printed")
                print("Article", self.__pageCounter, "printed", file=self.__fileOut)
                print("Article", self.__pageCounter, "printed", file=self.__fileOut2)
                print("\n\n************************************\n\n")
                print("\n\n************************************\n\n", file=self.__fileOut)
                print("\n\n************************************\n\n", file=self.__fileOut2)
            except Exception as e:
                print("Error in printing full page")
                print(str(e))

    # There is no need to add months
    def startDateAddMonth(self):
        if self.__startDate.month < 12:
            self.__startDate = datetime.datetime.strptime(str(self.__startDate.year) + str(self.__startDate.month + 1), "%Y%m")
        else:
            self.__startDate = datetime.datetime.strptime(str(self.__startDate.year + 1) + "01", "%Y%m")
        return self.__startDate

# Main loop
def main():
    avs = AgenciaVenezolana()
    avs.loadFirstResultsPage()
    n = 0

    while True: # An inequality can be used here to determine number of results and number of results pages
        print('\n#################################### Page ' + str(n) + " ####################################\n")
        try:
            linksList = avs.getSubLinks()
        except Exception as e:  # need exceptions to be more specific
            print("Error in getting next page. There are possibly no more pages.")
            print(e)
            break
        avs.printFullPageText(linksList)
        n += 1
        avs.goToNextResultsPage(n)



main()

totElapsedTime = time.time() - startTime
print("Total elapsed time: ", totElapsedTime)
