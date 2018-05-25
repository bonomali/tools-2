#!/bin/bash

# __  __     __  __     ______   ______     ______     ______     ______     __     _____
# /\ \_\ \   /\ \_\ \   /\  == \ /\  ___\   /\  == \   /\  ___\   /\  == \   /\ \   /\  __-.
# \ \  __ \  \ \____ \  \ \  _-/ \ \  __\   \ \  __<   \ \ \__ \  \ \  __<   \ \ \  \ \ \/\ \
# \ \_\ \_\  \/\_____\  \ \_\    \ \_____\  \ \_\ \_\  \ \_____\  \ \_\ \_\  \ \_\  \ \____-
#  \/_/\/_/   \/_____/   \/_/     \/_____/   \/_/ /_/   \/_____/   \/_/ /_/   \/_/   \/____/

user=$1
token=$2
url=$3
folder=blueprints.$(date +%F_%R)


echo "Backing Up Blueprints Entitled to User " $1 ":"
echo
echo

mkdir $folder

while read id; do
name=$(curl -ks --user $user:$token https://execdemo5.skygrid.cloud/api/blueprints/$id | jq -r '.results.name')
type=$(curl -ks --user $user:$token https://execdemo5.skygrid.cloud/api/blueprints/$id | jq -r '.results.blueprintType')
echo $name
curl -ks --user $user:$token https://$url/api/blueprints/$id | jq '.results | { id, name, version, tags, description, shortDescription, externalLink, imageLink, yml, visibility, params, entitlementType, entitledUsers, entitledUserGroups }' > $folder/"HCP-$type-$name.$(date +%F_%R).txt"
done <blueprintList.txt

rm blueprintList.txt
