# Flipside platform automation


## Installation

1. install python
2. install flipside-platform



## Synopsis of all commands

### Template

See all available templates

    flipside-template list


### Init

Initializes the flipside app

    flipside-init <app_name> <template_name>

Writes config into `.flipside`


### Build

To build locally:

    flipside-build


### Publish

Uploads the app into the master:

    flipside-publish --target=[aws|vagrant]


### Bootstrap

To bootstrap a master machine:

    flipside-bootstrap --target=[aws|vagrant] --keyname=<keyname>

    **keyname = pem file name, will be stored into .secret/ folder under project root**

With aws target this command bootstrap an aws machine, creating a configuration file in the project root folder ".flipside-config.json" containing some info on aws bootstrapped machine


### Provision

XXX TODO

Installs salt and ancillary packages in the master machine

    flipside-provision --target=[aws|vagrant] --salt-version --standalone


### Configure

Push salt states and pillars into the master

    flipside-configure --target=[aws|vagrant]


### Deploy

Deploy an application

    flipside-deploy --target=[aws|vagrant]


### SSH access

    flipside-ssh --target=[aws|vagrant]
