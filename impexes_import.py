'''
This script will automate the task of importing ImpEx files from the CCv2 ImpEx files import directory
to the Hybris HAC ImpEx Import console when there are numerous ImpEx files that need to be imported and order is a constraint.
(For instance, the bdbinitialdata\resources\bdbinitialdata\import directory found in the Galaxy project's CCv2's Bdbinitialdata extension
(It can be used primarily in CCv2 local setup.)

This script can be useful if you have numerous difficult-to-manage Unresolved issues with ImpEx Importing.

@author Dhyanaja Alva A
'''
import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning) 

import os, time
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


CHROMEDRIVER_PATH = './chromedriver'
HAC_IMPEX_IMPORT_URL = 'https://localhost:9002/console/impex/import'
HAC_LOGIN_USERNAME = 'admin'
HAC_LOGIN_PASSWORD = 'nimda'
IMPORTING_IMPEX_DIRECTORY = r'C:\CCv2\galaxy_ccv2\hybris\bin\custom\bdb\bdbinitialdata\resources\bdbinitialdata'
IMPORTING_IMPEX_DIRECTORY = r'C:\CCv2\embecta_ccv2\hybris\bin\custom\bdinitialdata\resources\bdinitialdata\import\coredata'

ENABLE_LOGGING = 'enable-logging'
EXCLUDE_SWITCHES = 'excludeSwitches'
IGNORE_CERTIFICATE_ERRORS = '--ignore-certificate-errors'
IGNORE_SSL_ERRORS_YES = '--ignore-ssl-errors=yes'

BODY = 'body'
ENTER = 'enter'
IMPORT_FINISHED_SUCCESSFULLY_MESSAGE = 'Import finished successfully'
J_USERNAME = 'j_username'
J_PASSWORD = 'j_password'
TAB = 'tab'

class ImpExImportManager:
    def __init__(self):
        self.__impex_files = self.__get_all_impex_files_to_be_imported()
    
    def are_all_impex_files_processed(self):
        import_statuses_for_impex_files = self.__impex_files.values()
        are_all_impex_files_processed = all(import_statuses_for_impex_files)

        return are_all_impex_files_processed

    def get_all_unprocessed_impex_files(self):
        unprocessed_impex_files = filter(lambda impex_file: not impex_file[1], self.__impex_files.items())
        unprocessed_impex_files = map(lambda impex_file: impex_file[0], unprocessed_impex_files)

        return unprocessed_impex_files
        
    def set_impex_file_is_being_processed(self, impex_file):
        self.__impex_files[impex_file] = True

    def __get_all_impex_files_to_be_imported(self):
        impex_files = dict()
        
        for (dirpath, _, filenames) in os.walk(IMPORTING_IMPEX_DIRECTORY):
            impex_files.update({os.path.join(dirpath, file): False for file in filenames})

        return impex_files

def log_in_to_hac(driver):
    username_element = driver.find_element(By.NAME, J_USERNAME)
    username_element.send_keys(HAC_LOGIN_USERNAME)

    password_element = driver.find_element(By.NAME, J_PASSWORD)
    password_element.send_keys(HAC_LOGIN_PASSWORD)
    password_element.send_keys(Keys.RETURN)

def main():
    options = webdriver.ChromeOptions()
    options.add_argument(IGNORE_SSL_ERRORS_YES)
    options.add_argument(IGNORE_CERTIFICATE_ERRORS)
    options.add_experimental_option(EXCLUDE_SWITCHES, [ENABLE_LOGGING])

    driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)
    driver.get(HAC_IMPEX_IMPORT_URL)

    log_in_to_hac(driver)

    impex_import_manager = ImpExImportManager()

    while not impex_import_manager.are_all_impex_files_processed():
        is_there_at_least_one_successful_import_in_this_round = False

        for impex_file in impex_import_manager.get_all_unprocessed_impex_files():
            try:
                # Navigate to the Import Script tab.
                import_script_tab_element = driver.find_element(By.XPATH, '//a[@href="#tabs-2"]')
                import_script_tab_element.click()

                # Click the Choose File button.
                time.sleep(1)
                actions = ActionChains(driver) 
                actions.send_keys(Keys.TAB + Keys.RETURN).perform()

                # Open the file in the Open File Dialog box.
                time.sleep(1)
                pyautogui.write(impex_file)
                pyautogui.press(TAB, interval=0.25)
                pyautogui.press(TAB, interval=0.25)
                pyautogui.press(TAB, interval=0.25)
                pyautogui.press(ENTER, interval=0.25)

                # Click the Import File button.
                time.sleep(1)
                import_file_button_element = driver.find_element(By.XPATH, '//input[@value="Import file"]')
                import_file_button_element.click()

                body_element = driver.find_element(By.TAG_NAME, BODY)
                body_element_text = body_element.text
                if IMPORT_FINISHED_SUCCESSFULLY_MESSAGE in body_element_text:
                    impex_import_manager.set_impex_file_is_being_processed(impex_file)
                    is_there_at_least_one_successful_import_in_this_round = True

            finally:
                driver.get(HAC_IMPEX_IMPORT_URL)

        if not is_there_at_least_one_successful_import_in_this_round:
            break

    print('The import of ImpEx files is finished.')

    print('Unable to import the following ImpEx files.:')
    for index, impex_file in enumerate(impex_import_manager.get_all_unprocessed_impex_files()):
        print(f'{index + 1} - {impex_file}')

if __name__ == '__main__':
    main()