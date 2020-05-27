from bs4 import BeautifulSoup as bs
import requests
import re
import time
def get_latest():
  start = time.time()
  title = []
  site = []
  img = []
  chaps = []
  url = "https://m.mangairo.com/manga-list/type-latest/ctg-all/state-all/page-1"
  content = requests.get(url)
  soup = bs(content.content,'html.parser')
  counter = 0
  for cnt in soup.find_all("a",{"class": "tooltip"}):
    counter+=1
    if cnt["href"] and counter % 2 == 0:
        site.append(cnt["href"])
    if cnt.img != None:
        img.append(cnt.img["src"])
        #if len(cnt.img["alt"]) < 18:
        title.append(cnt.img["alt"])
        continue
        
        #elif " " in cnt.img["alt"][17:len(cnt.img["alt"])]:
            #index = cnt.img["alt"][17:len(cnt.img["alt"])].index(" ")
            #print("index {} on {}".format(index,cnt.img["alt"][17:len(cnt.img["alt"])]))
        #newTitle = cnt.img["alt"][0:17+index] + "\n" + cnt.img["alt"][17+index:len(cnt.img["alt"])]
        #title.append(newTitle)
  return img,title,site
def get_popular(): 
  title = []
  site = []
  img = []
  chaps = []
  url = "https://m.mangairo.com/manga-list/type-topview/ctg-all/state-all/page-1"
  content = requests.get(url)
  soup = bs(content.content,'html.parser')
  counter = 0
  for cnt in soup.find_all("a",{"class": "tooltip"}):
    counter+=1
    if cnt["href"] and counter % 2 == 0:
        site.append(cnt["href"])
    if cnt.img != None:
        img.append(cnt.img["src"])
        title.append(cnt.img["alt"])
        continue
        
  return img,title,site
def get_search(search_input):
  title = []
  site = []
  img = []
  details = []
  url = "https://m.mangairo.com/search/" + search_input.replace(" ", "_")
  content = requests.get(url)
  soup = bs(content.content,'html.parser')
  for cnt in soup.find_all("div", {"class":"story-item"}):
    site.append(cnt.a["href"])
    img.append(cnt.img["src"])
    title.append(cnt.img["alt"])
    if cnt.find("span") :
      word = cnt.text
      word  = re.sub(r'\n+', '\n',word)
      details.append(word)
  return img,title,site,details

def get_manga(site):
  url = site
  content = requests.get(url)
  soup = bs(content.content,'html.parser')
  chap_url,description = [],[]
  img = ""
  for cnt in soup.find_all("a", {"class":"chapter-name text-nowrap"}):
    chap_url.append(cnt["href"])
  for cnt in soup.find_all("meta",{"property":"og:image"}):
    img = cnt["content"]
  for cnt in soup.find_all("div",{"class":"panel-story-info-description"}):
    description.append(cnt.text)

  return  chap_url,img,description
