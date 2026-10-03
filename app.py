from flask import Flask, request, render_template
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

application=Flask(__name__)

app=application

## Route for a home page

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/predictdata',methods=['GET','POST'])
def predict_datapoint():
    if request.method=='GET':
        return render_template('home.html')

    form_data = request.form
    reading_score = form_data.get('reading_score', '').strip()
    writing_score = form_data.get('writing_score', '').strip()

    if not reading_score or not writing_score:
        return render_template(
            'home.html',
            error='Enter both reading and writing scores to continue.',
            form_data=form_data
        )

    try:
        reading_score = float(reading_score)
        writing_score = float(writing_score)
    except ValueError:
        return render_template(
            'home.html',
            error='Scores must be numbers between 0 and 100.',
            form_data=form_data
        )

    if not 0 <= reading_score <= 100 or not 0 <= writing_score <= 100:
        return render_template(
            'home.html',
            error='Scores must be between 0 and 100.',
            form_data=form_data
        )

    try:
        data = CustomData(
            gender=form_data.get('gender'),
            race_ethnicity=form_data.get('ethnicity'),
            parental_level_of_education=form_data.get('parental_level_of_education'),
            lunch=form_data.get('lunch'),
            test_preparation_course=form_data.get('test_preparation_course'),
            reading_score=reading_score,
            writing_score=writing_score
        )

        pred_df = data.get_data_as_data_frame()
        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)
        return render_template('home.html', results=results[0])
    except Exception:
        app.logger.exception("Prediction request failed")
        return render_template(
            'home.html',
            error='We could not generate a prediction right now. Please check your inputs and try again.',
            form_data=form_data
        ), 500
    

if __name__=="__main__":
    app.run(host="0.0.0.0")        

