from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen
import time,random
import re,requests
def get_latest():
  title = []
  site = []
  img = []
  chaps = []
  url = "https://m.mangairo.com/manga-list/type-latest/ctg-all/state-all/page-1"
  data = requests.get(url, proxies={"http":"http://myproxy:3129"})

  soup = bs(data.content,'html.parser')
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
  data = requests.get(url, proxies={"http":"http://myproxy:3129"})

  soup = bs(data.content,'html.parser')
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
  data = requests.get(url, proxies={"http":"http://myproxy:3129"})

  soup = bs(data.content,'html.parser')
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
  data = requests.get(url, proxies={"http":"http://myproxy:3129"})

  soup = bs(data.content,'html.parser')
  chap_url,description,chap_name = [],[],[]
  img = ""  
  '''with open ("mangatest.txt","w+",encoding="utf8") as f:
    f.write(str(soup))'''

  if soup.find("div", {"class": "chapter_list"}):
    for cnt in soup.find_all("div", {"class":"chapter_list"}):
      for list_tag in cnt.find_all('li'):
        chap_url.append(list_tag.a["href"])
        chap_name.append(list_tag.text[0:list_tag.text.index(":")]) if ":" in list_tag.a["title"] else chap_name.append(list_tag.text)
          
  elif soup.find("a",{"class":"chapter-name text-nowrap"}):
    for cnt in soup.find_all("a", {"class":"chapter-name text-nowrap"}):
        chap_url.append(cnt["href"])
        chap_name.append(cnt.text) if not ":" in cnt.text else chap_name.append(cnt.text[0:cnt.text.index(":")]) 
          
  for cnt in soup.find_all("meta",{"property":"og:image"}):
    img = cnt["content"]
  for cnt in soup.find_all("div",{"class":"panel-story-info-description"}):
    description.append(cnt.text)
  return  chap_url,img,description,chap_name
