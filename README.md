# Flipside platform automation


## Installation

1. install python
2. install flipside-platform


## Init

See all available templates

    flipside-template list

Configures the flipside app

    flipside-init <app_name> <template_name>


## Build

To build locally:

    flipside-build

## Bootstrap

To bootstrap a machine:

    flipside-bootstrap --target=[aws|vagrant] --keyname=<keyname>

    **keyname = pem file name, will be stored into .secret/ folder under project root**

With aws target this command bootstrap an aws machine, creating a configuration file in the project root folder ".flipside-config.json" containing some info on aws bootstrapped machine
