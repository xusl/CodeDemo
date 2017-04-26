import kinterbasdb

con = kinterbasdb.connect(dsn='employee.fdb', user='sysdba',
password='masterkey')#, charset='utf-8')

cur = con.cursor()

cur.execute("select * from JOB")

# Retrieve all rows as a sequence and print that sequence:
print cur.fetchall()

#
#newLanguages = [
#    ('Lisp',  1958),
#    ('Dylan', 1995),
#  ]
#
#cur.executemany("insert into languages (name, year_released) values (?, ?)",
#    newLanguages
#  )
#
## The changes will not be saved unless the transaction is committed explicitly:
#con.commit()
