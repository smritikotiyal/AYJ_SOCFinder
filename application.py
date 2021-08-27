from flask import Flask, jsonify, request, render_template
import numpy as np
import pandas as pd
import os
import uuid 
import json
import re
import time
from datetime import datetime


# To configure MySQL DB
from flask_mysqldb import MySQL
import yaml

# For model dumping
import joblib

application = Flask(__name__)

basepath = "/var/flask-app/" # os.path.abspath(".")  | "./"
# basepath = "./"

# Configure db
db = yaml.load(open(basepath +'database.yaml'))
application.config['MYSQL_HOST'] = db['mysql_host']
application.config['MYSQL_USER'] = db['mysql_user']
application.config['MYSQL_PASSWORD'] = db['mysql_password']
application.config['MYSQL_DB'] = db['mysql_db']
application.config['MYSQL_PORT'] = db['mysql_port']
mysql = MySQL(application)

classes = []
list_most_prob_soc = []
list_most_prob_desc = []
# Results for RF and NB models respectively
result_rf = []
result_nb = []
json_soc = [{}]


@application.route('/')
@application.route('/findSOC.html')
def index():
    # Creating Classes List
    try:

        if(len(classes) == 0):
            cur = mysql.connection.cursor()
            resultValue = cur.execute("SELECT SOC FROM AYJ_SOCAvailableClasses")
            if resultValue > 0:
                availableSOC = cur.fetchall()
                for i in range(0, len(availableSOC)):
                    classes.append(availableSOC[i][0])
            cur.close()
            
        # [3564, 2137, 2121, 2133, 2423, 4161, 3513, 2126, 2421, 
        # 2129, 3416, 5434, 2424, 2124, 3545, 2135, 2134, 1131, 2231, 
        # 1135, 2431, 3542, 2436, 2136, 2473, 3543]
        print(classes)
        return render_template('findSOC.html')
    
    except Exception as e:
        # print("An exception occurred: ", e) 
        return render_template('error.html', error=e)
        # return render_template('findSOC.html')

