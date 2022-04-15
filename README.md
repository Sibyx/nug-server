# nug-server

**Work in progress**

Simple KVM switch with RFB output written in Python based on the
[asyncio](https://docs.python.org/3/library/asyncio-protocol.html) module.

This project is a part of my master thesis on the
[Faculty of Informatics and Information Technologies STU in Bratislava](https://www.fiit.stuba.sk/en.html) on the
subject of KVM switch implementation.

## Configuration

```toml
[general]
bind = "0.0.0.0:9001"
database = "/home/alarm/nug.db"
log_level = "INFO"

[syslog]
ip = "127.0.0.1"
port = 1514

[[dongles]]
ip = "10.0.0.1"
port = 5001
services = [ "mouse", "keyboard" ]

[[dongles]]
ip = "10.0.0.2"
port = 5002
services = [ "video" ]

```

## Dependencies

We us [ArchLinux ARM](https://archlinuxarm.org/) as base image.

- cmake (`pacman -S cmake`)
- opencv (`pacman -S opencv`)
- gcc (`pacman -S gcc`)
- numpy (`pip install numpy`)
- [tomli](https://github.com/hukkin/tomli)

---
With ❤️☕️🥃🍀 Jakub Dubec 2022
