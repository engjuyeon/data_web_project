import os.path

from flask import Flask, render_template, request, redirect, url_for
import pymysql
import numpy as np
import pandas as pd
import tensorflow as tf
import base64
import functools
import operator
##from Cython.Includes.cpython import type

 
tf.compat.v1.disable_eager_execution()
print(tf.__version__)

app = Flask(__name__)
app.secret_key = 'secret_four'

print(tf.version.VERSION)



@app.route('/', methods=['GET', 'POST'])
def index():
    
    print("===============================start==============================================================================")
    
    if request.method == 'GET':
        conn = pymysql.connect(host='127.0.0.1', user='root', password='0431', port = 3308, db='data_image', charset='utf8')
        print('연결완료')
        cur = conn.cursor()
        sql = 'SELECT image FROM image'
        cur.execute(sql)
        image = cur.fetchall()
           
        imageData = []
          
        for obj in image:
            imageData.append(obj)
           
        cur.close()
        conn.close()    
        print(imageData)
        str = functools.reduce(operator.add, (imageData[4]))
        str2 = functools.reduce(operator.add, (imageData[7]))
        str3 = functools.reduce(operator.add, (imageData[6]))
            
            
            ################################################################################################
            ################################################################################################
            ################################################################################################
            
            
        conn = pymysql.connect(host='127.0.0.1', user='root', password='0431', port = 3308, db='public_data_analysis', charset='utf8')
        print('=================연결완료=================')
        cur = conn.cursor()
        sql = 'SELECT P.기간, P.계, AP.total, E.total, G.gdp, O.합계, B.출생건수, B.사망건수, U.total FROM seoul_population AS P LEFT JOIN economically_active_population AS AP ON P.기간 = AP.year LEFT JOIN employment_rate AS E ON AP.year = E.year LEFT JOIN gdp AS G ON E.year = G.year LEFT JOIN one_person AS O ON G.year = O.기간 LEFT JOIN seoul_birth_death AS B ON O.기간 = B.기간 LEFT JOIN unemployment_rate AS U ON B.기간 = U.year ORDER BY P.기간'
        cur.execute(sql)
        chart = cur.fetchall()
            #chartData = pd.DataFrame(chart, columns=['year', 'birth', 'dead', 'economy', 'employ', 'one', 'unemploy' , 'total', 'gdp'])
           
           
        print("chart : " , chart)
           
        year = [];        
        birth = [];
            
        population = [];
        activity_population = [];
        employment_rate = [];
        gdp = [];
        one_person = [];
        death = [];
        unemployment_rate = [];
            
            
        for obj in chart:
            year.append(obj[0])
            population.append(obj[1])
            activity_population.append(obj[2])
            employment_rate.append(obj[3])
            gdp.append(obj[4])
            one_person.append(obj[5])
            birth.append(obj[6])
            death.append(obj[7])
            unemployment_rate.append(obj[8])
                
            
            
            
                 
        population.insert(0,"인구수");
        activity_population.insert(0,"경제활동 인구수");
        employment_rate.insert(0,"고용률");
        gdp.insert(0,"gdp");
        one_person.insert(0,"1인가구");
        death.insert(0,"사망건수");
        birth.insert(0,"출생건수");
        unemployment_rate.insert(0,"실업률");
        
           
        cur.close()
        conn.close()
        
        return render_template('index.html', imageData = str, imageData2 = str2, imageData3 = str3, year = year, birth = birth, population = population, activity_population = activity_population, 
                                   employment_rate = employment_rate, gdp = gdp, one_person = one_person, death = death, unemployment_rate = unemployment_rate)
        

    if request.method == 'POST':
        conn = pymysql.connect(host='127.0.0.1', user='root', password='0431', port = 3308, db='public_data_analysis', charset='utf8')
        print('연결완료')
        cur = conn.cursor()
        sql = 'SELECT * FROM total_data'
        cur.execute(sql)
        total = cur.fetchall()
        data = pd.DataFrame(total, columns=['year', 'total', 'one', 'economy', 'employ'
            , 'unemploy', 'GDP', 'birth', 'dead'])

        x_data = data[['GDP', 'birth', 'dead','economy', 'employ',  'one' ,'unemploy']]
        y_data = data[['total']]

        print(x_data, '\n\n')
        print(y_data)

        X = tf.keras.layers.Input(shape=[7])  # x_data 의 갯수
        H = tf.keras.layers.Dense(7, activation='swish')(X)
        y = tf.keras.layers.Dense(1)(H)
        model = tf.keras.models.Model(X, y)
        model.compile(loss='mse')

        model.fit(x_data, y_data, epochs=10000, verbose=0)
        # 파라미터를 전달 받습니다.
        GDP = int(request.form['GDP'])
        print(GDP)
        birth = int(request.form['birth'])
        print(birth)
        dead = int(request.form['dead'])
        print(dead)
        economy = int(request.form['economy'])
        print(economy)
        employ = int(request.form['employ'])
        print(employ)
        one = int(request.form.get('one', False))
        print(one)
        unemploy = int(request.form.get('unemploy', False))
        print(unemploy)
        data_input = [(GDP, birth, dead, economy, employ, one, unemploy)]
        insert_data = pd.DataFrame(data_input, columns=['GDP', 'birth', 'dead', 'economy', 'employ', 'one', 'unemploy'])

        # 결과 인구 수
        pop = model.predict(insert_data)
        
        print(pop)

        return render_template('return.html', prediction=pop)

if __name__ == "__main__":
    app.debug = True
    app.run()