#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Contacts:
#   - Chris Antenesse <cantenesse@sample.com>
#   - Norberto Lopes <nlopes@sample.com>

import copy
import logging
import os
import shutil
import signal
import time

import rpyc
from rpyc.utils.server import ThreadedServer

# ours
#from xml.etree.ElementTree import XML
import Config
import modules
from modules import parsers, functions
from modules.variables import SUCCESS, ERROR, BuildStates, ConfigXML, DeployController
from modules.classes import Application

ConfigXML.apps = parsers.AppsXML()
ConfigXML.build = parsers.BuildXML()

BUILD_ECONOMY = {}  # key: ID, value: (Application class, {})


def reload_configs():
    try:
        ConfigXML.apps = parsers.AppsXML()
        print("Successfully reloaded apps.xml.")
        logging.info("Successfully reloaded apps.xml.")
    except:
        print("Could not reload apps.xml.")
        logging.info("Could not reload apps.xml.")

    try:
        ConfigXML.build = parsers.BuildXML()
        print("Successfully reloaded build.xml.")
        logging.info("Successfully reloaded build.xml.")
        # reload build info for each application currently in progrss
        try:
            for bid in BUILD_ECONOMY:
                result = BUILD_ECONOMY[bid][0].reload_config()
                print(result[1])
            print(
                "Successfully reloaded the build info for the 'in progress' builds."
            )
            logging.info(
                "Successfully reloaded the build info for the 'in progress' builds.")
        except:
            print("Could not reload build info for build with id %s" % bid)
            logging.info("Could not reload build info for build with id %s" %
                         bid)
    except:
        print("Could not reload build.xml.")
        logging.info("Could not reload build.xml.")


def reload_config_handler(signum, frame):
    reload_configs()


