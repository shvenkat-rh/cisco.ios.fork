#!/usr/bin/python
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
"""
The module file for ios_vlans
"""
from __future__ import absolute_import, division, print_function


__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.vlans.vlans import (
    VlansArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.vlans.vlans import Vlans
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.ios import get_connection


def _is_l2_device(module):
    """fails module if device is L3."""
    connection = get_connection(module)
    check_os_type = connection.get_device_info()
    if check_os_type.get("network_os_type") == "L3":
        return False
    return True


def main():

    module = AnsibleModule(
        argument_spec=VlansArgs.argument_spec,
        mutually_exclusive=[["config", "running_config"]],
        required_if=[
            ["state", "merged", ["config"]],
            ["state", "replaced", ["config"]],
            ["state", "overridden", ["config"]],
            ["state", "rendered", ["config"]],
            ["state", "purged", ["config"]],
            ["state", "parsed", ["running_config"]],
        ],
        supports_check_mode=True,
    )

    if _is_l2_device(module) or module.params.get("state") in ["rendered", "parsed"]:
        result = Vlans(module).execute_module()
        module.exit_json(**result)
    else:
        module.fail_json("""Resource VLAN is not valid for the target device.""")


if __name__ == "__main__":
    main()
