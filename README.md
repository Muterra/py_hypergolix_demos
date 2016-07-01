# Hypergolix demos

## [Hypergolix 101: an echo server](/echo-101)

[![Hypergolix 101: an echo server](/echo-101/echo-101.png)](/echo-101)

Start with a newly-flashed Raspberry Pi. End with an echo server that shares objects between the Pi and another computer, dynamically propagating updates between them. Duration: about 10 minutes. [Read more here](/echo-101).

# Setting up a Hypergolix environment

Connecting an applciation to Hypergolix requires three things:

1. A "persistence server" (think of this as Amazon S3 + pub/sub + Golix object verification), shared between all communicating parties. This must be passed to Hypergolix when starting the service.
2. Hypergolix itself: the background service that performs all of the Golix crypto operations, object synchronization, etc. Each party has its own Hypergolix service.
3. A (websockets over localhost) IPC link to the Hypergolix service. The Hypergolix library includes this, provided you're coding in Python 3.5.1 or newer.

Hypergolix itself will soon ship including (**but not requiring**) a PaaS persistence server. In the meantime, you'll have to set one up yourself. Generally speaking, this involves running the ```demo-server.py``` script from within the demo repository. **Be aware that the demo server stores *everything* in volatile memory.** At the moment, the same is true of the Hypergolix service.

## Installing and running Hypergolix

### Prerequisites

1. Python 3.5.1+
2. On Linux and OSX, the ability to compile C extensions (python3-dev)

### Installation

From within a temp folder:

```
git clone https://github.com/Muterra/py_hypergolix .
pip install .
```

Or, if you'd like to tinker, clone it to a development director and run pip with the "editable" flag:

```
git clone https://github.com/Muterra/py_hypergolix .
pip install . -e
```

**Note:** best practices would have you install it within a virtualenv!

### Running Hypergolix

```
python3 -m hypergolix.service
```

Or, to run it in the background (Linux only):

```
python3 -m hypergolix.service &
```

Available flags:

```
--host        IP/web address for persistence provider. Default: localhost
--port        The persistence provider port. Default: 7770
--ipc_port    Port to use for websockets IPC. Default: 7772
--logfile     Dumps logging into a the specified file, relative to current dir.
              Default: None
--verbosity   Sets debug mode and specifies the logging level. Valid options:
                  debug       most verbose
                  info        somewhat more verbose
                  warning     the default Python verbosity
                  error       quiet
```

