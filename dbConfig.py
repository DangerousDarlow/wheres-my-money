from psycopg2.extras import register_uuid


class DbConfig:
    dbName = 'money'
    dbUser = 'postgres'
    dbPassword = 'STy6KEnk'


# required to read and write uuid type to postgres using psycopg2
register_uuid()

dbConfig = DbConfig()
dbConnectionString = f"dbname={dbConfig.dbName} user={dbConfig.dbUser} password={dbConfig.dbPassword}"
