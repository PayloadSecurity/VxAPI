####
# 15/11/2015 - Automatically process & E-Mail notify script for a VxStream Sandbox Webservice - (C) Payload Security
#
# Note: see "CONFIG SECTION" for details on how to setup
# ------------------------------
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from os import listdir, remove
from os.path import isfile
import os, sys, gzip
import time
import warnings
from StringIO import StringIO
import requests
import hashlib, traceback
import shutil 
import logging 
import time

###################################CONFIG SECTION####################################
# please use double backslashes. e.g. C:\\path\\path
monitorFolderPath = "monitorFolder"

defaultEnvironmentId = "1"
#Here you can enter a relative or absolute path, if using absolute on windows
# smtp server and port to be used when sending emails
smtp_server = "smtp.gmail.com"
port = 465
# The email address from which emails will be sent
from_addr = "noreply@payload-security.com"
# to_addr is a list of receivers
to_addr = "yourmail@test.com"
# username and password to be used when logging in 
username = "mailer@payload-security.com"
password = ""
subject = "Status update"

#Interval for which to check the updates
sleep_interval = 5

#id to use
environmentId = 1

#Summary API
apikey = ""
secret = ""
server = "https://<client>.vxstream-sandbox.com/api/"
verify = False

#Timeout for sending emails in seconds 
timeout = 45
################################END OF CONFIG######################################

user_agent = {'User-agent': 'VxStream Sandbox'}

logger = logging.getLogger("CORE")
logger.setLevel(logging.INFO)
fh = logging.FileHandler('core.log')
fh.setLevel(logging.INFO)
# create console handler with same log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - \n\t%(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
# Comment or uncomment the line bellow to get console output
logger.addHandler(ch)

#Threat Levels
threatLevels = ["No specific threat", "Suspicious", "Malicious"]

def join_path(p1, p2 = ""):
    if type(p1) is list:
        return os.path.join(*(p1 + [p2]))
    else:
        return os.path.join(p1, p2)

done_p = join_path(monitorFolderPath, "done")
inprogress_p = join_path(monitorFolderPath, "inprogress")
error_p = join_path(monitorFolderPath, "error")

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def clean_empty_dirs(path):
    for f in os.listdir(path):
        if os.path.isdir(join_path(path, f)):
            if os.listdir(join_path(path, f)) == [] and f != "done" and f != "inprogress" and f != "error":
                os.rmdir(join_path(path, f))

def get_summary(sha256):
    params = {'apikey': apikey, 'secret': secret, 'environmentId': environmentId}
    res = requests.get(server + "summary/" + sha256, headers=user_agent, params=params, verify=verify)
    data = res.json()
    if data["response_code"] == 0:
        return data["response"]
    else:
        return {}

def form_html_for_files(files, summaries):
    html_files = "The processed files are: <br>"
    for id in range(len(files)):
        html_files += "<b>NAME: {} </b><br>".format(files[id][0])
        if summaries[id] is not None:
            #Make some simple field replacements in summary
            summaries[id]["Threat Score"] = "{}/100".format(summaries[id]['confidence'])
            summaries[id].pop('confidence', None)
            summaries[id]["verdict_threatlevel"] = threatLevels[int(summaries[id]["verdict_threatlevel"])]

            for s_key in summaries[id].keys():
                html_files += ">>> {}: {} <br>".format(s_key, summaries[id][s_key])
        html_files += "<br>"
    return html_files
                            
def post(f_name, environmentid):
    f = open(f_name, "rb")
    files = {"file": f}
    data = {'apikey': apikey, 'secret': secret, 'environmentId': environmentid}
    try:
        submitUrl = server + "submit"
        res = requests.post(submitUrl, headers=user_agent, data=data, files=files, verify=verify)
        if res.status_code == 200:
            logger.info("Submitted file to VxStream Sandbox successfully: {}\n[Your SHA256: {}]".format(
                os.path.basename(f_name),
                hashlib.sha256(open(f_name, "rb").read()).hexdigest()))
            return hashlib.sha256(open(f_name, "rb").read()).hexdigest()
        else:
            logger.info("Error code: {}, returned when uploading: {}".format(res.status_code, f.name))
        f.close()
    except requests.exceptions.HTTPError, err:
        logger.info(err.read())
        traceback.print_exc()
    return None

def submit_file(path, environmentid=defaultEnvironmentId):
    # Search files
    out = None
    if os.path.isdir(path):
        f_names = os.listdir(path)
        for f_name in f_names:
            f_name = os.path.join(path, f_name)
            if not os.path.isdir(f_name):
                out = post(f_name, environmentid)
    else:
        out = post(path, environmentid)
    return out

def get_results(sha256, type='xml', environmentId=defaultEnvironmentId, save_dir="", f_name=""):
    stateUrl = server + 'state/' + sha256
    reportUrl = server + 'result/' + sha256
    params = {'apikey': apikey, 'secret': secret, 'environmentId': environmentId}

    res = requests.get(stateUrl, headers=user_agent, params=params, verify=verify)
    data = res.json()
    if data["response_code"] == 0 and data["response"]["state"] == 'SUCCESS':
        f_out_name = os.path.join(save_dir, '{}_{}.{}'.format(f_name, sha256, type))
        logger.info("Analysis of {} seems to be completed. Downloading report type {} to <{}>".format(
            sha256, type, f_out_name))
        #Need type in params
        params = {'apikey': apikey, 'secret': secret, 'environmentId': environmentId, 'type': type}
        res = requests.get(reportUrl, headers=user_agent, params=params, verify=verify)
        if type == "json":
            #Only for json we don't need to decompress it
            f_out = open(f_out_name, 'wb')
            f_out.write(res.content)
            f_out.close()
            logger.info("Saved file successfully")
            return ["SUCCESS"]
        elif (type == 'xml' or type == 'html' or type == 'bin'):
            #For all other formats we receive gzip
            f_out = open(f_out_name, 'wb')
            try:
                gzip_file_handle = gzip.GzipFile(fileobj=StringIO(res.content))
                f_out.write(gzip_file_handle.read())
            except Exception, e:
                logger.info(e)
                traceback.print_exc()

            f_out.close()
            logger.info("Saved file successfully")
            return ["SUCCESS"]
        else:
            logger.info("Error: unknown type <{}> is being requested.".format(type))
    elif data["response_code"] == 0:
        if data["response"]["state"] == "ERROR":
            return (data["response"]["state"], data["response"]["error"])
        else:
            return [data["response"]["state"]]

