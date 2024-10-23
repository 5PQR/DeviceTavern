import time
import os
import sys
import http.server
import socketserver
import json
import importlib
import subprocess
import urllib.parse
from urllib.parse import unquote
import configdefaults
import config
import warnings


print("------------------------------------------------------------------------------------")
print("                                                                              ")
print("                    .M\"\"\"bgd `7MM\"\"\"Mq.   .g8\"\"8q. `7MM\"\"\"Mq.         ")
print("                   ,MI    \"Y   MM   `MM..dP'    `YM. MM   `MM.                  ")
print("                   `MMb.       MM   ,M9 dM'      `MM MM   ,M9                    ")
print("                     `YMMNq.   MMmmdM9  MM        MM MMmmdM9                     ")
print("                   .     `MM   MM       MM.      ,MP MM  YM.                     ")
print("                   Mb     dM   MM       `Mb.    ,dP' MM   `Mb.                   ")
print("                   P\"Ybmmd\"  .JMML.       `\"bmmd\"' .JMML. .JMM.              ")
print("                                              MMb                                ")
print("                                               `Ybm9'                            ")
print("====================================================================================")
print("   ______ _____ _   _ _____ _____  _____   _____ ___  _   _ ___________ _   _ ")
print("   |  _  \  ___| | | |_   _/  __ \|  ___| |_   _/ _ \| | | |  ___| ___ \ \ | |")
print("   | | | | |__ | | | | | | | /  \/| |__     | |/ /_\ \ | | | |__ | |_/ /  \| |")
print("   | | | |  __|| | | | | | | |    |  __|    | ||  _  | | | |  __||    /| . ` |")
print("   | |/ /| |___\ \_/ /_| |_| \__/\| |___    | || | | \ \_/ / |___| |\ \| |\  |")
print("   |___/ \____/ \___/ \___/ \____/\____/    \_/\_| |_/\___/\____/\_| \_\_| \_/")
                                                                           
                                                                                                                                                               
                                                                                    


print("------------------------------------------------------------------------------------")
print("    AVAILABLE ENDPOINTS: check current/builtin/ui/demo.html file")
print("------------------------------------------------------------------------------------")
print("    HELP ME MAKE MORE TOOLS AT: PATREON.COM/SPQR_AETERNUM ")
print("====================================================================================")


def get_config(name):
    if hasattr(config, name):
        return getattr(config, name)
    elif hasattr(configdefaults, name):
        return getattr(configdefaults, name)
    else:
        raise AttributeError(f"'{name}' not found in config or configdefaults")


SCRIPT_OK = True

if not get_config("DEBUG"):
    warnings.filterwarnings("ignore")
    warnings.simplefilter(action='ignore', category=FutureWarning)
    print("====================================================================================")
    print("==================                 DEBUG MODE ACTIVE!                ===============")
    print("====================================================================================")


bhaptics_initiated = False
bhaptics_player = None
class HttpHandler(http.server.BaseHTTPRequestHandler):
    
    
   
    def end_headers(self): 
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

  
    def do_GET(self):
        global bhaptics_initiated, bhaptics_player
        try:
            start_time = time.time()
            
            parsed_url = urllib.parse.urlparse(self.path)
            path = parsed_url.path
            data = getParams(self.path)
            
            
            if path == '/bhaptics':
                if not bhaptics_initiated:
                    bhaptics_player = haptic_player.HapticPlayer()
                    bhaptics_initiated = True
                var_device1 = "gloveLFrame"
                var_device2 = "GloveL"
                var_point = 0
                var_intensity = 50
                var_duration = 100
                
                
                if data.get('device1') and data['device1'] != "" : var_device1 = data['device1']
                if data.get('device2') and data['device2'] != "" : var_device2 = data['device2']
                if data.get('point') and data['point'] != "" : var_point = data['point']
                if data.get('intensity') and data['intensity'] != "" : var_intensity = data['intensity']
                if data.get('duration') and data['duration'] != "" : var_duration = data['duration']
                
                bhaptics_player.submit_dot(var_device1, var_device2, [{"index": var_point, "intensity": var_intensity}], var_duration)
                
            
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {
                    "status": "ok",
                    "device1": var_device1,
                    "device2": var_device2,
                    "point": var_point,
                    "intensity": var_intensity,
                    "duration": var_duration
                }
                self.wfile.write(json.dumps(response).encode('utf-8'))
            elif self.path == '/status':
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {
                    "status": "running"
                }
                self.wfile.write(json.dumps(response).encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()
            elapsed_time = time.time() - start_time
            print(f"Request took: {elapsed_time:.2f} seconds")
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            error_message = f"An error occurred: {str(e)}"
            print(error_message)   
            self.wfile.write(b"Internal server error occurred.")

def getParams(url):
    query_params = {}
    if '?' in url:
        query_string = url.split('?')[1]
        query_params_list = query_string.split('&')
        for param in query_params_list:
            key_value = param.split('=')
            if len(key_value) == 2:
                key_value[0] = unquote(key_value[0])
                key_value[1] = unquote(key_value[1])
                query_params[key_value[0]] = key_value[1]
    return query_params

def check_and_install_package(package_name, version=None, upgrade=False, gpu=False):
    global SCRIPT_OK
    if not SCRIPT_OK:
        return
    try:
        importlib.import_module(package_name.split('[')[0])  # Handle extras like datasets[audio]
        print(f"    {package_name} is already installed.")
    except ImportError:
        print(f"    {package_name} Checking...")
        package = package_name if version is None else f"{package_name}=={version}"
        pip_command = [sys.executable, '-m', 'pip', 'install']  # Use virtual environment's pip
        
        if upgrade:
            pip_command.append('--upgrade')
        
        else:
            pip_command.append(package)
        
        if get_config('DEBUG'):
            subprocess.call(pip_command)
        else:
            subprocess.call(pip_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print(f"    Package ok: {package_name}!")
        

# Check and install packages

check_and_install_package('websocket-client','0.57.0')
check_and_install_package('python-osc','1.7.4')
check_and_install_package('keyboard','0.13.5')


if SCRIPT_OK:
    from bhaptics import haptic_player;
    httpd = socketserver.TCPServer(('127.0.0.1', 7068), HttpHandler)
    print("====================================================================================")
    print("                 ██████  ███████  █████  ██████  ██    ██ ██ ")
    print("                 ██   ██ ██      ██   ██ ██   ██  ██  ██  ██ ")
    print("                 ██████  █████   ███████ ██   ██   ████   ██ ")
    print("                 ██   ██ ██      ██   ██ ██   ██    ██       ")
    print("                 ██   ██ ███████ ██   ██ ██████     ██    ██ ")
    print("------------------------------------------------------------------------------------")
    print("    Listening for incoming requests...")
    httpd.serve_forever()