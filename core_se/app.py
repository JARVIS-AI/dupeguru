# Created On: 2011/09/20
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from hscommon.trans import trget
from hscommon.util import format_size

from core.app import (DupeGuru as DupeGuruBase, Column, format_timestamp, format_perc,
    format_words, format_dupe_count, cmp_value)
from core import prioritize
from . import __appname__

coltr = trget('columns')

class DupeGuru(DupeGuruBase):
    NAME = __appname__
    COLUMNS = [
        Column('name', coltr("Filename")),
        Column('folder_path', coltr("Folder")),
        Column('size', coltr("Size (KB)")),
        Column('extension', coltr("Kind")),
        Column('mtime', coltr("Modification")),
        Column('percentage', coltr("Match %")),
        Column('words', coltr("Words Used")),
        Column('dupe_count', coltr("Dupe Count")),
    ]
    DELTA_COLUMNS = {2, 4}
    METADATA_TO_READ = ['size', 'mtime']
    MATCHPERC_COL = 5
    DUPECOUNT_COL = 7
    
    def __init__(self, view, appdata):
        DupeGuruBase.__init__(self, view, appdata)
    
    def _get_display_info(self, dupe, group, delta):
        size = dupe.size
        mtime = dupe.mtime
        m = group.get_match_of(dupe)
        if m:
            percentage = m.percentage
            dupe_count = 0
            if delta:
                r = group.ref
                size -= r.size
                mtime -= r.mtime
        else:
            percentage = group.percentage
            dupe_count = len(group.dupes)
        return [
            dupe.name,
            str(dupe.folder_path),
            format_size(size, 0, 1, False),
            dupe.extension,
            format_timestamp(mtime, delta and m),
            format_perc(percentage),
            format_words(dupe.words) if hasattr(dupe, 'words') else '',
            format_dupe_count(dupe_count)
        ]
    
    def _get_dupe_sort_key(self, dupe, get_group, key, delta):
        if key == self.MATCHPERC_COL:
            m = get_group().get_match_of(dupe)
            return m.percentage
        if key == self.DUPECOUNT_COL:
            return 0
        r = cmp_value(dupe, self.COLUMNS[key])
        if delta and (key in self.DELTA_COLUMNS):
            r -= cmp_value(get_group().ref, self.COLUMNS[key])
        return r
    
    def _get_group_sort_key(self, group, key):
        if key == self.MATCHPERC_COL:
            return group.percentage
        if key == self.DUPECOUNT_COL:
            return len(group)
        return cmp_value(group.ref, self.COLUMNS[key])
    
    def _prioritization_categories(self):
        return prioritize.all_categories()
    