# 2 decorators same function
@application.route('/', methods=['POST'])
@application.route('/results/<id>', methods=['POST'])
# def socCode(id='socCode'):
def findSOC():
    print('The program is here.')
    if request.method == "POST":
        # print(request.form)
        msg = 'pending'
        JD = request.form.get('jd')
        back = request.form.get('jd2')
        dict_back_soc = {
            'SOC1' : request.form.get('s1'),
            'SOC2' : request.form.get('s2'),
            'SOC3' : request.form.get('s3'),
            'SOC4' : request.form.get('s4'),
            'SOC5' : request.form.get('s5'),
            'SOC6' : request.form.get('s6'),
        }

        dict_model_soc = {
            'M1' : request.form.get('M1'),
            'M2' : request.form.get('M2'),
            'M3' : request.form.get('M3'),
            'M4' : request.form.get('M4'),
            'M5' : request.form.get('M5'),
            'M6' : request.form.get('M6'),
        }

        result = request.form.get('suggestions')
        prediction = {}
        
        # Dataframe for Available Classes - ML models are trained for these
        df_prob = pd.DataFrame({"SOC": classes})
        df_prob.sort_values(by='SOC', ascending=True, inplace=True)

        def modelProbability(userJD, model):
            # Probabilities for RF
            list_model_prob = []
            dict_model_prob = {}
            y_proba = model.predict_proba(userJD)
            # print(y_proba)
            df_prob['model_prob'] = y_proba[0]
            df_prob.sort_values(by='model_prob', ascending=False, inplace=True)
            
            list_model_prob.append(df_prob['SOC'].iloc[0])
            list_model_prob.append(df_prob['SOC'].iloc[1])
            list_model_prob.append(df_prob['SOC'].iloc[2])
            
            dict_model_prob[1] = [df_prob['SOC'].iloc[0], df_prob['model_prob'].iloc[0]]
            dict_model_prob[2] = [df_prob['SOC'].iloc[1], df_prob['model_prob'].iloc[1]]
            dict_model_prob[3] = [df_prob['SOC'].iloc[2], df_prob['model_prob'].iloc[2]]

            # Reset Probability Dataframe
            df_prob.drop(['model_prob'], axis=1, inplace=True)
            df_prob.sort_values(by='SOC', ascending=True, inplace=True)

            return list_model_prob, dict_model_prob

        def mergeResults(dict_rf, dict_nb):
            main_dict_data = {}
            count = 1
            
            for k1, v1 in dict_rf.items():
                for k2, v2 in dict_nb.items():
                    if(v2[0] not in main_dict_data.values() and v1[0] not in main_dict_data.values()):
                        if(v1[0] == v2[0]):
                            main_dict_data[count] = v1[0]
                            break
                        else:
                            if(k1 == k2):
                                if(v1[1] > v2[1]):
                                    main_dict_data[count] = v1[0]
                                    count += 1
                                    main_dict_data[count] = v2[0]
                                    break
                                else:
                                    main_dict_data[count] = v2[0]
                                    count += 1
                                    main_dict_data[count] = v1[0]
                                    break
                count += 1
            main_list_data = list(main_dict_data.values())
            return main_dict_data, main_list_data

        def modelPredict(data):
            
            # Unseen JD from the User
            df_data = pd.DataFrame({"JD": [data]})

            # load, no need to initialize the loaded_rf
            loaded_model_rf = joblib.load(basepath + "static/models/random_forest.joblib")
            loaded_model_nb = joblib.load(basepath + "static/models/naive_baeyes.joblib")

            # pred = loaded_model.predict(df_data['JD'])

            # Fetching results for ML models
            result_rf, dict_rf = modelProbability(df_data['JD'], loaded_model_rf)
            result_nb, dict_nb = modelProbability(df_data['JD'], loaded_model_nb)
            result_nb.extend(result_rf)
            list_most_prob_soc = result_nb
            dict_data, list_data = mergeResults(dict_rf, dict_nb)
            # print('dict_data : ', dict_data)

            cur = mysql.connection.cursor()
            list_desc = []
            for soc in list_data:
                resultValue = cur.execute("select Description from AYJ_SOCDescription where SOC = %d;" %soc)
                if resultValue > 0:
                    # print(cur.fetchall())
                    availableSOC = cur.fetchall()
                    for i in range(0, len(availableSOC)):
                        list_desc.append(availableSOC[i][0])
                    
            cur.close()
            
            return list_most_prob_soc, list_data, list_desc
        
        try:
            if(JD != None):
                json_dict_soc = {}
                list_all_soc, list_merged_data, list_merged_desc  = modelPredict(JD)
                
                if(len(list_merged_data) == len(list_merged_desc)):
                    for i in range(1, len(list_merged_data)+1):
                        key = "SOC" + str(i)
                        key_d = key + "_desc_" + str(i)
                        json_dict_soc[key] = str(list_merged_data[i-1])
                        json_dict_soc[key_d] = list_merged_desc[i-1]
                    # json_dict_soc['pid'] = p_id

                for i in range(1, len(list_all_soc)+1):
                    key = "M" + str(i)
                    json_dict_soc[key] = str(list_all_soc[i-1])
                
                print('json_dict_soc : ', json_dict_soc)

                json_soc = [json_dict_soc]

                JD2 = re.sub(r"[^a-zA-Z0-9.,;:\"\'-~[\]{}()+*/@#$%^&<>?|= ]"," || ", JD)
                jobD = [{"JD": JD2}]  # create json
                print('first')

                return render_template('findSOC.html', data = json_soc, jobD = jobD) # {'JD' : JD})
            
            elif(result != None):
                list_model_soc = [dict_model_soc['M1'], 
                dict_model_soc['M2'], dict_model_soc['M3'], dict_model_soc['M4'], dict_model_soc['M5'], dict_model_soc['M6']]
                flag = True 
                if(result not in ['SOC1', 'SOC2', 'SOC3', 'SOC4', 'SOC5', 'SOC6']):
                    flag = False

                if(flag == True):
                    soc_val = dict_back_soc[result]
                else:
                    soc_val = result
                
                # To keep the flag value true in case same SOC code is manually entered that has 
                # already been suggested by the model
                if(soc_val in list_model_soc):
                    flag = True

                print('list_model_soc : ', list_model_soc)
                print(soc_val, flag)

                p_id = uuid.uuid1()
                print('p_id with results :', p_id)
                current_Date = datetime.now().date()
                # formatted_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cur = mysql.connection.cursor()
                insert_socdata_query = """INSERT INTO AYJ_SOCData(ID, JD, Date_Of_Entry, M1_SOC_1, M1_SOC_2, M1_SOC_3,
                M2_SOC_1, M2_SOC_2, M2_SOC_3) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s) """ 
                socdata_records = (p_id, back, current_Date, dict_model_soc['M1'], 
                dict_model_soc['M2'], dict_model_soc['M3'], dict_model_soc['M4'], dict_model_soc['M5'], dict_model_soc['M6'])
                cur.execute(insert_socdata_query, socdata_records)
                mysql.connection.commit()
                # cur.close()

                # cur = mysql.connection.cursor()
                insert_soctrue_query = """INSERT INTO AYJ_SOCTrue(SOC_ID, SOC, Flag) VALUES ( %s, %s, %s) """ 
                soctrue_records = (p_id, soc_val, flag)
                cur.execute(insert_soctrue_query, soctrue_records)
                mysql.connection.commit()
                cur.close()

                msg = 'success'
                return render_template('findSOC.html', msg=msg)

        except Exception as e:
            # print("An exception occurred: ", e) 
            return render_template('error.html', error=e)
            # return render_template('findSOC.html')
        
        

        
if __name__ == '__main__':
    application.run(debug=True)
