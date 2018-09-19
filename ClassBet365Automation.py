# -*- coding: cp1252 -*-
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd
import numpy as np
import os
import logging
import time
import sys
import traceback
sys.path.insert(0, "D:\Wetten\Odd Scraper")
import EigeneExceptions as eex


# Zu Erledigen:


# Verbesserungen:

# Wait für Ausklappen von Menüs(Javascript) ?? Einfach sleep()? -> Außerdem erstmal alle ausklappfunktionen mit sleep(1) versehen
# Durch Multithreading verschnellern
# Headless Browser



class Bet365Automation:
    def __init__(self, username='', password=''):
        self.username = username
        self.password = password
        self.data_path = 'Dateien'
        self.main_url = 'https://www.bet365.com/de/'
        self.driver = webdriver.Chrome('D:\Wetten\Odd Scraper\chromedriver')
        self.driver.implicitly_wait(5) # seconds
        self.error = False
        self.logger = 1
        self.init_logger()
        self.oddsFussball = pd.DataFrame()
        self.oddsFussballColumns = ['Country', 'Leaque', 'Data', 'Time', 'Hometeam', 'Awayteam', 'Homeodd', 'Drawodd', 'Awayodd']
        self.driver.get(self.main_url)
        self.debug = 1
        if not os.path.exists(self.data_path):
            os.mkdir(self.data_path)
        
##        self.click_to_main()
##        if self.error is False:
##            #self.get_screen()
##            self.get_Endergebnisse()
##            self.saveOddsAsExcel()
##        if self.error is False:
##            self.login()
##        sleep(5)
##        if self.error is False:
##            self.logout()

            
        #input('Kurzes Peauschen!')
        sleep(3)
        #self.driver.close()
        
    def execute(self):

    # Ablauf: 1. Klick zu Hauptseite; 2. Klick zur Fussballseite; 3. Elemente 'MarketGroup' holen -> MarketGroup[0] = 'Endergebnisse'; 4. Ländergruppen holen; 5. Iteration über Ländergruppen
    # 6. Liste der Ligen innerhalb jeweiliger Ländergruppe holen; # 7. Iteration über Liste der Ligen; 8. Aller vorigen Elemente wieder erfassen (MarketGroup[0], Ländergruppe, Liga ... Indexe Ländergruppe und Liga werden übergeben); 9. Klick auf Liga
    # 10. Begegnungen pro Liga scrapen; 11. Return von Ligaseite mit Partien
        if self.error is False:
            self.click_to_main()
            self.get_Endergebnisse()
##            self.saveOddsAsExcel("Bet365_Fussball_Odds")

        

    def init_logger(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(levelname)s:%(asctime)s:%(name)s:%(message)s')
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        log_name = "Bet365Logger.log"
        log_path = "Log"
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        file_handler = logging.FileHandler(os.path.join(log_path, log_name))
        file_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)
        self.logger.addHandler(file_handler)
        


    def get_screen(self):
        sleep(3)
        file_name = 'screenshot.png'
        file_path = os.path.join(self.data_path, file_name)
        self.logger.debug(type(self.driver.page_source))
        self.driver.get_screenshot_as_file(file_path) 


    def click_to_main(self):
    # 1. Klick zu Hauptseite
        try:
            sport_block = self.driver.find_element_by_xpath('//div[@id="dv1"]')
            sport_block.click()
        except Exception as e:
            self.error = True
            self.logger.error(e)
            self.logger.error(traceback.format_exc())
        

        

    def login(self):
        try:
            sleep(5)
            input_username = self.driver.find_element_by_xpath('//div[@class="hm-Login_UserNameWrapper "]/input[@class="hm-Login_InputField "]')
            input_username.send_keys(self.username)
            input_password_text = self.driver.find_element_by_xpath('//div[@class="hm-Login_PasswordWrapper "]/input[@type="text"]')
            input_password_text.click()
            sleep(2)
            input_password = self.driver.find_element_by_xpath('//div[@class="hm-Login_PasswordWrapper "]/input[@class="hm-Login_InputField "]')
            input_password.send_keys(self.password)
            sleep(2)
            ok_button = self.driver.find_element_by_xpath('//div[@class="hm-Login_PasswordWrapper "]/button[@class="hm-Login_LoginBtn "]')
            ok_button.click()
            
        except Exception as e:
            self.error = True
            self.logger.error('Funktion "login": Login Felder konnten nicht gefunden werden!')
            self.logger.error(e)



    def get_Endergebnisse(self):
    # 2. Klick zur Fussballseite
        if self.error is False:
            self.navigate_to_football()
