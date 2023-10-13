from time import time_ns
from math import prod
from base64 import b64decode

import os


class VWActorBehaviourDebugger():
    '''
    This class is used to debug the behaviour of a `VWActor` in the `VacuumWorld` universe.
    '''
    # These are just default values that are always programmatically overridden.
    DEBUG_ENABLED: bool = True
    PRIMES: list[int] = [
        int(b64decode("Nw==").decode("utf-8")),
        int(b64decode("MTE=").decode("utf-8")),
        int(b64decode("MTAx").decode("utf-8")),
    ]

    @staticmethod
    def debug() -> None:
        '''
        This method is used to debug the behaviour of a `VWActor` in the `VacuumWorld` universe.
        '''
        try:
            if VWActorBehaviourDebugger.DEBUG_ENABLED and time_ns() % prod(VWActorBehaviourDebugger.PRIMES) == 0:
                print(f"\n\n\n{b64decode('RmluYWwgRmFudGFzeSBWSUkgaXMgdGhlIGJlc3QgRmluYWwgRmFudGFzeSBldmVyISEh').decode('utf-8')}\n\n")
                print(f"{b64decode('VGhlIHNpbXVsYXRpb24gd2lsbCByZXN1bWUgc2hvcnRseS4=').decode('utf-8')}\n\n")
                print(f"{b64decode('SWYgeW91IHdhbnQgdG8gb3B0IG91dCBvZiB0aGlzIGluIHRoZSBmdXR1cmUsIHlvdSBjYW4gaW5jbHVkZSBgZGVidWdfZW5hYmxlZD1GYWxzZWAgaW4geW91ciBgcnVuKClgLg==').decode('utf-8')}\n\n")

        except Exception:
            pass
