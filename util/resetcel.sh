#!/bin/bash

declare CELDAPATH=$HOME/Dropbox/src/celda
declare CONFPATH=/etc/celda
declare LOGPATH=/var/log/celda

declare PYTHON=/usr/bin/python

echo "Limpiando las bitácoras..."
for f in $LOGPATH/*
do
	echo "Eliminando $f ..."
	rm $f
done
echo "[HECHO]"

echo "Reinstalando el proxy..."
$PYTHON $CELDAPATH/install -c $CONFPATH/celdad.conf -u $CELDAPATH/conf/users.conf -m $CELDAPATH/conf/casa.conf
echo "[HECHO]"

echo "Reinstalando los nodos internos..."
for (( k = 1; k < 6; k++ )); do
	echo "Reinstalando el espacio virtual $k..."
	echo "Usando archivo de configuración: $CONFPATH/celdad0$k.conf"
	mkdir -p
	$PYTHON $CELDAPATH/install -c $CONFPATH/celdad0$k.conf -m $CELDAPATH/conf/casa.conf
	echo "[HECHO]"
	echo "--------------------------------------------------------------------------------"
done
echo "[HECHO]"