##    # 3. Elemente 'MarketGroup' holen -> MarketGroup[0] = 'Endergebnisse'
##        if self.error is False:
##            try:
##                #self.driver.find_element_by_xpath('//div[@class="sm-MarketGroup "]') # Um in die Exception zu springen, weil .find_elements_by_xpath(...) eine leere Liste bei nicht vorhandenen Elementen zurückgibt, wodurch die Fehleroutine nicht ausgelöst wird
##                marketGroups = self.driver.find_elements_by_xpath('//div[@class="sm-MarketGroup "]')
##                assert len(marketGroups) != 0 # Test, ob marketGroups gefunden wurden
##
##                # Element MarketGroup[0] = 'Endergebnisse' wird falls notwendig aufgeklappt
##                try:
##                    if marketGroups[0].find_element_by_class_name('sm-MarketGroup_HeaderClosed '):
##                        marketGroups[0].click()
##                        sleep(1)
##                except Exception:
##                    pass
##                
##            except Exception as e:
##                self.error = True
##                self.logger.error(e)
##                self.logger.error(traceback.format_exc())
##            
##        if self.error is False:
##    # 4. Ländergruppen holen 
##            try:
##                #marketGroups[0].find_element_by_class_name('sm-Market ') # Um in die Exception zu springen, weil .find_elements_by_class_name(...) eine leere Liste bei nicht vorhandenen Elementen zurückgibt, wodurch die Fehleroutine nicht ausgelöst wird
##                countries = marketGroups[0].find_elements_by_class_name('sm-Market ')
##                assert len(countries) != 0 # Test, ob countries gefunden wurden
##                
##            except Exception as e:
##                self.error = True
##                self.logger.error(e)
##                self.logger.error(traceback.format_exc())
##                
##    # 5. Iteration über Ländergruppen
##            if self.error is False:
##                    for index_countries in range(4, 5):
##                        if index_countries > 0:
##
##                            # Elemente 'MarketGroup' holen -> MarketGroup[0] = 'Endergebnisse' (Muss pro Iteration wiederholt werden, weil immer von der letzten Liga zurückgesprungen wird)
##                            if self.error is False:
##                                try:
##                                    #self.driver.find_element_by_xpath('//div[@class="sm-MarketGroup "]') # Um in die Exception zu springen, weil .find_elements_by_xpath(...) eine leere Liste bei nicht vorhandenen Elementen zurückgibt, wodurch die Fehleroutine nicht ausgelöst wird
##                                    marketGroups = self.driver.find_elements_by_xpath('//div[@class="sm-MarketGroup "]')
##                                    assert len(marketGroups) != 0 # Test, ob marketGroups gefunden wurden
##
##                                    # Element MarketGroup[0] = 'Endergebnisse' wird falls notwendig aufgeklappt
##                                    try:
##                                        if marketGroups[0].find_element_by_class_name('sm-MarketGroup_HeaderClosed '):
##                                            marketGroups[0].click()
##                                            sleep(1)
##                                    except Exception:
##                                        pass
##                                    
##                                except Exception as e:
##                                    self.error = True
##                                    self.logger.error(e)
##                                    self.logger.error(traceback.format_exc())
##                        
##
##                            # Ländergruppe unter 'Ergebnisse' holen
##                            if self.error is False:
##                                try:
##                                    marketGroups[0].find_element_by_class_name('sm-Market ')# Um in die Exception zu springen, weil .find_elements_by_class_name(...) eine leere Liste bei nicht vorhandenen Elementen zurückgibt, wodurch die Fehleroutine nicht ausgelöst wird
##                                    element_country = marketGroups[0].find_elements_by_class_name('sm-Market ')[index_countries]
##                                    countrytext = element_country.find_element_by_class_name('sm-Market_GroupName ').text
##                                    self.logger.info("Ländergruppe {} von {}: {}".format(index_countries, len(countries)-1, countrytext.encode('utf-8').decode('ascii', "ignore")))
##
##                                    # Ländergruppe unter 'Endergebnisse' wird aufgeklappt falls notwendig
##                                    try:
##                                        element_country_headerclosed = element_country.find_element_by_xpath('.//div[@class="sm-Market_HeaderClosed "]')
##                                        element_country_headerclosed.click()
##                                        sleep(1)
##                    
##                                    except Exception:
##                                        pass
##                        
##                                except Exception as e:
##                                    self.error = True
##                                    self.logger.error(e)
##                                    self.logger.error(traceback.format_exc())
##                                    
##                                
##    # 6. Liste der Ligen innerhalb jeweiliger Ländergruppe holen
##                            if self.error is False:
##                                try:
##                                    #element_country.find_element_by_xpath('.//div[@class="sm-CouponLink sm-CouponLinkSelectable "]') # Um in die Exception zu springen, weil .find_elements_by_xpath(...) eine leere Liste bei nicht vorhandenen Elementen zurückgibt, wodurch die Fehleroutine nicht ausgelöst wird
##                                    ligalist = element_country.find_elements_by_xpath('.//div[@class="sm-CouponLink sm-CouponLinkSelectable "]')
##                                    assert len(ligalist) != 0
##                                    
##                                except Exception as e:
##                                    self.error = True                                    
##                                    self.logger.error(e)
##                                    self.logger.error(traceback.format_exc())
##                                                
##    # 7. Iteration über Liste der Ligen
##                            if self.error is False:
##                                # Durch jede Liga im jeweiligen Land wird iteriert
##                                for liga in ligalist:
##                                    print liga.text
##                                for index_liga in range(6):
##                                #for index_liga in range(2,3): 
##                                    # MarketGroup 'Endergebnisse' wird falls notwendig wieder aufgeklappt
##                                    # Ländergruppen unter 'Endergebnisse' werden aufgeklappt
##                                    # Ligen in Ländern werden nacheinnder abgearbeitet
##                                    
##    # 8. Aller vorigen Elemente wieder erfassen (MarketGroup[0], Ländergruppe, Liga ... Indexe Ländergruppe und Liga werden übergeben); 9. Klick auf Liga; 10. Begegnungen pro Liga scrapen; 11. Return von Ligaseite mit Partien
##                                    self.openMarketGroup(index_countries, index_liga)
##
##                            #if index_countries == 1: break      
##
##
##
    def navigate_to_football(self):
    # 2. Klick zur Fussballseite
        try:
            football_button = self.driver.find_element_by_xpath('//div[@class="wn-WebNavModule "]//div[contains(text(), "Fu") and contains(text(), "ball")]')
            football_button.click()
        except Exception as e:
            self.error = True
            self.logger.error(e)
            self.logger.error(traceback.format_exc())


            
    def openMarketGroup(self, index_countries, index_liga):

    # 8. Aller vorigen Elemente wieder erfassen (MarketGroup[0], Ländergruppe, Liga ... Indexe Ländergruppe und Liga werden übergeben)

        if self.error is False:
            # Elemente 'MarketGroup' holen -> MarketGroup[0] = 'Endergebnisse'
            try:
                #self.driver.find_elements_by_xpath('//div[@class="sm-MarketGroup "]') # Um in die Exception zu springen, weil .find_elements_by_class_name(...) eine leere Liste bei nicht vorhandenen Elementen zurückgibt, wodurch die Fehleroutine nicht ausgelöst wird
                marketGroups = self.driver.find_elements_by_xpath('//div[@class="sm-MarketGroup "]')
                assert len(marketGroups) != 0

                # MarketGroup 'Endergebnisse' wird falls notwendig wieder aufgeklappt
                try:
                    if marketGroups[0].find_element_by_class_name('sm-MarketGroup_HeaderClosed '):
                        marketGroups[0].click()
                        sleep(1)
                except Exception:
                    pass
                
            except Exception as e:
                    self.error = True
                    self.logger.error(e)
                    self.logger.error(traceback.format_exc())

        # Ländergruppe unter 'Ergebnisse' holen
        if self.error is False:
            try:
                marketGroups[0].find_element_by_class_name('sm-Market ')# Um in die Exception zu springen, weil .find_elements_by_class_name(...) eine leere Liste bei nicht vorhandenen Elementen zurückgibt, wodurch die Fehleroutine nicht ausgelöst wird
                element_country = marketGroups[0].find_elements_by_class_name('sm-Market ')[index_countries]
                countrytext = element_country.find_element_by_class_name('sm-Market_GroupName ').text

                # Ländergruppe wird falls notwendig wieder aufgeklappt
                try:
                    element_country_headerclosed = element_country.find_element_by_xpath('.//div[@class="sm-Market_HeaderClosed "]')
                    element_country_headerclosed.click()
                    sleep(1)
                except Exception:
                    pass
                
            except Exception as e:
                self.error = True
                self.logger.error(e)
                self.logger.error(traceback.format_exc())

        # Liste der Liga innerhalb jeweiliger Ländergruppe holen
        if self.error is False:           
            try:
                #element_country.find_element_by_xpath('.//div[@class="sm-CouponLink sm-CouponLinkSelectable "]') # Um implicitly_wait zu aktivieren # Um in die Exception zu springen, weil .find_elements_by_xpath(...) eine leere Liste bei nicht vorhandenen Elementen zurückgibt, wodurch die Fehleroutine nicht ausgelöst wird
                ligalist = element_country.find_elements_by_xpath('.//div[@class="sm-CouponLink sm-CouponLinkSelectable "]')
                assert len(ligalist) != 0
                
            except Exception as e:
                self.error = True                
                self.logger.error(e)
                self.logger.error(traceback.format_exc())