class Builder(rpyc.Service):
    logger_name = "Builder"
    logger = logging.getLogger(logger_name)

    def exposed_reload(self):
        """Reloads the configs.
        Same as sending a HUP signal to the daemon.
        """
        reload_configs()

    def exposed_save_config(self, type, xml_string):
        """Method to save configuration files directly to disk.

        @param type: The type of config, either app_xml or build_xml
        @type type: string

        @param xml_string: The xml document, appropriately formatted
        @type xml_string: string
        """

        if type != 'apps' and type != 'build':
            self.logger.error("Config %s isn't valid.", type)
            return ERROR, "ERROR: That config file doesn't exist."

        XML(xml_string)
        file_path = os.path.join(Config.get("config"), Config.get(type))
        shutil.copy(file_path, '.'.join((file_path, 'bak')))
        fh = open(file_path, 'w')
        fh.write(xml_string)
        fh.close()

    def exposed_reset(self, p_id, dry_run):
        """Reset the build state of a build.
        """

        if p_id not in BUILD_ECONOMY:
            self.logger.error("Build id %s is not valid.", p_id)
            return (ERROR, "ERROR: Not a valid build id.")

        app = BUILD_ECONOMY[p_id]
        app[1]["logger"].info("Build state before reset was: %d." %
                              app[1]["status"])

        app[1]["logger"].info("Resetting build state to: %d." %
                              BuildStates.BUILD_STATE_WAITING)

        # actually reset the build state
        app[1]["status"] = BuildStates.BUILD_STATE_WAITING

        return (SUCCESS, "Changed build state to: %d." %
                BuildStates.BUILD_STATE_WAITING)

    def exposed_dump(self):
        fname = os.path.join(Config.get("home"), Config.get("dump_fname"))
        fh = open(fname, "w")
        fh.write("""BUILD ECONOMY:
%s

APPS_XML:
%s

BUILD_XML:
%s""" % (str(BUILD_ECONOMY), ConfigXML.apps.pprint(),
         ConfigXML.build.pprint()))
        fh.close()

        return (SUCCESS, "Wrote dump to %s." % fname)

    def exposed_get_apps_info(self, specified_region=None, name=None):
        """
        Parses application information from config.xml.
        Returns a list of applications.
        """
        if specified_region == None:
            self.logger.error(
                "Region must be set. Look at the '-R' flag in the help.")
            return (
                ERROR,
                "ERROR: Region must be set. Look at the '-R' flag in the help."
            )

        self.logger.debug("User requested all applications information.")
        apps = []
        for app in ConfigXML.apps.get_apps(specified_region, None):
            a = Application(copy.deepcopy(app), self.logger, True)
            if name == a.name:
                tmp = str(a)
                del a
                return (SUCCESS, [tmp])
            elif name is None:
                tmp = str(a)
                del a
                apps.append(tmp)
        # if we got here and name is not None,
        # that means we didn't find an application with this name
        # return FAILURE
        if name is not None:
            self.logger.error("Application with name %s could not be found." %
                              name)
            return (ERROR,
                    "ERROR: Application with name %s could not be found." %
                    name)
        return (SUCCESS, apps)

    def exposed_get_app_info(self, specified_region, name):
        if specified_region == None:
            self.logger.error(
                "Region must be set. Look at the '-R' flag in the help.")
            return (
                ERROR,
                "ERROR: Region must be set. Look at the '-R' flag in the help."
            )

        app_info = self.exposed_get_apps_info(specified_region, name)
        if app_info[0] == SUCCESS:
            return (SUCCESS, app_info[1][0])
        else:
            return app_info

    def exposed_get_log_name(self, p_id, dry_run):
        if p_id not in BUILD_ECONOMY:
            self.logger.error("Build id %s is not valid.", p_id)
            return (ERROR, "ERROR: Not a valid build id.")

        return (SUCCESS, BUILD_ECONOMY[p_id][1]["logger_name"])

    def exposed_new_build(self, p_id, p_name, specified_region, dry_run):
        """
        Sets up a new build for the application specified by p_name.
        p_id should be the id to use to do future requests.

        Returns (SUCCESS, p_id) if successful.
        """

        if specified_region == None:
            self.logger.error(
                "Region must be set. Look at the '-R' flag in the help.")
            return (
                ERROR,
                "ERROR: Region must be set. Look at the '-R' flag in the help."
            )

        if p_id in BUILD_ECONOMY:
            self.logger.error("Build id %s is already in use." % p_id)
            return (ERROR, "ERROR: Build id %s is already in use." % p_id)

        self.logger.info("Setting up build id %s for application %s." %
                         (p_id, p_name))
        for app in ConfigXML.apps.get_apps(specified_region):
            if app["name"] == p_name:
                app["region"] = specified_region

                # setup a new logger with a new filename
                # the name of the logger will be REGION**APPNAME**ID**TIMESTAMP
                # the filename for this logger will be REGION**APPNAME**ID**TIMESTAMP.log
                logr_name = "%s.%s**%s**%s**%s" % (
                    self.logger_name, app["region"], p_name, p_id,
                    time.strftime(Config.get("log_timestamp_fmt",
                                             specified_region)))
                logr = logging.getLogger(logr_name)
                handler = logging.FileHandler("%s/%s.log" % (Config.get(
                    "logs", specified_region), logr_name))
                handler.setFormatter(logging.Formatter(Config.get(
                    "log_string_fmt", specified_region)))
                logr.addHandler(handler)
                BUILD_ECONOMY[p_id] = (
                    Application(
                        copy.deepcopy(app), logr),
                    {"status": BuildStates.BUILD_STATE_WAITING,
                     "logger": logr,
                     "logger_name": logr_name,
                     "timestamp": time.strftime(Config.get("log_timestamp_fmt",
                                                           specified_region))})
                self.logger.debug(
                    "Successful setup application %s with build id %s." %
                    (app["name"], p_id))
                return (SUCCESS, p_id)
        self.logger.error("No application found with name %s." % p_name)
        return (ERROR, "ERROR: No application found with that name %s." %
                p_name)

    def exposed_app_update(self, p_id, revision, checkout, dry_run):
        """
        Performs a svn update with all the magic that involves.
        AWARENESS: does not perform a checkout. Ask nlopes@sample.com for reasons.
        """
        if p_id not in BUILD_ECONOMY:
            self.logger.error("Build id %s is not valid.", p_id)
            return (ERROR, "ERROR: Not a valid build id.")

        if BUILD_ECONOMY[p_id][1]["status"] != BuildStates.BUILD_STATE_WAITING:
            if BUILD_ECONOMY[p_id][1][
                    "status"] == BuildStates.BUILD_STATE_ERRORED:
                self.logger.error(
                    "A previous command to this application (%s) errored out."
                    % BUILD_ECONOMY[p_id][0].name)
                return (
                    ERROR,
                    "ERROR: A previous command to this application errored out."
                )
            self.logger.error(
                "There is an ongoing operation on application %s." %
                BUILD_ECONOMY[p_id][0].name)
            return (
                ERROR,
                "ERROR: There is an ongoing operation on this application.")

        appname = BUILD_ECONOMY[p_id][0].name
        appsvn = BUILD_ECONOMY[p_id][0].svn
        apppath = BUILD_ECONOMY[p_id][0].path
        applogger = BUILD_ECONOMY[p_id][1]["logger"]

        tmpstr = "Updating project %s in svn location %s." % (appname, apppath)
        self.logger.info(tmpstr)
        applogger.info(tmpstr)

        print "application name: %s, application svn path: %s, apppath: %s" % (
            appname, appsvn, apppath)
        BUILD_ECONOMY[p_id][1]["status"] = BuildStates.BUILD_STATE_SVN_UPDATE
        if revision == "HEAD":
            rev, msg, changes = appsvn.update(checkout=checkout)
        else:
            rev, msg, changes = appsvn.update(rev=int(revision),
                                              checkout=checkout)
        BUILD_ECONOMY[p_id][1]["status"] = BuildStates.BUILD_STATE_WAITING
        if rev == -1 and msg == -1 and changes == []:
            tmpstr = "Project %s in svn location %s was not updated successfully." % (
                appname, apppath)
            BUILD_ECONOMY[p_id][1]["status"] = BuildStates.BUILD_STATE_ERRORED
            self.logger.error(tmpstr)
            self.logger.error("Not checked out.")
            applogger.info(tmpstr)
            return (ERROR, "ERROR: Not checked out.")
        if rev == -1 and msg == -2 and changes == []:
            tmpstr = "Project %s in svn location %s was not updated " \
                "successfully because couldn't access the svn." % (appname, apppath)
            self.logger.info(tmpstr)
            applogger.info(tmpstr)
            self.logger.info(appsvn.messages)
            applogger.info(appsvn.messages)
            BUILD_ECONOMY[p_id][1]["status"] = BuildStates.BUILD_STATE_ERRORED
            self.logger.error(
                "Could not update because I could not connect to the repository.")
            return (
                ERROR,
                "ERROR: Could not update because I could not connect to the repository."
            )

        tmpstr = "Project %s in svn location %s was updated successfully." % (
            appname, apppath)
        self.logger.info(tmpstr)
        applogger.info(tmpstr)

        # build up string from the changes
        # and log it!
        applogger.info("**Changes for revision %s below**" % appsvn.revision())
        str_ = ""
        for change in changes:
            str_ += "%s\n" % change
            applogger.info(change)
        return (SUCCESS, "buildId=%s,revision=%s,msg=%s,changes=%s" %
                (p_id, appsvn.revision(), msg or "", str_))

    def exposed_app_status(self, p_id, dry_run):
        """
        Grab status on the application.
        """
        if p_id not in BUILD_ECONOMY:
            self.logger.error("Build id %s is not valid.", p_id)
            return (ERROR, "ERROR: Not a valid build id.")

        self.logger.info("Retrieved build status for build id %s." % p_id)
        return (SUCCESS, "projectName=%s,buildId=%s,buildState=%s" %
                (BUILD_ECONOMY[p_id][0].name, p_id,
                 BUILD_ECONOMY[p_id][1]["status"]))

    def exposed_app_expire(self, p_id, dry_run):
        """
        Expire one or all builds.
        """
        if p_id == "all":
            for id_ in BUILD_ECONOMY:
                BUILD_ECONOMY[id_][1]["logger"].info(
                    "This build has just expired!")
            BUILD_ECONOMY.clear()
            self.logger.info("Expired all builds.")
            return (SUCCESS, "all")

        if p_id not in BUILD_ECONOMY:
            self.logger.error("Build id %s is not valid.", p_id)
            return (ERROR, "ERROR: Not a valid build id.")

        self.logger.info("Expired build id %s." % p_id)
        BUILD_ECONOMY[p_id][1]["logger"].info("This build has just expired!")
        del BUILD_ECONOMY[p_id]
        return (SUCCESS, p_id)

    def exposed_app_build(self, p_id, clean, bflags, dry_run):
        """
        Build an app with ant.
        """
        if p_id not in BUILD_ECONOMY:
            self.logger.error("Build id %s is not valid.", p_id)
            return (ERROR, "ERROR: Not a valid build id.")

        if BUILD_ECONOMY[p_id][1]["status"] != BuildStates.BUILD_STATE_WAITING:
            if BUILD_ECONOMY[p_id][1][
                    "status"] == BuildStates.BUILD_STATE_ERRORED:
                self.logger.error(
                    "A previous command to this application (%s) errored out."
                    % BUILD_ECONOMY[p_id][0].name)
                return (
                    ERROR,
                    "ERROR: A previous command to this application errored out."
                )
            self.logger.error(
                "There is an ongoing operation on application %s." %
                BUILD_ECONOMY[p_id][0].name)
            return (
                ERROR,
                "ERROR: There is an ongoing operation on this application.")

        if BUILD_ECONOMY[p_id][0].ant == None:
            BUILD_ECONOMY[p_id][1]["status"] = BuildStates.BUILD_STATE_ERRORED
            self.logger.error(
                "This application has no dynamic content to be built.")
            return (
                ERROR,
                "ERROR: This application has no dynamic content to be built.")

        isjava6 = False
        print(BUILD_ECONOMY[p_id][0].flags)
        if BUILD_ECONOMY[p_id][0].flags and (
                BUILD_ECONOMY[p_id][0].flags.get("java6", "no") == "yes"):
            isjava6 = True

        appname = BUILD_ECONOMY[p_id][0].name
        applogger = BUILD_ECONOMY[p_id][1]["logger"]
        appant = BUILD_ECONOMY[p_id][0].ant

        self.logger.info("Building application %s." % appname)
        applogger.info("Building application.")
        BUILD_ECONOMY[p_id][1]["status"] = BuildStates.BUILD_STATE_BUILDING
        res_clean = None
        if clean:
            if BUILD_ECONOMY[p_id][0].ant is None:
                # BUILD_ECONOMY[p_id][1]["status"] = BuildStates.BUILD_STATE_WAITING
                BUILD_ECONOMY[p_id][1][
                    "status"] = BuildStates.BUILD_STATE_ERRORED
                self.logger.error("No build type for application %s." %
                                  appname)
                return (ERROR, "ERROR: No build type on this application.")

            isold = False
            if BUILD_ECONOMY[p_id][0].flags and (
                    BUILD_ECONOMY[p_id][0].flags.get("old", "no") == "yes"):
                isold = True
            applogger.info("Performing an ant clean.")
            res_clean = BUILD_ECONOMY[p_id][0].ant.clean(bflags, isold,
                                                         isjava6)
            if res_clean[0] == ERROR:
                BUILD_ECONOMY[p_id][1][
                    "status"] = BuildStates.BUILD_STATE_ERRORED
                return (res_clean[0], res_clean[1])

        # if we got here, we can build the application
        applogger.info("Building with the following flags: %s." % bflags)
        # if old is in the flags, call old build
        if BUILD_ECONOMY[p_id][0].flags and (
                BUILD_ECONOMY[p_id][0].flags.get("old", "no") == "yes"):
            applogger.info(
                "This is a build that does not follow Simple Template Documentation.")
            res = appant.build_old(bflags, isjava6)
        else:
            res = appant.build(bflags, isjava6)

        # if we built up a string for the ant cmd, log it
        if appant.buildcmd:
            applogger.info("Ant cmd for this build was: %s." % appant.buildcmd)

        if res[0] == ERROR:
            BUILD_ECONOMY[p_id][1]["status"] = BuildStates.BUILD_STATE_ERRORED
        else:
            BUILD_ECONOMY[p_id][1]["status"] = BuildStates.BUILD_STATE_WAITING

        if res_clean:
            return (res[0],
                    (res_clean[1][0] + res[1][0], res_clean[1][1] + res[1][1]))
        return (res[0], res[1])

    def _try_extract(self, svn_path, target, name, applogger, lastdir):
        applogger.info("Extracting tarball %s/dist/*-%s.tar.gz into %s/%s/" %
                       (svn_path, name, target, lastdir))
        res = os.system("tar xzf %s/dist/*-%s.tar.gz -C %s/%s/" %
                        (svn_path, name, target, lastdir))
        if res == 0:
            applogger.info("Successfully extracted tarball."
                           "Removed tarball.")
            functions.exec_oe("rm -f %s/dist/*-%s.tar.gz" % (svn_path, name))
        else:
            applogger.error(
                "Failed to execute 'tar xzf %s/dist/*-%s.tar.gz -C %s/%s/'." %
                (svn_path, name, target, lastdir))
            logging.error(
                "Failed to execute 'tar xzf %s/dist/*-%s.tar.gz -C %s/%s/'." %
                (svn_path, name, target, lastdir))
            applogger.error("Will try to untar from target directory %s." %
                            target)
            logging.error("Will try to untar from target directory %s." %
                          target)
            applogger.info("Extracting tarball %s/dist/*-%s.tar.gz into %s/%s/"
                           % (target, name, target, lastdir))
            res = os.system("tar xzf %s/*-%s.tar.gz -C %s/%s/" %
                            (target, name, target, lastdir))
            if res != 0:
                applogger.error(
                    "Failed to execute 'tar xzf %s/*-%s.tar.gz -C %s/%s/'." %
                    (target, name, target, lastdir))
                logging.error(
                    "Failed to execute 'tar xzf %s/*-%s.tar.gz -C %s/%s/'." %
                    (target, name, target, lastdir))
            else:
                applogger.info("Successfully extracted tarball."
                               "Removed tarball.")
                functions.exec_oe("rm -f %s/*-%s.tar.gz" % (target, name))
        return res

    def _extract_tarball(self, p_id, type_of_content, dry_run):
        # if we are here, this app has a svn path defined
        applogger = BUILD_ECONOMY[p_id][1]["logger"]
        target = "%s/%s-%s" % (
            BUILD_ECONOMY[p_id][0].svn.path,
            Config.get("target", BUILD_ECONOMY[p_id][0].region),
            BUILD_ECONOMY[p_id][0].region)

        res = -1
        if type_of_content == "static":
            applogger.debug("Creating folder %s/www/" % target)
            functions.exec_oe("mkdir -p %s/www/" % target)
            res = self._try_extract(BUILD_ECONOMY[p_id][0].svn.path, target,
                                    "www", applogger, "www")
            if res != 0:
                applogger.info("Trying to extract using type of content: %s" %
                               type_of_content)
                res = self._try_extract(BUILD_ECONOMY[p_id][0].svn.path,
                                        target, type_of_content, applogger,
                                        "www")

        elif type_of_content == "dynamic":
            applogger.debug("Creating folder %s/webapp/" % target)
            functions.exec_oe("mkdir -p %s/webapp/" % target)
            res = self._try_extract(BUILD_ECONOMY[p_id][0].svn.path, target,
                                    "webapp", applogger, "webapp")
            if res != 0:
                applogger.info("Trying to extract using type of content: %s" %
                               type_of_content)
                res = self._try_extract(BUILD_ECONOMY[p_id][0].svn.path,
                                        target, type_of_content, applogger,
                                        "webapp")

        if res == 0:
            applogger.info(
                "Successfully extracted %s tarball for application %s." %
                (type_of_content, BUILD_ECONOMY[p_id][0].name))
            logging.info(
                "Successfully extracted %s tarball for application %s." %
                (type_of_content, BUILD_ECONOMY[p_id][0].name))
            return (SUCCESS, "%s tarball for %s extracted." % (
                type_of_content.capitalize(), BUILD_ECONOMY[p_id][0].name))
        else:
            applogger.error("Failed to extract %s tarball for %s." % (
                type_of_content.capitalize(), BUILD_ECONOMY[p_id][0].name))
            return (ERROR, "Failed to extract %s tarball for %s." % (
                type_of_content.capitalize(), BUILD_ECONOMY[p_id][0].name))

    def _move_content_into_target(self, p_id, type_of_content, dry_run):
        applogger = BUILD_ECONOMY[p_id][1]["logger"]
        flags = copy.deepcopy(BUILD_ECONOMY[p_id][0].flags)

        target = "%s/%s-%s" % (
            BUILD_ECONOMY[p_id][0].svn.path,
            Config.get("target", BUILD_ECONOMY[p_id][0].region),
            BUILD_ECONOMY[p_id][0].region)
        src_dir = "%s/%s/" % (target, type_of_content)

        if flags.get("loc%s" % type_of_content.capitalize()) is not None:
            src_dir = "%s%s" % (BUILD_ECONOMY[p_id][0].svn.path, flags.get(
                "loc%s" % type_of_content.capitalize()))
        else:
            if not os.path.isdir(src_dir):
                if type_of_content == "static":
                    src_dir = "%s%s" % (BUILD_ECONOMY[p_id][0].svn.path,
                                        "/dist/www/")
                elif type_of_content == "dynamic":
                    src_dir = "%s%s" % (BUILD_ECONOMY[p_id][0].svn.path,
                                        "/dist/webapp/")

        applogger.info("Source directory for this application will be: %s" %
                       src_dir)

        res = -1
        # set up the common rsync command line we want to use
        rsync_cmdline = 'rsync %s --delete --exclude "%s*" %s %s/*' % (
            Config.get("rsync_opts"), Config.get("target")[1:],
            Config.get("rsync_drone_excludes"), src_dir)

        if type_of_content == "static":
            applogger.debug("Creating folder %s/www/" % target)
            functions.exec_oe("mkdir -p %s/www/" % target)
            # rsyncs content into target directory ignoring the target directory
            # else applications like launcher (EU old) would not work
            applogger.debug('Executing: %s %s/www/' % (rsync_cmdline, target))
            res = os.system('%s %s/www/' % (rsync_cmdline, target))

            if res == 0:
                # try to delete directory TARGET if it was copied
                applogger.debug(
                    "Sync was successful, removing folder %s/www/%s*" %
                    (target, Config.get("target", BUILD_ECONOMY[p_id][
                        0].region).strip("/").split("/")[0]))
                res = os.system("rm -rf %s/www/%s*" % (target, Config.get(
                    "target",
                    BUILD_ECONOMY[p_id][0].region).strip("/").split("/")[0]))
        elif type_of_content == "dynamic":
            applogger.debug("Creating folder %s/webapp/" % target)
            functions.exec_oe("mkdir -p %s/webapp/" % target)
            # rsyncs content into target directory ignoring the target directory
            # else applications like launcher (EU old) would not work
            applogger.debug('Executing: %s %s/webapp/' %
                            (rsync_cmdline, target))
            res = os.system("%s %s/webapp/" % (rsync_cmdline, target))
            if res == 0:
                # try to delete directory TARGET if it was copied
                applogger.debug(
                    "Sync was successful, removing folder %s/webapp/%s" %
                    (target, Config.get("target", BUILD_ECONOMY[p_id][
                        0].region).strip("/").split("/")[0]))
                res = os.system("rm -rf %s/webapp/%s*" % (target, Config.get(
                    "target",
                    BUILD_ECONOMY[p_id][0].region).strip("/").split("/")[0]))

        if res == 0:
            applogger.info(
                "Successfully copied the %s content to the correct location for application %s."
                % (type_of_content, BUILD_ECONOMY[p_id][0].name))
            logging.info(
                "Successfully copied the %s content to the correct location for application %s."
                % (type_of_content, BUILD_ECONOMY[p_id][0].name))
            return (SUCCESS,
                    "%s content for %s copied to the correct location.\n" %
                    (type_of_content.capitalize(),
                     BUILD_ECONOMY[p_id][0].name))
        applogger.info(
            "Failed to copy the %s content to the correct location for application %s."
            % (type_of_content, BUILD_ECONOMY[p_id][0].name))
        logging.info(
            "Failed to copy the %s content to the correct location for application %s."
            % (type_of_content, BUILD_ECONOMY[p_id][0].name))
        return (ERROR, "%s content for %s was not copied successfully." %
                (type_of_content.capitalize(), BUILD_ECONOMY[p_id][0].name))

    def _rsync(self, p_id, type_of_content, rsync_opts, old, dry_run):
        applogger = BUILD_ECONOMY[p_id][1]["logger"]

        if dry_run:
            applogger.debug("DRY_RUN: ssh %s %s/apps.py --type %s %s" % (
                Config.get("nfs_ip", BUILD_ECONOMY[p_id][0].region),
                Config.get("nfs_utils", BUILD_ECONOMY[p_id][0].region),
                type_of_content, BUILD_ECONOMY[p_id][0].name))

            # XXX: implement for applications with the old flag
            if type_of_content == "static":
                applogger.info(
                    'Executing: rsync %s %s %s %s/dist/%s/www/ %s:DESTINATION_ON_NFS_FOLDER'
                    % (Config.get("rsync_opts"), rsync_opts,
                       Config.get("rsync_nfs_excludes"),
                       BUILD_ECONOMY[p_id][0].svn.path,
                       BUILD_ECONOMY[p_id][0].ant.binfo.get("build.type", ""),
                       Config.get("nfs_ip", BUILD_ECONOMY[p_id][0].region)))

            elif type_of_content == "dynamic":
                applogger.info(
                    'Executing: rsync %s %s %s %s/dist/%s/webapp/ %s:DESTINATION_ON_NFS_FOLDER'
                    % (Config.get("rsync_opts"), rsync_opts,
                       Config.get("rsync_nfs_excludes"),
                       BUILD_ECONOMY[p_id][0].svn.path,
                       BUILD_ECONOMY[p_id][0].ant.binfo.get("build.type", ""),
                       Config.get("nfs_ip", BUILD_ECONOMY[p_id][0].region)))
            return (SUCCESS, "Deployed %s %s content to the nfs." %
                    (BUILD_ECONOMY[p_id][0].name, type_of_content))

        applogger.debug("Executing: ssh %s %s/apps.py --type %s %s" % (
            Config.get("nfs_ip", BUILD_ECONOMY[p_id][0].region),
            Config.get("nfs_utils", BUILD_ECONOMY[p_id][0].region),
            type_of_content, BUILD_ECONOMY[p_id][0].name))

        rcode, output, error = functions.exec_oe(
            "ssh %s %s/apps.py --type %s %s" %
            (Config.get("nfs_ip", BUILD_ECONOMY[p_id][0].region),
             Config.get("nfs_utils", BUILD_ECONOMY[p_id][0].region),
             type_of_content, BUILD_ECONOMY[p_id][0].name))

        if len(output) > 0:
            nfs_folder = output
        else:
            applogger.info(
                "FAILURE: Tried to rsync %s content with a top dir in the NFS."
                % type_of_content)
            logging.info(
                "FAILURE: Tried to rsync %s content with a top dir in the NFS."
                % type_of_content)
            return (ERROR,
                    "Tried to rsync %s content with a top dir in the NFS ." %
                    type_of_content)

        res = -1
        if type_of_content == "static":
            if old:
                applogger.info(
                    "Syncing application from %s/%s-%s/www/ to %s:%s." %
                    (BUILD_ECONOMY[p_id][0].svn.path,
                     Config.get("target", BUILD_ECONOMY[p_id][0].region),
                     BUILD_ECONOMY[p_id][0].region,
                     Config.get("nfs_ip", BUILD_ECONOMY[p_id][0].region),
                     nfs_folder))
                res = os.system(
                    r'rsync %s %s %s %s/%s-%s/www/ %s:%s' %
                    (Config.get("rsync_opts"), rsync_opts,
                     Config.get("rsync_nfs_excludes"),
                     BUILD_ECONOMY[p_id][0].svn.path,
                     Config.get("target", BUILD_ECONOMY[p_id][0].region),
                     BUILD_ECONOMY[p_id][0].region,
                     Config.get("nfs_ip", BUILD_ECONOMY[p_id][0].region),
                     nfs_folder))
            else:
                applogger.info(
                    'Executing: rsync %s %s %s %s/dist/%s/www/ %s:%s' %
                    (Config.get("rsync_opts"), rsync_opts,
                     Config.get("rsync_nfs_excludes"),
                     BUILD_ECONOMY[p_id][0].svn.path,
                     BUILD_ECONOMY[p_id][0].ant.binfo.get("build.type", ""),
                     Config.get("nfs_ip", BUILD_ECONOMY[p_id][0].region),
                     nfs_folder))

                res = os.system(
                    r'rsync %s %s %s %s/dist/%s/www/ %s:%s' %
                    (Config.get("rsync_opts"), rsync_opts,
                     Config.get("rsync_nfs_excludes"),
                     BUILD_ECONOMY[p_id][0].svn.path,
                     BUILD_ECONOMY[p_id][0].ant.binfo.get("build.type", ""),
                     Config.get("nfs_ip", BUILD_ECONOMY[p_id][0].region),
                     nfs_folder))

        if type_of_content == "dynamic":
            if old:
                applogger.info(
                    "Syncing application from %s/%s-%s/webapp/ to %s:%s." %
                    (BUILD_ECONOMY[p_id][0].svn.path,
                     Config.get("target", BUILD_ECONOMY[p_id][0].region),
                     BUILD_ECONOMY[p_id][0].region,
                     Config.get("nfs_ip", BUILD_ECONOMY[p_id][0].region),
                     nfs_folder))
                res = os.system(
                    r'rsync %s %s %s %s/%s-%s/webapp/ %s:%s' %
                    (Config.get("rsync_opts"), rsync_opts,
                     Config.get("rsync_nfs_excludes"),
                     BUILD_ECONOMY[p_id][0].svn.path,
                     Config.get("target", BUILD_ECONOMY[p_id][0].region),
                     BUILD_ECONOMY[p_id][0].region,
                     Config.get("nfs_ip", BUILD_ECONOMY[p_id][0].region),
                     nfs_folder))
            else:
                applogger.info(
                    'Executing: rsync %s %s %s %s/dist/%s/webapp/ %s:%s' %
                    (Config.get("rsync_opts"), rsync_opts,
                     Config.get("rsync_nfs_excludes"),
                     BUILD_ECONOMY[p_id][0].svn.path,
                     BUILD_ECONOMY[p_id][0].ant.binfo.get("build.type", ""),
                     Config.get("nfs_ip", BUILD_ECONOMY[p_id][0].region),
                     nfs_folder))

                res = os.system(
                    r'rsync %s %s %s %s/dist/%s/webapp/ %s:%s' %
                    (Config.get("rsync_opts"), rsync_opts,
                     Config.get("rsync_nfs_excludes"),
                     BUILD_ECONOMY[p_id][0].svn.path,
                     BUILD_ECONOMY[p_id][0].ant.binfo.get("build.type", ""),
                     Config.get("nfs_ip", BUILD_ECONOMY[p_id][0].region),
                     nfs_folder))
        if res == 0:
            # XXX: Changing ownership on the NFS. This is stupid as it is. Do NOT do it!
            res_own = os.system(
                r'ssh %s %s -R %s.%s %s' %
                (Config.get("nfs_ip", BUILD_ECONOMY[p_id][0].region),
                 Config.get("nfs_chown", BUILD_ECONOMY[p_id][0].region),
                 Config.get("nfs_user", BUILD_ECONOMY[p_id][0].region),
                 Config.get("nfs_group", BUILD_ECONOMY[p_id][0].region),
                 nfs_folder))
            if res_own == 0:
                applogger.info(
                    "Successfully changed ownership (%s.%s) on the nfs for folder %s ."
                    % (Config.get("nfs_user", BUILD_ECONOMY[p_id][0].region),
                       Config.get("nfs_group", BUILD_ECONOMY[p_id][0].region),
                       nfs_folder))
            else:
                # it's ok to not return error here
                applogger.info(
                    "Could not change ownership (%s.%s) on the nfs for folder %s ."
                    % (Config.get("nfs_user", BUILD_ECONOMY[p_id][0].region),
                       Config.get("nfs_group", BUILD_ECONOMY[p_id][0].region),
                       nfs_folder))

            applogger.info("Deployed %s %s content to the nfs." %
                           (BUILD_ECONOMY[p_id][0].name, type_of_content))
            return (SUCCESS, "Deployed %s %s content to the nfs." %
                    (BUILD_ECONOMY[p_id][0].name, type_of_content))
        applogger.error("Could not deploy %s %s content to the nfs." %
                        (BUILD_ECONOMY[p_id][0].name, type_of_content))
        return (ERROR, "Could not deploy %s %s content to the nfs." %
                (BUILD_ECONOMY[p_id][0].name, type_of_content))

    def _check_content(self, flags, type_content):
        if flags:
            if flags.get("static",
                         "yes") == "yes" and type_content == "static":
                return type_content
            if flags.get("dynamic",
                         "yes") == "yes" and type_content == "dynamic":
                return type_content
        else:
            if type_content:
                return type_content
        # last resort return None
        return None

    def _app_deploy_old(self, p_id, type_content, rsync_delete, nonfs,
                        dry_run):
        """
        If we are here, everything is set for the application,
        so we don't need to do any kinds of checks.
        """
        result = []
        clback = None

        applogger = BUILD_ECONOMY[p_id][1]["logger"]

        # if we got here... we have flags (even if it's only flag "old")
        flags = copy.deepcopy(BUILD_ECONOMY[p_id][0].flags)

        # if we are doing this through tarballs...
        if flags.get("tarball", "no") == "yes":
            clback = self._extract_tarball
        else:
            clback = self._move_content_into_target

        if self._check_content(flags, type_content) == "static":
            res = clback(p_id, "static", dry_run)
            if res[0] == SUCCESS:
                result.append(res[1])

        elif self._check_content(flags, type_content) == "dynamic":
            res = clback(p_id, "dynamic", dry_run)
            if res[0] == SUCCESS:
                result.append(res[1])

        elif self._check_content(flags, type_content) == None:
            if flags.get("static", "yes") == "yes":
                res = clback(p_id, "static", dry_run)
                if res[0] == SUCCESS:
                    result.append(res[1])
            if flags.get("dynamic", "yes") == "yes":
                res = clback(p_id, "dynamic", dry_run)
                if res[0] == SUCCESS:
                    result.append(res[1])

        msg = "\n".join(result)
        # if we have nonfs set to False (default), deploy the content to the nfs.
        if nonfs:
            applogger.info("nonfs flag was passed. Not deploying to the nfs.")
        else:
            res = self._rsync_deploy(p_id, type_content, flags, rsync_delete,
                                     True, dry_run)
            # if we have an error, ignore previous messages (XXX: should we return the previous messages?)
            if res[0] == ERROR:
                msg = ""

        return (res[0], msg + res[1])

    def _rsync_deploy(self,
                      p_id,
                      type_content,
                      flags,
                      rsync_delete,
                      old=False,
                      dry_run=False):
        # XXX: log this method properly!!!
        msg = ""

        rsync_opts = "-r "
        if rsync_delete:
            rsync_opts = "--delete "

        if self._check_content(flags, type_content) == None:
            # this is a special case where it's a new application and there are no flags _AT_ALL_
            # Todd should call with the type defined ./cli.py -D 1 --type <static>/<dynamic>
            if flags is None:
                res_static = self._rsync(p_id, "static", rsync_opts, old,
                                         dry_run)
                if res_static[0] == ERROR:
                    return (res_static[0], res_static[1])
                msg += "\n" + res_static[1]
                res_dynamic = self._rsync(p_id, "dynamic", rsync_opts, old,
                                          dry_run)
                if res_dynamic[0] == ERROR:
                    return (res_dynamic[0], res_dynamic[1])
                msg += "\n" + res_dynamic[1]

            else:
                if flags.get("static", "yes") == "yes":
                    res_static = self._rsync(p_id, "static", rsync_opts, old,
                                             dry_run)
                    if res_static[0] == ERROR:
                        return (res_static[0], res_static[1])
                    msg += "\n" + res_static[1]
                if flags.get("dynamic", "yes") == "yes":
                    res_dynamic = self._rsync(p_id, "dynamic", rsync_opts, old,
                                              dry_run)
                    if res_dynamic[0] == ERROR:
                        return (res_dynamic[0], res_dynamic[1])
                    msg += "\n" + res_dynamic[1]

        elif self._check_content(flags, type_content) == "static":
            res_static = self._rsync(p_id, "static", rsync_opts, old, dry_run)
            if res_static[0] == ERROR:
                return (res_static[0], res_static[1])
            msg += "\n" + res_static[1]

        elif self._check_content(flags, type_content) == "dynamic":
            res_dynamic = self._rsync(p_id, "dynamic", rsync_opts, old,
                                      dry_run)
            if res_dynamic[0] == ERROR:
                return (res_dynamic[0], res_dynamic[1])
            msg += "\n" + res_dynamic[1]

        return (SUCCESS, msg)

    def exposed_app_deploy(self, p_id, flags_, type_content, rsync_delete,
                           nonfs, region, dry_run):
        """
        Deploy application into nfs.
        """

        if p_id not in BUILD_ECONOMY:
            self.logger.error("Build id %s is not valid.", p_id)
            return (ERROR, "ERROR: Not a valid build id.")

        if BUILD_ECONOMY[p_id][1]["status"] != BuildStates.BUILD_STATE_WAITING:
            if BUILD_ECONOMY[p_id][1][
                    "status"] == BuildStates.BUILD_STATE_ERRORED:
                self.logger.error(
                    "A previous command to this application (%s) errored out."
                    % BUILD_ECONOMY[p_id][0].name)
                return (
                    ERROR,
                    "ERROR: A previous command to this application errored out."
                )
            self.logger.error(
                "There is an ongoing operation on application %s." %
                BUILD_ECONOMY[p_id][0].name)
            return (
                ERROR,
                "ERROR: There is an ongoing operation on this application.")

        BUILD_ECONOMY[p_id][1]["status"] = BuildStates.BUILD_STATE_SYNCING

        applogger = BUILD_ECONOMY[p_id][1]["logger"]

        # if flags were passed from the command line, put them into place
        if flags_:
            self.logger.info("Flags were passed from the command line." \
                                 "Updating application with these new flags.")
            applogger.info("Flags were passed from the command line." \
                               "Updating application deploy with these new flags.")
            BUILD_ECONOMY[p_id][0].compile_new_flags(flags_)

        flags = None
        if BUILD_ECONOMY[p_id][0].flags:
            flags = copy.deepcopy(BUILD_ECONOMY[p_id][0].flags)

        # if we pass on a region, make sure we save the region we had before,
        # in case we go back to an operation that requires it
        tmp_region = None
        if (region is not None) and (flags is not None):
            regions = flags.get("regions", None)
            if regions is not None:
                if region in regions:
                    tmp_region = BUILD_ECONOMY[p_id][0].region
                    BUILD_ECONOMY[p_id][0].region = region

        if flags:
            # if this is an application that uses an old config,
            # call another method specifically for this.
            applogger.info("The following flags apply:")
            for flag in flags:
                applogger.info("%s -> %s" % (flag, flags[flag]))

            if flags.get("old", "no") == "yes":
                result = self._app_deploy_old(p_id, type_content, rsync_delete,
                                              nonfs, dry_run)
                BUILD_ECONOMY[p_id][1][
                    "status"] = BuildStates.BUILD_STATE_WAITING
                if tmp_region is not None:
                    BUILD_ECONOMY[p_id][0].region = tmp_region
                return (result[0], result[1])

        if nonfs:
            applogger.info(
                "nonfs flag was passed and this is an application that follows the Simple Template Documentation.")
            applogger.info(
                "You will not see any content on the nfs at this point.")
            BUILD_ECONOMY[p_id][1]["status"] = BuildStates.BUILD_STATE_WAITING
            if tmp_region is not None:
                BUILD_ECONOMY[p_id][0].region = tmp_region
            return (SUCCESS, "")

        res = self._rsync_deploy(p_id,
                                 type_content,
                                 flags,
                                 rsync_delete,
                                 dry_run=dry_run)
        BUILD_ECONOMY[p_id][1]["status"] = BuildStates.BUILD_STATE_WAITING
        if tmp_region is not None:
            BUILD_ECONOMY[p_id][0].region = tmp_region
        return (res[0], res[1])

    def _run_deploy(self, p_id, cmd, ip=None, appname=None, type_content=None):
        if ip != None:
            return os.system(cmd % (
                Config.get("nfs_ip", BUILD_ECONOMY[p_id][0].region),
                Config.get("nfs_utils", BUILD_ECONOMY[p_id][0].region), ip))

        # if we don't pass an ip, we have an appname and type_content for sure
        if (appname == None) and (type_content == None):
            self.logger.error("Appname and type_content can't _EVER_ be None")
            return -1
        self.logger.info(
            cmd % (Config.get("nfs_ip", BUILD_ECONOMY[p_id][0].region),
                   Config.get("nfs_utils", BUILD_ECONOMY[p_id][0].region),
                   appname, type_content))
        return os.system(
            cmd % (Config.get("nfs_ip", BUILD_ECONOMY[p_id][0].region),
                   Config.get("nfs_utils", BUILD_ECONOMY[p_id][0].region),
                   appname, type_content))

    def exposed_app_restart(self, p_id, type_content, ip, region, dry_run):
        # XXX: comment this!!!
        # USES deploy2.py
        # WARNING: THIS IS ABSOLUTE CRAP! Please rewrite this (actually rewrite deploy2.py first!) properly.
        #          Actually touches the deploy file a second time and delays the restart for 30secs (read deploy2.py).
        if BUILD_ECONOMY[p_id][1]["status"] == BuildStates.BUILD_STATE_ERRORED:
            self.logger.error(
                "A previous command to this application (%s) errored out." %
                BUILD_ECONOMY[p_id][0].name)
            return (
                ERROR,
                "ERROR: A previous command to this application errored out.")

        if ip != "":
            res = self._run_deploy(p_id, DeployController.FORCE_RESTART, ip=ip)
            if res == 0:
                return (SUCCESS, "Successfully restarted the tomcat on ip %s."
                        % ip)
            return (ERROR, "Could not restart the tomcat on ip %s." % ip)

        appname = BUILD_ECONOMY[p_id][0].name
        applogger = BUILD_ECONOMY[p_id][1]["logger"]

        # if we pass on a region, make sure we save the region we had before,
        # in case we go back to an operation that requires it
        tmp_region = None
        flags = BUILD_ECONOMY[p_id][0].flags
        if (region is not None) and (flags is not None):
            regions = flags.get("regions", None)
            if regions is not None:
                if region in regions:
                    tmp_region = BUILD_ECONOMY[p_id][0].region
                    BUILD_ECONOMY[p_id][0].region = region

        res = -1
        if type_content:
            res = self._run_deploy(p_id,
                                   DeployController.RESTART,
                                   appname=appname,
                                   type_content=type_content)
        else:
            msg = ""
            if BUILD_ECONOMY[p_id][0].flags.get("static", "yes") == "yes":
                res = self._run_deploy(p_id,
                                       DeployController.RESTART,
                                       appname=appname,
                                       type_content="static")
                if res == 0:
                    msg = "%s%s" % (
                        msg,
                        "Successfully touched deploy file for static.\n\n")
                else:
                    msg = "%s%s" % (
                        msg, "Could not touch deploy file for static.\n\n")

            if BUILD_ECONOMY[p_id][0].flags.get("dynamic", "yes") == "yes":
                res = self._run_deploy(p_id,
                                       DeployController.RESTART,
                                       appname=appname,
                                       type_content="dynamic")
                if res == 0:
                    msg = "%s%s" % (
                        msg,
                        "Successfully touched deploy file for dynamic and restart the tomcats for application %s with id %s.\n\n"
                        % (appname, p_id))
                else:
                    msg = "%s%s" % (
                        msg,
                        "Could not touch deploy file for dynamic and restart the tomcats.\n\n"
                    )

            # change back the region to what it was
            if tmp_region is not None:
                BUILD_ECONOMY[p_id][0].region = tmp_region

            # possible bug here... because it will only check the last res
            applogger.info(msg)
            if res == 0:
                return (SUCCESS, msg)
            return (ERROR, msg)

        # change the region back to what it was
        if tmp_region is not None:
            BUILD_ECONOMY[p_id][0].region = tmp_region

        if res == 0:
            applogger.info(
                "Successfully restarted the tomcats for application %s with id %s."
                % (appname, p_id))
            return (
                SUCCESS,
                "Successfully restarted the tomcats for application %s with id %s."
                % (appname, p_id))
        applogger.info(
            "Could not restart the tomcats for application %s with id %s." %
            (appname, p_id))
        return (ERROR,
                "Could not restart the tomcats for application %s with id %s."
                % (appname, p_id))

    def exposed_app_sync(self, p_id, type_content, region, dry_run):
        # XXX: comment this!!!
        appname = BUILD_ECONOMY[p_id][0].name
        if BUILD_ECONOMY[p_id][1]["status"] == BuildStates.BUILD_STATE_ERRORED:
            self.logger.error(
                "A previous command to this application (%s) errored out." %
                BUILD_ECONOMY[p_id][0].name)
            return (
                ERROR,
                "ERROR: A previous command to this application errored out.")

        applogger = BUILD_ECONOMY[p_id][1]["logger"]

        # if we pass on a region, make sure we save the region we had before,
        # in case we go back to an operation that requires it
        tmp_region = None
        flags = BUILD_ECONOMY[p_id][0].flags
        if (region is not None) and (flags is not None):
            regions = flags.get("regions", None)
            if regions is not None:
                if region in regions:
                    tmp_region = BUILD_ECONOMY[p_id][0].region
                    BUILD_ECONOMY[p_id][0].region = region

        res = -1
        if type_content:
            res = self._run_deploy(p_id,
                                   DeployController.SYNC,
                                   appname=appname,
                                   type_content=type_content)
        else:
            msg = ""
            if BUILD_ECONOMY[p_id][0].flags.get("static", "yes") == "yes":
                res = self._run_deploy(p_id,
                                       DeployController.SYNC,
                                       appname=appname,
                                       type_content="static")
                if res == 0:
                    msg = "%s%s" % (
                        msg,
                        "Successfully touched deploy file for static.\n\n")
                else:
                    msg = "%s%s" % (
                        msg, "Could not touch deploy file for static.\n\n")

            if BUILD_ECONOMY[p_id][0].flags.get("dynamic", "yes") == "yes":
                res = self._run_deploy(p_id,
                                       DeployController.SYNC,
                                       appname=appname,
                                       type_content="dynamic")
                if res == 0:
                    msg = "%s%s" % (
                        msg,
                        "Successfully touched deploy file for dynamic.\n\n")
                else:
                    msg = "%s%s" % (
                        msg, "Could not touch deploy file for dynamic.\n\n")

            # change the region back to what it was
            if tmp_region is not None:
                BUILD_ECONOMY[p_id][0].region = tmp_region

            # possible bug here... because it will only check the last res
            applogger.info(msg)
            if res == 0:
                return (SUCCESS, msg)
            return (ERROR, msg)

        # change the region back to what it was
        if tmp_region is not None:
            BUILD_ECONOMY[p_id][0].region = tmp_region

        if res == 0:
            applogger.info("Touched deploy file successfully in the nfs.")
            return (SUCCESS, "Touched deploy file successfully in the nfs.")
        applogger.info("Was not able to touch deploy file in the nfs.")
        return (ERROR, "Was not able to touch deploy file in the nfs.")


if __name__ == '__main__':
    logging.basicConfig(filename="%s/server-%s" % (Config.get(
        "server_logs"), time.strftime(Config.get("log_timestamp_fmt"))),
                        level=logging.DEBUG,
                        format=Config.get("log_string_fmt"),
                        datefmt=Config.get("log_timestamp_fmt"))

    signal.signal(signal.SIGHUP, reload_config_handler)
    ThreadedServer(Builder, port=Config.get("server_port")).start()
