# -*- coding: utf-8 -*-

PLUGIN_NAME = "Artists-Title Separator"
PLUGIN_AUTHOR = "divyinfo"
PLUGIN_DESCRIPTION = '''If the title tag of the file matches "Artists-Title", split them into %ARTISTS% and %TITLE%, and put them in corresponding tags. Implemented for right-click menu.'''
PLUGIN_VERSION = "0.1"
PLUGIN_API_VERSIONS = ["1.0"]


from picard.log import info, warning, error

from picard.metadata import register_track_metadata_processor

from picard.file import File
from picard.cluster import Cluster, ClusterList

from picard.track import Track
from picard.album import Album

from picard.ui.itemviews import BaseAction, register_album_action, register_cluster_action, register_clusterlist_action, register_track_action, register_file_action

import re, os

def prep_file(file):
    if (isinstance(file, File)):

        p = re.compile(ur'^\s*(' + file.metadata['artist'].strip() + ur')\s*-\s*(.*)$', re.UNICODE)
        m = p.search(file.metadata['title'].strip())

        if m:
            # info(str(m.groups().__len__()) + ': ' + (', '.join(m.group(i) for i in range(0, m.groups().__len__()))))

            file.metadata['artist'] = m.group(1).strip()
            file.metadata['title'] = m.group(2).strip()

            file.set_pending()

class PrepArtistsAction(BaseAction):
    NAME = 'Split artists and title'

    def callback(self, objs):
        for obj in objs:
            if (isinstance(obj, File)):
                prep_file(obj)
            elif (isinstance(obj, Cluster) or \
                isinstance(obj, ClusterList) or \
                isinstance(obj, Track) or \
                isinstance(obj, Album)):
                for f in obj.iterfiles():
                    prep_file(f)

register_file_action(PrepArtistsAction())
register_cluster_action(PrepArtistsAction())
register_clusterlist_action(PrepArtistsAction())

register_track_action(PrepArtistsAction())
register_album_action(PrepArtistsAction())