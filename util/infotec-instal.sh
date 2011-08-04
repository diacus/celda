#!/bin/bash
#===============================================================================
#
#          FILE:  infotec-instal.sh
# 
#         USAGE:  ./infotec-instal.sh 
# 
#   DESCRIPTION:  
# 
#       OPTIONS:  ---
#  REQUIREMENTS:  ---
#          BUGS:  ---
#         NOTES:  ---
#        AUTHOR:  Diego Rodrigo Guzmán Santamaría (diacus), dr.guzsant@gmail.com
#       COMPANY:  UAM-Iztapalapa, PCyTI :: México D.F.
#       VERSION:  1.0
#       CREATED:  15/07/11 14:41:14 CDT
#      REVISION:  ---
#===============================================================================

declare MACHINES="142 143 144 145"
declare LOCALMAC="146"
declare RED="192.168.3"
declare SRCPATH=$HOME/Dropbox/src/celda
declare CONFPATH=$SRCPATH/conf
declare SHELL=/usr/bin/ssh
declare RSYNC=/usr/bin/rsync

echo Instalando la maquina local...
#$PYTHON $SRCPATH/install -c /etc/celda/celdad.conf -u $SRCPATH/conf/users.conf -m $SRCPATH/conf/infotec.conf

for m in $MACHINES
do
	echo Actualizando el nodo $RED.$m
	$RSYNC -av $SRCPATH `whoami`@$RED.$m:
	$SHELL `whoami`@$RED.$m $PYTHON celda/install -u celda/conf/users.conf -m celda/conf/infotec.conf -c /etc/celda/celdad.conf
done



