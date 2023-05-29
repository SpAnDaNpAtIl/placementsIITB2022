import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from bs4 import BeautifulSoup

with open('jobs.json') as f:
    data = json.load(f)


link = 'https://campus.placements.iitb.ac.in/applicant/job/{}'.format(data[0].get('id'))
driver = webdriver.Firefox(executable_path=r'C:\Users\spand\Downloads\geckodriver.exe')
driver.get('https://campus.placements.iitb.ac.in/')
delay = 20 # seconds
try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'cdk-describedby-message-container')))
except TimeoutException:
    print("Loading took too much time!")

res = []
undone=[]
for i in range(len(data)):
    print(i+1, len(data),data[i]['id'])
    try:
        driver.get('https://campus.placements.iitb.ac.in/applicant/job/{}'.format(data[i].get('id')))
        time.sleep(3)  # depending on your internet speed and account safety
        # pgData = driver.find_element(By.CLASS_NAME, 'container p-5')
        # tried using selenium find elements but not working
        # alternative
        page = driver.page_source.encode('utf-8')
        soup = BeautifulSoup(page, 'html.parser')
        pgData = soup.find('div', {'class': 'container p-5'})
        pgData = pgData.find_all('div', {'class': 'panel mt-3 mb-3 d-flex flex-column'})

        ##########job info###############
        jobDetails = pgData[0].find('div').get_text('\n')
        tempVar = pgData[0].find_all('table')
        tempVar2 = tempVar[0].find_all('tr')[-1].find_all('td')
        try:
            postingLoc = tempVar2[0].get_text()
        except:
            postingLoc = 'NA'
        try:
            AccoDet = tempVar2[1].get_text()
        except:
            AccoDet = 'NA'
        try:
            bondApp = tempVar[-1].find_all('tr')[-1].find('td').get_text()
        except:
            bondApp = 'NA'

        #########eligibility criteria
        elg = pgData[1].find_all('table')

        elgCriteria = elg[0].find('tbody').find_all('tr')
        depts = []
        for j in range(len(elgCriteria)):
            chkBoxes = elgCriteria[j].find_all('td')[1:]
            dept = []
            for k in chkBoxes:
                box = k.find('div')
                """
                if len(box.contents)==0:
                    dept.append(False)
                else:
                    if 'mat-checkbox-checked' not in box.find('mat-checkbox')['class']:
                        dept.append(False)
                    else:
                        dept.append(True)
                        """
                try:
                    if 'mat-checkbox-checked' not in box.find('mat-checkbox')['class']:
                        dept.append(False)
                    else:
                        dept.append(True)
                except:
                    dept.append(False)
            depts.append(dept)

        elgCriteriaIDC = elg[1].find('tbody').find_all('tr')
        deptsIDC = []
        for j in range(len(elgCriteriaIDC)):
            chkBoxes = elgCriteriaIDC[j].find_all('td')[1:]
            dept = []
            for k in chkBoxes:
                box = k.find('div')
                try:
                    if 'mat-checkbox-checked' not in box.find('mat-checkbox')['class']:
                        dept.append(False)
                    else:
                        dept.append(True)
                except:
                    dept.append(False)
                """
                if len(box.contents) == 0 or 'mat-checkbox-checked' not in box.find('mat-checkbox')['class']:
                    dept.append(False)
                else:
                    dept.append(True)
                    """
            deptsIDC.append(dept)

        ###########compensation details#############
        currType = pgData[2].find('p').get_text().split(" ")[-1]
        compDetails = pgData[2].find('table').find_all('tr')[1:]
        compDet = []
        for j in compDetails:
            tempComp = j.find_all('td')
            compDet.append({'program': tempComp[1].get_text(), 'gross': int(tempComp[3].get_text().replace(',', '')),
                            'ctc': int(tempComp[4].get_text().replace(',', '')), 'cat': tempComp[5].get_text()})

        ###########selection process####################
        selection = []
        selProc = pgData[3].find('table').find_all('tr')[1:]
        for j in selProc:
            tempSel = j.find_all('td')
            try:
                duration = tempSel[1].get_text()
            except:
                duration = 'NA'
            selection.append({'process': tempSel[0].get_text(), 'duration': duration})

        ########additional info################33
        try:
            addInfo = pgData[4].find('div').get_text('\n')
        except:
            addInfo = 'NA'

        comRes = data[i]
        comRes['jobDetails'] = jobDetails
        comRes['postingLoc'] = postingLoc
        comRes['AccoDet'] = AccoDet
        comRes['bondApp'] = bondApp
        comRes['depts'] = depts
        comRes['deptsIDC'] = deptsIDC
        comRes['currType'] = currType
        comRes['compDet'] = compDet
        comRes['selection'] = selection
        comRes['addInfo'] = addInfo
        res.append(comRes)
    except:
        undone.append(i)
        print('error')


