import os
import time
import subprocess
from slackclient import SlackClient

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
BOT_CHANNEL = os.environ.get("BOT_CHANNEL")
UAT_API_TEST = "uat_sofasoda_api_test"

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def uat_sofasoda_api_test(channel):
    """
        Proceed uat_api_test and send report to BOT_CHANNEL channel in Slack.
        BOT_CHANNEL is config at sodabot.sh in local server.
    """
    
    slack_client.api_call("chat.postMessage", channel=channel, text="Running test...", as_user=True)
    bashCommand = "./uatsofasodaapitest.sh || true"
    subprocess.check_output(['bash','-c', bashCommand])       
    f = open('log.txt', 'r')
    newf = open('Slack.msg', 'w')
    log = f.readlines()
    f.close()
    for line in log:
        if 'testsuite SUCCEEDED' in line or 'testsuite FAILED' in line:
            line = line.replace("[91m", ":x:")
            line = line.replace("[92m", ":white_check_mark:")
            line = line.replace("[0m", "")
            newf.write(line)
        
    f = open('log.txt', 'r')
    log = f.read()
    f.close()
    response = "```" + log + "```"
    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
    
    newf = open('Slack.msg', 'r')            
    response = newf.read()
    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
    

uat_sofasoda_api_test(BOT_CHANNEL)
