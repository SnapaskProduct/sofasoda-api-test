import os
import time
import subprocess
from slackclient import SlackClient

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"
UAT_SOFASODA_API_TEST = "uat_sofasoda_api_test"
LOG = "dump_log"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


        
def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
               "* command to see what can I do for you."
    if command.startswith(EXAMPLE_COMMAND):
        response = "`%s` Proceed UAT SOFASODA API regression test\n`%s` Dump debug log for last run" %(UAT_SOFASODA_API_TEST,LOG)
        
    if command.startswith(UAT_API_TEST):
        slack_client.api_call("chat.postMessage", channel=channel, text="Running " + command + "...", as_user=True)
        bashCommand = "./uatsofasodaapitest.sh || true"
        subprocess.check_output(['bash','-c', bashCommand])       
        f = open('log.txt', 'r')
        log = f.readlines()
        f.close()
        newf = open('Slack.msg', 'w')
        runFail = False
        for line in log:
            if 'testsuite SUCCEEDED' in line:
                line = line.replace("[92m", ":white_check_mark:")
                line = line.replace("[0m", "")
                newf.write(line)
            elif 'testsuite FAILED' in line:
                runFail = True
                line = line.replace("[91m", ":x:")
                line = line.replace("[0m", "")
                newf.write(line)
        if runFail:        
            newf.write('<@U5MG4NSE4> <@U6YP9GR0C> <@UCQ830H7X> some cases were fail, please check!')
        newf = open('Slack.msg', 'r')            
        response = newf.read()
        
    if command.startswith(LOG):
        f = open('logErr.txt', 'r')
        log = f.read()
        f.close()
        response = "```" + log + "```"
        
    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None
    
    
if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("SofasodaBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
