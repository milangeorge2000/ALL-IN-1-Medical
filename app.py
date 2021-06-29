from werkzeug.utils import secure_filename
import numpy as np
import pickle
import os
from flask import Flask,render_template,request,send_file,safe_join,request,abort
import pickle
import shutil
import pandas
import pandas as pd


from tensorflow.keras.models import load_model

from tensorflow.keras.preprocessing import image

cardio_model = pickle.load(open('cardio.pkl','rb'))
diabetes_model = pickle.load(open('diabetes_model.pkl','rb'))
thyroid_model = pickle.load(open('th.pkl','rb'))


app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    # Main page
    return render_template('index.html')


@app.route('/index.html', methods=['GET'])
def home_one():
    # Main page
    return render_template('index.html')



@app.route('/instruction.html', methods=['GET'])
def instruction():
    # Main page
    return render_template('instruction.html')


@app.route('/contact.html', methods=['GET'])
def contact():
    # Main page
    return render_template('contact.html')



@app.route('/malaria.html', methods=['GET'])
def malaria():
    # Main page
    return render_template('indexm.html')

@app.route('/cardio.html', methods=['GET'])
def cardio():
    # Main page
    return render_template('cardioredit.html')



@app.route('/diabetes.html', methods=['GET'])
def diabetes():
    # Main page
    return render_template('diabetes.html')

@app.route('/thyroid.html', methods=['GET'])
def thyroid():
    # Main page
    return render_template('thyroid.html')


@app.route('/pneumonia.html', methods=['GET'])
def pneumonia():
    # Main page
    return render_template('indexn.html')



@app.route('/cardio_predict',methods=['GET','POST'])
def cardio_predict():
    array = list()
    age = int(request.form['age'])
    gender = int(request.form['gender'])
    height = int(request.form['height'])
    weight = float(request.form['weight'])
    ap_hi = int(request.form['ap_hi'])
    ap_lo = int(request.form['ap_lo'])
    Cholesterol = int(request.form['Cholesterol'])
    glucose = int(request.form['glue'])
    smoke = int(request.form['smoke'])
    alco = int(request.form['alco'])
    active = int(request.form['active'])

    array = array + [age,gender,height,weight,ap_hi,ap_lo,Cholesterol,glucose,smoke,alco,active]
    

    output = int(cardio_model.predict([array])[0])

    
    if output == 1 :
      return render_template('cardio_result.html',pred='Person is Affected with CardioVascular Disease')


    else :
      return render_template('cardio_result.html',pred='Person is Normal')




@app.route('/cardio_csv')
def cardio_csv():
  return render_template('cardio_csv.html')

