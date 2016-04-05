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

    :param file_path: Local or remote location of a given file.
    :type file_path: string.

    Access to a remote location is allowed only with http[s] protocol.
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
    return file_content

def load_file(enode, file_path):
    """
    Load a given file to the remote host(enode)
    
    :param enode: Engine node to communicate with.
    :type enode: topology.platforms.base.BaseNode
    :param str file_path: Local or remote location of a given file.
     Remote location is allowed only with http[s] protocol.
    """
    file_content = _get_content_file(file_path)
    file_name = _get_filename(file_path)
    command = 'echo "{}" >> {}'.format(file_content, file_name)
    response = enode(command)
    return response

__all__ = [
    'load_file'
]
