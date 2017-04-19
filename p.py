
from Tkinter import *
import sqlite3
import pandas
import matplotlib
import numpy as np
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

  #connects to database
dbConnection = sqlite3.connect('/Users/kimo/Desktop/project/EconLabTool.db')
global cursor 
cursor = dbConnection.cursor()

#imports quandl csv data into sqlite
# df = pandas.read_csv('House Price 1975_2016.csv')
# df.to_sql('House Price Index All States (1975-2016)', dbConnection)
#main frame


root = Tk()
root.title('EconToolLab: Descriptive Statistics')
root.geometry('750x850')
toolsFrame = Frame(root)
toolsFrame.grid(sticky="nsew")
toolsFrame.grid_rowconfigure(20, weight=1)
toolsFrame.grid_columnconfigure(6, weight=1)
var = StringVar()




#top level menu for the main window
navBar = Menu(root)

statisticsMenu = Menu(navBar)
statisticsMenu.add_command(label = 'Univariate Analysis')
statisticsMenu.add_command(label='Bivariate Analysis')
navBar.add_cascade(label = 'Descriptive Statistics', menu = statisticsMenu)

regressionMenu = Menu(navBar)
regressionMenu.add_command(label = 'Import Data')
regressionMenu.add_command(label= 'Linear Regression')
navBar.add_cascade(label = 'Regression Analysis', menu = regressionMenu)

helpMenu = Menu(navBar)
helpMenu.add_command(label = 'Getting started')
helpMenu.add_command(label = 'Help')
navBar.add_cascade(label = 'About the EconToolLab', menu = helpMenu)
root.config(menu=navBar)

chosenIndicator = StringVar()
checkedMax  = IntVar()
checkedMin = IntVar()
checkedMean = IntVar()
checkedStd = IntVar()
checkedVar = IntVar()
checkedRange = IntVar()
checkedMedian = IntVar()
checkedMed = IntVar()
checkedPlot = IntVar()
checkedHist = IntVar()
values = []
dates = []
maxim = IntVar()
label = StringVar()






def query ():
  
  if startYear.get():
    cursor.execute('SELECT * from [' + chosenIndicator.get()+'] where strftime("%Y", date) between "' + startYear.get() +'" and "' + endYear.get() +'" order by date asc')
  else:
    cursor.execute('SELECT * from [' + chosenIndicator.get()+'] order by date asc')
  valueCanvas = Canvas(toolsFrame)
  scrollbar = Scrollbar(valueCanvas)
  
  valueCanvas.grid(row=0, rowspan= 11, column= 7, columnspan=2, padx = (70,0))
  listbox = Listbox(valueCanvas, background='grey', height=20, width=20)
  listbox.grid(row=0, sticky=E)
  listbox.insert(END, 'Date                      Value')
  for column in cursor:
    dates.append(str(column[1]))
    values.append(column[2])
    index=0
    for date in dates:
      listbox.insert(END, date+'             ' +str(values[index]))
      index+=1
  
  scrollbar.grid(row=0, column=7, sticky=N+S)
  listbox.config(yscrollcommand=scrollbar.set)
  scrollbar.config(command=listbox.yview)
#plotting time series
  y = values
  if checkedPlot.get() ==1:
    x = mdates.datestr2num(dates)
    plot = Figure(figsize=(6,4))
    axes = plot.add_subplot(111)
    axes.set_title(chosenIndicator.get())
    axes.set_xlabel('year')
    axes.set_ylabel('value')
    axes.plot(x, y)
    axes.xaxis_date()
    canvas = FigureCanvasTkAgg(plot, master=toolsFrame)
    canvas.draw()
    canvas.get_tk_widget().grid(row = 28, column = 0, columnspan=10, rowspan=6, sticky = NW)
  if checkedHist.get() == 1:
    plot = Figure(figsize=(6,4))
    axes = plot.add_subplot(111)
    axes.hist(y, bins = 10, rwidth=0.3, normed=True)
    canvas = FigureCanvasTkAgg(plot, master=toolsFrame)

    canvas.get_tk_widget().grid(row = 28, column = 0, columnspan=10, rowspan=6, sticky = NW)
    canvas.draw()
    
    calcStat = Label(toolsFrame, textvariable = values).grid(row = 7, column = 0, sticky ='NW')

  
  if checkedMax.get() == 1:
    maxim = np.max(values)
    maxLabel = Label(toolsFrame, text = 'Maximum value is ' + str(maxim), fg = '#518242', font=('Helvetica', 15))
    maxLabel.grid(column = 0, row = 11, sticky = W, padx=(20,0))

  if checkedMin.get() == 1:
    minim = np.min(values)
    minLabel = Label(toolsFrame, text = 'Minimum value is ' + str(minim), fg = '#518242', font=('Helvetica', 14))
    minLabel.grid(column = 0, row = 12, sticky = W, padx=(20,0))
  

  if checkedMean.get() == 1:
    mean = np.average(values)
    meanLabel = Label(toolsFrame, text = 'Mean value is ' + str(mean), fg = '#518242', font=('Helvetica', 14))
    meanLabel.grid(column = 0, row = 13, sticky = W, padx=(20,0))
  
  if checkedStd.get() == 1:
    stdDev = np.std(values)
    stdLabel = Label(toolsFrame, text = 'Standard deviation is ' + str(stdDev), fg = '#518242', font=('Helvetica', 14))
    stdLabel.grid(column = 0, row = 14, sticky = W, padx=(20,0))
  
  if checkedMed.get() == 1:
    median = np.median(values)
    medLabel = Label(toolsFrame, text = 'Median value is ' + str(median), fg = '#518242', font=('Helvetica', 14))
    medLabel.grid(column = 0, row = 15, sticky = W, padx=(20,0))

  if checkedRange.get() == 1:
    rang = np.max(values) - np.min(values)
    rangeLabel = Label(toolsFrame, text = 'Range is ' + str(rang), fg = '#518242', font=('Helvetica', 14))
    rangeLabel.grid(column = 0, row = 16, sticky = W, padx=(20,0))
  


