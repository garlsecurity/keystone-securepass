#
# /usr/lib/python2.7/site-packages/keystone/identity/backends
# /usr/lib/python2.7/site-packages/keystone-9.0.0-py2.7.egg-info/entry_points.txt
#

from __future__ import absolute_import
import uuid

from oslo_config import cfg
from oslo_log import log
from oslo_log import versionutils
import six

from keystone.common import clean
from keystone.common import driver_hints
from keystone.common import models
from keystone import exception
from keystone.i18n import _
from keystone import identity

#from securepass import utils
from securepass import securepass


CONF = cfg.CONF

LOG = log.getLogger(__name__)

## Options
CONF.register_opt(cfg.StrOpt(
    "app_id", default="test"), group="securepass")

CONF.register_opt(cfg.StrOpt(
    "app_secret", default="test"), group="securepass")

CONF.register_opt(cfg.StrOpt(
    "endpoint", default="https://beta.secure-pass.net"), group="securepass")

CONF.register_opt(cfg.StrOpt(
    "realm", default="login.farm"), group="securepass")

class Identity(identity.IdentityDriverV8):
    def __init__(self, conf=None):
        super(Identity, self).__init__()

        if conf is None:
            self.conf = CONF
        else:
            self.conf = conf

	LOG.warning("securepass init %s" % conf)

	LOG.warning("securepass app_id %s" % CONF.securepass.app_id)
	LOG.warning("securepass app_secret %s" % CONF.securepass.app_secret)

        # global securepass conf
        self.realm      = CONF.securepass.realm
        self.sp_handler = securepass.SecurePass(app_id=CONF.securepass.app_id,
                                    app_secret=CONF.securepass.app_secret,
                                    endpoint=CONF.securepass.endpoint)

    def is_domain_aware(self):
        return False

    def generates_uuids(self):
        return False

    @property
    def is_sql(self):
        """Indicate if this Driver uses SQL."""
        return False

    def default_assignment_driver(self):
        # TODO(morganfainberg): To be removed when assignment driver based
        # upon [identity]/driver option is removed in the "O" release.
        return 'sql'

    # Identity interface
    def authenticate(self, user_id, password):
        try:
            if self.sp_handler.user_auth(user=user_id,
                                    secret=password):

                user = self.sp_handler.user_info(user_id)

                user_ref = {}
                user_ref['id'] = user_id
                user_ref['name'] = user_id
                user_ref['enabled'] = user['enabled']

                return user_ref

            else:
                raise AssertionError(_('Invalid user / password'))
        except:
            raise AssertionError(_('An error occurred with SecurePass'))


    def get_user(self, user_id):
	LOG.warning("SecurePass user %s" % user_id)

        try:
            user = self.sp_handler.user_info(user_id)

            user_ref = {}
            user_ref['id'] = user_id
            user_ref['name'] = user_id
            user_ref['email'] = user['email']
            user_ref['description'] = "%s %s" % (user['name'], user['surname'])
            user_ref['enabled'] = user['enabled']

    	    return user_ref

        except:
            raise AssertionError(_('An error occurred with SecurePass'))            

    def list_users(self, hints):
        try:
	   users = []

           for user in self.sp_handler.user_list(realm=self.realm):

              user_detail = self.sp_handler.user_info(user)

              user_ref = {}
              user_ref['id'] = user
              user_ref['name'] = user
              user_ref['email'] = user_detail['email']
              user_ref['description'] = "%s %s" % (user_detail['name'], user_detail['surname'])
              user_ref['enabled'] = user_detail['enabled']

              users.append(user_ref)

           return users

        except:
            raise AssertionError(_('An error occurred with SecurePass'))            


    def get_user_by_name(self, user_name, domain_id):
        # domain_id will already have been handled in the Manager layer,
        # parameter left in so this matches the Driver specification
	LOG.warning("SecurePass user %s" % user_name)

        try:
	    LOG.warning("User %s" % user_name)
            user = self.sp_handler.user_info(user_name)

            user_ref = {}
            user_ref['id'] = user_name
            user_ref['name'] = user_name
            user_ref['email'] = user['email']
            user_ref['description'] = "%s %s" % (user['name'], user['surname'])
            user_ref['enabled'] = user['enabled']

	    return user_ref

        except:
            raise AssertionError(_('An error occurred with SecurePass'))   

    # CRUD -- Not allowed in SecurePass
    def create_user(self, user_id, user):
        raise exception.NotImplemented() 

    def update_user(self, user_id, user):
        raise exception.NotImplemented() 

    def delete_user(self, user_id):
        raise exception.NotImplemented() 

    def create_group(self, group_id, group):
        raise exception.NotImplemented() 

    def get_group(self, group_id):
        raise exception.NotImplemented() 

    def get_group_by_name(self, group_name, domain_id):
        raise exception.NotImplemented() 

    def update_group(self, group_id, group):
        raise exception.NotImplemented() 

    def delete_group(self, group_id):
        raise exception.NotImplemented() 

    def add_user_to_group(self, user_id, group_id):
        raise exception.NotImplemented() 

    def remove_user_from_group(self, user_id, group_id):
        raise exception.NotImplemented() 

    def list_groups_for_user(self, user_id, hints):
        raise exception.NotImplemented() 

    def list_groups(self, hints):
        raise exception.NotImplemented() 

    def list_users_in_group(self, group_id, hints):
        raise exception.NotImplemented() 

    def check_user_in_group(self, user_id, group_id):
        raise exception.NotImplemented() 
