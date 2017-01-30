# Keystone driver for SecurePass

This is the OpenStack Keystone driver for SecurePass.
It works with domains as well.

Install on Keystone with:
* python setup.py build
* python setup.py install

Create a domain file under /etc/keystone/domains/keystone.DOMAIN.conf:
```
[identity]
driver = securepass
```

and config info on /etc/keystone/keystone.conf:
```
[securepass]
app_id = <<APP_ID>>
app_secret =  <<APP_SECRET>>
realm = REALM/DOMAIN
```

*Note* that this behaviour will change in future
