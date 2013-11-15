dotipython
==========

IPython profile for use with Zope/Plone.

This profile man be used from buildout as follows (the `client-debug` name
below should refer to a buildout part defining a Zope instance used for
development):

```
[ipzope]
# An IPython Shell for interactive use with Zope running.
#
# It requires the `ipy_profile_zope.py` configuration script.
# Get this from git@github.com:collective/dotipython.git
# and put it in your profile directory. Depending on your setup, 
# this may be at 
# `$HOME/.ipython/profile_zope/startup`,
# `$HOME/.config/ipython/profile_zope/startup` (Ubuntu 12.04), or see
# http://ipython.org/ipython-doc/dev/config/overview.html#configuration-file-location
# for more details.
#
recipe = zc.recipe.egg
eggs =
    ipython
    ${client-debug:eggs}
initialization =
    import sys, os
    os.environ["INSTANCE_HOME"] = "${client-debug:location}"
    sys.argv[1:1] = "--profile=zope".split()
scripts = ipython=ipzope
```
