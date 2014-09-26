#!/bin/bash
set -e
profile=my_profile
csdir="/home/karel/.steam/steam/SteamApps/common/Counter-Strike Global Offensive/csgo/cfg/"
configs="config.cfg autoexec.cfg"
configdir=$(readlink -f $(dirname "$0"))
date=$(date +%Y%m%d)

show_usage() {
cat << EOF
Usage: ${0##*/} [-h] [-p PROFILE]
Back up your existing Counter Strike: Global Offensive configurations and link
in new ones.
    -h          display this help and exit
    -p PROFILE  try to setup the profile by name and exit
EOF
}

while :; do
    case $1 in
        -h|-\?|--help) # show a help message
            show_usage
            exit 0
            ;;
        -p|--profile) # a profile name has been specified!
            if [ "$2" ]; then
                profile=$2
                shift 2
                continue
            else
                show_usage
                exit 1
            fi
            ;;
        --profile=?*)
            profile=${1#*=} # delete everything up to '=' and assign remainder.
            shift
            ;;
        --profile=) # empty profile case
            show_usage
            exit 1
            ;;

        -c|--counter-strike-dir)
            if [ "$2" ]; then
                csdir=$2
                shift 2
                continue
            else
                show_usage
                exit 1
            fi
            ;;
        --counter-strike-dir=?*)
            csdir=${1#*=} # delete everything up to '=' and assign remainder.
            shift
            ;;
        --counter-strike-dir=) # empty profile case
            show_usage
            exit 1
            ;;

        --) # end of options
            shift
            break
            ;;
        -?*) # unknown option
            show_usage
            exit 1
            ;;
        *) # default
            break
    esac
done

cd "$csdir"
for f in $configs; do
    if [ -L "$f" ] && [ -d "$f" ]; then
        unlink "$f"
    elif [ -f $f ]; then
        mv "$f" "$f.$date.bk"
    fi
    ln -s "$configdir/profiles/$profile/$f" "$f"
done

exit 0
