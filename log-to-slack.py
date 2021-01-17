#Authored by George Kroon, 03/12/2020
#Script to import variables from log.csv of Ansible playbook runs and create a message to push to Slack.

from slack_webhook import Slack
import csv
import time



slack = Slack(url='https://hooks.slack.com/services/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')



#Open and read the CSV file.
with open('/root/js-automation/log.csv') as file:
    reader = csv.reader(file)

#Skips the CSV header line.
    next(reader)

#Parse rows.
    for row in reader:        

        #Message components from the csv
        user = row[8]
        playbook = row[5]
        product = row[1]
            
        if row[3] in (None, " "):
            vars = 'No variables were passed.'
        else:
            vars = row[3]

        state_bin = row[4]
     
        if state_bin == '1':
            state = 'SUCCEEDED'
        elif state_bin == '0':
            state = 'FAILED'
        else:
            state = 'UNDETERMINED'

        start = row[2]
        end = row[6]
        exec_date = row[0]
        #exec_time = row[9]

        msg1 = 'User ' + user + ' just ran the ' + playbook + ' playbook to deploy ' + product + '. Here are the details:'
        msg2 = 'Final State: ' + state + '\nStarted: ' + start + '\nFinished: ' + end + '\nExecution Date: ' + exec_date + '\nPlaybook Variables: ' + vars
        #msg2 = 'Final State: ' + state + '\nStarted: ' + start + '\nFinished: ' + end + '\nExecution Date: ' + exec_date + '\nExecution Time: ' + exec_time + '\nPlaybook Variables: ' + vars

    slack.post(text=msg1,
       attachments = [{
           "text": msg2
        }]
    )
