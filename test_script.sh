#!/bin/sh
echo "Example for webhook script"
echo "###################### PING ####################"
ping -c 5 google.com
echo "################### TEST ECHO ##################"
echo "test"
echo "###################### PWD #####################"
pwd
echo "#################### IFCONFIG ##################"
ifconfig
echo "################ SCRIPT ARGUMENTS ##############"
echo $@
echo "________________________________________________"
