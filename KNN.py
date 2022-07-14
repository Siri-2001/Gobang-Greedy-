import numpy as np
import pandas as pd
from math import sqrt
import matplotlib.pyplot as plt
df=pd.read_csv("iris.data")
data=np.array(df)
'''读取文件'''
rds = np.random.RandomState(5)
rds.shuffle(data)
'''数据打乱，便于划分测试集与训练集'''
#print(data)
test_radio=0.3
train_data=data[0:int(len(data)*(1-test_radio))]
test_data=data[int(len(data)*(1-test_radio)):]
def get_most(top_k):
    '''得到最近k个点中'''
    count_list=[]
    for i in top_k:
        count_list.append(top_k.count(i))
    return top_k[np.argmax(count_list)]
def KNN(test_list,k):
    result_list=[]
    for x_list in test_list:
        dis_list=np.array([sqrt(np.sum((x_list[0:4]-k[0:4])**2)) for k in train_data])
        top_k=[train_data[i,-1] for i in np.argsort(dis_list)[:k]]
        result_list.append(get_most(top_k))
    result_list=np.array(result_list)
    count=0
    for i in range(len(result_list)):
        if result_list[i]==test_list[i,-1]:
            count+=1
    print(count/len(result_list))
    return count/len(result_list)

plt.plot(range(1,20),[KNN(test_data,i) for i in range(1,20)])
plt.xlim(1,20)
plt.ylim(0.93,0.99)
plt.show()
