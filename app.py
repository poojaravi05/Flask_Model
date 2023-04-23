from flask import Flask, render_template, request, make_response
import pickle
import numpy as np
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from selenium import webdriver
from io import BytesIO, StringIO

app = Flask(__name__)

styles = getSampleStyleSheet()

# Load the saved model
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get input data from the form
    brand = request.form['brand']
    model_name = request.form['model']
    year = int(request.form['year'])
    mileage = int(request.form['mileage'])
    
    # Convert input data to a 2-dimensional array
    input_data = np.array([[year, mileage]])
    
    # Make predictions using the loaded model
    predictions = model.predict(input_data)
    predicted_price = "${:,.2f}".format(predictions[0])  # Format the predicted price with '$' symbol
    
    return render_template('result.html', brand=brand, model=model_name, year=year, mileage=mileage, predicted_price=predicted_price)

@app.route('/generate_pdf', methods=['GET'])
def generate_pdf():
    # Capture screenshots of each step using Selenium
    # Replace the following lines with your own code to capture screenshots at different steps
    driver = webdriver.Chrome()  # Use appropriate webdriver for your browser
    driver.get('http://localhost:5000/')  # Replace with the URL of your web application
    screenshot1 = driver.get_screenshot_as_png()
    # Capture more screenshots as needed
    driver.quit()

    # Create a PDF document
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))

    # Add the screenshots to the PDF document
    elements = []
    # Convert the screenshots to image objects and add them to the elements list
    elements.append(Image(BytesIO(screenshot1), width=doc.width, height=doc.height*0.7))
    # Add more screenshots as needed
    
    # Add other relevant information to the PDF document
    elements.append(Paragraph('Name: Pooja Honneshwari Ravi', styles['Normal']))
    elements.append(Paragraph('Batch Code: LISUM20', styles['Normal']))
    elements.append(Paragraph('Submission Date: April 22, 2023', styles['Normal']))
    elements.append(Paragraph('Submitted to: GitHub', styles['Normal']))

    # Build the PDF document
    doc.build(elements)

    # Seek to the beginning of the buffer
    buffer.seek(0)

    # Create a response with the PDF as attachment
    response = make_response(buffer.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=deployment_steps.pdf'
    response.headers['Content-Type'] = 'application/pdf'

    return response

if __name__ == '__main__':
    app.run(debug=True)
