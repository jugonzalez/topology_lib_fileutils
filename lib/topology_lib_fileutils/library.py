# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
topology_lib_fileutils communication library implementation.
"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division
import re
import pexpect
import requests

def _get_filename(file_path):
    """
    Get file name from a given path

    :param file_path: path of a given file.
    :type file_path: string.
    """
    pattern_name = re.compile('(((?<=/)|^)[^/]+$)')
    file_name = pattern_name.findall(file_path)[0][0]
    return file_name

def _get_content_file(file_path):
    """
    Get file from the given location and return its content.

    :param str file_path: Local or remote location of a given file.
    All file location which do not use 'http[s]' in its path,
    will be handled as local location.
    """
    remote_path = re.compile('http[s]?://')
    if remote_path.match(file_path):
        command = 'wget {}'.format(file_path)
        file_content = requests.get(file_path).text
    else:
        file_content = open(file_path).read()
    file_content = file_content.replace('"',"'")
    return file_content

def load_file(enode, src_file_path, dst_file_path=None, shell=None):
    """
    Load a given file to the remote host(enode)
    
    :param enode: Engine node to communicate with.
    :type enode: topology.platforms.base.BaseNode
    :param str src_file_path: Local or remote location of a given file.
     Remote location is allowed only with http[s] protocol.
    :param str src_file_path: path at the remote host to save file.
    """
    file_content = _get_content_file(src_file_path)
    file_name = _get_filename(src_file_path)

    if dst_file_path is None:
        dst_file_path = '/tmp'

    command = 'echo "{}" >> {}/{}'.format(file_content, dst_file_path, file_name)
    response = enode(command)
    return response

__all__ = [
    'load_file'
]
