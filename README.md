# pulmo
Application to manage applications enablement projects. It allows application enablement (to test), and pass to production of each project.


### Package Installation debian stretch
```bash
sudo apt-get install python-dev
sudo apt-get install python-pip
sudo apt-get install libpq-dev
sudo apt-get install libyaml-dev
sudo apt-get install libldap2-dev
sudo apt-get install libsasl2-dev
sudo apt-get install gettext
sudo apt-get install libjpeg-dev
sudo apt-get install zlib1g-dev
sudo apt-get install python-dnspython # for reidi
sudo apt-get install mariadb-client # for dumpserver
sudo apt-get install pkg-config
sudo apt-get install libgtk2.0-dev
sudo apt-get install libgirepository1.0-dev
```

### Python lib Installation
```bash
pip install -r requieremens.txt
```
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

pg_hba.conf
hostssl  pulmo_db     pulmo_owner        ::1/128                 password
/etc/init.d/postgresql restart
psql -h localhost -U pulmo_owner -p 5432 -d pulmo_db
```

### Showing models
```bash
sudo aptitude install python-pygraphviz

python manage.py graph_models -a -o myapp_models.pdf
```

