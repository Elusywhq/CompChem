#!/bin/bash

if [[ $(hostname) == *"vanda"* ]]; then
    git -C /atlas/home/$USER/bin/ORCA pull
    git -C /atlas/home/$USER/bin/Elusy_Personal pull
else
    git -C ~/bin/ORCA pull
    git -C ~/bin/Elusy_Personal pull
fi
exit 0