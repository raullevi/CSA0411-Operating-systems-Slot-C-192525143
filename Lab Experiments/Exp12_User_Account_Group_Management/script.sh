#!/bin/bash 
GROUP=oslab 
USER=student2 
  
groupadd $GROUP && echo "Group $GROUP created" 
useradd -m $USER && echo "User $USER created" 
usermod -aG $GROUP $USER && echo "User $USER added to group $GROUP" 
  
echo "User details:" 
id $USER 
grep "^$GROUP:" /etc/group 
  
usermod -L $USER && echo "Account $USER locked" 
passwd -S $USER 
  
userdel -r $USER 2>/dev/null && echo "User $USER deleted" 
groupdel $GROUP && echo "Group $GROUP deleted" 
id $USER 2>&1
