from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
from time import time
from datetime import datetime
from helper_functions import *

app = Flask(__name__)
app.secret_key = 'secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

class Database(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_type = db.Column(db.String())
    url_link = db.Column(db.String())
    doc_path = db.Column(db.String())
    created_data = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return 'Name %r>' % self.id

UPLOAD_FOLDER = 'static/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/database')
def database():
    histories = Database.query.order_by(Database.created_data)
    return render_template('database.html', histories=histories)

@app.route('/summarizer', methods=['POST', 'GET'])
def summarizer():
    original_text = 'Default Text Summarizer'
    summary_freq = 'Text Summarizer'
    summary_luhn = 'Text Summarizer'
    percentage = ''
    time_ = ''
    if request.method == 'POST':
        url_link = request.form.get('url_link')
        pdf_file = request.files['pdf_file']
        typed_file = request.form.get('typed_file')
        percent_val = request.form.get('percentage')

        if not percent_val:
            percentage = 0.1
        else:
            percentage = int(percent_val) / 100
        
        time_ = time()

        if pdf_file:
            filename = secure_filename(pdf_file.filename)

            if filename.endswith('.pdf'):
                pdf_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                path_pdf = 'static/upload/' + filename
                original_text = text_from_pdf(path_pdf)

                # add to the database
                new_data = Database(doc_path='path_pdf')
                try:
                    db.session.add(new_data)
                    db.session.commit()
                except:
                    return "Couldn't add path to database"
            
            elif filename.endswith('.png') or filename.endswith('.jpg'):
                pdf_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                path_pdf = 'static/upload/' + filename
                original_text = text_from_image(path_pdf)
            else:
                flash('Not accepted')
                return redirect(url_for('summarizer'))
            plot_wordcloud(original_text)
            summary_freq = summarize_by_freq(original_text, percentage)
            summary_luhn = summarize_by_luhn(original_text, percentage)
        
        """
        if url_link:
            try:
                original_text = text_from_url(url_link)
                plot_wordcloud(original_text)
                summary_freq = summarize_by_freq(original_text, percentage)
                summary_luhn = summarize_by_luhn(original_text, percentage)
            except:
                flash('Try again later, or enter a valid url-link')
                return redirect(url_for('summarizer'))

            if typed_file:
                original_text = typed_file
                plot_wordcloud(original_text)
                summary_freq = summarize_by_freq(original_text, percentage)
                summary_luhn = summarize_by_luhn(original_text, percentage)
                """

        return render_template('summarizer.html', original_text=original_text, summary_freq=summary_freq, summary_luhn=summary_luhn, time_=time_)

if __name__ == '__main__':
    app.run(debug=True)