# pulmo

Projects aplication administration


### Package Installation
```bash
sudo apt-get install python2.7
sudo apt-get install postgresql-9.3
sudo apt-get install python-psycopg2
sudo apt-get install python-pip
sudo apt-get install python-yaml
sudo pip install django==1.7.4
sudo pip install django-extensions
pip install django-bootstrap-themes
```
### Postgres configuration
```bash
createdb murex_db;
createuser murex_owner -P;

/etc/postgresql/9.3/main/pg_hba.conf
hostssl  murex_db     murex_owner        ::1/128                 password
/etc/init.d/postgresql restart
psql -h localhost -U murex_owner -p 5432 -d murex_db
```
### App configuration
```bash
python manage.py syncdb
python manage.py migrate
```
