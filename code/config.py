from dotenv import load_dotenv
from os import getenv

# ssh -i ~/.ssh/ssh_p student@158.160.134.86
# curl -H Metadata-Flavor:Google 169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token

DB_NAME = 'sqlite3.db'


load_dotenv()
TOKEN = getenv('TOKEN')
FOLDER_ID = getenv('FOLDER_ID')
IAM_TOKEN = getenv('IAM_TOKEN')
MAX_SIMBOLS = 2000
MAX_LEN_PER_MESSAGE = 100
MAX_SIMBOLS_PER_USER = 500
MAX_STT_BLOCK_PER_USER = 12
