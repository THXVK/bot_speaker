import requests
from config import IAM_TOKEN, FOLDER_ID

# ssh -i ~/.ssh/ssh_p student@158.160.134.86
# curl -H Metadata-Flavor:Google 169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token


def make_requests(user_text: str):
    headers = {
        'Authorization': f'Bearer {IAM_TOKEN}',
    }
    data = {
        "text": user_text,
        'lang': 'ru-RU',
        'voice': 'filipp',
        'folderId': f'{FOLDER_ID}'
    }
    response = requests.post('https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize', headers=headers, data=data)

    if response.status_code == 200:
        with open('voice.ogg', 'wb') as f:
            f.write(response.content)

    else:
         print(f"{response.status_code}")


if __name__ == "__main__":

    text = "проснитесь мистер фримен"
    make_requests(text)

