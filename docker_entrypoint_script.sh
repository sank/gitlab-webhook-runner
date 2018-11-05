#!/bin/bash
if ! [ -z "$GITLABWEBHOOK_HOSTNAME" ]; then
    echo This docker service connects to your server via ssh and runs the script on that server.

    echo Enter host, user and password for access to script on your server by ssh.
    read -p "Enter hostname: " hostname
    read -p "Enter username: " username
    read -sp "Enter password: " password

    export GITLABWEBHOOK_HOSTNAME=$hostname
    export GITLABWEBHOOK_USERNAME=$username

    # Generate public key for access to server by key
    ssh-keygen -f /root/.ssh/id_rsa -P "" -C "docker@container.$HOSTNAME" > /dev/null
    if [ $? -ne 0 ]; then
        echo ERROR! Failed to run: ssh-keygen -f /root/.ssh/id_rsa -P -C docker@container.$HOSTNAME > /dev/null
        exit $?
    fi

    # Copy public key to server
    echo
    echo Now the public key will be copied to $username@$hostname.
    echo --------
    sshpass -p $password ssh-copy-id -i /root/.ssh/id_rsa.pub -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no $username@$hostname
    echo --------
    if [ $? -eq 0 ]; then
        echo Copy completed successfully. Check output above.
    else
        echo ERROR! Failed to run: sshpass -p $password ssh-copy-id -i /root/.ssh/id_rsa.pub -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no $username@$hostname
        exit $?
    fi

    echo
    echo Service is ready for start!
    echo Run command: $ docker start $HOSTNAME
fi
