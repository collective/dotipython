dotipython
==========

IPython profile for use with Zope/Plone.

This profile can be used from buildout as follows (the `client-debug` name
below should refer to a buildout part defining a Zope instance used for
development):

```
[ipzope]
# a IPython Shell for interactive use with zope running.
# you also need to put git@github.com:collective/dotipython.git
# in the $HOME/.ipython/profile_zope/startup directory for the following to
# work.
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
