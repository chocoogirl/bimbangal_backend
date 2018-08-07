 [![Python](https://i.imgur.com/6dLrqAk.png)](https://www.python.org/) [![Gunicorn](https://i.imgur.com/JUAy3me.png)](http://gunicorn.org/)                  [![Pylons Waitress](https://i.imgur.com/7CdJSYL.png)](https://docs.pylonsproject.org/projects/waitress/en/latest/)            [![Redis](https://i.imgur.com/WL6ImbT.png)](https://redis.io/)  [![MongoDB](https://i.imgur.com/iglZaGb.png)](https://docs.mongodb.com/manual/administration/install-community/)  
# Bimbangal Backend

### Pre-requisites

* Python 3.6.x
* Gunicorn
* Waitress(For Windows Support)
* Redis
* MongoDB

### Install

* Clone the repo
* Create venv inside repo (Highly recommended)
* Run pip install requirements
* Run setup
* Run `bimbangal` command
 
    ```
    $ git clone CLONE_URL
    $ cd CLONED_FOLDER
    $ python3 -m venv venv
    $ source ./venv/bin/activate
    $ pip3 install -r requirements.tx
    $ python setup.py
    $ bimbangal
    $ API is served at LOCALHOST
    ```


### To Do
- Add OAuth2
- Add nonce for extra security

