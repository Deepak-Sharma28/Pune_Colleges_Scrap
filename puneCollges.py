from bs4 import BeautifulSoup
import requests,json,csv
from pprint import pprint
with open("pharmacycls.html","r") as f:
    html=f.read()
soup=BeautifulSoup(html,"html.parser")

mainDiv = soup.find("div",class_="row listing-block-cont js-scrolling-container")
# print(mainDiv)

allDiv = mainDiv.find_all('div',class_="top-block")

links_of_colleges = []
dic = {}
s_no = 0


#for all colleges's links


for i in allDiv :
    s_no+=1
    a = i.find('a')['href']
    arr = a.split('-')
    link = ""
    for j in range(len(arr)):
        if j == len(arr)-1 :
            break
        else:
            link+=arr[j]
            link+='-'
    if len(link)!=0 :
        dic[s_no] = (link+'pune')

college_no = 0
all_colleges = {}


for url in dic :

    link = dic[url]
    response = requests.get(link)
    res = BeautifulSoup(response.text,'html.parser')

    college_no +=1
    college_details = {}

    college_data = res.find('div', class_= "college_data")
    h1 = college_data.find('h1',class_= "college_name").text.strip()

    college_details['College_Name'] = h1

    #for college estd and college type

    extra_info = college_data.find('div',class_='extra_info')
    span = extra_info.find_all('span')
    for i in range(len(span)) :
        if span[i] is not None :
            if i == 2 :
                college_details['College_Estd'] = span[i].text.strip()
            elif i == 4 :
                college_details['College_Type'] = span[i].text.strip()




    try:
        college_rating = res.find('div' , class_="college_rating pull-right") 
        spans = college_rating.find_all('span')
        rating = spans[0].text.strip()
        review = spans[1].text.strip()
    except :
        pass



    college_details['Rating'] = rating
    college_details['Reviews'] = review



    #for location

    address_row = res.find('div', class_= "address row")
    loc_block = address_row.find('div', class_="loc_block")
    lr = loc_block.find('div',class_="lr")
    h3 = lr.find('h3').text.strip()
    location = h3.split('\n')
    address = ""
    for i in location :
        address+=i
        address+=" "
    college_details['Location'] = address

    #for contacts

    p = address_row.find('p', class_="lr_detail").text.strip()
    college_details['Contact_details'] = p

    all_colleges[college_no] = college_details



final_data = open('pharmacycolleges.json','w+')
json.dump(all_colleges,final_data, indent=4)









