import numpy as np
import scipy.optimize
import matplotlib.pyplot as plt
import pandas as pd
import sys
import seaborn as sns
import pathlib as path
import os

sns.set()

date = os.path.sys.argv[1].split("/")
name = os.path.basename(sys.argv[1]).split("_")
graph_name = str(name[0]) + "_" + str(name[1]) + "_" + str(name[6])

def fit_func (x,A,x0,g,B):
        return A*((x0**4)/((x**2-x0**2)**2+(4*(g**2)*(x**2)))) + B

df = pd.read_csv(sys.argv[1], header = None, sep = " ", names = ("shift","Inte"))
dffit = df.query(" -25 < shift < -15 or 15 < shift <25")
dffit = pd.DataFrame(dffit)
print(dffit)

p_ini = np.array([500,5,2,-15])


def fitfunc(x, A, x0, g, B):
        return A*(((x0**3)*g)/((x**2-x0**2)**2+(4*(g**2)*(x**2)))) + B

p_optimal,convariance = scipy.optimize.curve_fit(fitfunc, dffit["shift"], dffit["Inte"], p_ini)
convariance = np.sqrt(np.diag(convariance))
for i,v in enumerate(p_ini):
    print ("paramater",i,"=",p_optimal[i],"±",convariance[i])

y = fitfunc(df["shift"],p_optimal[0], p_optimal[1], p_optimal[2], p_optimal[3])

plt.clf()
ymax = 1000
plt.ylim(-100,ymax)
#plt.xlim(1,10)
plt.plot(df["shift"],df["Inte"], ".",markersize = 3)
plt.plot(df["shift"],y,"-")

plt.title(graph_name)
#props = dict(boxstyle = "round", facecolor = "wheat", alpha = 0.5) #グラフテキストのボックス条件
#plt.text(-42,ymax*0.9,"FWHM=" + str(p_optimal[2]) +"\n peak=" + str(p_optimal[1]),bbox = props)
plt.xlabel("Shift(GHz)")
plt.ylabel("Intensity")

plt.show(0)

print("OK? y/n")
ans = input()

if ans == "n":
    plt.close()
    print(graph_name)
    sys.exit()
elif ans == "y":
    plt.savefig(date[1]+ "_" + graph_name + "-graph.eps")
    peak_FWHM =  pd.DataFrame( [[int(name[6].strip("K")),
                 p_optimal[1],
                 convariance[1],
                 p_optimal[2],
                 convariance[2]]],
                 columns = ["Temp.","peak","peak_conv","FWHM","FWHM_conv"]
                 )
    if os.path.isfile("peak_FWHM.csv"): #ファイルが存在するかどうか
        peak_FWHM.to_csv("peak_FWHM.csv",header = None,index = None,mode = "a")
    else:
        peak_FWHM.to_csv("peak_FWHM.csv",index = None,sep = " ")
    print(graph_name)
    plt.close()
else:
    print("error!")
    print(graph_name)
