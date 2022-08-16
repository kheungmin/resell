import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def send_slack():
    message_file = '/home/ubuntu/airflow/dags/resell/insta_celeb_monitoring/message.txt'
    if os.path.isfile(message_file):
        f = open(message_file, 'r', encoding='utf-8')
        message = f.read()
        f.close()
        os.remove(message_file)

        slack_token = 'xoxb-3199109467058-3851214835316-94m8OQhZ2lTnpAaDLl6UJNo0'
        client = WebClient(token=slack_token)

        try:
            response_msg = client.chat_postMessage(channel='4irjordan', text=message)
            print(response_msg['ok'])
        except SlackApiError as e:
            print('Error: {}'.format(e.response['error']))