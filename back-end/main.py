from flask import Flask,request,jsonify,render_template
from flask_cors import CORS
import random
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import smtplib,ssl
import numpy as np
import mysql.connector
import joblib
import csv
import json
import os
from werkzeug.utils import secure_filename
import pandas as pd
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostClassifier, AdaBoostRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
# import requests
from sklearn.impute import SimpleImputer
import PyPDF2
import re

app=Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'myfiles'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="placement"
)

# create a mycursor object
mycursor = mydb.cursor()


#Define the list of required skills along with their required threshold values
required_skills = {
    "PYTHON": 5,
    "JAVA": 5,
    "DBMS": 5,
    "COMPUTER NETWORKS": 5,
    "MACHINE LEARNING": 5,
    "APTITUDE SKILLS": 5,
    "FULL STACK DEVELOPMENT": 5,
    "COMMUNICATION SKILLS": 5
}
def pdf_text_extractor(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)

        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    skills_text = extract_skills(text)
    return skills_text


def extract_skills(resume_text):
    # Use a regular expression to capture the skills section
    skills_match = re.search(r'TECHNICAL SKILLS([\s\S]+?)(?:\n\n|\n\n\n)', resume_text)

    if skills_match:
        return skills_match.group(1).strip()

    return "Skills section not found."
# Function to identify skill gaps for a student
def identify_skill_gaps(student):
    gaps = []
    for skill, threshold in required_skills.items():
        if student[skill] < threshold:
            gaps.append(skill)
    return gaps


def mail_send(otp,mail):
    try:
        s = smtplib.SMTP('smtp.office365.com', 587)
    except Exception as e:
        s = smtplib.SMTP_SSL('smtp.office365.com', 465)
    s.ehlo()
    s.starttls()
    s.login("abbijananee.20it@sonatech.ac.in", "Mother5abbi")
        
    msg = MIMEMultipart()
    msg['From']='abbijananee.20it@sonatech.ac.in'
    msg['To']=mail
    msg['Subject']="Registration Confirmation"

    html=f'''\
        <!DOCTYPE html>
<html>

<head>
    <title></title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <style type="text/css">
        body,
        table,
        td,
        a {"-webkit-text-size-adjust: 100%;-ms-text-size-adjust: 100%;"}
        table,td {"mso-table-lspace: 0pt;mso-table-rspace: 0pt;"}
        img {"-ms-interpolation-mode: bicubic;"}
        /* RESET STYLES */
        img {"border: 0;height: auto;line-height: 100%;outline: none;text-decoration: none;"}

        table {"border-collapse: collapse !important;"}

        body {"height: 100% !important;margin: 0 !important;padding: 0 !important;width: 100% !important;"}

        /* iOS BLUE LINKS */
        a[x-apple-data-detectors] {"color: inherit !important;text-decoration: none !important;font-size: inherit !important;font-family: inherit !important;font-weight: inherit !important;line-height: inherit !important;"}

        /* MOBILE STYLES */
        /* ANDROID CENTER FIX */
        div[style*="margin: 16px 0;"] {"margin: 0 !important;"}
    </style>
</head>

<body style="background-color: #f4f4f4; margin: 0 !important; padding: 0 !important;">
    <!-- HIDDEN PREHEADER TEXT -->
    <div style="display: none; font-size: 1px; color: #fefefe; line-height: 1px; font-family: 'Lato', Helvetica, Arial, sans-serif; max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden;"> Here is your One Time Password
    </div>
    <table border="0" cellpadding="0" cellspacing="0" width="100%">
        <!-- LOGO -->
        
        <tr>
            <td bgcolor="#bf1591" align="center" style="padding: 60px 10px 0px 10px; background-color: linear-gradient(135deg, #f26ace 10%, #bf1591 100%)">
                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">
                    <tr>
                        <td bgcolor="#ffffff" align="center" valign="top" style="padding: 40px 20px 20px 20px; border-radius: 4px 4px 0px 0px; color: #111111; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 48px; font-weight: 400; letter-spacing: 4px; line-height: 48px;">
                            <h1 style="font-size: 48px; font-weight: 400; margin: 2;">Hey there!</h1> <img src="https://i.ibb.co/G0t2czh/logo.jpg" width="125" height="120" srcset="" style="display: block; border: 0px;" alt="Logo" />
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td bgcolor="#f4f4f4" align="center" style="padding: 0px 10px 20px 10px;">
                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">
                    <tr>
                        <td bgcolor="#ffffff" align="left" style="padding: 20px 30px 10px 30px; color: #666666; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px;">
                            <h3 style="margin: 0; " align="center">Here is your One Time Password</h3>
                        </td>
                    </tr>
					<tr>
                        <td bgcolor="#ffffff" align="left" style=" color: #666666; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px;">
                            <p style="margin: 0; " align="center">to validate your email address</p>
                        </td>
                    </tr>
					
                    <tr>
                        <td bgcolor="#ffffff" align="left">
                            <table width="100%" border="0" cellspacing="0" cellpadding="0">
                                <tr>
                                    <td bgcolor="#ffffff" align="center" style="padding: 0px 5px 0px 20px;">
                                        <table border="0" cellspacing="0" cellpadding="0">
                                            <tr>
                                                <td align="center" style="border-radius: 3px; " ><h1 style="font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 70px; letter-spacing: 15px;">{otp}</h1></td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr> <!-- COPY -->
                    <tr>
                        <td bgcolor="#ffffff" align="left" style=" color: #666666; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px; padding-bottom: 20px;">
                            <p style="margin: 0; color: #ff4d4d;" align="center" >Valid for 5 minutes only</p>
                        </td>
                    </tr>
                    <tr>
                        <td bgcolor="#ffffff" align="left" style="padding: 0px 30px 20px 30px; color: #666666; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px;">
                            <p style="margin: 0;" align="center">If you didn't request this , you can ignore this email.</p>
                        </td>
                    </tr>
                    <tr>
                        <td bgcolor="#ffffff" align="left" style="padding: 0px 30px 40px 30px; border-radius: 0px 0px 4px 4px; color: #666666; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px;">
                            <p style="margin: 0; "align="center">Thanks!<br>CB Team</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        
    </table>
</body>
</html>
        
        '''
    msg.attach(MIMEText(html, 'html'))
    
    s.send_message(msg)
    return "Success"

