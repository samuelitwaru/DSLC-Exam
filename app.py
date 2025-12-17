import flask
import pandas as pd
from joblib import load

with open('random_forest_model.joblib', 'rb') as f:
    model = load(f)

# Initialize the Flask application
app = flask.Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        form_fields = [
            {"type": 'select', "name": 'Gender', "options": [{"value": "0", "label": "Male"}, {"value": "1", "label": "Female"}], "label": 'Gender', "value": "1"},
            {"type": 'select', "name": 'Married', "options": [{"value": "0", "label": "No"}, {"value": "1", "label": "Yes"}], "label": 'Maried', "value": "0"},
            {"type": 'select', "name": 'Dependents', "options": [{"value": "0", "label": "0"}, {"value": "1", "label": "1"}, {"value": "2", "label": "2"}, {"value": "3", "label": "3+"}], "label": 'Dependants'},
            {"type": 'select', "name": 'Education', "options": [{"value": "0", "label": "Not Graduate"}, {"value": "1", "label": "Graduate"}], "label": 'Education'},
            {"type": 'select', "name": 'Self_Employed', "options": [{"value": "0", "label": "No"}, {"value": "1", "label": "Yes"}], "label": 'Self Employed'},
            {"type": 'number', "name": 'Applicant_Income',  "label": 'Applicant Income', "value": "5000"},
            {"type": 'number', "name": 'Coapplicant_Income',  "label": 'Coapplicant Income', "value": "2000"},
            {"type": 'number', "name": 'Loan_Amount',  "label": 'Loan Amount', "value": "150"},
            {"type": 'number', "name": 'Term',  "label": 'Loan Term (in days)', "value": "360"},
            {"type": 'select', "name": 'Credit_History', "options": [{"value": "0", "label": "No"}, {"value": "1", "label": "Yes"}], "label": 'Credit History', "value": "1"},
            {"type": 'select', "name": 'Area',  "options": [{"value": "0", "label": "Rural"}, {"value": "1", "label": "Semiurban"}, {"value": "2", "label": "Urban"}],  "label": 'Area', "value": "1"},
        ]
        return(flask.render_template('main.html', form_fields=form_fields))

    if flask.request.method == 'POST':
        # Get the input values from the form
        input_features = [float(x) for x in flask.request.form.values()]
        print('inputs: ', input_features)
        features_value = [input_features]
        features_name = [
            'Gender', 'Married', 'Dependents', 'Education', 'Self_Employed',
            'Applicant_Income', 'Coapplicant_Income', 'Loan_Amount', 'Term',
            'Credit_History', 'Area'
        ]
        df = pd.DataFrame(features_value, columns=features_name)
        
        # Make prediction using the loaded model
        prediction = model.predict(df)
        output = prediction[0]

        return flask.render_template('main.html', original_input=features_value, result=output)
    
if __name__ == '__main__':
    app.run(debug=True)