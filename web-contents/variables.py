SUCCESS = 0
ERROR = -1

class ConfigXML:
    """Contains variables for xml config files that we use.
    apps : apps.xml
    build : build.xml
    """
    apps = None
    build = None

class BuildStates:
    BUILD_STATE_ERRORED = -1       # build errored, no command is allowed after this
    BUILD_STATE_QUEUED = 0         # in the web's queue
    BUILD_STATE_PENDING = 1        # this is the first build in the queue, we do some stuff before we kick it off
    BUILD_STATE_SVN_UPDATE = 2     # build is doing the SVN update
    BUILD_STATE_BUILDING = 3       # compiling
    BUILD_STATE_RESTARTING = 4     # servers restarting
    BUILD_STATE_SYNCING = 5        # syncing in progress
    BUILD_STATE_CANCELED = 6       # build was canceled
    BUILD_STATE_WAITING = 7        # id and appname submitted to the build server

class DeployController:
    # define here the name of the script
    _name = "deploy2.py"
    _ssh = "ssh -t -t"
    
    # definition of the calls we make
    FORCE_RESTART = "%(ssh)s %%s %%s/%(name)s --restart %%s" % {'ssh':_ssh, 'name':_name}
    SYNC = "%(ssh)s %%s %%s/%(name)s %%s %%s norestart" % {'ssh':_ssh, 'name':_name}
    RESTART = "%(ssh)s %%s %%s/%(name)s %%s %%s" % {'ssh':_ssh, 'name':_name}
