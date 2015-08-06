#!/bin/bash
#===============================================================================
#
#          FILE: getip.sh
# 
#         USAGE: ./getip.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: James Zhu (000), zhujian0805@gmail.com
#  ORGANIZATION: JZ
#       CREATED: 2014年10月14日 12时55分04秒 CST
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error

site=$1

./get-free-ip.py ldapmaster.sample.net R4t5y6u7 cn${site}-wow > cn${site}-wow.txt &
./get-free-ip.py ldapmaster.sample.net R4t5y6u7 cn${site}-pub > cn${site}-pub.txt &
./get-free-ip.py ldapmaster.sample.net R4t5y6u7 cn${site}-vlan99 > cn${site}-vlan99.txt &
