# Persistent local customizations
include default.local
# Persistent global definitions
include globals.local

include disable-common.inc
include disable-devel.inc
# include disable-exec.inc
include disable-passwdmgr.inc
include disable-programs.inc
# include disable-xdg.inc

caps.drop all
# Spoof id number in /etc/machine-id file - a new random id is generated inside the sandbox.
machine-id
# TODO: custom netfilter (here a default one is loaded)
netfilter
nonewprivs
noroot
protocol unix,inet,inet6
seccomp

disable-mnt
private-cache
private-dev
