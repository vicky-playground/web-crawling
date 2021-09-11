#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install xlsxwriter')

import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

"""
=================================製作Pandas表格===================================================================
"""

# 01製作欄位
columns = [
    '公司名稱', '職缺名稱', '工作內容', '網頁連結', '職缺類別', '薪資', '工作類型', '工作地點', '需求技能', '相關能力', '工作經驗', '教育程度', '科系要求', '語言條件', '其他', '公司福利'
]

# 02製作空表格
df_empty = pd.DataFrame(columns=columns)

"""
=================================此行開始為先爬取第一頁各職位標題及連結==============================================
"""

url = 'https://www.104.com.tw/jobs/search/?ro=0&keyword=%E9%87%91%E8%9E%8D%E7%A0%94%E7%A9%B6%E5%93%A1&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=1&asc=0&page=1&mode=s&jobsource=2018indexpoc'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.54'
}

page = 1
"""
動用以下for迴圈可以選擇欲爬取頁數
"""
No = 1
for i in range(0, 1):
    res = requests.get(url, headers=headers)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')


    titleSoupList = soup.select('h2.b-tit')

    a = 3
    for i in range(20):
        titleSoup = titleSoupList[a]
        title = titleSoup.select('a')
        print(str(No) + '. ' + title[0].text +'\n')
        No += 1
        articleUrl = 'https:' + title[0]['href']
        print(articleUrl + '\n')
        
        """
        ========================此行開始為內容頁爬取=====================
        """
        
        Code = articleUrl[27: 32]
        contentUrl = 'https://www.104.com.tw/job/ajax/content/' + Code + '?jobsource=jolist_c_relevance'
        headers = {
            "Referer": "https://www.104.com.tw/job/" + str(Code), 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.54'
        }
        res = requests.get(contentUrl, headers = headers)
        jsonData = json.loads(res.text)
        jsonData
        lst2jsonData = list(jsonData.values())
        
        """
        公司名稱
        """
        jsonHeader = lst2jsonData[0]['header']
        jsonHeader = jsonHeader['custName']
        
        """
        00工作內容
        """
        jsonDetail = lst2jsonData[0]['jobDetail']
        jobContent = jsonDetail['jobDescription']
        
        """
        00-1職缺類別
        """
        jsonDetail = lst2jsonData[0]['jobDetail']
        jobDetCat = jsonDetail['jobCategory']           
        jDCseq = 0
        jDCNo = 1
        yJD = 0
        YJDyJD = ""
        for i in jobDetCat:
            Answer = str(jDCNo) + '. ' + jobDetCat[jDCseq:jDCseq+1][0]['description'] + ' '
            for i in range(len(Answer)):
                ch = Answer[i]
                YJDyJD += ch
                yJD += 1
            jDCseq += 1
            jDCNo += 1
        jobCategory = YJDyJD 
        
        """
        00-2工作待遇
        """
        jobDetSal = jsonDetail['salary']
        
        """
        00-3工作性質
        """
        jobDetJT = jsonDetail['jobType']
        if jobDetJT == 1:
            y5 = ' ' + '全職'
        else:
            y5 = ' ' + '非全職'
        jobType = y5

        """
        00-4上班地點
        """
        jobDetAddRe = jsonDetail['addressRegion']
        jobDetAddDe = jsonDetail['addressDetail']
        jobDetIndAr = jsonDetail['industryArea']
        jobLocation = ' ' + jobDetAddRe + jobDetAddDe + jobDetIndAr

        """
        01要求技能總dict
        """
        jsonDetail = lst2jsonData[0]['condition']

        """
        01-1技術項dict
        """
        jobConSpe = jsonDetail['specialty']
        jCSseq = 0
        jCSNo = 1
        yJCS = 0
        YJCSyjCS = ""
        for i in jobConSpe:
            Answer = str(jCSNo) + '. ' + jobConSpe[jCSseq:jCSseq+1][0]['description'] + ' '    
            for i in range(len(Answer)):
                ch = Answer[i]
                YJCSyjCS += ch
                yJCS += 1    
            jCSseq += 1
            jCSNo += 1
        jobSpecialty = YJCSyjCS
        
        """
        01-2其他技能項dict
        """
        jobConOther = jsonDetail['skill']
        jCOseq = 0
        jCONo = 1
        yCO = 0
        YCOyCO = ""
        for i in jobConOther:
            Answer = str(jCONo) + '. ' + jobConOther[jCOseq:jCOseq+1][0]['description'] + ' '    
            for i in range(len(Answer)):
                ch = Answer[i]
                YCOyCO += ch
                yCO += 1         
            jCOseq += 1
            jCONo += 1
        jobSkill = YCOyCO
        
        """
        01-3工作經驗
        """
        jobConExp = jsonDetail['workExp']
        
        """
        01-4學歷要求
        """
        jobConEdu = jsonDetail['edu']
        
        """
        01-5科系要求-其下面為list
        因此print(' ' + jobConMaj)這行不可加str
        """
        jobConMaj = jsonDetail['major']
        jCMseq = 0
        jCMNo = 1
        yCM = 0
        YCMyCM = ""
        for i in jobConMaj:
            Answer = str(jCMNo) + '. ' + jobConMaj[jCMseq:jCMseq+1][0] + ' '
            for i in range(len(Answer)):
                ch = Answer[i]
                YCMyCM += ch
                yCM += 1  
            jCMseq += 1
            jCMNo += 1
        jobMajor = YCMyCM
            
        """
        01-6語文條件
        """
        jobConLan = jsonDetail['language']
        jCLseq = 0
        jCLNo = 1
        yCL = 0
        YCLyCL=""
        for i in jobConLan:
            Answer = str(jCLNo) + '. ' + jobConLan[jCLseq:jCLseq+1][0]['language'] + ': ' + jobConLan[jCLseq:jCLseq+1][0]['ability']
            for i in range(len(Answer)):
                ch = Answer[i]
                YCLyCL += ch
                yCL += 1 
            jCLseq += 1
            jCLNo += 1
        jobLanguage = YCLyCL
        
        """
        01-7其他
        """
        jobConElse = jsonDetail['other']
        
        """
        02-1福利制度
        """
        jobWelfare = lst2jsonData[0]['welfare']
        jobWelWel = jobWelfare['welfare']
        
        """
        ======================此行開始為內容頁細部爬取結束=====================
        """
        
        """
        ======================將製作出的Pandas表格合併進入原始空表格============================
        """
        data = [
            [jsonHeader, title[0].text, jobContent, articleUrl, jobCategory, jobDetSal, jobType, 
            jobLocation, jobSpecialty, jobSkill, jobConExp, jobConEdu, jobMajor, jobLanguage, jobConElse, jobWelWel]
        ]
        
        df_104 = pd.DataFrame(data=data, columns=columns)
        df_empty = df_104.append(df_empty)
        """
        ======================Pandas Data合併完成============================
        """
        a += 1
        
    """
    ======================合併Pandas表格資料=================================
    """
    
    page += 1
    newUrl = 'https://www.104.com.tw/jobs/search/?ro=0&keyword=%E9%87%91%E8%9E%8D%E7%A0%94%E7%A9%B6%E5%93%A1&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=1&asc=0&page= ' + str(page) + '&mode=s&jobsource=2018indexpoc'
    url = newUrl
df_empty = df_empty.reset_index(drop=True)
df_empty

df_empty.to_excel('金融研究員.xlsx', encoding='utf-8-sig', engine='xlsxwriter')


# In[ ]:




