import pandas as pd
import numpy as np
import pickle
import socket
import json

ziggurat_host = '195.133.36.135'
ziggurat_port = 43000
ziggurat_username = 's2'
ziggurat_key = 'secret'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Connects to socket
def socket_connect():
    global s
    print('Connecting to socket.')
    try:
        s.shutdown(socket.SHUT_RDWR)
    except:
        pass

    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ziggurat_host, ziggurat_port))


# This function will send a length delimited message based on our custom protocol to Ziggurat
def socket_send(message):
    message_to_send = message + '\r\n'
    request = len(message_to_send).to_bytes(4, 'big') + bytes(message_to_send, 'utf-8')

    print('Sending:', request)
    try:
        sent = s.sendall(request)
        if sent == 0:
            raise RuntimeError("Error: Socket connection broken.")
    except:
        # Socket error, retry creating socket
        print('Socket error. Reconnecting.')
        socket_connect()


# This function will receive a length delimited message based on our custom protocol from Ziggurat
def socket_receive():
    if len(socket_receive_data) > 0:
        handle_receive(b'')

    while True:
        chunk = s.recv(1024)
        if chunk == b'':
            print("socket connection broken")
            socket_connect()
        handle_receive(chunk)


# Socket receive buffer
socket_receive_data = b''


def handle_receive(chunk):
    global socket_receive_data
    socket_receive_data += chunk

    while True:
        if len(socket_receive_data) < 4:
            return

        header_end = 4
        header_len = int.from_bytes(socket_receive_data[:header_end], "big")

        if header_len > len(socket_receive_data[header_end:]):
            # Data is not fully received
            return

        body = socket_receive_data[header_end:header_end + header_len]
        inspect_message(body)
        socket_receive_data = socket_receive_data[header_end + header_len:]


def inspect_message(message):
    print('New message arrived:')
    print(message)
    json_message = json.loads(message)
    if json_message['type'] == 'mladenOpenPositionPredictionRequest':
        on_mladen_open_position_prediction_request(json_message)


def on_mladen_open_position_prediction_request(json_message):
    """
    Please Enter the parameters according to the following format :
    ['open','high','low','close','P_Level Pivot 1H','S_Level_1 Pivot 1H','S_Level_2 Pivot 1H',
                                   'S_Level_3 Pivot 1H','S_Level_4 Pivot 1H','R_Level_1 Pivot 1H',
                                   'R_Level_2 Pivot 1H','R_Level_3 Pivot 1H','R_Level_4 Pivot 1H',
                                   'P_Level Pivot 1D','S_Level_1 Pivot 1D','S_Level_2 Pivot 1D',
                                   'S_Level_3 Pivot 1D','S_Level_4 Pivot 1D','R_Level_1 Pivot 1D',
                                   'R_Level_2 Pivot 1D','R_Level_3 Pivot 1D','R_Level_4 Pivot 1D',
                                   'P_Level Pivot 4H','S_Level_1 Pivot 4H','S_Level_2 Pivot 4H',
                                   'S_Level_3 Pivot 4H','S_Level_4 Pivot 4H','R_Level_1 Pivot 4H',
                                   'R_Level_2 Pivot 4H','R_Level_3 Pivot 4H','R_Level_4 Pivot 4H',
                                   'p 1d_prev','s1 1d_prev','s2 1d_prev','s3 1d_prev','s4 1d_prev',
                                   'r1 1d_prev','r2 1d_prev','r3 1d_prev','r4 1d_prev','p 4h_prev',
                                   's1 4h_prev','s2 4h_prev','s3 4h_prev','s4 4h_prev','r1 4h_prev',
                                   'r2 4h_prev','r3 4h_prev','r4 4h_prev','p 1h_prev','s1 1h_prev',
                                   's2 1h_prev','s3 1h_prev','s4 1h_prev','r1 1h_prev','r2 1h_prev',
                                   'r3 1h_prev','r4 1h_prev','buy','sell']
    """

    if json_message['side'] == 'sell':
        # Sell
        params = [json_message['open'], json_message['high'], json_message['low'], json_message['close'],
                  json_message['pivotH1'], json_message['s1H1'], json_message['s2H1'], json_message['s3H1'],
                  json_message['s4H1'], json_message['r1H1'], json_message['r2H1'], json_message['r3H1'],
                  json_message['r4H1'], json_message['pivotD1'], json_message['s1D1'], json_message['s2D1'],
                  json_message['s3D1'], json_message['s4D1'], json_message['r1D1'], json_message['r2D1'],
                  json_message['r3D1'], json_message['r4D1'], json_message['pivotH4'], json_message['s1H4'],
                  json_message['s2H4'], json_message['s3H4'], json_message['s4H4'], json_message['r1H4'],
                  json_message['r2H4'], json_message['r3H4'], json_message['r4H4'], json_message['prevPivotD1'],
                  json_message['prevS1D1'], json_message['prevS2D1'], json_message['prevS3D1'],
                  json_message['prevS4D1'], json_message['prevR1D1'], json_message['prevR2D1'],
                  json_message['prevR3D1'], json_message['prevR4D1'], json_message['prevPivotH4'],
                  json_message['prevS1H4'], json_message['prevS2H4'], json_message['prevS3H4'],
                  json_message['prevS4H4'], json_message['prevR1H4'], json_message['prevR2H4'],
                  json_message['prevR3H4'], json_message['prevR4H4'], json_message['prevPivotH1'],
                  json_message['prevS1H1'], json_message['prevS2H1'], json_message['prevS3H1'],
                  json_message['prevS4H1'], json_message['prevR1H1'], json_message['prevR2H1'],
                  json_message['prevR3H1'], json_message['prevR4H1'], 0, 1]
        print(params)

        # Load pretrained model and predict te result using it
        filename = 'finalized_model.sav'
        loaded_model = pickle.load(open(filename, 'rb'))
        predicted = prediction(params, loaded_model)
        print(predicted[0])
        # If prediction resulted true, we can send sell command
        if predicted[0] != 0:
            json_prediction_message = {
                "type": "mladenOpenPositionPredictionResponse",
                "clientSideId": json_message['clientSideId'],
                "predictionResult": predicted[0]
            }
            socket_send(json.dumps(json_prediction_message))

    elif json_message['side'] == 'buy':
        # Buy
        params = [json_message['open'], json_message['high'], json_message['low'], json_message['close'],
                  json_message['pivotH1'], json_message['s1H1'], json_message['s2H1'], json_message['s3H1'],
                  json_message['s4H1'], json_message['r1H1'], json_message['r2H1'], json_message['r3H1'],
                  json_message['r4H1'], json_message['pivotD1'], json_message['s1D1'], json_message['s2D1'],
                  json_message['s3D1'], json_message['s4D1'], json_message['r1D1'], json_message['r2D1'],
                  json_message['r3D1'], json_message['r4D1'], json_message['pivotH4'], json_message['s1H4'],
                  json_message['s2H4'], json_message['s3H4'], json_message['s4H4'], json_message['r1H4'],
                  json_message['r2H4'], json_message['r3H4'], json_message['r4H4'], json_message['prevPivotD1'],
                  json_message['prevS1D1'], json_message['prevS2D1'], json_message['prevS3D1'],
                  json_message['prevS4D1'], json_message['prevR1D1'], json_message['prevR2D1'],
                  json_message['prevR3D1'], json_message['prevR4D1'], json_message['prevPivotH4'],
                  json_message['prevS1H4'], json_message['prevS2H4'], json_message['prevS3H4'],
                  json_message['prevS4H4'], json_message['prevR1H4'], json_message['prevR2H4'],
                  json_message['prevR3H4'], json_message['prevR4H4'], json_message['prevPivotH1'],
                  json_message['prevS1H1'], json_message['prevS2H1'], json_message['prevS3H1'],
                  json_message['prevS4H1'], json_message['prevR1H1'], json_message['prevR2H1'],
                  json_message['prevR3H1'], json_message['prevR4H1'], 1, 0]

        # Load pretrained model and predict te result using it
        filename = 'finalized_model.sav'
        loaded_model = pickle.load(open(filename, 'rb'))
        predicted = prediction(params, loaded_model)
        print(predicted[0])
        # If prediction resulted true, we can send buy command
        if predicted[0] != 0:
            json_prediction_message = {
                "type": "mladenOpenPositionPredictionResponse",
                "clientSideId": json_message['clientSideId'],
                "predictionResult": predicted[0]
            }
            socket_send(json.dumps(json_prediction_message))
    else:
        print(f"open position prediction request received with invalid side: {json_message['side']}")


