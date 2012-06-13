uwsgi_simple_app
================

example uwsgi application

instruction:

virtualenv uwsgi_simple_app --no-site-packages --python=python2.7
git clone git://github.com/niko83/uwsgi_simple_app.git uwsgi_simple_app/src
source  uwsgi_simple_app/bin/activate
pip install -r uwsgi_simple_app/src/requirements.pip
sudo ln -s /var/www/uwsgi_simple_app/src/nginx.conf  /etc/nginx/sites-enabled/uwsgi_simple_app
sudo /etc/init.d/nginx reload
#update hosts  
#xxx.xxx.xxx.xxx	uwsgi_simple_app.loc
