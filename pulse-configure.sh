#!/bin/bash

# Define read-only constants
typeset -r HOSTGROUP_NAME="WiiMote"
typeset -r HOSTGROUP_SOURCES="accelerometer-x,accelerometer-y,accelerometer-z,button-a,button-b,button-up,button-down,button-right,button-left,button-1,button-2,button-plus,button-minus,button-home,position,battery"

#
# Helper function to test for a command
#
function CommandExists()
{
  type "$1" > /dev/null 2>&1
  if [ $? == 1 ]
  then
    echo "$1 command does exist"
    exit 1
  fi
}

Main()
{
  CommandExists jq
  CommandExists "hostgroup-search"
  CommandExists "hostgroup-create"
  CommandExists "hostgroup-update"

  # Look for an existing hostgroup
  hostgroup=$(hostgroup-search -n "$HOSTGROUP_NAME")

  # Determine if the hostgroup already exists
  hostgroup_exists=$(echo $hostgroup | jq '.result | length')

  # If the host group does not exist create the hostgroup , otherwise update the hostgroup
  if [ "$hostgroup_exists" == 0 ]
  then
    # Create the hostgroup
    hostgroup-create -n "$HOSTGROUP_NAME" -s "$HOSTGROUP_SOURCES" | jq .
  else
    # extract the hostgroup id so we can update 
    hostgroup_id=$(echo $hostgroup | jq '.result[0].id')
    # Update the hostgroup
    hostgroup-update -i "$hostgroup_id" -n "$HOSTGROUP_NAME" -s "$HOSTGROUP_SOURCES" | jq .
  fi
}

Main 
