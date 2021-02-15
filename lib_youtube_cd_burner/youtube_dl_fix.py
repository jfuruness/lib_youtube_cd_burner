#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains class Youtube_dl_fix

This class inherits from yotube dl and fixes a method that causes
everything to crash if ffmpeg cannot convert a song, instead of just
skipping it. I wrote this a while ago before I knew to write good docs
and before I knew properly about inheritance, so idk where the change
is, but it's in there. You could probably diff these funcs with youtube
dl's to find it but idc

Design Choices:
-Youtube dl uses ffmpeg to convert files, but this breaks on webm songs
    -Encountered these when downloading russian songs
    -Instead of breaking, we skip that song
Possible Future Improvements:
    -Figure out the changes I made and document them
    -Now that I know inheritance, go back and take out unnessecary funcs
"""

import itertools
import os
import json
import random
import youtube_dl
from youtube_dl.utils import encodeFilename, PostProcessingError, orderedSet

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__Lisence__ = "MIT"
__Version__ = "0.1.0"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"
__status__ = "Production"


class Youtube_dl_fix(youtube_dl.YoutubeDL):

    def __init__(self, *args, **kwargs):
        youtube_dl.YoutubeDL.__init__(self, *args, **kwargs)

    def post_process(self, filename, ie_info):
        """Run all the postprocessors on the given file."""

        try:
            info = dict(ie_info)
            info['filepath'] = filename
            pps_chain = []
            if ie_info.get('__postprocessors') is not None:
                pps_chain.extend(ie_info['__postprocessors'])
            pps_chain.extend(self._pps)
            for pp in pps_chain:
                files_to_delete = []
                try:
                    files_to_delete, info = pp.run(info)
                except PostProcessingError as e:
                    self.report_error(e.msg)
                if files_to_delete and not self.params.get('keepvideo', False):
                    for old_filename in files_to_delete:
                        self.to_screen(
                            'Deleting original file %s (pass -k to keep)'
                            % old_filename)
                        try:
                            os.remove(encodeFilename(old_filename))
                        except (IOError, OSError):
                            self.report_warning(
                                'Unable to remove downloaded original file')
        except BaseException:
            print("Problem postprocessing")

    def process_ie_result(self, ie_result, download=True, extra_info={}):
        """
        Take the result of the ie(may be modified) and resolve all unresolved
        references (URLs, playlist items).
        It will also download the videos if 'download'.
        Returns the resolved ie_result.
        """
        result_type = ie_result.get('_type', 'video')

        if result_type in ('url', 'url_transparent'):
            ie_result['url'] = youtube_dl.utils.sanitize_url(ie_result['url'])
            extract_flat = self.params.get('extract_flat', False)
            if ((extract_flat == 'in_playlist' and 'playlist' in extra_info) or
                    extract_flat is True):
                if self.params.get('forcejson', False):
                    self.to_stdout(json.dumps(ie_result))
                return ie_result

        if result_type == 'video':
            self.add_extra_info(ie_result, extra_info)
            return self.process_video_result(ie_result, download=download)
        elif result_type == 'url':
            # We have to add extra_info to the results because it may be
            # contained in a playlist
            return self.extract_info(ie_result['url'],
                                     download,
                                     ie_key=ie_result.get('ie_key'),
                                     extra_info=extra_info)
        elif result_type == 'url_transparent':
            # Use the information from the embedding page
            info = self.extract_info(
                ie_result['url'], ie_key=ie_result.get('ie_key'),
                extra_info=extra_info, download=False, process=False)

            # extract_info may return None when ignoreerrors is enabled and
            # extraction failed with an error, don't crash and return early
            # in this case
            if not info:
                return info

            force_properties = dict(
                (k, v) for k, v in ie_result.items() if v is not None)
            for f in ('_type', 'url', 'id', 'extractor',
                      'extractor_key', 'ie_key'):
                if f in force_properties:
                    del force_properties[f]
            new_result = info.copy()
            new_result.update(force_properties)

            # Extracted info may not be a video result (i.e.
            # info.get('_type', 'video') != video) but rather an url or
            # url_transparent. In such cases outer metadata (from ie_result)
            # should be propagated to inner one (info). For this to happen
            # _type of info should be overridden with url_transparent. This
            # fixes issue from https://github.com/rg3/youtube-dl/pull/11163.
            if new_result.get('_type') == 'url':
                new_result['_type'] = 'url_transparent'

            return self.process_ie_result(
                new_result, download=download, extra_info=extra_info)
        elif result_type in ('playlist', 'multi_video'):
            # We process each entry in the playlist
            playlist = ie_result.get('title') or ie_result.get('id')
            self.to_screen('[download] Downloading playlist: %s' % playlist)

            playlist_results = []

            playliststart = self.params.get('playliststart', 1) - 1
            playlistend = self.params.get('playlistend')
            # For backwards compatibility, interpret -1 as whole list
            if playlistend == -1:
                playlistend = None

            playlistitems_str = self.params.get('playlist_items')
            playlistitems = None
            if playlistitems_str is not None:
                def iter_playlistitems(format):
                    for string_segment in format.split(','):
                        if '-' in string_segment:
                            start, end = string_segment.split('-')
                            for item in range(int(start), int(end) + 1):
                                yield int(item)
                        else:
                            yield int(string_segment)
                playlistitems = orderedSet(iter_playlistitems(
                    playlistitems_str))

            ie_entries = ie_result['entries']

            def make_playlistitems_entries(list_ie_entries):
                num_entries = len(list_ie_entries)
                return [
                    list_ie_entries[i - 1] for i in playlistitems
                    if -num_entries <= i - 1 < num_entries]

            def report_download(num_entries):
                self.to_screen(
                    '[%s] playlist %s: Downloading %d videos' %
                    (ie_result['extractor'], playlist, num_entries))

            if isinstance(ie_entries, list):
                n_all_entries = len(ie_entries)
                if playlistitems:
                    entries = make_playlistitems_entries(ie_entries)
                else:
                    entries = ie_entries[playliststart:playlistend]
                n_entries = len(entries)
                _str_1 = '[%s] playlist %s: Collected %d '
                _str_1 += 'video ids (downloading %d of them)'
                self.to_screen(_str_1 %
                               (ie_result['extractor'],
                                playlist,
                                n_all_entries,
                                n_entries))
            elif isinstance(ie_entries, youtube_dl.utils.PagedList):
                if playlistitems:
                    entries = []
                    for item in playlistitems:
                        entries.extend(ie_entries.getslice(
                            item - 1, item
                        ))
                else:
                    entries = ie_entries.getslice(
                        playliststart, playlistend)
                n_entries = len(entries)
                report_download(n_entries)
            else:  # iterable
                if playlistitems:
                    entries = make_playlistitems_entries(list(itertools.islice(
                        ie_entries, 0, max(playlistitems))))
                else:
                    entries = list(itertools.islice(
                        ie_entries, playliststart, playlistend))
                n_entries = len(entries)
                report_download(n_entries)

            if self.params.get('playlistreverse', False):
                entries = entries[::-1]

            if self.params.get('playlistrandom', False):
                random.shuffle(entries)

            x_forwarded_for = ie_result.get('__x_forwarded_for_ip')

            for i, entry in enumerate(entries, 1):
                self.to_screen(
                    '[download] Downloading video %s of %s' % (i, n_entries))
                # This __x_forwarded_for_ip thing is a bit ugly but requires
                # minimal changes
                if x_forwarded_for:
                    entry['__x_forwarded_for_ip'] = x_forwarded_for
                extra = {
                    'n_entries': n_entries,
                    'playlist': playlist,
                    'playlist_id': ie_result.get('id'),
                    'playlist_title': ie_result.get('title'),
                    'playlist_uploader': ie_result.get('uploader'),
                    'playlist_uploader_id': ie_result.get('uploader_id'),
                    'playlist_index': i + playliststart,
                    'extractor': ie_result['extractor'],
                    'webpage_url': ie_result['webpage_url'],
                    'webpage_url_basename': youtube_dl.utils.url_basename(
                        ie_result['webpage_url']),
                    'extractor_key': ie_result['extractor_key'],
                }

                reason = self._match_entry(entry, incomplete=True)
                if reason is not None:
                    self.to_screen('[download] ' + reason)
                    continue

                try:

                    entry_result = self.process_ie_result(entry,
                                                          download=download,
                                                          extra_info=extra)
                    playlist_results.append(entry_result)
                except BaseException as e:
                    print("Problem occured downloading a file: {}".format(e))
                    continue
            ie_result['entries'] = playlist_results
            self.to_screen('[download] Finished downloading playlist: %s'
                           % playlist)
            return ie_result
        elif result_type == 'compat_list':
            self.report_warning(
                'Extractor %s returned a compat_list result. '
                'It needs to be updated.' % ie_result.get('extractor'))

            def _fixup(r):
                self.add_extra_info(
                    r,
                    {
                        'extractor': ie_result['extractor'],
                        'webpage_url': ie_result['webpage_url'],
                        'webpage_url_basename': youtube_dl.utils.url_basename(
                            ie_result['webpage_url']),
                        'extractor_key': ie_result['extractor_key'],
                    }
                )
                return r
            ie_result['entries'] = [
                self.process_ie_result(_fixup(r), download, extra_info)
                for r in ie_result['entries']
            ]
            return ie_result
        else:
            raise Exception('Invalid result type: %s' % result_type)
