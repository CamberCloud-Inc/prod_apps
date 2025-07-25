#!/bin/bash
# Check if breakVelocity argument is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <breakVelocity>"
    echo "Example: $0 0.0005"
    exit 1
fi

# Get breakVelocity from command line argument
BREAK_VELOCITY=$1

sed -i "s/\${breakVelocity}/$BREAK_VELOCITY/g" unbreakable.lmp && \
lmp -in unbreakable.lmp



    // {
    //   "type": "Select",
    //   "label": "Breakup Velocity",
    //   "name": "breakVelocity",
    //   "description": "Sets the velocity of the front and back faces of the nanotube, aiming to tear it apart",
    //   "defaultValue": "None",
    //   "hidden": false,
    //   "required": true,
    //   "disabled": false,
    //   "options": [
    //     {
    //       "label": "None",
    //       "value": "0"
    //     },
    //     {
    //       "label": "Weak",
    //       "value": "0.0005"
    //     },
    //     {
    //       "label": "Strong",
    //       "value": "0.001"
    //     }
    //   ]
    // }