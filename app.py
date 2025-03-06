from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')

@app.route('/')
def home():
    return render_template('index.html', now=datetime.now())

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Create email content
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = os.getenv('EMAIL_USER')
        msg['Subject'] = f'Portfolio Contact from {name}'
        
        body = f"""
        Name: {name}
        Email: {email}
        
        Message:
        {message}
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASSWORD'))
                server.send_message(msg)
            flash('Message sent successfully!', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            flash('Failed to send message. Please try again later.', 'error')
            return redirect(url_for('home'))
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
