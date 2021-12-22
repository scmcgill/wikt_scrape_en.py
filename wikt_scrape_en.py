# currently only works for some tests on finding foreign translations of english wiktionary words
# how to add grammatical info based on part of speech?
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
        # delete trailing underscore and return URL
    return search_term[:-1]
# check for a link to another translation page
def check_linked_translations():
    pseudo_navframe = soup.find("div", class_="pseudo NavFrame")
    if pseudo_navframe:
        navhead = pseudo_navframe.find("div", class_="NavHead")
        link = navhead.find('a',   attrs={'href': re.compile(r'^\/wiki*')})
        if link: 
            URL = "https://en.wiktionary.org" + link.get("href")
            return(URL)
# grab translation from selected languages for each translation table
def get_translations():
    transl = soup.find_all("div", {"id": re.compile(r'Translations-*')})
    # languages whose list items will be selected
    langs = ["fr", "de", "es", "ar", "fa"] 
    # check for list item for each language
    for x in transl:
        # get English meaning of each definition
        print( "\n" + x.find("div", class_="NavHead").text)
        for el in langs:
            # print translation for each meaning/language, if present
            spans =x.find_all("span", lang=el)
            if spans:
                span_texts = ""
                for span in spans:
                   span_texts += span.text + ", "
                #span_texts = span_texts.rstrip(span_texts[-4])
                print("    " + el + ": " + span_texts[:-2])
# fill URL from arguments
URL = "https://en.wiktionary.org/wiki/" + get_search_term() + "#English"
page = requests.get(URL)
# soup it
soup = BeautifulSoup(page.content, "html.parser")
get_translations()
# repeat process for any linked pages for a given word
if check_linked_translations():
    URL = check_linked_translations()
    page = requests.get(URL)
    # soup it
    soup = BeautifulSoup(page.content, "html.parser")
    get_translations()
