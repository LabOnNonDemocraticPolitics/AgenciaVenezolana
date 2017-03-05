# Theodore Chu
# March 4, 2017
# For the USC Lab on Non-Democratic Politics under the direction of Erin Baggott Carter and Brett Logan Carter
# Scrapes the Agencia Venezolana
# Prints all sections
# Encodes in utf-8

# Dates are not used in Agencia Venezolana archive
# Waits 5-10 minutes every 100 pages to avoid crashing the archive

import math  # this lets you do math
import io # this allows encoding in utf-8
import time  # this lets you slow down your scraper so you don't crash the website =/
import random  # this lets you draw random numbers.
import datetime  # this lets you create a list of dates
from selenium import webdriver  # the rest of these let you create your scraper

# prompt for start date
# prompt for end date
# name the file out
# load first date
# get the number of results
# go to the first page on the first date
# get all links from the first page on the first date
# go to each article from first page on first date. print to file
# repeat for all links on first date (while loop)
# repeat for all dates until the last date (while loop)

startTime = time.time()

#url = "http://www.avn.info.ve/buscar?page=1&key="

class AgenciaVenezolana(object):
    def __init__(self):
        directory = input("Enter Directory: (ex: C:/Users/Theodore/Desktop/Programming/Scraping/AgenciaVenezolana/). Press Enter for example:")
        if directory == "":
            directory = "C:/Users/Theodore/Desktop/Programming/Scraping/AgenciaVenezolana/"

        fileOutName = input("Enter file out name. Please omit \".txt\" (ex: avs2016.txt):")
        self.__fileOut = io.open(directory + fileOutName + ".txt", "a", encoding="utf-8")
        self.__pageCounter = 0
        queryInput = input("Insert search term (if none, enter \"none\"):")
        if queryInput == "" or queryInput == "none":
            queryInput = ""
        self.__query = queryInput.strip()
        self.__driver = webdriver.Firefox()

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
                #if "contenido" in link: # Agencia Venezolana does not allow changes in article type. This filters content only
                #    linksList.append(link)
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
                self.__driver.get(url)
                time.sleep(random.uniform(1, 10))

                # Print Title
                titleData = self.__driver.find_element_by_class_name("titulo")
                title = titleData.text
                print(title)
                print(title, file=self.__fileOut)

                # Date
                dateData = self.__driver.find_element_by_class_name("fecha-hora")
                dateText = dateData.text
                print(dateText)
                print(dateText, file=self.__fileOut)

                # Author (is not needed)
                #authorData = self.__driver.find_element_by_class_name("autor")
                #authorText = authorData.text
                #print(authorText)
                #print(authorText, file=self.__fileOut)


                # Print the story in the article
                content = self.__driver.find_element_by_class_name("contenido")
                storydata = content.find_elements_by_tag_name("p")
                for story in storydata:
                    storyText = story.text
                    print(storyText)
                    print(storyText, file=self.__fileOut)

                self.__pageCounter += 1
                print("Article", self.__pageCounter, "printed")
                print("\n\n************************************\n\n")
                print("\n\n************************************\n\n", file=self.__fileOut)
                if self.__pageCounter % 100 == 0:
                    print("Current time:", datetime.datetime.now().time())
                    print("Sleeping. . .")
                    time.sleep(random.uniform(300, 600))
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

    def closeFile(self):
        self.__fileOut.close()


# Main loop
def main():
    avs = AgenciaVenezolana()
    startPage = input("Enter the page number to start at. Integers only. If starting from beginning, enter \"0\"")
    if startPage == 0:
        avs.loadFirstResultsPage()
        n = 0
    else:
        n = int(startPage)
        avs.goToNextResultsPage(n)

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
    avs.closeFile()



main()

totElapsedTime = time.time() - startTime
print("Total elapsed time: ", totElapsedTime)
print("Current time:", datetime.datetime.now().time())
