# -*- coding: utf-8 -*-

# Contacts:
#   - Chris Antenesse <cantenesse@sample.com>
#   - Norberto Lopes <nlopes@sample.com>

import copy
import locale
import logging

import os
import sys
import subprocess

import pysvn

# ours
sys.path.append(os.path.abspath(".."))
import Config
import functions
import parsers
from variables import SUCCESS, ERROR, ConfigXML

SVN_NOTIFICATIONS = {
    pysvn.wc_notify_action.add: 'A',
    pysvn.wc_notify_action.commit_added: 'A',
    pysvn.wc_notify_action.commit_deleted: 'D',
    pysvn.wc_notify_action.commit_modified: 'M',
    pysvn.wc_notify_action.commit_postfix_txdelta: None,
    pysvn.wc_notify_action.commit_replaced: 'R',
    pysvn.wc_notify_action.copy: 'c',
    pysvn.wc_notify_action.delete: 'D',
    pysvn.wc_notify_action.failed_revert: 'F',
    pysvn.wc_notify_action.resolved: 'R',
    pysvn.wc_notify_action.restore: 'R',
    pysvn.wc_notify_action.revert: 'R',
    pysvn.wc_notify_action.skip: 'skip',
    pysvn.wc_notify_action.status_completed: None,
    pysvn.wc_notify_action.status_external: 'X',
    pysvn.wc_notify_action.update_add: 'A',
    pysvn.wc_notify_action.update_completed: None,
    pysvn.wc_notify_action.update_delete: 'D',
    pysvn.wc_notify_action.update_external: 'X',
    pysvn.wc_notify_action.update_update: 'U',
    pysvn.wc_notify_action.annotate_revision: 'A',
}


class BuildManager(object):
    def __init__(self, name, btype, specified_region, path, logger):
        super(BuildManager, self).__init__()
        self.logger = logger
        self.orig_path = os.getcwd()
        self.cur_path = path
        self.binfo = ConfigXML.build.get_build_info(btype, specified_region)
        self.application_name = name
        self.buildcmd = None
        self.region = specified_region

    def _parse_build_flags(self, bflags):
        del self.binfo
        self.binfo = {}
        tmp_flags = bflags.strip().split(",")
        for flag in tmp_flags:
            name, value = flag.strip().split("=")
            if name == "target" and value is not None:
                self.binfo["target"] = value
            elif name == "target" and value is None:
                return (ERROR, ("No target build specified.", None))
            else:
                self.binfo[name.strip()] = value.strip()
        return (SUCCESS, (None, None))

    def _build_flags_str(self):
        flagstr = ""
        for (name, value) in self.binfo.items():
            # we want to ignore the target value
            if name == "target":
                continue

            if name == "app.tagname" and (value is None or value == ""):
                flagstr += "-D%s=%s " % (name, self.application_name)
            else:
                flagstr += "-D%s=%s " % (name, value)
        return flagstr

    def _build_skel(self, bflags):
        if not self.binfo and bflags == "":
            return (ERROR, ("Need building info.", ""))

        # if build flags are passed into this function
        # we want to populate binfo with those flags
        # which means we lose the default settings for this app
        # unless it's loaded again
        if bflags != "":
            return self._parse_build_flags(bflags)

    def clean(self, bflags, isold, isjava6):
        result = self._build_skel(bflags)
        if result is not None:
            if result[0] == ERROR:
                return result

        # change to path
        os.chdir(self.cur_path)
        if isold:
            functions.export_var(
                "TARGET_DIR",
                "%s%s-%s" % (self.cur_path.rstrip("/"),
                             Config.get("target", self.region), self.region))
        functions.export_var(self._CMD_HOME_NAME,
                             Config.get(self._CMD_NAME, self.region))
        if isjava6:
            functions.export_var("JAVA_HOME", Config.get("java6", self.region))
        else:
            functions.export_var("JAVA_HOME", Config.get("java", self.region))
        functions.export_var("CATALINA_HOME", Config.get(
            "tomcat", self.region))
        if "build.type" in self.binfo:
            result = functions.exec_oe(
                self._CMD_CLEAN %
                (self._CMD_NAME, "-Dbuild.type=%s" % self.binfo["build.type"]))
        else:
            result = functions.exec_oe(self._CMD_CLEAN % (self._CMD_NAME, ""))
        if isjava6:
            functions.export_var("JAVA_HOME", Config.get("java6", self.region))
        else:
            functions.export_var("JAVA_HOME", Config.get("java", self.region))
        functions.export_var("CATALINA_HOME", "")
        functions.export_var(self._CMD_HOME_NAME, "")
        if isold:
            functions.export_var("TARGET_DIR", "")
        os.chdir(self.orig_path)
        return (result[0], (result[1], result[2]))

    def build(self, bflags, isjava6):
        result = self._build_skel(bflags)
        if result is not None:
            if result[0] == ERROR:
                return result

        flagstr = self._build_flags_str()
        os.chdir(self.cur_path)
        if isjava6:
            functions.export_var("JAVA_HOME", Config.get("java6", self.region))
        else:
            functions.export_var("JAVA_HOME", Config.get("java", self.region))
        functions.export_var("CATALINA_HOME", Config.get(
            "tomcat", self.region))
        functions.export_var(self._CMD_HOME_NAME,
                             Config.get(self._CMD_NAME, self.region))
        self.buildcmd = self._CMD_BUILD % (self._CMD_NAME, flagstr,
                                           Config.get(self._CMD_TARGET_NAME,
                                                      self.region))
        result = functions.exec_oe(self.buildcmd)
        if isjava6:
            functions.export_var("JAVA_HOME", Config.get("java6", self.region))
        else:
            functions.export_var("JAVA_HOME", Config.get("java", self.region))
        functions.export_var("CATALINA_HOME", "")
        functions.export_var(self._CMD_HOME_NAME, "")
        os.chdir(self.orig_path)
        return (result[0], (result[1], result[2]))


