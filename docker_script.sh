#!/bin/sh
# script params:
# -a: action - push|merge
# -p: gitlab project
# -b: branch name

# parse aruments
while getopts a:p:b: option
do
case "${option}"
in
a) action=${OPTARG};;
p) project=${OPTARG};;
b) branch=$OPTARG;;
esac
done

ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no $GITLABWEBHOOK_USERNAME@$GITLABWEBHOOK_HOSTNAME "$GITLABWEBHOOK_SCRIPTPATH -a $action -p $project -b $branch"
