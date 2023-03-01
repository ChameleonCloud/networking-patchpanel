# networking-patchpanel


Example configuration file:

```
# neutron/ml2_conf.ini
[DEFAULT]

[ml2]
# ... other options merged from upstream config file

# important! These drivers will attempt to bind ports, IN ORDER, with the first one to successfully bind "winning"
mechanism_drivers = patchpanel,genericswitch,baremetal,openvswitch

[genericswitch:<tor_switch_name>]
# ngs options

[genericswitch:<patchpanel_switch_name>]
# ngs options

[patchpanel]
patchpanel_switch = <patchpanel_switch_name>
pseudowire_vlan_range = "2000:3000"
```
