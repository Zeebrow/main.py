# Copyright (C) 2022 zeebrow

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


class APP_CONST:
    DEFAULT_APP_NAME = 'quickhost'
    DEFAULT_OPEN_PORTS = ['22']
    DEFAULT_VPC_CIDR = '172.16.0.0/16'
    DEFAULT_SUBNET_CIDR = '172.16.0.0/24'


class QHExit:
    OK = 0
    GENERAL_FAILURE = 1
    ABORTED = 2
    KNOWN_ISSUE = 3
    # 2x - security-related
    NOT_QH_USER = 21
    FAIL_AUTH = 22
