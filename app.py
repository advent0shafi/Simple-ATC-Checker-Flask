from flask import Flask, request, render_template, jsonify
import os
import docx
import PyPDF2
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    return '\n'.join([paragraph.text for paragraph in doc.paragraphs])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'resume' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['resume']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        keywords = request.form.get('keywords').split(',')

        if filename.rsplit('.', 1)[1].lower() == 'pdf':
            resume_text = extract_text_from_pdf(file_path)
        elif filename.rsplit('.', 1)[1].lower() in {'doc', 'docx'}:
            resume_text = extract_text_from_docx(file_path)
        else:
            return jsonify({"error": "Unsupported file format"}), 400

        filtered_results = [line for line in resume_text.split('\n') if any(keyword.strip().lower() in line.lower() for keyword in keywords)]

        return jsonify({"filtered_results": filtered_results}), 200

    return jsonify({"error": "File not allowed"}), 400

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