def prediction(params, model):
    df = pd.DataFrame(columns=['open', 'high', 'low', 'close',
                               'P_Level Pivot 1H', 'S_Level_1 Pivot 1H', 'S_Level_2 Pivot 1H',
                               'S_Level_3 Pivot 1H', 'S_Level_4 Pivot 1H', 'R_Level_1 Pivot 1H',
                               'R_Level_2 Pivot 1H', 'R_Level_3 Pivot 1H', 'R_Level_4 Pivot 1H',
                               'P_Level Pivot 1D', 'S_Level_1 Pivot 1D', 'S_Level_2 Pivot 1D',
                               'S_Level_3 Pivot 1D', 'S_Level_4 Pivot 1D', 'R_Level_1 Pivot 1D',
                               'R_Level_2 Pivot 1D', 'R_Level_3 Pivot 1D', 'R_Level_4 Pivot 1D',
                               'P_Level Pivot 4H', 'S_Level_1 Pivot 4H', 'S_Level_2 Pivot 4H',
                               'S_Level_3 Pivot 4H', 'S_Level_4 Pivot 4H', 'R_Level_1 Pivot 4H',
                               'R_Level_2 Pivot 4H', 'R_Level_3 Pivot 4H', 'R_Level_4 Pivot 4H',
                               'p 1d_prev', 's1 1d_prev', 's2 1d_prev', 's3 1d_prev', 's4 1d_prev',
                               'r1 1d_prev', 'r2 1d_prev', 'r3 1d_prev', 'r4 1d_prev', 'p 4h_prev',
                               's1 4h_prev', 's2 4h_prev', 's3 4h_prev', 's4 4h_prev', 'r1 4h_prev',
                               'r2 4h_prev', 'r3 4h_prev', 'r4 4h_prev', 'p 1h_prev', 's1 1h_prev',
                               's2 1h_prev', 's3 1h_prev', 's4 1h_prev', 'r1 1h_prev', 'r2 1h_prev',
                               'r3 1h_prev', 'r4 1h_prev', 'buy', 'sell'])
    df.loc[0] = params
    data = np.asarray(df)
    p = model.predict(data)
    return p


# Login to Ziggurat
json_login_message = {
    "type": "login",
    "name": ziggurat_username,
    "key": ziggurat_key,
}

socket_connect()

# Send login JSON data to socket server
socket_send(json.dumps(json_login_message))

while True:
    socket_receive()
