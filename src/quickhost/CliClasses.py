from collections import namedtuple

class CliResponse(namedtuple('CliResponse', ['stdout', 'stderr', 'rc'])):
   __slots__ = ()
