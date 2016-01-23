# -*- coding: utf-8 -*-

import os
import sys
import copy
from odict import OrderedDict

sys.path.append(os.path.abspath(".."))
import Config

try:
    import xml.etree.cElementTree as ET
except:
    import cElementTree as ET


class AppsXML:
    """
    Parser for apps.xml
    """

    def __init__(self):
        self._tree = ET.parse(os.path.join(
            Config.get("config"), Config.get("apps_xml")))
        self.root = self._tree.getroot()
        self.changed_region = None
        if self.root.tag != "apps":
            raise InvalidRoot(self.root.tag)

    def _get_app_info(self, app):
        info = OrderedDict()

        info["name"] = app.get("name")
        if app.get("path"):
            info["path"] = app.get("path")
        if app.get("buildtype"):
            info["buildtype"] = app.get("buildtype")

        for node in app:
            info[node.tag] = OrderedDict()
            for node_ in node:
                if node.tag == "fs":
                    info[node.tag][node_.get("type")] = node_.get("path")
                else:
                    info[node.tag][node_.get("name")] = node_.get("value")
        # XXX: return copy.deepcopy(info)
        return info

    def _set_region(self, specified_region):
        # Point to the correct region
        found = False

        if self.changed_region != specified_region:
            # reset to the top of the tree
            self.root = self._tree.getroot()
            for region in self.root:
                if region.get("name") == specified_region:
                    self.root = region
                    self.changed_region = specified_region
                    return True

            # revert the changes because we didn't find the region
            # that was passed to us
            for region in self.root:
                if region.get("name") == self.changed_region:
                    self.root = region
                    return True

        # in case we are calling this but 
        # we already set the region (the same region)
        if self.changed_region is not None:
            found = True

        return found

    def get_apps(self, specified_region, names=[]):
        apps_lst = []

        found_region = self._set_region(specified_region)

        if not found_region:
            return apps_lst

        for app in self.root:
            if names:
                for name in names:
                    if app.get("name") == name:
                        d = self._get_app_info(app)
                        d['region'] = specified_region
                        apps_lst.append(d)
            else:
                d = self._get_app_info(app)
                d['region'] = specified_region
                apps_lst.append(d)

        return apps_lst

    def get_app(self, specified_region, name):
        found_region = self._set_region(specified_region)
        if not found_region:
            return apps_lst

        for app in self.root:
            if app.get("name") == name:
                return self._get_app_info(app)
        return None

    def pprint(self):
        return ET.tostring(self.root)


class BuildXML:
    """
    Parser for build.xml
    """

    def __init__(self):
        self._tree = ET.parse(os.path.join(
            Config.get("config"), Config.get("build_xml")))
        self.root = self._tree.getroot()
        self.changed_region = None

        if self.root.tag != "builds":
            raise InvalidRoot(self.root.tag)

        #self.builds = self.tree["nodes"]

    def _get_build_info(self, build):
        flags_strs = {"target": build.get("target")}

        for flag in build[0]:
            flags_strs[flag.get("name")] = flag.get("value")

        return copy.deepcopy(flags_strs)

    def _set_region(self, specified_region):
        # Point to the correct region
        found = False

        if self.changed_region != specified_region:
            # reset to the top of the tree
            self.root = self._tree.getroot()
            for region in self.root:
                if region.get("name") == specified_region:
                    self.root = region
                    self.changed_region = specified_region
                    return True

            # revert the changes because we didn't find the region
            # that was passed to us
            for region in self.root:
                if region.get("name") == self.changed_region:
                    self.root = region
                    return True

        # in case we are calling this but 
        # we already set the region (the same region)
        if self.changed_region is not None:
            found = True

        return found

    def get_build_info(self, type, specified_region):
        found_region = self._set_region(specified_region)

        if not found_region:
            return None

        for build in self.root:
            if build.get("type") == type:
                return self._get_build_info(build)
        return None

    def pprint(self):
        return ET.tostring(self.root)
