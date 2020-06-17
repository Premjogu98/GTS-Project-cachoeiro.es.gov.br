from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
import Global_var
import sys, os
import ctypes
import string
import requests
import urllib.request
import urllib.parse
import re
import html
from Insert_On_Datbase import create_filename,insert_in_Local


def ChromeDriver():
    File_Location = open("D:\\0 PYTHON EXE SQL CONNECTION & DRIVER PATH\\cachoeiro.es.gov.br\\Location For Database & Driver.txt", "r")
    TXT_File_AllText = File_Location.read()
    Chromedriver = str(TXT_File_AllText).partition("Driver=")[2].partition("\")")[0].strip()
    # chrome_options = Options()
    # chrome_options.add_extension('D:\\0 PYTHON EXE SQL CONNECTION & DRIVER PATH\\cachoeiro.es.gov.br\\Browsec-VPN.crx')  # ADD EXTENSION Browsec-VPN
    # browser = webdriver.Chrome(executable_path=str(Chromedriver),chrome_options=chrome_options)
    browser = webdriver.Chrome(executable_path=str(Chromedriver))
    browser.get(
        """https://chrome.google.com/webstore/detail/browsec-vpn-free-and-unli/omghfjlpggmjjaagoclmmobgdodcjboh?hl=en" ping="/url?sa=t&amp;source=web&amp;rct=j&amp;url=https://chrome.google.com/webstore/detail/browsec-vpn-free-and-unli/omghfjlpggmjjaagoclmmobgdodcjboh%3Fhl%3Den&amp;ved=2ahUKEwivq8rjlcHmAhVtxzgGHZ-JBMgQFjAAegQIAhAB""")
    for Add_Extension in browser.find_elements_by_xpath('/html/body/div[4]/div[2]/div/div/div[2]/div[2]/div'):
        Add_Extension.click()
        break
    import wx
    app = wx.App()
    wx.MessageBox(' -_-  Add Extension and Select Proxy Between 30 SEC -_- ', 'Info', wx.OK | wx.ICON_WARNING)
    time.sleep(30)  # WAIT UNTIL CHANGE THE MANUAL VPN SETTING
    browser.get("https://prefeitura.cachoeiro.es.gov.br/servicos/site.php?nomePagina=LICITACAO")
    browser.set_window_size(1024, 600)
    browser.maximize_window()
    # browser.switch_to.window(browser.window_handles[1])
    # browser.close()
    # browser.switch_to.window(browser.window_handles[0])
    # time.sleep(2)
    time.sleep(1)
    # browser.get('https://prefeitura.cachoeiro.es.gov.br/servicos/site.php?nomePagina=LICITACAO')
    # time.sleep(20)  # WAIT UNTIL CHANGE THE MANUAL VPN SETTING
    # browser.set_window_size(1024, 600)
    # browser.maximize_window()
    # browser.switch_to.window(browser.window_handles[1])
    # browser.close()
    # browser.switch_to.window(browser.window_handles[0])
    Scraping_data(browser)


# def Translate_close(text_without_translate):
#     a1 = 0
#     while a1 == 0:
#         try:
#             String2 = str(text_without_translate)
#             url = "https://translate.google.com/m?hl=en&sl=auto&tl=en&ie=UTF-8&prev=_m&q=" + str(String2) + ""
#             response1 = requests.get(str(url))
#             response2 = response1.url
#             user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
#             # url = "https://translate.google.com/m?hl=en&sl=auto&tl=en&ie=UTF-8&prev=_m&q=" + str(String2) + ""
#             headers = {'User-Agent': user_agent, }
#             request = urllib.request.Request(response2, None, headers)  # The assembled request
#             time.sleep(2)
#             try:
#                 response = urllib.request.urlopen(request)
#                 htmldata: str = response.read().decode('utf-8')
#                 trans_data = re.search(r'(?<=dir="ltr" class="t0">).*?(?=</div>)', htmldata).group(0)
#                 return trans_data
#             except:
#                 pass
#         except Exception as e:
#             a1 = 0
#             exc_type, exc_obj, exc_tb = sys.exc_info()
#             fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#             print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname,
#                   "\n", exc_tb.tb_lineno)
#             time.sleep(5)