def otp_gen():
    digit="0123456789"
    password=""
    i=0
    for i in range(6):
        password=password+random.choice(digit)
        i+1
    print("Your password is "+str(password))
    file1 = open("myfile.txt","w")
    file1.write(password)
    file1.close()
    return password

@app.route('/register',methods=["POST"])
def register():
    mail=request.json['umail']
    pwd=request.json['upwd']
    opt=otp_gen()
    mm=mail_send(opt, mail)
    sql = "INSERT INTO login_table (user_mail,user_password) VALUES (%s, %s)"
    values = (mail, pwd)
    mycursor.execute(sql, values)
    mydb.commit()
    
    return jsonify(opt)

@app.route('/sregister',methods=["POST"])
def sregister():
    mail=request.json['umail']
    pwd=request.json['upwd']
    opt=otp_gen()
    mm=mail_send(opt, mail)
    sql = "INSERT INTO login_table (user_mail,user_password) VALUES (%s, %s)"
    values = (mail, pwd)
    mycursor.execute(sql, values)
    mydb.commit()
    
    return jsonify(opt)

@app.route('/otp',methods=["GET"])
def otp():
    file1 = open("myfile.txt","r+")
    myotp=file1.read()
    return jsonify(myotp)

@app.route('/student_data',methods=["GET"])
def data():
    sql = "SELECT * FROM student_data"
    mycursor.execute(sql)
    result = mycursor.fetchall()  
    if result:
        data = [dict(zip([key[0] for key in mycursor.description], row)) for row in result]
        return jsonify(data)
    else:
        return jsonify('Not')
    
@app.route('/login',methods=["POST"])
def login():
    mail=request.json['umail']
    pwd=request.json['upwd']
    sql = "SELECT * FROM login_table WHERE user_mail = %s AND user_password = %s"
    values = (mail, pwd)
    mycursor.execute(sql, values)
    result = mycursor.fetchone()
    if result:
        return jsonify('Success')
    else:
        return jsonify('Not')

