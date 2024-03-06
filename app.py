from flask import Flask, render_template, request, redirect, Response, session
from weather import *
import socket, boto3
from datetime import datetime
import logging


app = Flask(__name__)
app.secret_key = 'gjygffj77fjhj@ujyg'


app.logger.setLevel(logging.INFO)  # Set log level to INFO
handler = logging.FileHandler('app.log')  
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')  # Define log message format
handler.setFormatter(formatter)  # Set formatter for the handler
app.logger.addHandler(handler)



@app.route('/', methods=['POST', 'GET'])
def results():
    if request.method == 'GET':
        return render_template('index.html', method='get', container=socket.gethostname())

    if request.method == 'POST':
        input_location = request.form.get("place")
        location_data = get_lat_lon(input_location)
        FullPlace = location_data[2]
        
        form_data = get_forecast(location_data)
        session['forecast'] = form_data
        session['address'] = FullPlace
        global city
        city = FullPlace.split(",")[0]
        if form_data == "error":
            app.logger.warning('Unknown place')
            return render_template('index.html', method='not found', container=socket.gethostname())
        current_temp = get_current_temp(location_data)
        app.logger.info(f"Searched City: {FullPlace}")
        return render_template('index.html', form_data=form_data, FullPlace=FullPlace, method='post',current_temp=current_temp, container=socket.gethostname(), lat=location_data[0],lon=location_data[1])


@app.route('/download_image')
def download_image():
    s3_client = boto3.client('s3')
    obj = s3_client.get_object(Bucket="staticwebsiteapp", Key="sky.jpg")
    app.logger.info('Downloaded sky')
    return Response(obj["Body"].read(), mimetype='Content-Type',
                    headers={'Content-Disposition': 'attachment; filename=sky.jpg'})


@app.route('/save_to_dynamo')
def create_backup():
    for key, value in session['forecast'].items():
        session['forecast'][key] = str(value)

    dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
    table = dynamodb.Table('backup_weather')
    backup_date = datetime.now().isoformat()

    table.put_item(
        Item={"city": session['address'], "backup_date": backup_date, "Sunday": session['forecast']["Sunday"],
              "Monday": session['forecast']["Monday"], "Tuesday": session['forecast']["Tuesday"],
              "Wednesday": session['forecast']["Wednesday"], "Thursday": session['forecast']["Thursday"],
              "Friday": session['forecast']["Friday"], "Saturday": session['forecast']["Saturday"]})
    app.logger.info('saved to dynamo')
    return redirect('/') 


@app.route('/auto_backup')
def create_auto_backup():
    city = 'Tel Aviv'
    forecast = get_forecast(get_lat_lon(city))
    for key, value in forecast.items():
        forecast[key] = str(value)
    dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
    table = dynamodb.Table('backup_weather')
    backup_date = datetime.now().isoformat()
    table.put_item(Item={"city": city, "backup_date": backup_date, "Sunday": forecast["Sunday"],
                         "Monday": forecast["Monday"], "Tuesday": forecast["Tuesday"],
                         "Wednesday": forecast["Wednesday"], "Thursday": forecast["Thursday"],
                         "Friday": forecast["Friday"], "Saturday": forecast["Saturday"]})
    return redirect('/')

if __name__ == "__main__":
    app.run()