def check_todo():
    # Go through all files in the todo directory and submit them for processing
    folder_queue = [""]
    while len(folder_queue) != 0:
        tmp = folder_queue.pop(0)
        base_in = join_path(monitorFolderPath, tmp)
        base_out = join_path(inprogress_p, tmp)
        files = []
        for f in listdir(base_in):
            if isfile(join_path(base_in, f)) and f != "core.py":
                logger.info("New file found: {}".format(f))
                files.append(f)
            else:
                if f != "done" and f != "inprogress" and f != "error":
                    folder_queue.append(f)
        
        for f in files:
            f_path = join_path(base_in, f)
            try:
                mkdir(base_out)
                res = submit_file(f_path, environmentId)
                if res is not None:
                    #Remove the file from todo
                    os.remove(f_path)
                    #Add the file to inprogress
                    f_out = open(join_path(base_out, f), "w")
                    #Write the sha256 to file
                    f_out.write(res)
                    f_out.close()
            except Exception, e:
                logger.error(e)
                traceback.print_exc()
   
def check_inprogress():
    # Go through everything that is inprogress and check is
    # something finished.
    folder_queue = [""]
    files_done = []
    while len(folder_queue) != 0:
        tmp = folder_queue.pop(0)
        base_in = join_path(inprogress_p, tmp)
        base_out = join_path(done_p, tmp)
        files = []
        for f in listdir(base_in):
            if isfile(join_path(base_in, f)):
                files.append(f)
            else:
                folder_queue.append(f)

        for fi in files:
            f_path = join_path(base_in, fi)
            try:
                #Read the file to check, insed of it is the sha256
                sha256 = open(f_path, "r").read().strip()
                mkdir(base_out)
                res = get_results(sha256, save_dir=base_out, f_name=fi)
                if res[0] == "SUCCESS":
                    #Remove the file from inprogress
                    os.remove(f_path)
                    files_done.append((fi, sha256))
                if res[0] == "ERROR":
                    #Move the file from inprogress to error and add the error message to it
                    logger.error("There was an error when processing file: {}. File moved to error folder".format(fi))
                    os.remove(f_path)
                    f = open(error_p + "/{}_".format(time.time()) + fi + "__error__.txt", "w")
                    f.write(res[1])
                    f.close()
            except Exception, e:
                logger.error(e)
                traceback.print_exc()
    return files_done

def send_email(files, summaries):
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject
    
    # Form a html message
    html_header = """
    <html>
    <head></head>
    <body>
    """
    html_footer = """
    </body>
    </html>
    """
    html_intro = """This is a status report from VxStream<br><br>"""
    html_dir = """Reports have been saved in: {}<br><br>""".format(join_path(done_p))
    html_files = form_html_for_files(files, summaries)       
    
    html = html_header + html_intro + html_dir + html_files + html_footer
    msg.attach(MIMEText(html, 'html'))
    
    if port == 587:
        mailserver = smtplib.SMTP(smtp_server, port, timeout=timeout)
        # identify ourselves to smtp client
        mailserver.ehlo()
        # secure our email with tls encryption
        mailserver.starttls()
        # re-identify ourselves as an encrypted connection
        mailserver.ehlo()
        mailserver.login(username, password)
    elif port == 465:
        mailserver = smtplib.SMTP_SSL(smtp_server, port, timeout=timeout)
        mailserver.ehlo()
        mailserver.login(username, password)
    else:
        #No encryption 
        mailserver = smtplib.SMTP(smtp_server, port, timeout=timeout)

    mailserver.sendmail(from_addr, to_addr, msg.as_string())
    mailserver.quit()

def start():
    #INIT everything
    warnings.filterwarnings("ignore")
    mkdir(join_path(monitorFolderPath, "inprogress"))
    mkdir(join_path(monitorFolderPath, "done"))
    mkdir(join_path(monitorFolderPath, "error"))
    logger.info("################## Monitoring started ###################")

    while True:
        done = check_inprogress()
        check_todo()
        
        summaries = []
        #Collect summaries for all processed documents
        for one in done:
            try:
                logger.info("Getting summary for: {}".format(one[0]))
                summaries.append(get_summary(one[1]))
                logger.info("Summary received for: {}".format(one[0]))
            except Exception, e:
                logger.error("There was an error: {} when getting summary for: {}".format(e, one[0]))
                summaries.append(None)
                traceback.print_exc()

        # Clean empty dirs
        clean_empty_dirs(inprogress_p)
        clean_empty_dirs(monitorFolderPath)

        if len(done) > 0:
            try:
                logger.info("Sending email")
                send_email(done, summaries)
                logger.info("---------------EMAIL SENT----------------\n")
            except Exception, e:
                logger.error("There was an error when sending email: {}".format(e))
                traceback.print_exc()

        # Wait <sleep_interval> then do everything again
        time.sleep(sleep_interval)

if __name__=="__main__":
    start()