def Scraping_data(browser):
    a = False
    while a == False:
        try:
            Reference_Number_list = []
            Reference_Number = ''
            for Reference_Number in browser.find_elements_by_xpath('//*[@id="tab_licitacoes"]'):
                Reference_Number = Reference_Number.get_attribute('innerText')
                Reference_Number = Reference_Number.partition("-")[2].partition(' ').strip().replace(" ", '')
                Reference_Number_list.append(Reference_Number)
            if Reference_Number == "":
                for tr in range(2, 40, 4):
                    for Reference_Number in browser.find_elements_by_xpath('//*[@id="customers"]/tbody/tr['+str(tr)+']/td'):
                        Reference_Number = Reference_Number.get_attribute('innerText')
                        Reference_Number = Reference_Number.partition("-")[2].partition('(')[0].strip()
                        Reference_Number_list.append(Reference_Number)
            tr = 3
            for Reference_Number_list1 in Reference_Number_list:

                SegField = []
                for data in range(42):
                    SegField.append('')
                # Reference Number

                SegField[13] = Reference_Number_list1

                # Title
                for Title in browser.find_elements_by_xpath('//*[@id="customers"]/tbody/tr['+str(tr)+']'):
                    Title = Title.get_attribute('innerText').replace('\n', '')
                    Title = Title.partition('OBJETO:')[2].partition('ABERTURA:')[0].replace('<br>', '').replace('<strong>', '').strip()
                    if Title != '':
                        # Title = Translate(str(Title))
                        Title = string.capwords(str(Title))
                        SegField[19] = Title
                    break

                # DeadLine
                for OPENING in browser.find_elements_by_xpath('//*[@id="customers"]/tbody/tr['+str(tr)+']'):
                    OPENING = OPENING.get_attribute('innerText')
                    OPENING = OPENING.partition('ABERTURA:')[2].partition('às')[0].replace('<br>', '').replace('<strong>', '').strip()
                    datetime_object = datetime.strptime(OPENING, "%d/%m/%Y")
                    OPENING = datetime_object.strftime("%Y-%m-%d")
                    SegField[24] = OPENING
                    break
                # Notice Type
                SegField[14] = "2"

                # Purchaser_Name
                SegField[12] = "CITY HALL OF ITAPEMIRIM WATERFALL"

                # Purchaser_Name
                SegField[2] = "Jeronimo Monteiro Square, 28 - Cachoeiro de Itapemirim Center - ES. ZIP Code: 29300-170"

                SegField[7] = "BR"

                SegField[1] = "semus.licitacao@cachoeiro.es.gov.br"

                SegField[22] = "0"
                SegField[26] = "0.0"

                SegField[27] = "0"  # Financier
                SegField[28] = 'https://prefeitura.cachoeiro.es.gov.br'
                SegField[31] = "cachoeiro.es.gov.br"
                SegField[18] = "Título: "+SegField[19]+"<br>\n Fecha de cierre: "+SegField[24]
                for SegIndex in range(len(SegField)):
                    print(SegIndex, end=' ')
                    print(SegField[SegIndex])
                    SegField[SegIndex] = html.unescape(str(SegField[SegIndex]))
                    SegField[SegIndex] = str(SegField[SegIndex]).replace("'", "''")
                tr += 4

                check_date(SegField)
                print(" Total: " + str(Global_var.Total) + " Duplicate: " + str(
                    Global_var.duplicate) + " Expired: " + str(Global_var.expired) + " Inserted: " + str(
                    Global_var.inserted) + " Skipped: " + str(Global_var.skipped) + " Deadline Not given: " + str(
                    Global_var.deadline_Not_given) + " QC Tenders: " + str(
                    Global_var.QC_Tender), "\n")

            ctypes.windll.user32.MessageBoxW(0, "Total: " + str(Global_var.Total) + "\n""Duplicate: " + str(
                Global_var.duplicate) + "\n""Expired: " + str(Global_var.expired) + "\n""Inserted: " + str(
                Global_var.inserted) + "\n""Skipped: " + str(Global_var.skipped) + "\n""Deadline Not given: " + str(
                Global_var.deadline_Not_given) + "\n""QC Tenders: " + str(
                Global_var.QC_Tender) + "", "cachoeiro.es.gov.br", 1)
            Global_var.Process_End()
            browser.close()
            sys.exit()

            a = True
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n",
                  exc_tb.tb_lineno)
            a = False


def check_date(SegFeild):
    tender_date = str(SegFeild[24])
    nowdate = datetime.now()
    date2 = nowdate.strftime("%Y-%m-%d")
    try:
        if tender_date != '':
            deadline = time.strptime(tender_date , "%Y-%m-%d")
            currentdate = time.strptime(date2 , "%Y-%m-%d")
            if deadline > currentdate:
                insert_in_Local(SegFeild)
                Global_var.Total += 1
            else:
                print("Tender Expired")
                Global_var.expired += 1
        else:
            print("Deadline was not given")
            Global_var.deadline_Not_given += 1
    except Exception as e:
        exc_type , exc_obj , exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Error ON : " , sys._getframe().f_code.co_name + "--> " + str(e) , "\n" , exc_type , "\n" , fname , "\n" , exc_tb.tb_lineno)


ChromeDriver()
