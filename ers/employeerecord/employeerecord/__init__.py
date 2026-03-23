# Ensure PyMySQL is used as MySQLdb if available
try:
	import pymysql
	pymysql.install_as_MySQLdb()
except Exception:
	pass

