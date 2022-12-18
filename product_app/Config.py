import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
SAURON_CLIENT_SECRET = os.getenv("SAURON_CLIENT_SECRET")

JIRABOT_USERNAME = os.getenv("JIRABOT_USERNAME")
JIRABOT_PASSWORD = os.getenv("JIRABOT_PASSWORD")

JIRA_USER = os.getenv("JIRA_USER")
JIRA_PASSWORD = os.getenv("JIRA_PASSWORD")

DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

# вывод инфы кредов :)
# s = []
# f = open('Config.py')
# for line in f.readlines():
#     if line.find("=") == -1:
#         continue
#     s.append(line.rstrip().split('=')[0])
#
# for i in s:
#     print(i,"=",os.getenv(i))
# f.close()
# exit(1)
