import os

# Dynamically determine the user's home directory
USER_HOME_DIR = os.path.expanduser('~')
ROOT_DIR = os.path.join(USER_HOME_DIR, 'Videos', 'Lesson Study')

# Define channel IDs and query formats
# Channel E.G. White Audio 'id': 'UCPS3A-60tKmKTCKWZMT9upA'
CHANNEL_IDS = {
    'hopess': {'id': 'UCm34NbuHzE9t9hHutOxwIOA', 'query_format': 'Lesson {lesson_number}', 'first_result': False, 'confirm_download': True},
    'sabbathschoollikeplus': {'id': 'UCkO6iQI4HBYFolkrbmQWDHw', 'query_format': '{lesson_title} Lesson {lesson_number} Q{quarter} {year}', 'first_result': True, 'confirm_download': False},
    'claudiocarneiro': {'id': 'UCvJRu-jirSkv6yuxakirENg', 'query_format': '{year} Q{quarter} Lesson {lesson_number} – {lesson_title} – Audio by Percy Harrold', 'first_result': True, 'confirm_download': False},
    '3abn': {'id': 'UCw_AthKfwqB3XYpboTFZFmg', 'query_format': '{lesson_title} | Sabbath School Panel by 3ABN - Lesson {lesson_number} Q{quarter} {year}', 'first_result': True, 'confirm_download': False},
    'itiswritten': {'id': 'UCtWyoUrGPAkZgnp2486Ir4w', 'query_format': 'Sabbath School - {year} Q{quarter} Lesson {lesson_number}: {lesson_title}', 'first_result': True, 'confirm_download': False},
    'HopeLives365': {'id': 'UCOuDMda3jxj-g_iI1P2d2zw', 'query_format': 'Sabbath School with Mark Finley | Lesson {lesson_number} — Q{quarter} – {year}', 'first_result': True, 'confirm_download': False},
    'egwhiteaudio': {'id': 'UCvJRu-jirSkv6yuxakirENg', 'query_format': '{year} Q{quarter} Lesson {lesson_number} – EGW Notes – {lesson_title}', 'first_result': True, 'confirm_download': False},
}