@app.route('/upload_students', methods=['POST'])
def upload_students():
    # Get the uploaded CSV file
    csv_file = request.files['file']

    if not csv_file:
        return jsonify({'error': 'No file provided'}), 400

    if not csv_file.filename.endswith('.csv'):
        return jsonify({'error': 'Invalid file format. Please upload a CSV file'}), 400
    
    filename = secure_filename(csv_file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    csv_file.save(file_path)
 
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        columns_to_fill = ['ACADEMICS', 'MOCK INTERVIEW', 'PYTHON', 'JAVA', 'DBMS', 'COMPUTER NETWORKS',
                            'MACHINE LEARNING', 'APTITUDE SKILLS', 'FULL STACK DEVELOPMENT',
                            'NUMBER OF CERTIFICATIONS', 'NUMBER OF PROJECTS']

        numeric_columns = df.select_dtypes(include=[np.number]).columns

        for column in columns_to_fill:
            zero_rows = df[df[column] == 0]

            if not zero_rows.empty:
                train_data = df[df[column] != 0]
                y = train_data[column]
                X = train_data[numeric_columns]

                imputer = SimpleImputer(strategy='mean')
                X[numeric_columns] = imputer.fit_transform(X)

                model = AdaBoostRegressor()
                model.fit(X, y)

                prediction_features = zero_rows[numeric_columns]
                prediction_features[numeric_columns] = imputer.transform(prediction_features)

                predicted_values = model.predict(prediction_features)
                df.loc[df[column] == 0, column] = predicted_values


    selected_features = df[['PYTHON', 'JAVA', 'DBMS', 'COMPUTER NETWORKS', 'MACHINE LEARNING', 'APTITUDE SKILLS', 'FULL STACK DEVELOPMENT', 'COMMUNICATION SKILLS']]

    target_variable = df['SKILLS']

    X_train, X_test, y_train, y_test = train_test_split(selected_features, target_variable, test_size=0.2, random_state=42)

    base_classifier = DecisionTreeClassifier(max_depth=1)

    adaboost_classifier = AdaBoostClassifier(base_classifier, n_estimators=50, random_state=42)


    adaboost_classifier.fit(X_train, y_train)

    y_pred = adaboost_classifier.predict(X_test)
    y_pred_probabilities = adaboost_classifier.predict_proba(selected_features)
    threshold = 0.5
    df['STATUS'] = ['Yes' if score[1] > threshold else 'No' for score in y_pred_probabilities]
        
    df['REMARKS'] = ""

    for index, row in df.iterrows():
        student_name = row['NAMES']
        gaps = identify_skill_gaps(row)
        if df.at[index, 'STATUS'] == 'Yes':
            df.at[index, 'REMARKS'] = "Well-prepared"
        else:
            if not gaps:
                df.at[index, 'REMARKS'] = "Well-prepared"
                df.at[index, 'STATUS'] = "Yes"
            else:
                missing_skills = ', '.join(gaps)
                df.at[index, 'REMARKS'] = f"Missing skills: {missing_skills}"


    df.to_csv('./myfiles/updated.csv', index=False)

    with open('./myfiles/updated.csv', 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
           
            sql_check = "SELECT NAMES FROM student_data WHERE NAMES = %s"
            values_check = (row['NAMES'],)
            mycursor.execute(sql_check, values_check)
            result_check = mycursor.fetchone()

            if result_check:
               
                sql_update = """
                UPDATE student_data
                SET ACADEMICS = %s, `MOCK INTERVIEW` = %s, PYTHON = %s, JAVA = %s,
                    DBMS = %s, `COMPUTER NETWORKS` = %s, `MACHINE LEARNING` = %s,
                    `APTITUDE SKILLS` = %s, `FULL STACK DEVELOPMENT` = %s,
                    `COMMUNICATION SKILLS` = %s, INTERNSHIPS = %s,
                    `NUMBER OF CERTIFICATIONS` = %s, `CERTIFICATIONS DOMAIN` = %s,
                    `NUMBER OF PROJECTS` = %s, `PROJECT DOMAIN` = %s, SKILLS = %s,
                    STATUS = %s, REMARKS = %s
                WHERE NAMES = %s
                """
                values_update = (row['ACADEMICS'], row['MOCK INTERVIEW'], row['PYTHON'],
                                row['JAVA'], row['DBMS'], row['COMPUTER NETWORKS'],
                                row['MACHINE LEARNING'], row['APTITUDE SKILLS'],
                                row['FULL STACK DEVELOPMENT'], row['COMMUNICATION SKILLS'],
                                row['INTERNSHIPS'], row['NUMBER OF CERTIFICATIONS'],
                                row['CERTIFICATIONS DOMAIN'], row['NUMBER OF PROJECTS'],
                                row['PROJECT DOMAIN'], row['SKILLS'], row['STATUS'],
                                row['REMARKS'], row['NAMES'])
                mycursor.execute(sql_update, values_update)
            else:
            
                sql_insert = """
                INSERT INTO student_data (NAMES, ACADEMICS, `MOCK INTERVIEW`, PYTHON,
                    JAVA, DBMS, `COMPUTER NETWORKS`, `MACHINE LEARNING`, `APTITUDE SKILLS`,
                    `FULL STACK DEVELOPMENT`, `COMMUNICATION SKILLS`, INTERNSHIPS,
                    `NUMBER OF CERTIFICATIONS`, `CERTIFICATIONS DOMAIN`, `NUMBER OF PROJECTS`,
                    `PROJECT DOMAIN`, SKILLS, STATUS, REMARKS)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values_insert = (row['NAMES'], row['ACADEMICS'], row['MOCK INTERVIEW'], row['PYTHON'],
                                row['JAVA'], row['DBMS'], row['COMPUTER NETWORKS'],
                                row['MACHINE LEARNING'], row['APTITUDE SKILLS'],
                                row['FULL STACK DEVELOPMENT'], row['COMMUNICATION SKILLS'],
                                row['INTERNSHIPS'], row['NUMBER OF CERTIFICATIONS'],
                                row['CERTIFICATIONS DOMAIN'], row['NUMBER OF PROJECTS'],
                                row['PROJECT DOMAIN'], row['SKILLS'], row['STATUS'], row['REMARKS'])
                mycursor.execute(sql_insert, values_insert)

                mydb.commit()


        return jsonify({'message': 'Student data uploaded successfully'}), 200
    return jsonify({'message': 'Student data uploaded successfully'}), 200
    
@app.route('/delete_student',methods=['POST'])
def delete_student():
    mail=request.json['id']
   
    sql = "DELETE FROM student_data WHERE id= %s"
    values = (mail,)
    print(mail)
    mycursor.execute(sql, values)
    return jsonify('Success')

@app.route('/resume', methods=['POST'])
def resume():
    csv_file = request.files['file']

    if not csv_file:
        return jsonify({'error': 'No file provided'}), 400

    if not csv_file.filename.endswith('.pdf'):
        return jsonify({'error': 'Invalid file format. Please upload a PDF file'}), 400
    
    filename = secure_filename(csv_file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    csv_file.save(file_path)
    extracted_text = pdf_text_extractor(file_path)
    return jsonify(extracted_text)


@app.route('/get_clusters', methods=['GET'])
def get_clusters():
    df = pd.read_csv("C:\\Users\\exam01\\Downloads\\data\\place.csv")

    features = df[['ACADEMICS', 'MOCK INTERVIEW', 'PYTHON', 'JAVA', 'DBMS', 'COMPUTER NETWORKS', 'MACHINE LEARNING', 'APTITUDE SKILLS', 'FULL STACK DEVELOPMENT', 'COMMUNICATION SKILLS', 'INTERNSHIPS', 'NUMBER OF CERTIFICATIONS', 'NUMBER OF PROJECTS']]

    le = LabelEncoder()

    for col in features.columns:
        if features[col].dtype == 'object':
            features[col] = le.fit_transform(features[col])

    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    k = 3
    kmeans = KMeans(n_clusters=k, random_state=42)
    df['CLUSTER'] = kmeans.fit_predict(features_scaled)

    df['SALARY'] = np.random.choice([300000, 500000, 700000], size=len(df))

   
    result = df[['NAMES', 'SALARY', 'CLUSTER']].to_dict(orient='records')

    return jsonify(result)



@app.route('/api/get_data', methods=['GET'])
def get_data():
    return jsonify(data.to_dict(orient='records'))

@app.route('/api/calculate_salary', methods=['POST'])
def calculate_salary():
    
    req_data = request.get_json()
    x = np.array([req_data['PYTHON'], req_data['JAVA'], req_data['DBMS'], req_data['COMPUTER NETWORKS'], req_data['MACHINE LEARNING'], req_data['APTITUDE SKILLS'], req_data['FULL STACK DEVELOPMENT'], req_data['COMMUNICATION SKILLS']])

    total_score = np.sum(x)
    assigned_salary = 300000 if total_score < 50 else (500000 if total_score > 60 else 700000)

    return jsonify({'assigned_salary': assigned_salary})
df = pd.read_csv('C:\\Users\\exam01\\Downloads\\data\\place.csv')
features = df[['ACADEMICS', 'MOCK INTERVIEW', 'PYTHON', 'JAVA', 'DBMS', 'COMPUTER NETWORKS', 'MACHINE LEARNING', 'APTITUDE SKILLS', 'FULL STACK DEVELOPMENT', 'COMMUNICATION SKILLS', 'INTERNSHIPS', 'NUMBER OF CERTIFICATIONS', 'NUMBER OF PROJECTS']]

le = LabelEncoder()

for col in features.columns:
    if features[col].dtype == 'object':
        features[col] = le.fit_transform(features[col])

scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# KMeans clustering
k = 3
kmeans = KMeans(n_clusters=k, random_state=42)

# Add a 'Cluster' column to the DataFrame
df['Cluster'] = kmeans.fit_predict(features_scaled)

# Define the conditions for Python, Java, etc. skills
python_skill_condition = 5
java_skill_condition = 5
dbms_skill_condition = 5
computer_networks_condition = 5
machine_learning_condition = 5
full_stack_condition = 5

@app.route('/')
def index():
    return render_template('index.html', clusters=df['Cluster'].unique())

@app.route('/cluster/<int:cluster_id>')
def get_cluster(cluster_id):
    cluster_data = df[df['Cluster'] == cluster_id]
    return render_template('cluster.html', cluster_data=cluster_data)

@app.route('/filtered_names', methods=['POST'])
def filtered_names():
    # Get user input from the form
    python_skill_condition = int(request.form['python_skill'])
    java_skill_condition = int(request.form['java_skill'])
    dbms_skill_condition = int(request.form['dbms_skill'])
    computer_networks_condition = int(request.form['computer_networks_skill'])
    machine_learning_condition = int(request.form['machine_learning_skill'])
    full_stack_condition = int(request.form['full_stack_skill'])

    # Filter names based on user input
    filtered_names_python = [row['NAMES'] for index, row in df.iterrows() if isinstance(row['PYTHON'], (int, float)) and int(row['PYTHON']) > python_skill_condition]
    filtered_names_java = [row['NAMES'] for index, row in df.iterrows() if isinstance(row['JAVA'], (int, float)) and int(row['JAVA']) > java_skill_condition]
    filtered_names_dbms = [row['NAMES'] for index, row in df.iterrows() if isinstance(row['DBMS'], (int, float)) and int(row['DBMS']) > dbms_skill_condition]
    filtered_names_computer = [row['NAMES'] for index, row in df.iterrows() if isinstance(row['COMPUTER NETWORKS'], (int, float)) and int(row['COMPUTER NETWORKS']) > computer_networks_condition]
    filtered_names_machine = [row['NAMES'] for index, row in df.iterrows() if isinstance(row['MACHINE LEARNING'], (int, float)) and int(row['MACHINE LEARNING']) > machine_learning_condition]
    filtered_names_fullstack = [row['NAMES'] for index, row in df.iterrows() if isinstance(row['FULL STACK DEVELOPMENT'], (int, float)) and int(row['FULL STACK DEVELOPMENT']) > full_stack_condition]

    # Pass the filtered names to the template
    return render_template('filtered_names.html', 
                           filtered_names_python=filtered_names_python,
                           filtered_names_java=filtered_names_java,
                           filtered_names_dbms=filtered_names_dbms,
                           filtered_names_computer=filtered_names_computer,
                           filtered_names_machine=filtered_names_machine,
                           filtered_names_fullstack=filtered_names_fullstack)

if '__main__'== __name__:
    app.run(debug=True)
