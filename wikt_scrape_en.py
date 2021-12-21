# why is jsoup version getting all items from a given language/translation, but this is only getting the first for each?
# currently only works for some tests on finding foreign translations of english wiktionary words
# how to add grammatical info based on part of speech?
# what to do when there are multiple elements that are translated?
import re
import sys # be able to add arguments
import requests
from bs4 import BeautifulSoup

# add underscores to string arguments to complete URL
def get_search_term():
    search_term = ""
    for el in range(len(sys.argv) - 1):
        # add underscores    
        search_term += (sys.argv[el + 1] + "_")
        # delete trailing underscore
    search_term = search_term.rstrip(search_term[-1])
    return search_term
def check_linked_translations():
    pseudo_navframe = soup.find("div", class_="pseudo NavFrame")
    if pseudo_navframe:
        navhead = pseudo_navframe.find("div", class_="NavHead")
        link = navhead.find('a',   attrs={'href': re.compile(r'^\/wiki*')})
        if link: 
            URL = "https://en.wiktionary.org" + link.get("href")
            return(URL)



def get_translations():
    transl = soup.find_all("div", {"id": re.compile(r'Translations-*')})
    #print(len(transl))
    # languages whose list items will be selected
    langs = ["fr", "de", "es", "ar", "fa"] 
    # check for list item for each language
    for x in transl:
        # get English meaning of each definition
        print( "\n" + x.find("div", class_="NavHead").text)
        for el in langs:
            # print translation for each language, if there
            item =x.find("span", lang=el)
            if item:
                print("    " + el + ": " + item.text)
# fill URL from arguments string
URL = "https://en.wiktionary.org/wiki/" + get_search_term() + "#English"
page = requests.get(URL)
# soup it
soup = BeautifulSoup(page.content, "html.parser")

# Needs to follow hrefs for pages like "book" that lead to a different page.  If used as function, href can be checked for and the function can be called again on that link.  

get_translations()
if check_linked_translations():
    URL = check_linked_translations()
    page = requests.get(URL)
    # soup it
    soup = BeautifulSoup(page.content, "html.parser")
    get_translations()

#get_translations()
