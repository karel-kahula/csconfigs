#!/usr/bin/python
# setup.py
# Date: September 25, 2014
# Author: Karel Kahula, kkahula@gmail.com
#
# Updates your CSGO configuration to a new one. ez pz lemon squeezy
#

import os
import time
import shutil
from optparse import OptionParser
from os.path import expanduser

default_profile = "my_profile"
cs_dir = os.path.join(expanduser("~"),".steam/steam/SteamApps/common/Counter-Strike Global Offensive/csgo/cfg/")
configs = ["config.cfg", "autoexec.cfg", "userconfig.cfg"]
today = time.strftime("%Y%m%d")
configs_dir= os.path.dirname(os.path.realpath(__file__))


def list_profiles():
    profiles = [x[1] for x in os.walk(os.path.join(configs_dir,'profiles'))][0]
    if len(profiles) < 1:
        print "There do not appear to be any profiles available."
        exit(1)
    for p in sorted(profiles,key=str.lower):
        print p


def switch_profile(options):
    profile_dir = os.path.join(configs_dir, 'profiles', options.profile)
    if not os.path.exists(profile_dir):
        print "The profile, '%s', does not appear to exist. Aborting." % \
            options.profile
        exit(1)
    if not os.path.exists(options.csgo_dir):
        print 'The CSGO directory does not appear to exist. Aborting.'
        exit(1)

    for cfg in configs:
        cfg_source = os.path.join(profile_dir, cfg)
        cfg_dest = os.path.join(options.csgo_dir,cfg)
        if os.path.exists(cfg_dest) and os.path.islink(cfg_dest):
            os.unlink(cfg_dest)
        elif os.path.exists(cfg_dest):
            shutil.move(cfg_dest, os.path.join(options.csg_dir,
                "%s.%s.bk" % (cfg,today)))
        if os.path.exists(cfg_source):
            # finally create link here
            os.symlink(cfg_source, cfg_dest)


def main():
    op = OptionParser()
    op.add_option("-p","--profile",dest="profile",
        help="The configuration profile to use", metavar="PROFILE",
        default=default_profile)
    op.add_option("-c","--csgo-config-dir", dest="csgo_dir",
        help="The CS:GO cfg directory", metavar="DIR",default=cs_dir)
    #op.add_option("-i","--import",action="store_true",dest="do_import",
        #default=False, help="Copy exiting configurations to `my_profile` before creating symlinks")
    op.add_option("-l","--list",action="store_true",dest="list_profiles",
        default=False, help="List all currently available configuration profiles and exit")

    options, args = op.parse_args()
    if options.list_profiles:
        list_profiles()
    else:
        switch_profile(options)
    exit(0)

if __name__ == '__main__':
    main()
