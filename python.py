python 1.py '{"OPLG":false, "OPLG_FOLDER": "", "OPLG_UPGRADE": false, "OPLG_UPGRADE_FOLDER": "", "SIS": false, "SIS_FOLDER": "", "GIT_AGENT": false, "GIT_AGENT_FOLDER": "", "PRIVATE_CLOUD": false, "PRIVATE_CLOUD_FOLDER": ""}
# python 1.py '{\"OPLG\":false, \"OPLG_FOLDER\": \"\", \"OPLG_UPGRADE\": false, \"OPLG_UPGRADE_FOLDER\": \"\", \"SIS\": false, \"SIS_FOLDER\": \"\", \"GIT_AGENT\": false, \"GIT_AGENT_FOLDER\": \"\", \"PRIVATE_CLOUD\": false, \"PRIVATE_CLOUD_FOLDER\": \"\"}'

# python 1.py '{\"OPLG\":\"true\", \"OPLG_FOLDER\": \"\", \"OPLG_UPGRADE\": false, \"OPLG_UPGRADE_FOLDER\": \"\", \"SIS\": false, \"SIS_FOLDER\": \"\", \"GIT_AGENT\": false, \"GIT_AGENT_FOLDER\": \"\", \"PRIVATE_CLOUD\": false, \"PRIVATE_CLOUD_FOLDER\": \"\"}'


import os
import sys
import subprocess
import json
import shutil           # for copy file
import time

PARAM_OPLG = ""
PARAM_OPLG_FOLDER = "Default_StormOPLG_dev"          # if received another version default will be replaced with new folder name



def receive_parameters():
    global PARAM_OPLG
    global PARAM_OPLG_FOLDER
    
    received_param = sys.argv[1]
    print "\nreceived_param: {}\n".format(received_param)
    params_json_data = json.loads(received_param)
    print "\nparams_json_data: {}\n".format(params_json_data)
    
    PARAM_OPLG = params_json_data["OPLG"] == "true"
    print "PARAM_OPLG: {}  {}".format(PARAM_OPLG, type(PARAM_OPLG))
    new_OPLG_FOLDER = params_json_data["OPLG_FOLDER"]
    if new_OPLG_FOLDER != "":
        PARAM_OPLG_FOLDER = new_OPLG_FOLDER
    print "PARAM_OPLG_FOLDER: {}  {}".format(PARAM_OPLG_FOLDER, type(PARAM_OPLG_FOLDER))


def add_file_progress():
    print "\nCreate file install_in_progress.txt"
    install_file = open("install_in_progress.txt", "w")
    install_file.close()


def remove_file_progress():
    print "Remove file install_in_progress"
    path = "C:\install_in_progress.txt"
    if os.path.exists(path):
        os.remove(path)


def restart_pc():
    print "RESTART after instllation"
    subprocess.call(["shutdown", "-r", "-t", "00"])


def copyFile(src, dest):
    print "COPY FILE from '{}' to '{}'".format(src, dest)
    try:
        shutil.copy(src, dest)
    # eg. src and dest are the same file
    except shutil.Error as e:
        print('Error: %s' % e)
    # eg. source or destination doesn't exist
    except IOError as e:
        print('Error: %s' % e.strerror)
    print "END COPING"


def install_product(app_path, app_name, installing_limit):
    print "\nSTART installation..."
    command = "START /WAIT {}\{} /s /a /s /norestart".format(app_path, app_name)
    print "\n{}".format(command)
    subprocess.call(command, shell = True)
    
    print "\nINSTALLING {}...".format(app_name)
    if app_name == "StormRunnerLoadGenerator.exe":
        app_name = "StormRunnerLGSetup.exe"
    start_time = time.time()
    while True:
        if (time.time() - start_time) > installing_limit:
            print "running too long"
            break
        
        time.sleep(30)
        tmp = os.popen("tasklist").read()
        if app_name in tmp:
            print "{} running".format(app_name)        
        else:
            print "{} not running".format(app_name)
            break
    
    elapsed_time = time.time() - start_time
    print "elapsed_time: {}".format(elapsed_time)
    
    print "\nWAIT FOR END OF INSTALLING..."
    cur_finish_process_name = "stormagent_cfg.exe"
    start_time = time.time()
    while True:
        if (time.time() - start_time) > installing_limit:
            print "running too long"
            break
    
        time.sleep(30)
        tmp = os.popen("tasklist").read()
        if cur_finish_process_name in tmp:
            print "{} running".format(cur_finish_process_name)
            print "installing ended"
            break
        else:
            print "{} not running".format(cur_finish_process_name)


def create_workspace_dir():
    print "\nCreate WORKSPACE dir"
    command = "mkdir c:\WORKSPACE"
    print "\n{}".format(command)
    subprocess.call(command, shell = True)


def mount_disk():
    print "\nMOUNT P:"
    command = "if not exist P: net use P: \\\\server.net\products /user:emea\username userpass /persistent:no"
    print "\n{}".format(command)
    subprocess.call(command, shell = True)


def unmount_disk():
    print "\nUNMOUNT P:"
    command = "if exist P: net use P: /delete /y"
    print "\n{}".format(command)
    subprocess.call(command, shell = True)
    
        
#def run_subprocess(cur_command):
 #   process = subprocess.call(command, shell = True, stdout=subprocess.PIPE)
  #  process.wait()
   # if process.returncode == 0:
#        print "sucess"
 #   else:
  #      print "error"


    

print "**************************************************"
print "\nPYTHON SCRIPT STARTED"
receive_parameters()

#add_file_progress()
create_workspace_dir()
mount_disk()

copyFile("P:\LT\STORM\win32_release\Default_StormOPLG_dev\StormRunnerLoadGenerator.exe", "C:\WORKSPACE\StormRunnerLoadGenerator.exe")

if PARAM_OPLG:
	#
    install_product("C:\WORKSPACE", "StormRunnerLoadGenerator.exe", 1800)       # 1800 - 30 minutes

#unmount_disk()

#remove_file_progress()

print "FINISH"

#restart_pc()