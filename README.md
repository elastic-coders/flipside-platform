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

When target is aws:
- the newly created key is stored under `.secrets` dir
- the master configuration is stored in `.flipside-platform.yaml`


### Provision

Installs salt and ancillary packages in the master machine

    flipside-provision --target=[aws|vagrant] --salt-version --no-standalone

Salt version defaults to `stable`

Standalone mode can be set using the `--standalone` option


### Configure

XXX TODO

Push salt states and pillars into the master

    flipside-configure --target=[aws|vagrant]


### Deploy

XXX TODO

Deploy an application

    flipside-deploy --target=[aws|vagrant]


### SSH access

    flipside-ssh --target=[aws|vagrant]
