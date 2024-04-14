from dotenv import load_dotenv
from os import getenv

# ssh -i ~/.ssh/ssh_p student@158.160.134.86
# curl -H Metadata-Flavor:Google 169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token

DB_NAME = 'sqlite3.db'


load_dotenv()
TOKEN = getenv('TOKEN')
FOLDER_ID = getenv('FOLDER_ID')
IAM_TOKEN = getenv('IAM_TOKEN')
MAX_SIMBOLS = 20
MAX_LEN_PER_MESSAGE = 10
