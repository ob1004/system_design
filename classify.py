# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 23:22:19 2021

@author: Administrator
"""

import csv

print("classify")

class1=['诉讼','立案','司法','法律文书','起诉','法院','涉诉','仲裁','判决']
class2=['投资者关系活动','接待日','调研','集体接待']
class3=['辞职','任命','辞任','财务总监','聘任','解聘','董秘','人员调整','董事长','选举','总经理']
out1 = open('all_class.csv','w', newline='',encoding='utf-8-sig')
csv_write=csv.writer(out1,dialect='excel')  
with open('all.csv','r', encoding='utf-8-sig') as file:
    file.readline()
    reader=csv.reader(file)
    for line in reader:
        temp=0
        for j in class1:
            if j in line[3]:
                line.append('司法案件')
                temp=1
                break
        if temp==1:
            csv_write.writerow(line)
            continue
        for j in class2:
            if j in line[3]:
                line.append('调研活动')
                temp=1
                break
        if temp==1:
            csv_write.writerow(line)
            continue
    
        for j in class3:
            if j in line[3]:
                line.append('人事变动')
                temp=1
                break
        if temp==1:
            csv_write.writerow(line)

        if temp==0:
            line.append('其他')
            csv_write.writerow(line)
out1.close()
