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

To bootstrap a machine (later you can provision salt on it):

    flipside-bootstrap --target=[aws|vagrant] --keyname=<keyname>

When target is aws:

- the newly created key is stored under `.secrets` dir
- the master configuration is stored in `.flipside-platform.yaml`


### Provision

Installs salt and ancillary packages in the master machine

    flipside-provision --target=[aws|vagrant]

Salt version defaults to `stable latest`

Standalone (masterless) mode can be set using the `--standalone` option


### Configure

Push salt states and pillars into the master

    flipside-configure --target=[aws|vagrant]

**KNOWN ISSUES**:

The following salt config files are global and shared between all apps:
- `.flipside/salt/config.yaml`
- `.flipside/salt/state/top.sls`
- `.flipside/salt/pillar/top.sls`

Every `flipside-configure` overwrites what was written by the previous one. To
overcome this issue, just make sure all apps in a single master have the same
files

Multiple app instances of the same templates are not supported on a single
 master. Fixing this is trivial: app put their state files in separate paths and app pillars and other config have to be prefixed by {{ app_name }}


### Deploy

Deploy an application

    flipside-deploy --target=[aws|vagrant]

**KNOWN ISSUES**: deploys all apps together


### SSH access

    flipside-ssh --target=[aws|vagrant]
