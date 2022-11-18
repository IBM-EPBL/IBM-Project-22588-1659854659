import pandas as pd 
import numpy as np
from datetime import date
import matplotlib.pyplot as plot
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.lib.pagesizes import A4
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from .models import SalesData,RegularSales
def Predict(prod_id,m_name):
    df = pd.DataFrame(list(SalesData.objects.values('mart_name','month','sales','product_id')))
    df = df[(df.product_id == prod_id)]
    df = df[(df.mart_name == m_name)]
    todays_date = date.today()
    df.drop(['mart_name','product_id'], axis=1,inplace = True)
    X = np.array(df['month']).reshape(-1, 1)
    y = np.array(df['sales']).reshape(-1, 1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.09, random_state=0)
    regr = LinearRegression()
    regr.fit(X_train, y_train)
    y_pred = regr.predict(X_test)
    y_test = y_test.astype(np.float)
    print('Mean Absolute Error (MAE):', metrics.mean_absolute_error(y_test, y_pred))
    print('Mean Squared Error (MSE):', metrics.mean_squared_error(y_test, y_pred))
    print('Root Mean Squared Error (RMSE):', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
    mape = np.mean(np.abs(np.subtract(y_test,y_pred) / np.abs(y_test)))
    print('Mean Absolute Percentage Error (MAPE):', round(mape * 100, 2))
    print('Accuracy:', round(100*(1 - mape), 2))
    month = [todays_date.month - 1, todays_date.month, todays_date.month + 1, todays_date.month + 2]
    m = np.array(month).reshape(-1,1)
    y_pred = regr.predict(m)
    # print(y_pred)
    y_pred = list(y_pred)
    dict = []
    pred_val = []
    for i in range(len(m)):
        dict.append(month[i] % 12 if month[i] > 12 else month[i])
        pred_val.append(int(y_pred[i]))
    return(round(100*(1 - mape), 2),dict,pred_val)

def visualize(m_name):
    df = pd.DataFrame(list(RegularSales.objects.values('mart_name','prod_name','sales','date')))
    df = df[(df.mart_name == m_name)]
    df.drop(['mart_name'], axis=1,inplace = True)
    print(df.head())
    plot.barh(df["prod_name"],df["sales"])
    plot.savefig('myplot.png', dpi=1000)

def createPDF():
    canv = Canvas('text-on-image.pdf',pagesize=A4)
    img = ImageReader('myplot.png')
    registerFont(TTFont('arial','C:\\windows\\fonts\\arial.ttf'))
    x = 120
    y = 500
    w = 389
    h = 236
    canv.setFont("Courier", 24)
    canv.drawString(280, 800, "Report")  
    canv.drawString(200, 750, "Name :")  
    canv.drawString(300, 750, "Tharani")  
    canv.drawString(200, 700, "Mart Name :")  
    canv.drawString(300, 750, "Mart A") 
    canv.drawImage(img,x,y,w,h,anchor='sw',anchorAtXY=True,showBoundary=False)
    canv.setFont('arial',14)
    canv.setFillColor((1,0,0)) #change the text color
    canv.drawCentredString(x+w*0.5,y+h*0.5,'')
    canv.save()