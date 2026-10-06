try:
    import pymysql
    # PyMySQL en remplacement pur Python de mysqlclient
    pymysql.install_as_MySQLdb()
    pymysql.version_info = (2, 2, 0, 'final', 0)
except ImportError:
    pass
