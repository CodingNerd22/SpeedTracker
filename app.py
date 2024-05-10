from flask import Flask, request, render_template
import folium
import webbrowser

app = Flask(__name__)

acceleration = 90

india = (28.226970,85.360079,7.780659,71.958998,"India",100)
maha = (21.502134,80.420399,15.335041,73.129429,"Maharashtra",80)
pune = (18.810898,74.272216,18.146635,73.406465,"Pune_District",60)
pune_city=[(18.464027,73.890073,18.450187,73.879436,"Kondhwa_bdk",40),
           (18.460659,73.885614,18.456763,73.883309,"VIIT_Campus",20),
           (18.459998,73.885293,18.459764,73.884178,"Campus_Road",20)]

NH48 = [ (18.449246,73.842189,18.440294,73.834266,"Narhe_M-S_highway",40),
        (18.440376,73.842802,18.430466,73.833757,"Jambhulwadi_lake",40),
         (18.430197,73.849096,18.412526,73.841712,"Jambhulwadi_lake_to_Katraj_T",50),
         (18.412803,73.853863,18.394479,73.846957,"Katraj_T",50),
         (18.394398,73.861455,18.378352,73.849226,"Katraj_T_-_Katraj_G",40),
         (18.430673,73.840756,18.348872,73.843860,"Shindevadi",40),
         (18.348595,73.860399,18.326125,73.846842,"KhedSivapur_Toll",60),
         (18.325783,73.883729,18.301240,73.850087,"Shivare",80),
         (18.300669,73.881781,18.268657,73.863955,"M_B_Highway",60),
         (18.268494,73.906023,18.236525,73.877602,"Nasrapur",80),
         (18.235857,73.944403,18.203898,73.906513,"Dhangwadi",80),
         (18.202316,73.976654,18.174788,73.939502,"Urmad_River_Bridge",60),
         (18.174706,73.962408,18.157955,73.949662,"NH965DD_Junction",40)]

def indiaplt(india, point) :
    output = []
    if (point[0] > india[2] and point[0] < india[0] and point[1] > india[3] and point[1] < india[1]):
        output.append(f"{india[4]} --> Speed limit is {india[5]}")
        limit=india[5]
        if (limit<=acceleration):
            output.append("Please Slow Down")
        else:
            output.append("Safe Speed in India")
            output.extend(mahaplt(maha, point))
    else:
        output.append("Not in India")
    return output

def mahaplt(maha, point) :
    output = []
    if (point[0] > maha[2] and point[0] < maha[0] and point[1] > maha[3] and point[1] < maha[1]):
        output.append(f"{maha[4]} --> Speed limit is {maha[5]}")
        limit=maha[5]
        if (limit<=acceleration):
            output.append("Please Slow Down")
            output.extend(puneplt(pune, point))
        else:
            output.append("Safe Speed in Maharashtra")
            output.extend(puneplt(pune, point))
    else :
        output.append("Somewhere else from Maharashtra")
    return output

def puneplt(pune, point) :
    output = []
    if (point[0] > pune[2] and point[0] < pune[0] and point[1] > pune[3] and point[1] < pune[1]):
        output.append(f"{pune[4]} --> Speed limit is {pune[5]}") 
        limit=pune[5]
        if (limit<=acceleration):
            output.append("Please Slow Down")
            output.extend(punecityplt(pune_city, point))
            output.extend(nh48plt(NH48, point))
        else:
            output.append("Safe Speed in Pune")
            output.extend(punecityplt(pune_city, point))
            output.extend(nh48plt(NH48, point))
    else :
        output.append("Not in Pune")
    return output

def punecityplt(pune_city, point) :
    output = []
    for i in range(len(pune_city)):
        pune_city1 =pune_city[i]
        if (point[0] > pune_city1[2] and point[0] < pune_city1[0] and point[1] > pune_city1[3] and point[1] < pune_city1[1]) :
            output.append(f"{pune_city1[4]} --> Speed limit is {pune_city1[5]}")
            limit = pune_city1[5]
            if (limit <= acceleration):
                output.append("Please Slow Down")
            else:
                output.append("Safe Speed")
    return output

def nh48plt(NH48, point) :
    output = []
    for i in range(len(NH48)):
        nh48dat =NH48[i]
        if (point[0] > nh48dat[2] and point[0] < nh48dat[0] and point[1] > nh48dat[3] and point[1] < nh48dat[1]) :
            output.append(f"{nh48dat[4]} --> Speed limit is {nh48dat[5]}")
            limit = nh48dat[5]
            if (limit <= acceleration):
                output.append("Please Slow Down")
            else:
                output.append("Safe Speed")
    return output

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/coordinates', methods=['POST'])
def coordinates():
    data = request.json
    latitude = data['latitude']
    longitude = data['longitude']
    point = (latitude, longitude)
    output = indiaplt(india, point)
    return '<br>'.join(output)

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000/')
    app.run(debug=True)