for i in undone:
    print(i+1, len(data),data[i]['id'])
    try:
        driver.get('https://campus.placements.iitb.ac.in/applicant/job/{}'.format(data[i].get('id')))
        time.sleep(3)  # depending on your internet speed and account safety
        # pgData = driver.find_element(By.CLASS_NAME, 'container p-5')
        # tried using selenium find elements but not working
        # alternative
        page = driver.page_source.encode('utf-8')
        soup = BeautifulSoup(page, 'html.parser')
        pgData = soup.find('div', {'class': 'container p-5'})
        pgData = pgData.find_all('div', {'class': 'panel mt-3 mb-3 d-flex flex-column'})

        ##########job info###############
        jobDetails = pgData[0].find('div').get_text('\n')
        tempVar = pgData[0].find_all('table')
        tempVar2 = tempVar[0].find_all('tr')[-1].find_all('td')
        try:
            postingLoc = tempVar2[0].get_text()
        except:
            postingLoc = 'NA'
        try:
            AccoDet = tempVar2[1].get_text()
        except:
            AccoDet = 'NA'
        try:
            bondApp = tempVar[-1].find_all('tr')[-1].find('td').get_text()
        except:
            bondApp = 'NA'

        #########eligibility criteria
        elg = pgData[1].find_all('table')

        elgCriteria = elg[0].find('tbody').find_all('tr')
        depts = []
        for j in range(len(elgCriteria)):
            chkBoxes = elgCriteria[j].find_all('td')[1:]
            dept = []
            for k in chkBoxes:
                box = k.find('div')
                """
                if len(box.contents)==0:
                    dept.append(False)
                else:
                    if 'mat-checkbox-checked' not in box.find('mat-checkbox')['class']:
                        dept.append(False)
                    else:
                        dept.append(True)
                        """
                try:
                    if 'mat-checkbox-checked' not in box.find('mat-checkbox')['class']:
                        dept.append(False)
                    else:
                        dept.append(True)
                except:
                    dept.append(False)
            depts.append(dept)

        elgCriteriaIDC = elg[1].find('tbody').find_all('tr')
        deptsIDC = []
        for j in range(len(elgCriteriaIDC)):
            chkBoxes = elgCriteriaIDC[j].find_all('td')[1:]
            dept = []
            for k in chkBoxes:
                box = k.find('div')
                try:
                    if 'mat-checkbox-checked' not in box.find('mat-checkbox')['class']:
                        dept.append(False)
                    else:
                        dept.append(True)
                except:
                    dept.append(False)
                """
                if len(box.contents) == 0 or 'mat-checkbox-checked' not in box.find('mat-checkbox')['class']:
                    dept.append(False)
                else:
                    dept.append(True)
                    """
            deptsIDC.append(dept)

        ###########compensation details#############
        currType = pgData[2].find('p').get_text().split(" ")[-1]
        compDetails = pgData[2].find('table').find_all('tr')[1:]
        compDet = []
        for j in compDetails:
            tempComp = j.find_all('td')
            compDet.append({'program': tempComp[1].get_text(), 'gross': int(tempComp[3].get_text().replace(',', '')),
                            'ctc': int(tempComp[4].get_text().replace(',', '')), 'cat': tempComp[5].get_text()})

        ###########selection process####################
        selection = []
        selProc = pgData[3].find('table').find_all('tr')[1:]
        for j in selProc:
            tempSel = j.find_all('td')
            try:
                duration = tempSel[1].get_text()
            except:
                duration = 'NA'
            selection.append({'process': tempSel[0].get_text(), 'duration': duration})

        ########additional info################33
        try:
            addInfo = pgData[4].find('div').get_text('\n')
        except:
            addInfo = 'NA'

        comRes = data[i]
        comRes['jobDetails'] = jobDetails
        comRes['postingLoc'] = postingLoc
        comRes['AccoDet'] = AccoDet
        comRes['bondApp'] = bondApp
        comRes['depts'] = depts
        comRes['deptsIDC'] = deptsIDC
        comRes['currType'] = currType
        comRes['compDet'] = compDet
        comRes['selection'] = selection
        comRes['addInfo'] = addInfo
        res.append(comRes)
    except:
        undone.append(i)
        print('error')



with open('res.json', 'w') as fe:
    json.dump(res, fe)