To stop Hypergolix, send it SIGTERM or SIGINT (if you don't know what those are, press ```Ctrl```+```C```).

# Contributing

Help is welcome and needed. Unfortunately we're so under-staffed that we haven't even had time to make a thorough contribution guide. In the meantime:

## Guide

+ Issues are great! Open them for anything: feature requests, bug reports, etc. 
+ Fork, then PR.
+ Open an issue for every PR.
  + Use the issue for all discussion.
  + Reference the PR somewhere in the issue discussion.
+ Please be patient. We'll definitely give feedback on anything we bounce back to you, but especially since we lack a contribution guide, style guide, etc, this may be a back-and-forth process.
+ Please be courteous in all discussion.

## Project priorities

Note: these needs are specific to external contributors. Internal development priorities differ substantially.

+ Contribution guide
+ Code of conduct
+ Get feedback from other people who have replicated demos
+ Fix code in written echo-101 demo to match the demo video

See also:

+ [Golix contributions](https://github.com/Muterra/doc-golix#contributing)
+ [Hypergolix contributions](https://github.com/Muterra/py_hypergolix#contributing)

## Sponsors and backers

If you like what we're doing, please consider [sponsoring the project](https://opencollective.com/golix#sponsor) or [becoming a backer](https://opencollective.com/golix).

**Sponsors**

  <a href="https://opencollective.com/golix/sponsors/0/website" target="_blank"><img src="https://opencollective.com/golix/sponsors/0/avatar"></a>
  <a href="https://opencollective.com/golix/sponsors/1/website" target="_blank"><img src="https://opencollective.com/golix/sponsors/1/avatar"></a>
  <a href="https://opencollective.com/golix/sponsors/2/website" target="_blank"><img src="https://opencollective.com/golix/sponsors/2/avatar"></a>
  <a href="https://opencollective.com/golix/sponsors/3/website" target="_blank"><img src="https://opencollective.com/golix/sponsors/3/avatar"></a>
  <a href="https://opencollective.com/golix/sponsors/4/website" target="_blank"><img src="https://opencollective.com/golix/sponsors/4/avatar"></a>

-----

**Backers**

  <a href="https://opencollective.com/golix/backers/0/website" target="_blank"><img src="https://opencollective.com/golix/backers/0/avatar"></a>
  <a href="https://opencollective.com/golix/backers/1/website" target="_blank"><img src="https://opencollective.com/golix/backers/1/avatar"></a>
  <a href="https://opencollective.com/golix/backers/2/website" target="_blank"><img src="https://opencollective.com/golix/backers/2/avatar"></a>
  <a href="https://opencollective.com/golix/backers/3/website" target="_blank"><img src="https://opencollective.com/golix/backers/3/avatar"></a>
  <a href="https://opencollective.com/golix/backers/4/website" target="_blank"><img src="https://opencollective.com/golix/backers/4/avatar"></a>
  <a href="https://opencollective.com/golix/backers/5/website" target="_blank"><img src="https://opencollective.com/golix/backers/5/avatar"></a>
  <a href="https://opencollective.com/golix/backers/6/website" target="_blank"><img src="https://opencollective.com/golix/backers/6/avatar"></a>
  <a href="https://opencollective.com/golix/backers/7/website" target="_blank"><img src="https://opencollective.com/golix/backers/7/avatar"></a>
  <a href="https://opencollective.com/golix/backers/8/website" target="_blank"><img src="https://opencollective.com/golix/backers/8/avatar"></a>
  <a href="https://opencollective.com/golix/backers/9/website" target="_blank"><img src="https://opencollective.com/golix/backers/9/avatar"></a>
  <a href="https://opencollective.com/golix/backers/10/website" target="_blank"><img src="https://opencollective.com/golix/backers/10/avatar"></a>
  <a href="https://opencollective.com/golix/backers/11/website" target="_blank"><img src="https://opencollective.com/golix/backers/11/avatar"></a>
  <a href="https://opencollective.com/golix/backers/12/website" target="_blank"><img src="https://opencollective.com/golix/backers/12/avatar"></a>
  <a href="https://opencollective.com/golix/backers/13/website" target="_blank"><img src="https://opencollective.com/golix/backers/13/avatar"></a>
  <a href="https://opencollective.com/golix/backers/14/website" target="_blank"><img src="https://opencollective.com/golix/backers/14/avatar"></a>
  <a href="https://opencollective.com/golix/backers/15/website" target="_blank"><img src="https://opencollective.com/golix/backers/15/avatar"></a>
  <a href="https://opencollective.com/golix/backers/16/website" target="_blank"><img src="https://opencollective.com/golix/backers/16/avatar"></a>
  <a href="https://opencollective.com/golix/backers/17/website" target="_blank"><img src="https://opencollective.com/golix/backers/17/avatar"></a>
  <a href="https://opencollective.com/golix/backers/18/website" target="_blank"><img src="https://opencollective.com/golix/backers/18/avatar"></a>
  <a href="https://opencollective.com/golix/backers/19/website" target="_blank"><img src="https://opencollective.com/golix/backers/19/avatar"></a>
  <a href="https://opencollective.com/golix/backers/20/website" target="_blank"><img src="https://opencollective.com/golix/backers/20/avatar"></a>
  <a href="https://opencollective.com/golix/backers/21/website" target="_blank"><img src="https://opencollective.com/golix/backers/21/avatar"></a>
  <a href="https://opencollective.com/golix/backers/22/website" target="_blank"><img src="https://opencollective.com/golix/backers/22/avatar"></a>
  <a href="https://opencollective.com/golix/backers/23/website" target="_blank"><img src="https://opencollective.com/golix/backers/23/avatar"></a>
  <a href="https://opencollective.com/golix/backers/24/website" target="_blank"><img src="https://opencollective.com/golix/backers/24/avatar"></a>
  <a href="https://opencollective.com/golix/backers/25/website" target="_blank"><img src="https://opencollective.com/golix/backers/25/avatar"></a>
  <a href="https://opencollective.com/golix/backers/26/website" target="_blank"><img src="https://opencollective.com/golix/backers/26/avatar"></a>
  <a href="https://opencollective.com/golix/backers/27/website" target="_blank"><img src="https://opencollective.com/golix/backers/27/avatar"></a>
  <a href="https://opencollective.com/golix/backers/28/website" target="_blank"><img src="https://opencollective.com/golix/backers/28/avatar"></a>
  <a href="https://opencollective.com/golix/backers/29/website" target="_blank"><img src="https://opencollective.com/golix/backers/29/avatar"></a>

