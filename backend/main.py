import flask
from flask import jsonify
import torch
import pandas as pd
import numpy as np
from model import Net

MODEL_PATH = './trained_model.pth'

app = flask.Flask("__main__")

@app.route('/')
def my_index() :
    return flask.render_template('index.html', token='Hello Flask+React')


def full_history():
    data = pd.read_csv('crime_data.csv')
    data['Offense Start DateTime'] = pd.to_datetime(data['Offense Start DateTime'])
    unfiltered = data[['Offense Start DateTime', 'Latitude', 'Longitude']].dropna()
    mask = (unfiltered['Latitude'] != 0.) & (unfiltered['Longitude'] != 0.)
    data = unfiltered[mask]
    labels = data[['Latitude', 'Longitude']].to_numpy()
    return labels

def predict(month, day, hour):
    input = np.array([month, day, hour, 0])
    device = torch.device("cpu")

    model = Net()
    model = model.to(device)
    model.load_state_dict(torch.load(MODEL_PATH, map_location='cpu'))
    model.eval()

    minute_log = np.ndarray((60, 2))
    with torch.no_grad():
        for i in range(0, 60):
            input[-1] = i
            data = torch.from_numpy(input)
            data = data.float().to(device)
            prediction = model(data)
            minute_log[i] = prediction.cpu().numpy()
    minute_log[:, 0] += 47.6
    minute_log[:, 1] -= 122.3
    np.savetxt('minute.txt', minute_log)
    return minute_log

@app.route('/crime')
def crimeMinute():
    # input = [month, day, hour, minute]
    input = np.array([12, 10, 1, 0])

    device = torch.device("cpu")

    model = Net()

    model = model.to(device)
    model.load_state_dict(torch.load(MODEL_PATH, map_location='cpu'))
    model.eval()

    minute_log = np.ndarray((60,2))
    minute_list = []
    with torch.no_grad():
        for i in range(0, 60):
            input[-1] = i
            data = torch.from_numpy(input)
            data = data.float().to(device)
            prediction = model(data)
            minute_log[i] = prediction.cpu().numpy()
    minute_log[:, 0] += 47.6
    minute_log[:, 1] -= 122.3

    for i in range(0, 60):
        minute_list.append({'lat' : minute_log[i, 0], 'long' : minute_log[i,1]})
    # np.save('minute.npy', minute_log)
    # np.savetxt('minute.txt', minute_log)
    return jsonify({'list':minute_list})

    # return jsonify({'crimes': minute_log})
    # output should be similar to: 47.6, -122.3

app.run(debug=True)