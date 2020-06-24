# Packager [![Build Status](https://cloud.drone.io/api/badges/tinvaan/packager/status.svg)](https://cloud.drone.io/tinvaan/packager)
A `yaml` based source-code to package bundler.

## Supported formats
| Format | Host | Status |
| -------|------|--------|
| `.deb` | Ubuntu/Debian (`apt`, `dpkg`) | Active |
| `.rpm` | RHEL, Yum | TODO |
| `.tar.gz`, `.tar.xz` | ArchLinux/Pacman | TODO |


## Features
* Create multiple package formats from your source code through a single command
* `packager` log tightly integrated with `git` history and `CHANGELOG` -- Coming soon!
* Publish your packages via CLI -- Coming soon!

## Installation
Clone the repository and install using `pip` installer. This project requires Python `3.x`.
```bash
$ pip install .
```

## Usage
Initialize `packager` in your project repository.
```bash
$ packager init
```
This creates a `.packager` folder and a `config.yml` inside. Update the `config.yml` with required settings. Below is an example `config.yml`.
```yaml
package:
    name: example-deb
    version: 1.0.0
    description: "An example packager config for a debian package"
    build: cmake
    authors:
        - Harish Navnit <harishnavnit@gmail.com>
    targets:
        - debian
```

Check if the config.yml is valid.
```bash
$ packager validate .packager/config.yml

Config file at .packager/config.yml is valid
```

Build the package
```bash
$ packager build .packager/config.yml

dpkg-deb: building package 'example-deb' in '/tmp/deb-pkg-tools-build-5ef82tfb/example-deb_1.0.0_all.deb'.
Lintian is not installed, skipping sanity check.
```
