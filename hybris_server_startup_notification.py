'''
This script will track the commencement/ start of the Hybris server and notify the developer.

Note: When the Hybris server is set to start, this program should be explicitly started. 
This program must be called from the platform directory of the Hybris instance you are starting.
(This process can be automated by including the batch command "start /B python <DIRECTORY_NAME>\hybris_server_startup_notification.py
" in the hybrisserver.bat file, which can be found in the Hybris platform directory.)

@author Dhyanaja Alva A
'''
import glob, os, time
from win10toast import ToastNotifier


HYBRIS_SERVER_STARTUP_NOTIFICATION_MESSAGE = 'Hybris Server Started'
HYBRIS_SERVER_STARTUP_NOTIFICATION_SUB_MESSAGE = ' '

SERVER_STARTUP = 'Server startup'
LAUNCHING_A_JVM = 'Launching a JVM'
CONSOLE_LOG_FILES = f'{os.getcwd()}/../../log/tomcat/console-*'

def get_the_latest_console_log_file():
    console_log_files = glob.glob(CONSOLE_LOG_FILES)
    latest_console_log_file = max(console_log_files, key=os.path.getctime)
    
    return latest_console_log_file
    
def wait_until_server_startup_message_appears_in_the_console_log_file(console_log_file):
    while True:
        time.sleep(2)

        console_logs = get_console_log_file_content(console_log_file) 
        if console_logs.rfind(SERVER_STARTUP) > console_logs.rfind(LAUNCHING_A_JVM):
            return

def get_console_log_file_content(console_log_file_name):       
    with open(console_log_file_name) as console_log_file:
        console_log_file_content = console_log_file.read()
    
    return console_log_file_content
            
def show_windows_notification():
    toaster = ToastNotifier()
    toaster.show_toast(HYBRIS_SERVER_STARTUP_NOTIFICATION_MESSAGE, HYBRIS_SERVER_STARTUP_NOTIFICATION_SUB_MESSAGE)
   
def main():
    time.sleep(3)
    
    latest_console_log_file = get_the_latest_console_log_file()    
    wait_until_server_startup_message_appears_in_the_console_log_file(latest_console_log_file)
    show_windows_notification()

if __name__ == '__main__':
    main()
    
