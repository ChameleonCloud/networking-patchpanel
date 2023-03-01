import networking_generic_switch.generic_switch_mech as generic_switch
import oslo_log.log as logging
from oslo_config import cfg
from neutron_lib.api.definitions import portbindings

CONF = cfg.CONF
LOG = logging.getLogger(__name__)


DEVICE_OWNER_PREFIX = "patchpanel:"
DEVICE_OWNER_KEY = "device_owner"

class PatchPanelDriver(generic_switch.GenericSwitchDriver):

    def initialize(self):
        return super().initialize()

    def create_network_postcommit(self, context):

        # ngs ensures vlan is present on all switches within the same physnet
        # do we need different behavior for patchpanel?
        return super().create_network_postcommit(context)

    def delete_network_postcommit(self, context):

        # ngs deletes vlans from all switches in same physnet
        return super().delete_network_postcommit(context)

    def update_port_postcommit(self, context):

        # ngs checks local_link_information to map neutron port to physical switchport
        # we could modify/extend this behavior for the shadow ports?
        return super().update_port_postcommit(context)

    def delete_port_postcommit(self, context):

        # ngs unplugs port from switch on delete
        return super().delete_port_postcommit(context)

    def bind_port(self, context):

        port = context.current
        network = context.network.current
        binding_profile = port['binding:profile']
        local_link_information = binding_profile.get('local_link_information')

        # if port is not of type baremetal, we can't do anything
        vnic_type = port[portbindings.VNIC_TYPE]
        if not vnic_type == portbindings.VNIC_BAREMETAL:
            return False

        # if port isn't owned by us, don't do anything. Next plugin in order will attempt
        port_owner = port.get(DEVICE_OWNER_KEY, "")
        if not port_owner.startswith(DEVICE_OWNER_PREFIX):
            return False

        #TODO implement PP port binding behavior

        return super().bind_port(context)