class BuildManagerOld(BuildManager):
    def __init__(self, name, btype, specified_region, path, logger):
        super(BuildManagerOld, self).__init__(name, btype, specified_region,
                                              path, logger)

    def build_old(self, bflags, isjava6):
        result = self._build_skel(bflags)
        if result is not None:
            if result[0] == ERROR:
                return result

        flagstr = self._build_flags_str()
        os.chdir(self.cur_path)
        functions.export_var(
            "TARGET_DIR",
            "%s%s-%s" % (self.cur_path.rstrip("/"),
                         Config.get("target", self.region), self.region))
        if isjava6:
            functions.export_var("JAVA_HOME", Config.get("java6", self.region))
        else:
            functions.export_var("JAVA_HOME", Config.get("java", self.region))
        functions.export_var("CATALINA_HOME", Config.get(
            "tomcat", self.region))
        functions.export_var(self._CMD_HOME_NAME,
                             Config.get(self._CMD_NAME, self.region))
        self.buildcmd = self._CMD_BUILD % (self._CMD_NAME, flagstr,
                                           self.binfo["target"])
        result = functions.exec_oe(self.buildcmd)
        functions.export_var("TARGET_DIR", "")
        if isjava6:
            functions.export_var("JAVA_HOME", Config.get("java6", self.region))
        else:
            functions.export_var("JAVA_HOME", Config.get("java", self.region))
        functions.export_var("CATALINA_HOME", "")
        functions.export_var(self._CMD_HOME_NAME, "")
        os.chdir(self.orig_path)
        return (result[0], (result[1], result[2]))


class Maven(BuildManager):
    _CMD_HOME_NAME = "MAVEN_HOME"
    _CMD_NAME = "mvn"
    _CMD_BUILD = "%s %s %s"
    _CMD_CLEAN = "%s %s clean"
    _CMD_TARGET_NAME = "mvn_def_target"

    def __init__(self, name, btype, specified_region, path, logger):
        super(Maven, self).__init__(name, btype, specified_region, path,
                                    logger)


