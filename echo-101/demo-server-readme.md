Setting up a demo persistence server for Hypergolix experimentation is easy. But, keep in mind that it's storing everything in local memory. So "nothing is permanent" and all that jazz.

Just run the included ```demo-server.py``` script (within this repository). Available flags are:

```
--host      Specify the persistence server's host. Default: localhost
--port      Specify the persistence server's port. Default: 7770
--logfile   Send logging info to the specified file, relative to current dir.
            Default: None
--verbosity Sets debug mode and specifies the logging level. Valid options:
                debug       most verbose
                info        somewhat more verbose
                warning     the default Python verbosity
                error       quiet
```