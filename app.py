from flask import Flask, render_template, request
import pytesseract
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    text = ""
    if request.method == 'POST':
        file = request.files['file']
        if not file:
            return 'No file uploaded', 400
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        text = convert_image_to_text(filepath)
        
        # Optional: remove the image after processing
        os.remove(filepath)

    return render_template('index.html', text=text)

def convert_image_to_text(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text

if __name__ == '__main__':
    app.run(debug=True)