def nestedMenu(frame,row,var):
# nested dropdown menu for economic variables
  econIndicators = {'GDP': ['Real Gross Domestic Product (1930-2016)', 
             'Potential GDP (1949-2027)', 'Lagging Index (1948 - 2017)'],
  				   'Inflation and price': ['Annual Inflation Rate (1914-2017)', 
  				   'Chained CPI (1999-2017)',
             'Producer Price Index for Commodities (1994-2017)'
  				   ],
  				   'Labor': ['Labor force participation (1948-2017)','Employment rate(non-farm 1939-2017)', 
             'Employment rate for women (1964-2017)',
             'Unemployment rate (1948-2017)'],
  				   'Housing': ['Housing Market Index (1985-2017)',
             'House Price Index All States (1975-2016)',
             '30-year Fixed Mortgage Rates (1971-2017)',
             'Annual Rate for Total Construction (2002-2016)'],
  				   'Exports/Imports': ['Imports/Exports rates(1989-2016)'],
  				   'Industry': ['Manufacturing and Trade Inventories and Sales (1992-2017)'],
  				   'Investment':['Angel investment by sector (2002-2015)'],
  				   'Equity':['S&P 500 index (1950-2017)', 'US Treasury Long Term Rates (2000-2017)'
  	
  ]}

  chosenIndicator.set('Real Gross Domestic Product (1930-2016)') #default indicator
  nestedMenu = Menubutton(frame, textvariable = var)
  mainMenu = Menu(nestedMenu, tearoff= False)
  nestedMenu.config(menu = mainMenu)

  for indicator in(econIndicators.keys()):
  	option = Menu(mainMenu)
  	mainMenu.add_cascade(label = indicator, menu = option)
  	mainMenu.add_separator()
  	for nestedIndicator in econIndicators[indicator]:
                  option.add_checkbutton(label=nestedIndicator, variable = var, onvalue=nestedIndicator, offvalue=0)
                  option.add_separator()
  nestedMenu.grid(row =row, columnspan = 2, sticky = 'EW', padx = (40,0), pady = (20, 0))

nestedMenu(toolsFrame,0, chosenIndicator)

#checkbuttons for statistical tools
descStatLabel = Label(toolsFrame, text = 'Descriptive Statistics:', font=('Helvetica 15 underline'))
descStatLabel.grid(row = 1,column = 0, pady=(20,0), padx = (40,0), sticky = W)
variance = Checkbutton(toolsFrame,  onvalue=1, variable = checkedVar, offvalue=0, text = 'Variance').grid(row = 2,column = 0, pady=(10,0), padx = (40,0), sticky = W)

std = Checkbutton(toolsFrame, variable = checkedStd, onvalue=1, offvalue=0, text = 'Std.Deviation').grid(row = 2, column = 1, columnspan = 1, pady=(10,0),  sticky= W)

mean = Checkbutton(toolsFrame, variable = checkedMean, onvalue=1, offvalue=0, text = 'Mean').grid(row = 3, column = 0, sticky = W, padx = (40,0), pady=(8,0))
median = Checkbutton(toolsFrame,  variable = checkedMed, onvalue=1, offvalue=0, text = 'Median').grid(row = 3, column = 1, sticky = W, pady=(8,0))


minValue = Checkbutton(toolsFrame,  variable = checkedMin, onvalue=1, offvalue=0, text = 'Minimum').grid(row = 4, column = 0, sticky = W, padx = (40,0), pady=(8,0))
maxValue = Checkbutton(toolsFrame, variable = checkedMax, onvalue=1, offvalue=0, text = 'Maximum').grid(row = 4, column = 1, sticky = W, pady=(8,0))

rangeValue = Checkbutton(toolsFrame,  variable = checkedRange, onvalue=1, offvalue=0, text = 'Range').grid(row = 5, column = 0, sticky = W, padx = (40,0), pady = (8,0))
plotLabel = Label(toolsFrame, text = 'Plot Style:', font=('Helvetica 15 underline'))
plotLabel.grid(row = 6,column = 0, pady=(30,0), padx = (40,0), sticky = W)
plotValue = Checkbutton(toolsFrame,  variable = checkedPlot, text = 'Time Series Graph').grid(row = 7, column = 0, sticky = W, padx = (40,0), pady = (8,10))
histValue = Checkbutton(toolsFrame,  variable = checkedHist, text = 'Histogram').grid(row = 7, column = 1, sticky = W, pady = (8,10))
startLabel = Label(toolsFrame, text = 'Start Year').grid(row = 8, column = 0, padx = (40,0),sticky = NW)
startYear = Entry(toolsFrame)
startYear.grid(row = 8, column = 1, sticky = NW)
endLabel = Label(toolsFrame, text = 'End Year').grid(row = 9, column = 0, padx = (40,0), sticky=NW)
endYear = Entry(toolsFrame)
endYear.grid(row = 9, column = 1, sticky = NW)
submitButton = Button(toolsFrame, text = 'Submit', width= 10, command = query)
submitButton.grid(row = 10, column = 1,  padx = (75,0), pady=(0,0), sticky=W)