class Ant(BuildManagerOld):
    _CMD_HOME_NAME = "ANT_HOME"
    _CMD_NAME = "ant"
    _CMD_BUILD = "%s %s %s"
    _CMD_CLEAN = "%s %s -emacs clean"
    _CMD_TARGET_NAME = "ant_def_target"

    def __init__(self, name, btype, specified_region, path, logger):
        super(Ant, self).__init__(name, btype, specified_region, path, logger)


class Svn(object):
    """Easier interface for pysvn.
    Add methods as needed here."""

    def __init__(self, url, path, logger):
        self.logger = logger
        self.client = pysvn.Client()
        self.head = pysvn.Revision(pysvn.opt_revision_kind.head)
        self.url = url
        self.path = path
        self.client.callback_notify = self._log
        self.messages = []

        # if it's ready to do operations on it
        self.ready = True

        try:
            lcode, enc = locale.getdefaultlocale()
            locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
            self.info = self.client.info(self.path)
        except pysvn.ClientError, e:
            locale.setlocale(locale.LC_ALL, "%s.%s" % (lcode, enc))
            self.ready = False

    def update(self, rev=None, checkout=False):
        """Update to a revision.
        Return a tuple with revision number, revision message and
        the list of the changes for all files."""

        revision = self.head

        # if we don't have this here, we need to restart the server
        # in order to load svn information again and set self.ready

        lcode, enc = locale.getdefaultlocale()
        locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

        try:
            self.info = self.client.info(self.path)
        except pysvn.ClientError, e:
            print "not ready"
            self.ready = False

        if not self.ready and not checkout:
            print "1"
            locale.setlocale(locale.LC_ALL, "%s.%s" % (lcode, enc))
            return (-1, -1, [])
        elif not self.ready and checkout:
            print "2"
            # XXX: Implementation of checkout should go in here
            locale.setlocale(locale.LC_ALL, "%s.%s" % (lcode, enc))
            return (-1, -1, [])

        # If we are here... the app is checked out and we only want to update
        if rev:
            revision = pysvn.Revision(pysvn.opt_revision_kind.number, rev)

        # if update fails, it probably needs a cleanup
        # if it fails during the cleanup or the update
        # after the cleanup, do really raise the exception.
        try:
            rev_ = self.client.update(
                self.path, recurse=True, revision=revision)
        except pysvn.ClientError, e:
            try:
                # if this is not successful, *probably* means that we don't
                # have connection to the repository _OR_ that its parent
                # folder needs a cleanup
                self.client.cleanup(self.path)

                # XXX: we should enforce a cleanup on the parent folder here

                # cleanup messages if there are any
                self.messages = []
                rev_ = self.client.update(
                    self.path, recurse=True, revision=revision)
            except pysvn.ClientError, ee:
                print ee
                locale.setlocale(locale.LC_ALL, "%s.%s" % (lcode, enc))
                return (-1, -2, [])
            locale.setlocale(locale.LC_ALL, "%s.%s" % (lcode, enc))

        # the callback was called so we have messages
        # grab them and delete them
        changes = copy.deepcopy(self.messages)
        self.messages = []
        return (rev_, 0, changes)

    def _log(self, dct):
        if dct['action'] == pysvn.wc_notify_action.update_completed:
            self.revision_update_complete = dct['revision']
        elif dct['path'] != '' and SVN_NOTIFICATIONS[
                dct['action']] is not None:
            msg = '%s %s' % (SVN_NOTIFICATIONS[dct['action']], dct['path'])
            self.messages.append(msg)

    def revision(self):
        """Grab the revision number as a number. Oo"""
        lcode, enc = locale.getdefaultlocale()
        locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
        self.info = self.client.info(self.path)
        locale.setlocale(locale.LC_ALL, "%s.%s" % (lcode, enc))
        return self.info.revision.number

    def cleanup(self):
        """Perform svn cleanup."""
        lcode, enc = locale.getdefaultlocale()
        locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
        self.client.cleanup(self.path)
        locale.setlocale(locale.LC_ALL, "%s.%s" % (lcode, enc))


