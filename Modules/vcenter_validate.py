from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl

def find_portgroup_by_vlan(si, vlan_id):
    """
    Function to find a portgroup in vCenter that matches the specified VLAN ID and return its name and VLAN ID.
    """
    content = si.RetrieveContent()
    for datacenter in content.rootFolder.childEntity:
        if hasattr(datacenter, 'networkFolder'):
            networks = datacenter.networkFolder.childEntity
            for network in networks:
                if isinstance(network, vim.dvs.DistributedVirtualPortgroup):
                    if hasattr(network.config.defaultPortConfig, 'vlan'):
                        vlan_config = network.config.defaultPortConfig.vlan
                        if isinstance(vlan_config, vim.dvs.VmwareDistributedVirtualSwitch.VlanIdSpec) and vlan_config.vlanId == vlan_id:
                            return network.name, vlan_config.vlanId
    return None, None
