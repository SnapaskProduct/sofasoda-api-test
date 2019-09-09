# pyresttest-api-test
pyresttest API test scripts with slack bot

1. Install pyresttest

https://github.com/svanoort/pyresttest

2. Pull code to local machine (Builder)

3. Slack API token is saved in local machine where as /Users/twserver/Development/backup/startbot.sh, check this link about bot token info:

https://amazing-snapask.slack.com/services/220384228881?updated=1

4. Bot will be launched upon builder bootup. Config over here:

>/Library/LaunchDaemons/org.starterbot.plist

How to remove it from bootup:
>sudo launchctl unload /Library/LaunchDaemons/org.starterbot.plist

How to add it to bootup:
>sudo launchctl load /Library/LaunchDaemons/org.starterbot.plist

Reference:
https://www.fullstackpython.com/blog/build-first-slack-bot-python.html



