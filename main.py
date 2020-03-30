from flask import Flask , render_template
import requests
from bs4 import BeautifulSoup
from waitress import serve
import os
app = Flask(__name__)

statesList = []
confirmedCasesIndia = []
confirmedCasesForegin = []

@app.route("/")
def home():
    html = requests.get("https://www.mohfw.gov.in/")
    soup = BeautifulSoup(html.content,'html.parser')
    table_div = soup.findAll("div",{"class":"table-responsive"})
    last = None
    for last in table_div:
        pass
    if last:
        tr = last.findAll('tr')
        i = 0
        for tr_elem in tr:

            if i is not 0:
                i=i+1
                td_elem=tr_elem.findAll('td')
                j=0
                for td in td_elem:
                    if j is not 0:
                        if j is 1:
                            statesList.append(td.getText())
                        if j is 2:
                            confirmedCasesIndia.append(td.getText())
                        if j is 3:
                            confirmedCasesForegin.append(td.getText())
                        j = j+1
                        continue
                    j=1
                    continue
            i=1
        # print(statesList)  
        statesList.pop(len(statesList)-1)
        confirmedCasesIndia.pop(len(confirmedCasesIndia)-1)
        confirmedCasesForegin.pop(len(confirmedCasesForegin)-1)
        # print(confirmedCasesIndia)

        statesListLat = ['Tamil Nadu', 'Telengana',
                 'Madhya Pradesh', 'Haryana', 'Chhattisgarh',
                 'Maharashtra', 'Tripura', 'Karnataka', 'Kerala', 'Uttar Pradesh',
                 'Assam', 'West Bengal', 'Gujarat', 'Odisha', 'Rajasthan', 'Himachal Pradesh',
                 'Andaman and Nicobar Islands', 'Andhra Pradesh', 'Bihar', 'Chandigarh',
                 'Delhi', 'Goa', 'Ladakh', 'Manipur', 'Mizoram', 'Punjab', 'Puducherry', 'Uttarakhand','Jammu and Kashmir']


    stateLatLong = [[11.059821,	78.387451],
                [17.123184,	79.208824],
                [23.473324,	77.947998],
                [29.238478,	76.431885],
                [21.295132,	81.828232],
                [19.601194,	75.552979],
                [23.745127,	91.746826],
                [15.317277,	75.713890],
                [10.850516,	76.271080],
                [28.207609,	79.826660],
                [26.244156,	92.537842],
                [22.978624,	87.747803],
                [22.309425,	72.136230],
                [20.940920,	84.803467],
                [27.391277,	73.432617],
                [32.084206,	77.571167],
                [11.7401, 92.6586],
                [15.9129, 79.7400],
                [25.0961, 85.3131],
                [30.7333, 76.7794],
                [28.7041, 77.1025],
                [15.2993, 74.1240],
                [34.152588, 77.577049],
                [24.6637, 93.9063],
                [23.1645, 92.9376],
                [31.1471, 75.3412], 
                [11.9416, 79.8083], [30.0668, 79.0193],[34.083656,74.797371]]
    
    latitude =[]
    longitude=[]
    staes = []

    for state in statesList:
        if state in statesListLat:
            index = statesListLat.index(state)
            latitude.append(stateLatLong[index][0])
            longitude.append(stateLatLong[index][1])
            staes.append(state)
    
    colors = []

    totalConfirmed = []
    


    for item in confirmedCasesIndia:
        val = 0
        index = confirmedCasesIndia.index(item)
        val = int(item)+int(confirmedCasesForegin[index])
        totalConfirmed.append(val)

    for item in totalConfirmed:
        if int(item) > 255:
            colors.append("rgb(255,0,0)")
            continue
        colors.append("rgb("+str(item)+",0,0)")
    
    print(staes)
    print(totalConfirmed)    

    return render_template("index.html",state = staes,confirm = totalConfirmed, lat = latitude,lang = longitude,colors = colors,len = len(confirmedCasesForegin))

# home()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # serve(app,listen = "*:"+port)
    app.run()