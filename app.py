from flask import Flask, render_template, request

import pandas as pd
import numpy as np
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

application = Flask(__name__)
app = application

# Route for home page
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predictdata', methods=['GET','POST'])
def predict_depost():
    if request.method =='GET':
        return render_template('home.html')
    else:
        data = CustomData(
            age = request.form.get('age'),
            job = request.form.get('job'),
            marital = request.form.get('marital'),
            education = request.form.get('education'),
            default = request.form.get('default'),
            balance = request.form.get('balance'),
            housing = request.form.get('housing'),
            loan = request.form.get('loan'),
            contact = request.form.get('contact'),
            day = request.form.get('day'),
            month = request.form.get('month'),
            duration = request.form.get('duration'),
            campaign = request.form.get('campaign'),
            pdays = request.form.get('pdays'),
            previous = request.form.get('previous'),
            poutcome = request.form.get('poutcome')
        )

        pred_df = data.get_data_as_dataframe()
        print(pred_df)

        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)

        result = results[0]

        if result ==0.0:
            result='Less chance for collecting term deposit'

        else:
            result = 'High chance for collecting term deposit'

        return render_template('home.html', results=result)
    

if __name__ =="__main__":
    app.run(host='0.0.0.0')
