import environ


@environ.config(prefix='')
class RecorderConfig:
    @environ.config
    class Source:
        path = environ.var()
        fps = environ.var()

    @environ.config
    class Records:
        basepath = environ.var()
        histsize = environ.var()

    @environ.config
    class Listener:
        host = environ.var("127.0.0.1")
        port = environ.var("8080")

    source = environ.group(Source)
    records = environ.group(Records)
    listener = environ.group(Listener)