# Hier weiter        
        # Liga holen
        if self.error is False:
            liga = ligalist[index_liga]
            ligatext = liga.text
            self.logger.info("{} von {} scrapen: {}".format(index_liga, len(ligalist)-1, ligatext.encode('utf-8').decode('ascii', "ignore")))
    # 9. Klick auf Liga
            liga.click()           
    # 10. Begegnungen pro Liga scrapen
            self.scrapeLigaOdds(ligatext, countrytext)
    # 11. Return von Ligaseite mit Partien
        if self.error is False:
            try:
                sleep(1)
                self.driver.find_element_by_class_name('cl-BreadcrumbTrail_BackButton ').click()
                sleep(1)
            except Exception as e:
                self.error = True            
                self.logger.error(e)
                self.logger.error(traceback.format_exc())
        if self.error is False:
            self.logger.info("Scraping Done.")
            
                

# Es werden nicht alle Ligen ordentlich gescraped - wird irgendwann abgebrochen - vermutlich Ladezeit zu lang -> sleep verlängern
# Hier weitermachen: try-except ausprobieren, wenn wettbewerb nicht da ist, dass in exception geht - soup.find_all gibt was zurück, wenn nicht gefunden? -> Schritt für Schritt und entsprechend nur für 1,2 Ligen (Schleife anpassen für Test)
    def scrapeLigaOdds(self, ligatext, countrytext):

        if self.error is False:
            self.driver.find_element_by_class_name('gl-ParticipantOddsOnly_Odds') # Gewährleistet, dass die Seite geladen ist (in Kombination mit implicitly_wait) -> Das Element gibt es nicht auf der vorigen Seite
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            self.logger.info("Soup geholt!")

            # Findet Modul, wo alles drin steht
            try:
                modul = soup.find('div', attrs = {"class":"gl-MarketGrid"})

                if modul is None:
                    raise eex.NonTypeError("Funktion 'scrapeLigaOdds': modul in soup wurde nicht gefunden!")

            except eex.NonTypeError as e:
                self.error = True
                self.logger.error("NonTypeError: {}".format(e.data))
                self.logger.error(e)
                
        if self.error is False:

                try:
                    # Findet Container, wo Endergebnisse der Liga drin stehen
                    contain_endergebnisse = modul.find('div', attrs = {"class":"gl-MarketGroup"})

                    if contain_endergebnisse is None:
                        raise eex.NonTypeError("Funktion 'scrapeLigaOdds': contain_endergebnisse('class':'gl-MarketGroup') wurde nicht gefunden!")

                    # Findet Wrapper, wo Endergebnisse der Liga drin stehen
                    group_wrapper = contain_endergebnisse.find('div', attrs = {"class":"gl-MarketGroup_Wrapper"})

                    if group_wrapper is None:
                        raise eex.NonTypeError("Funktion 'scrapeLigaOdds': group_wrapper('class':'gl-MarketGroup_Wrapper') wurde nicht gefunden!")

                    # Findet 5 Container, in denen unmittelbar die Begegnungen und Quoten ausgegeben werden (in liste gespeichert)
                    contain_games = group_wrapper.div.contents

                    
                    

                except AttributeError as e:
                    self.error = True
                    self.logger.error('Funktion "scrapeLigaOdds": Ein Element (group_wrapper.div) wurde nicht gefunden!')
                    self.logger.error(e)
                except eex.NonTypeError as e:
                    self.error = True
                    self.logger.error("NonTypeError: {}".format(e.data))
                    self.logger.error(e)

                # contain_games[0] -> Container, wo Datum, Uhrzeit und Mannschaften enthalten sind
                # contain_games[1] -> Heim-Quote
                # contain_games[2] -> Unentschieden-Quote
                # contain_games[3] -> Auswärts-Quote
                # Iteriert wird über len(contain_games[0].contents)
        if self.error is False:
                self.logger.info(len(contain_games[0]))

                if self.error is False:
                    
                    try:
                        begegnungen = contain_games[0].contents
                        home_odds = contain_games[1].contents
                        draw_odds = contain_games[2].contents
                        away_odds = contain_games[3].contents
                        
                    except AttributeError as e:
                            self.error = True
                            self.logger.error('Funktion "scrapeLigaOdds": Einen der Container contain_games[x] nicht gefunden!')
                            self.logger.error(e)
                
                for i in range(len(contain_games[0])):

                    if self.error is False:
                        
                        try:
                            
                            # Datum holen
                            if 'sl-MarketHeaderLabel_Date' in begegnungen[i]['class']:
                                self.logger.info("Datum!")
                                date = begegnungen[i].text           
                            # Rest holen, in Form bringen (als DataFrame) und in DataFrame der Instanz der Klasse abspeichern  (not in -> Live-Spiele ausschließen)
                            if ('sl-CouponParticipantWithBookCloses' in begegnungen[i]['class']) and ('sl-CouponParticipantWithBookCloses_ClockPaddingLeft') not in begegnungen[i]['class']:
                                self.logger.info("Begegnung!")
                                time = begegnungen[i].contents[0].div.text
                                match = begegnungen[i].contents[1].div.text
                                print match
                                hometeam, awayteam = match.split(' v ')
                                homeodd = home_odds[i].span.text
                                drawodd = draw_odds[i].span.text
                                awayodd = away_odds[i].span.text
                                game = [countrytext, ligatext, date, time, hometeam, awayteam, homeodd, drawodd, awayodd]
                                game_df = pd.DataFrame(np.array(game).reshape(1,len(game)), columns=self.oddsFussballColumns)
                        
                                self.oddsFussball = self.oddsFussball.append(game_df, ignore_index=True)

                        except Exception as e:
                            self.error = True
                            self.logger.error('Funktion "scrapeLigaOdds": Mit einem Element in der For-Schleife (eine Begegnung) stimmt was nicht!')
                            self.logger.error(e)

              
                
        
    def logout(self):
        try:
            sleep(2)
            member_button = self.driver.find_element_by_xpath('//div[@class="hm-MembersInfoButton_AccountIcon "]')
            member_button.click()
            sleep(2)
            abmelden_button = self.driver.find_element_by_xpath('//div[contains(text(), "Abmelden")]')
            abmelden_button.click()
        except Exception as e:
            self.error = True
            self.logger.error('Funktion "logout": Logout Felder konnten nicht gefunden werden')
            self.logger.error(e)


    def saveOddsAsExcel(self, outfile):

        datum = time.strftime("%d_%m_%Y_%H_%M_%S")
        writer = pd.ExcelWriter(outfile + "_" + datum + ".xlsx")
        self.oddsFussball.to_excel(writer, 'Odds')
        writer.save()
        
        
        





if __name__ == '__main__':

    bet365 = Bet365Automation()
    bet365.execute()
    
