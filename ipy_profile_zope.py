# -*- coding: utf-8 -*-
#
# File: ipy_profile_zope.py
#
# Copyright (c) InQuant GmbH
#
# An ipython profile for zope and plone. Some ideas
# stolen from http://www.tomster.org.
#
# German Free Software License (D-FSL)
#
# This Program may be used by anyone in accordance with the terms of the 
# German Free Software License
# The License may be obtained under <http://www.d-fsl.org>.

__author__ = """Stefan Eletzhofer <stefan.eletzhofer@inquant.de>"""
__docformat__ = 'plaintext'
__revision__ = "$Revision$"

from IPython import ipapi
from IPython import Release
import sys
import os
import textwrap

# The import below effectively obsoletes your old-style ipythonrc[.ini],
# so consider yourself warned!
# import ipy_defaults

class ZopeDebug(object):
    def __init__(self, PORTAL_PATH="plone" ):

        self.portal_path = PORTAL_PATH

        self.instancehome = os.environ.get( "INSTANCE_HOME" )

        configfile = os.environ.get( "CONFIG_FILE" )
        if configfile is None and self.instancehome is not None:
            configfile = os.path.join( self.instancehome, "etc", "zope.conf" )

        if configfile is None:
            raise RuntimeError( "CONFIG_FILE env not set" )

        print "CONFIG_FILE=", configfile
        print "INSTANCE_HOME=", self.instancehome

        self.configfile = configfile

        from Zope2 import configure
        configure( configfile )

        import Zope2
        app = Zope2.app()

        from Testing.makerequest import makerequest
        self.app = makerequest( app )

        self._make_permissive()
        self._pwd = self.portal or self.app

        try:
            from zope.component import getSiteManager
            from zope.component import getGlobalSiteManager
            from zope.app.component.hooks import setSite, clearSite

            if self.portal is not None:
                setSite( portal )

                gsm = getGlobalSiteManager()
                sm = getSiteManager()

                if sm is gsm:
                    print "ERROR SETTING SITE!"
        except:
            pass


    @property
    def utils(self):
        class Utils(object):
            commit = self.commit
            sync = self.sync
            objectInfo = self.objectInfo
            ls = self.ls
            pwd = self.pwd
            cd = self.cd

            @property
            def cwd(self):
                return self.pwd()

        return Utils()

    @property
    def namespace(self):
        return dict( utils=self.utils, app=self.app, portal=self.portal )

    @property
    def portal(self):
        return getattr( self.app, self.portal_path, None )

    def pwd(self):
        return self._pwd

    def _make_permissive(self):
        """
        Make a permissive security manager with all rights. Hell,
        we're developers, aren't we? Security is for whimps. :)
        """
        from Products.CMFCore.tests.base.security import PermissiveSecurityPolicy
        import AccessControl
        from AccessControl.SecurityManagement import newSecurityManager
        from AccessControl.SecurityManager import setSecurityPolicy

        _policy = PermissiveSecurityPolicy()
        self.oldpolicy = setSecurityPolicy(_policy)
        newSecurityManager(None, AccessControl.User.system)

    def _newApp(self):
        import Zope2
        #return makerequest( Zope2.app() )
        return Zope2.app()

    def commit(self):
        """
        Commit the transaction.
        """
        import transaction
        transaction.get().commit()

    def sync(self):
        """
        Sync the app's view of the zodb.
        """
        self.app._p_jar.sync()

    def objectInfo( self, o ):
        """
        Retrun a descriptive string of an object
        """
        Title = ""
        t = getattr( o, 'Title', None )
        if t:
            Title = t()
        return "id '%-20s', Title '%-30s' (%s) Folderish: %s" % ( o.getId(), Title, getattr( o, 'portal_type', o.meta_type), o.isPrincipiaFolderish )

    def cd( self, path ):
        """
        Change current dir to a specific folder.

         cd( ".." )
         cd( "/plone/Members/admin" )
         etc.
        """
        cwd = self.pwd()
        x = cwd.unrestrictedTraverse( path )
        if x is None:
            raise KeyError( "Can't cd to %s" % path )

        print "%s -> %s" % ( self.pwd().getId(), x.getId() )
        self._pwd = x

    def ls( self, x=None ):
        """
        List object(s)
        """
        if x is None:
            x = self.pwd()
        print self.objectInfo( x )
        if x.isPrincipiaFolderish:
            for id, o in x.objectItems():
                print "    ", self.objectInfo( o )

zope_debug = None


def main():
    global zope_debug
    ip = ipapi.get()
    o = ip.options
    # autocall to "full" mode (smart mode is default, I like full mode)
    
    SOFTWARE_HOME = os.environ.get( "SOFTWARE_HOME" )
    sys.path.append( SOFTWARE_HOME )
    print "SOFTWARE_HOME=%s\n" % SOFTWARE_HOME

    zope_debug = ZopeDebug()

    # I like my banner minimal.
    o.banner = "ZOPE Py %s IPy %s\n" % (sys.version.split('\n')[0],Release.version)
    
    print textwrap.dedent("""\
        ZOPE mode iPython shell.

          Bound names:
           app
           portal
           utils.{ %s }
  
        Uses the $SOFTWARE_HOME and $CONFIG_FILE environment
        variables.
        """ % ( ",".join([ x for x in dir(zope_debug.utils) if not x.startswith("_") ] ) ) )


    ip.user_ns.update( zope_debug.namespace )


main()
# vim: set ft=python ts=4 sw=4 expandtab :
