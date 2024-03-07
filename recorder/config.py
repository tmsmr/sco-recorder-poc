import environ


@environ.config(prefix='')
class RecorderConfig:
    @environ.config
    class Source:
        path = environ.var()
        fps = environ.var()

    @environ.config
    class Snapshots:
        basepath = environ.var()
        histsize = environ.var()

    @environ.config
    class Listener:
        host = environ.var("127.0.0.1")
        port = environ.var("8080")

    source = environ.group(Source)
    snapshots = environ.group(Snapshots)
    listener = environ.group(Listener)
