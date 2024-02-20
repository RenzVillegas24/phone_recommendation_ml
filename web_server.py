from flask import Flask, render_template, request, jsonify
import json
import utils as ut
import pandas as pd

pp = pd.read_csv('clean_phone_data_final.csv')
app = Flask(__name__, template_folder='template')

# Almacena los datos recibidos del ESP32
data = {'gasto': [], 'presion': [], 'vibracion': []}


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/get-phone', methods=['POST'])
def get_data():
    event_dict = request.get_json()
    top_n = event_dict.get('top_n', 10)

    # remove the values with any
    event_dict = {k: v for k, v in event_dict.items() if v.lower() != 'any'}

    # remove top_n from event_dict
    event_dict.pop('top_n', None)

    # add log here
    print(event_dict)
    import phone_recomend as pr

    response = jsonify({"phones" : pr.get_top_recommendation(**event_dict)})
    return response


@app.route('/get-top', methods=['POST'])
def receive_data():
    message_dict = {}

    try:
        event_dict = request.get_json()
        top_n = event_dict.get('top_n', 20)

        if event_dict.get('type', None) == 'all':        
            message_dict['type'] = 'return-all'

            message_dict['top'] = {col: '\n'.join(['Any'] + list(ut.get_top_words(pp[col].astype(str).to_list(), 20).keys())) for col in pp.columns}
        else:
            message_dict['type'] = 'return-top'
            col = event_dict.get('type', None).split('-')[-1]

            message_dict['top'] = '\n'.join(['Any'] + list(ut.get_top_words(pp[col].astype(str).to_list(), 20).keys()))

        message_dict['status'] = 'success'  

        return jsonify(message_dict)
    except Exception as e:
        print(f"Error receiving data: {str(e)}")

        return jsonify({'success': False, 'error': str(e)})




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
