from flask import Flask, render_template, redirect
from forms import DetailForm
import pandas as pd
from matplotlib import pyplot as plt 
import seaborn as sns
import datetime as dt
from datetime import date
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

app.config['SECRET_KEY']='f0b2c0cf4c8180fe7a86874bdb337d0e'

@app.route("/", methods=['POST', 'GET'])
def home():
    form = DetailForm()
    if form.validate_on_submit():

        choice = int(form.options.data)
        state = form.state.data
        dates = form.dates.data

        df = pd.read_csv('covid_19.csv', parse_dates=['Date'], dayfirst=True)
        df = df[['Date', 'State/UnionTerritory','Cured','Deaths','Confirmed']]
        df.columns = ['date', 'state','cured','deaths','confirmed']

        def covid_case_predictor():
            v = state
            current_state = df[df.state == v]
            current_state['date']=current_state['date'].map(dt.datetime.toordinal)
            x=current_state['date']
            y=current_state['confirmed']
            x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3)
            lr = LinearRegression()
            lr.fit(np.array(x_train).reshape(-1,1),np.array(y_train).reshape(-1,1))
            date_entry = dates
            year, month, day = map(int, date_entry.split('-'))
            date1 = date(year, month, day)
            
            d0 = date(2020, 11, 16)
            d1 = date(date1.year, date1.month, date1.day)
            delta = d1 - d0
            z=delta.days+737497
            a=lr.predict(np.array([[z]]))
            return a
        
        def covid_death_case_predictor():
            v = state
            current_state = df[df.state == v]
            current_state['date']=current_state['date'].map(dt.datetime.toordinal)
            x=current_state['date']
            y=current_state['deaths']
            x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3)
            lr = LinearRegression()
            lr.fit(np.array(x_train).reshape(-1,1),np.array(y_train).reshape(-1,1))
            date_entry = dates
            year, month, day = map(int, date_entry.split('-'))
            date1 = date(year, month, day)
            
            d0 = date(2020, 11, 16)
            d1 = date(date1.year, date1.month, date1.day)
            delta = d1 - d0
            z=delta.days+737497
            a=lr.predict(np.array([[z]]))
            return a

        def covid_recovered_case_predictor():
            v = state
            current_state = df[df.state == v]
            current_state['date']=current_state['date'].map(dt.datetime.toordinal)
            x=current_state['date']
            y=current_state['cured']
            x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3)
            lr = LinearRegression()
            lr.fit(np.array(x_train).reshape(-1,1),np.array(y_train).reshape(-1,1))
            date_entry = dates
            year, month, day = map(int, date_entry.split('-'))
            date1 = date(year, month, day)
            
            d0 = date(2020, 11, 16)
            d1 = date(date1.year, date1.month, date1.day)
            delta = d1 - d0
            z=delta.days+737497
            a=lr.predict(np.array([[z]]))
            return a

        def covid_active_cases():
            a=covid_case_predictor() 
            b=covid_death_case_predictor() 
            c=covid_recovered_case_predictor() 
            return (a-(b+c))

        covid_case_predictor_ans=None
        covid_death_case_predictor_ans=None
        covid_recovered_case_predictor_ans=None
        covid_active_cases_ans=None

        ans=[-1]*4
        labels=["Covid Case Prediction : ","Covid Death Case Predictor : ","Covid Recovered Case Predictor : ","Covid Active Cases : "]

        if choice==1:
            ans[0]=int(covid_case_predictor()[0][0]) if covid_case_predictor()[0][0]>=0 else 0
        elif choice==2:
            ans[1]=int(covid_death_case_predictor()[0][0]) if covid_death_case_predictor()[0][0]>=0 else 0
        elif choice==3:
            ans[2]=int(covid_recovered_case_predictor()[0][0]) if covid_recovered_case_predictor()[0][0]>=0 else 0
        elif choice==4:
            ans[3]=int(covid_active_cases()[0][0]) if covid_active_cases()[0][0]>=0 else 0
        elif choice==5:
            ans[0]=int(covid_case_predictor()[0][0]) if covid_case_predictor()[0][0]>=0 else 0
            ans[1]=int(covid_death_case_predictor()[0][0]) if covid_death_case_predictor()[0][0]>=0 else 0
            ans[2]=int(covid_recovered_case_predictor()[0][0]) if covid_recovered_case_predictor()[0][0]>=0 else 0
            ans[3]=int(covid_active_cases()[0][0]) if covid_active_cases()[0][0]>=0 else 0


        return render_template('form.html', form=form, ans=ans ,labels=labels, error=0 )
    else:
        return render_template('form.html', form=form, ans=None, labels=None , error=-1)


        # 
        # df = pd.read_csv('covid_19.csv', parse_dates=['Date'], dayfirst=True)
        # df = df[['Date', 'State/UnionTerritory','Cured','Deaths','Confirmed']]
        # df.columns = ['date', 'state','cured','deaths','confirmed']
        # df.tail()
        # today = df[df.date == '2020-07-17']
        # max_confirmed_cases=today.sort_values(by="confirmed",ascending=False)
        # top_states_confirmed=max_confirmed_cases[0:5]
        # sns.set(rc={'figure.figsize':(15,10)})
        # sns.barplot(x="state",y="confirmed",data=top_states_confirmed,hue="state")
        # plt.show()
        # maha = df[df.state == 'Maharashtra']
        # sns.set(rc={'figure.figsize':(15,10)})
        # sns.lineplot(x="date",y="confirmed",data=maha,color="g")
        # plt.show()
        # maha['date']=maha['date'].map(dt.datetime.toordinal)
        # maha.head()
        # x=maha['date']
        # y=maha['confirmed']
        # x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3)
        # from sklearn.linear_model import LinearRegression
        # lr = LinearRegression()
        # lr.fit(np.array(x_train).reshape(-1,1),np.array(y_train).reshape(-1,1))
        # output = lr.predict(np.array([[int(form.date.data)]]))
        # accuracy = lr.score(np.array(x_train).reshape(-1,1),np.array(y_train).reshape(-1,1))

        # def covid_case_predictor(v, i):
        #     current_state = df[df.state == v]
        #     from sklearn.model_selection import train_test_split
        #     current_state['date']=current_state['date'].map(dt.datetime.toordinal)
        #     x=current_state['date']
        #     y=current_state['confirmed']
        #     x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3)
        #     from sklearn.linear_model import LinearRegression
        #     lr = LinearRegression()
        #     lr.fit(np.array(x_train).reshape(-1,1),np.array(y_train).reshape(-1,1))
        #     a=lr.predict(np.array([[i]]))
        #     return a

        # answer = covid_case_predictor(form.state.data, int(output[0][0]))
        # 

    #     return render_template('form.html', form=form, output=int(answer[0][0]), accuracy=(accuracy*100))
    # else:
    #     return render_template('form.html', form=form, output=0, accuracy=0)
        
if __name__=="__main__":
    app.run(debug=True)