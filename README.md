# pulmo
Application to manage applications enablement projects. It allows application enablement (to test), and pass to production of each project.

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

pip install -r app/requirements.txt
```

### Application configuration
```bash
cp pulmo/settings.tpl.py pulmo/settings.py
```

### Util commands
```bash
python manage.py migrate

pip freeze > app/requirements.txt
pip install -r app/requirements.txt
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

### Showing models
```bash
sudo aptitude install python-pygraphviz

python manage.py graph_models -a -o myapp_models.pdf
```

