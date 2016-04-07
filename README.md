# pulmo

Projects aplication administration


### Package Installation
```bash
apt-get install apache2=2.4.10-10+deb8u4
apt-get install apache2 libapache2-mod-wsgi
apt-get install python2.7=2.7.9-2
apt-get install postgresql=9.3
apt-get install python-psycopg2=2.5.4+dfsg-1
apt-get install python-pip=1.5.6-5
apt-get install python-yaml=3.11-2
apt-get install python-dev
apt-get install python-ldap
apt-get install gettext=0.19.3-2
sudo pip install Django==1.8.5
sudo pip install django-extensions -v 1.5.7
sudo pip install django-bootstrap-themes -v 3.1.2
sudo pip install python-redmine
```
### Postgres configuration
```bash
createdb pulmo_db;
createuser pulmo_owner -P;

/etc/postgresql/9.3/main/pg_hba.conf
hostssl  pulmo_db     pulmo_owner        ::1/128                 password
/etc/init.d/postgresql restart
psql -h localhost -U pulmo_owner -p 5432 -d pulmo_db
```
### App configuration
```bash
python manage.py syncdb
python manage.py migrate
```

### Showing models
```bash
sudo aptitude install python-pygraphviz

python manage.py graph_models -a -o myapp_models.pdf
```

