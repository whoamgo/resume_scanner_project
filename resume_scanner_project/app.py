from flask import Flask, render_template, request
import os
import docx2txt
import re

app = Flask(__name__)
UPLOAD_FOLDER = 'resumes'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define a basic skill set
SKILLS = [
    'python', 'java', 'c++', 'javascript', 'html', 'css',
    'flask', 'django', 'sql', 'mysql', 'mongodb',
    'excel', 'machine learning', 'data analysis', 'deep learning',
    'git', 'github', 'linux', 'communication', 'teamwork'
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan_resume():
    file = request.files['resume']
    if file and file.filename.endswith('.docx'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        text = docx2txt.process(filepath).lower()

        found_skills = [skill for skill in SKILLS if re.search(r'\b' + re.escape(skill) + r'\b', text)]
        missing_skills = [skill for skill in SKILLS if skill not in found_skills]

        return render_template('result.html', found=found_skills, missing=missing_skills)
    return "Invalid file format. Only .docx allowed."

if __name__ == '__main__':
    app.run(debug=True)