@app.route('/cardio_uploader', methods = ['GET', 'POST'])
def cardio_upload_file():
   if request.method == 'POST':
      f = request.files['file']
      data = pd.read_csv(f)
      data['age'] = data['age'].apply(lambda x : x//365)
      # print(data.values) 
      prediction = cardio_model.predict(data.values) 
      print(prediction)   
      final = pd.DataFrame({'Output':prediction})
      # path = r"C:\Users\D'BUG\Desktop\medical_project\static\client\csv\cardio_result.csv"
      path1 = r"static\client\csv\cardio_result.csv"
      path2 = r"static\client\csv\diabetes_result.csv"
      path3 = r"static\client\csv\thyroid_result.csv"
      try:
        os.remove(path1)
        os.remove(path2)
        os.remove(path3)



      except:
          print('No such file')

      # app.config["CLIENT_CSV"] = r"C:\Users\D'BUG\Desktop\medical_project\static\client\csv"
      app.config["CLIENT_CSV"] = r"static\client\csv"
      final.to_csv('cardio_result.csv')
      # destination = r"C:\Users\D'BUG\Desktop\medical_project\static\client\csv"
      destination = r"static\client\csv"
      # source = r"C:\Users\D'BUG\Desktop\medical_project\cardio_result.csv"
      source = r"cardio_result.csv"
      shutil.move(source,destination)
      # return 'file uploaded successfully'
      return render_template('cardio_csv_download.html')

@app.route('/cardio_csv_result')
def csv_result():
    safe_path = safe_join(app.config["CLIENT_CSV"], 'cardio_result.csv')

    
    return send_file(safe_path, as_attachment=True)


@app.route('/diabetes_predict',methods=['GET','POST'])
def diabetes_predict():
    array = list()
    pregnancies = int(request.form['pregnancies'])
    glucose = int(request.form['glucose'])
    bloodpressure = int(request.form['bloodpressure'])
    skinthickness = float(request.form['skinthickness'])
    insulin = int(request.form['insulin'])
    bmi = float(request.form['bmi'])
    dpf = float(request.form['dpf'])
    age = int(request.form['age'])
    

    array = array + [pregnancies,glucose,bloodpressure,skinthickness,insulin,bmi,dpf,age]
    

    output = int(diabetes_model.predict([array])[0])

    
    if output == 1 :
      return render_template('diabetes_result.html',pred='Person is Affected with Diabetes')


    else :
      return render_template('diabetes_result.html',pred='Person is Normal')




@app.route('/diabetes_csv')
def diabetes_csv():
  return render_template('diabetes_csv.html')

@app.route('/diabetes_uploader', methods = ['GET', 'POST'])
def diabetes_upload_file():
   if request.method == 'POST':
      f = request.files['file']
      data = pd.read_csv(f)
      # data['age'] = data['age'].apply(lambda x : x//365)
      # print(data.values) 
      prediction = diabetes_model.predict(data.values) 
      print(prediction)   
      final = pd.DataFrame({'Output':prediction})
      # path = r"C:\Users\D'BUG\Desktop\medical_project\static\client\csv\cardio_result.csv"
      path1 = r"static\client\csv\diabetes_result.csv"
      path2 = r"static\client\csv\cardio_result.csv"
      path3 = r"static\client\csv\thyroid_result.csv"
      try:
        os.remove(path1)
        os.remove(path2)
        os.remove(path3)

      except:
          print('No such file')

     
     # app.config["CLIENT_CSV"] = r"C:\Users\D'BUG\Desktop\medical_project\static\client\csv"
      app.config["CLIENT_CSV"] = r"static\client\csv"
      final.to_csv('diabetes_result.csv')
      # destination = r"C:\Users\D'BUG\Desktop\medical_project\static\client\csv"
      destination = r"static\client\csv"
      # source = r"C:\Users\D'BUG\Desktop\medical_project\cardio_result.csv"
      source = r"diabetes_result.csv"
      shutil.move(source,destination)
      # return 'file uploaded successfully'
      return render_template('diabetes_csv_download.html')







      
      

@app.route('/diabetes_csv_result')
def diabetes_csv_result():
    safe_path = safe_join(app.config["CLIENT_CSV"], 'diabetes_result.csv')

    
    return send_file(safe_path, as_attachment=True)



@app.route('/thyroid_predict',methods=['GET','POST'])
def thyroid_predict():
    array = list()
    t3 = float(request.form['ttt'])
    fti = float(request.form['ffti'])
    tsh = float(request.form['the'])
    t4u = float(request.form['ddd']) 
    tt4 = float(request.form['tttha'])  
    age = float(request.form['num'])
    sex = float(request.form['gender'])
    ont = float(request.form['thy'])
    ts = float(request.form['surgery'])
    qht = float(request.form['query'])
    qhyt = float(request.form['hyper'])
    sick =float(request.form['cough'])
    goitre = float(request.form['goi'])
    tsh_me = float(request.form['meas'])
    tt3_me = float(request.form['measu'])
    tt4_me = float(request.form['measure'])
    t4u_me = float(request.form['measured'])
    fti_me = float(request.form['fmeasure'])
    tbg_me = float(request.form['tmeasure'])

    array = array + [t3,fti,tsh,t4u,tt4,age,sex,ont,ts,qht,qhyt,sick,goitre,tsh_me,tt3_me,tt4_me,t4u_me,fti_me,tbg_me]
    
    
    output = int(thyroid_model.predict([array])[0])

    
    if output == 1 :
      return render_template('thyroid_result.html',pred='Person is Affected with Thyroid Disease')


    else :
      return render_template('thyroid_result.html',pred='Person is Normal')













@app.route('/thyroid_csv')
def thyroid_csv():
  return render_template('thyroid_csv.html')

@app.route('/thyroid_uploader', methods = ['GET', 'POST'])
def thyroid_upload_file():
   if request.method == 'POST':
      f = request.files['file']
      data = pd.read_csv(f)
      # data['age'] = data['age'].apply(lambda x : x//365)
      # print(data.values) 
      prediction = thyroid_model.predict(data.values) 
      print(prediction)   
      final = pd.DataFrame({'Output':prediction})
      # path = r"C:\Users\D'BUG\Desktop\medical_project\static\client\csv\cardio_result.csv"
      path1 = r"static\client\csv\diabetes_result.csv"
      path2 = r"static\client\csv\cardio_result.csv"
      path3 = r"static\client\csv\thyroid_result.csv"
      try:
        os.remove(path1)
        os.remove(path2)
        os.remove(path3)

      except:
          print('No such file')

      app.config["CLIENT_CSV"] = r"C:\Users\D'BUG\Desktop\medical_project\static\client\csv"
      # app.config["CLIENT_CSV"] = r"static\client\csv"
      final.to_csv('thyroid_result.csv')
      destination = r"C:\Users\D'BUG\Desktop\medical_project\static\client\csv"
      # destination = r"static\client\csv"
      source = r"C:\Users\D'BUG\Desktop\medical_project\thyroid_result.csv"
      # source = r"diabetes_result.csv"
      shutil.move(source,destination)
      # return 'file uploaded successfully'
      return render_template('thyroid_csv_download.html')

@app.route('/thyroid_csv_result')
def thyroid_csv_result():
    safe_path = safe_join(app.config["CLIENT_CSV"], 'thyroid_result.csv')

    
    return send_file(safe_path, as_attachment=True)


@app.route('/predict_malaria', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        print('reached')
        folder = r'uploads'
        for filename in os.listdir(folder):
          file_path = os.path.join(folder, filename)
          if os.path.isfile(file_path) or os.path.islink(file_path):
              os.unlink(file_path)
          elif os.path.isdir(file_path):
             shutil.rmtree(file_path)
           
        f = request.files['file']
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        



        img = image.load_img(file_path,target_size=(224,224)) ##loading the image
        img = np.asarray(img) ##converting to an array
        img = img / 255 ##scaling by doing a division of 255
        img = np.expand_dims(img, axis=0) ##expanding the dimensions
        saved_model = load_model("modelv19_malaria.h5") ##loading the model
        output = saved_model.predict(img)
        if output[0][0] > output[0][1]:
          result = "Infected"
        else:
           result = "Uninfected"


        return result








@app.route('/predict_pneumonia', methods=['GET', 'POST'])
def upload2():
    if request.method == 'POST':
        # Get the file from post request
        print('reached')
        folder = r'uploads'
        for filename in os.listdir(folder):
          file_path = os.path.join(folder, filename)
          if os.path.isfile(file_path) or os.path.islink(file_path):
              os.unlink(file_path)
          elif os.path.isdir(file_path):
             shutil.rmtree(file_path)
           
        f = request.files['file']
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        



        img = image.load_img(file_path,target_size=(224,224)) ##loading the image
        img = np.asarray(img) ##converting to an array
        img = img / 255 ##scaling by doing a division of 255
        img = np.expand_dims(img, axis=0) ##expanding the dimensions
        saved_model = load_model("modelvgg19_lung.h5") ##loading the model
        output = saved_model.predict(img)
        if output[0][0] > 0.5:
          result = "Infected with Penumonia"
        else:
           result = "Normal"


        return result






if __name__ == '__main__':
    app.run(debug=True)