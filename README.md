# pulmo
Application to manage applications enablement projects. It allows application enablement (to test), and pass to production of each project.


### Package Installation debian buster
```bash
apt install git
apt install python-dev
apt install python-pip
apt install pkg-config
apt install libpq-dev
apt install libyaml-dev
apt install libldap2-dev
apt install libsasl2-dev
apt install gettext
apt install libjpeg-dev
apt install zlib1g-dev
apt install libgtk2.0-dev
apt install libgirepository1.0-dev
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