class Application(object):
    def __init__(self, dct, logger, read_only=False):
        self.logger = logger
        self.read_only = read_only

        # this should always come in the end of __init__
        self._load_config(dct)

    def _load_config(self, dct):
        self.name = dct["name"]
        self.path = None
        self.svn = None
        self.ant = None
        self.btype = None
        self.flags = {}
        self.deps = []
        self.region = dct["region"]

        if "buildtype" in dct:
            self.btype = dct["buildtype"]

        if "flags" in dct:
            self._convert_to_new_flag_format(dct["flags"])

        if "path" in dct:
            self.path = dct["path"]
            if not self.read_only:
                self.svn = Svn(
                    functions.get_real_svn_location(self.path),
                    Config.get("svn", self.region) + functions.escape_os_path(
                        self.path), self.logger)
            if self.btype:
                if self.flags.get("dynamic",
                                  "yes") == "yes" and not self.read_only:
                    if self.flags.get("maven", "no") == "yes":
                        self.ant = Maven(
                            self.name, self.btype, self.region,
                            Config.get("svn", self.region) +
                            functions.escape_os_path(self.path), self.logger)
                    else:
                        self.ant = Ant(
                            self.name, self.btype, self.region,
                            Config.get("svn", self.region) +
                            functions.escape_os_path(self.path), self.logger)

        if "fs" in dct:
            if "static" in dct["fs"]:
                self.flags["locStatic"] = dct["fs"]["static"]
            if "dynamic" in dct["fs"]:
                self.flags["locDynamic"] = dct["fs"]["dynamic"]

        if "dependencies" in dct:
            self.deps = dct["dependencies"]

    def reload_config(self):
        for app in ConfigXML.apps.get_apps():
            if app["name"] == self.name:
                if self.svn:
                    del self.svn
                if self.ant:
                    del self.ant
                self._load_config(copy.deepcopy(app))
                return (SUCCESS,
                        "Application %s reloaded successfully." % self.name)
        return (ERROR, """I could not load this application anymore: %s.\n
                If you changed an application name you do need to _restart_ the build server."""
                % self.name)

    def _convert_to_new_flag_format(self, flags):
        """This takes old style flags and puts them as new style flags."""
        for flag in flags:
            # old flags style
            if flag == "nostatic":
                self.flags["static"] = "no"
            elif flag == "nodynamic":
                self.flags["dynamic"] = "no"
            elif flag == "nostatictarball" or flag == "nodynamictarball":
                self.flags["tarball"] = "no"
            elif flag == "nodelete":
                self.flags["delete"] = "no"
            elif flag == "old":
                self.flags["old"] = "yes"
                # if it's an old configured application and we haven't
                # seen nostatictarball or nodynamictarball, we assume
                # tarball = yes
                self.flags["tarball"] = self.flags.get("tarball", "yes")
            elif flag == "java6":
                self.flags["java6"] = "yes"
            elif flag == "maven":
                self.flags["maven"] = "yes"
            elif flag == "nomenu" or flag == "clean" or flag == "fullclean" or \
                    flag == "sync-only" or flag == "update-only":
                continue

            # new flags style
            elif flags[flag] is not None:
                self.flags[flag] = flags[flag]

    def compile_new_flags(self, flags):
        """flags is a string: name=value separated by commas.
        This is if someone actually passes flags through cli.
        """

        for flag in flags.strip().split(","):
            name, value = flag.strip().split("=")
            self.flags[name.strip()] = value.strip()

    def __str__(self):
        str_ = "projectName=%s" % self.name
        if self.path:
            svn_loc = functions.get_real_svn_location(self.path)
            if svn_loc:
                str_ += ",svnLocation=%s" % svn_loc
        if self.btype:
            str_ += ",projectBuild=%s" % self.btype

        tmp_s = ','.join(
            ["%s=%s" % (name, value) for (name, value) in self.flags.items()])
        if tmp_s != '':
            str_ += ",projectFlags=[%s]" % (tmp_s)

        if self.deps:
            str_ += ",dependencies=[%s]" % ",".join(self.deps)
        return str_
