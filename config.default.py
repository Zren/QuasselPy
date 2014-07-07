import os

#--- Sqlite: (Windows) CurrentUser 
# Eg: sqlite:///C:\Users\Admin\AppData\Roaming\quassel-irc.org\quassel-storage.sqlite
uri = 'sqlite:///' + os.environ.get('APPDATA') + r'\quassel-irc.org\quassel-storage.sqlite'


#--- Sqlite: (Windows) NetworkService 
# uri = 'sqlite:///' + r'C:\Windows\ServiceProfiles\NetworkService\AppData\Roaming\quassel-irc.org\quassel-storage.sqlite'

#--- Postgres
# uri = 'postgresql+pg8000://quassel:quassel@localhost/quassel'

#---
print(uri)
