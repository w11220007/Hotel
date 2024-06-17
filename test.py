import urllib
db_password = "Quochung@0904"
db_password_quoted = urllib.parse.quote(db_password)
print(db_password_quoted)