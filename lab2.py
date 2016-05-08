import urllib2
import pandas as pd
import os
from datetime import datetime

dict = {'01':'22', '02':'24', '03':'23', '04':'25', '05':'3', '06':'4', '07':'8', '08':'17', '09':'20', '10':'21',
         '11':'9', '12':'9', '13':'10', '14':'11', '15':'12', '16':'13', '17':'14', '18':'15', '19':'16', '20':'25',
         '21':'17', '22':'18', '23':'6', '24':'1', '25':'2', '26':'7', '27':'5'}

areaindex = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27']

names = []


def dldata(index):
    "downloading data file"
    url = ("http://www.star.nesdis.noaa.gov/smcd/emb/vci/gvix/G04/ts_L1/ByProvince/Mean/L1_Mean_UKR.R" + index + ".txt")
    vhi_url = urllib2.urlopen(url)
    dt = datetime.strftime(datetime.now(), "%Y-%m-%d_%H-%M-%S")
    names.append("vhi_id_" + index + "_" + dt + ".csv")
    out = open("vhi_id_" + index + "_" + dt + ".csv", 'wb')
    out.write(vhi_url.read())
    out.close()
    return


def frameread(path):
    df = pd.read_csv(path, index_col=False, header=1)
    df.columns = ['year', 'week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI','less15VHI', 'less35VHI']
    df = df.drop(list(df[df['VHI'] == -1].index))
    return df


def changeindex():
    for filename in os.listdir("."):
        if filename.__len__() == 33 and filename[29:33] == '.csv':
            os.rename(filename, filename[:7] + dict[filename[7:9]] + filename[9:])
    return


def clearfiles():
    for filename in os.listdir("."):
        if (filename.__len__() == 33 and filename[29:33] == '.csv') or (filename.__len__() == 32 and filename[28:32] == '.csv'):
            os.remove(filename)
            names.pop()
    return


def byyear(index, year):
    dldata(index)
    df = frameread(names[names.__len__() - 1])
    print ('VHI in year ' + str(year) + ':')
    print ('max: ' + str(max(df.loc[df.year == year, 'VHI'])))
    print ('min: ' + str(min(df.loc[df.year == year, 'VHI'])))
    print '\n'
    return


def extreme(index, perc):
    dldata(index)
    df = frameread(names[names.__len__() - 1])
    print df.loc[df.less15VHI > perc, ['year', 'week', 'VHI', 'less15VHI']]
    return


def medium(index, perc):
    dldata(index)
    df = frameread(names[names.__len__() - 1])
    print df.loc[df.less35VHI > perc, ['year', 'week', 'VHI', 'less35VHI']]
    return



