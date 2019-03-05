# boa-environment-mgmt plugin


## Preface

This document describes the functionality provided by the boa-environment-mgmt-plugin.

See the **[XL Release Documentation](https://docs.xebialabs.com/xl-release/index.html)** for background information on XL Release and release concepts.


## Overview

The boa-environment-mgmt-plugin is an XL Release plugin that allows you to:

  * Programmatically create environment if they are not present.
  * Create application if not present. 


## Requirements

* XL Release 8.5+

## Installation

* Copy the latest JAR file from the [releases page](https://github.com/xebialabs-external/boa-environment-mgmt-plugin/releases) into the `XL_RELEASE_SERVER/plugins` directory.
* Restart the XL Release server.

## Tasks ##
+ Create Environment
  * `releaseEnvironment`: Name of the release variable having release environment(`list`) 
  * `spkComponentsToRelease`: Name of the release variable having component names (`list`)
  * `envNameToEnvTypeMapping`: Name of the release variable having env name to env type mapping (`key-value map`)
  * `spkName`: Name of the release variable having spk name (`string`)

+ Create Application
  * `releaseEnvironment`: Name of the release variable having release environment(`list`) 
  * `spkComponentsToRelease`: Name of the release variable having component names (`list`)
  * `envNameToEnvTypeMapping`: Name of the release variable having env name to env type mapping (`key-value map`)
  * `spkName`: Name of the release variable having spk name (`string`)


