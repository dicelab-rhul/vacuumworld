from time import time_ns
from typing import List
from math import prod
from base64 import b64decode
from playsound import playsound

import os


class ActorBehaviourDebugger():
    DEBUG_ENABLED: bool = True  # This is just a default value that is always programmatically overridden.
    PRIMES: List[int] = [1, 1, 1]  # This is just a default value that is always programmatically overridden.

    @staticmethod
    def debug() -> None:
        try:
            if ActorBehaviourDebugger.DEBUG_ENABLED and time_ns() % prod(ActorBehaviourDebugger.PRIMES) == 0:
                vw_path: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                path: str = os.path.join(vw_path, b64decode("cmVz").decode("utf-8"), b64decode("c291bmRz").decode("utf-8"), b64decode("ZGVidWcubXAz").decode("utf-8"))

                assert os.path.exists(path)

                print("\n\n\n{}\n\n".format(b64decode("RmluYWwgRmFudGFzeSBWSUkgaXMgdGhlIGJlc3QgRmluYWwgRmFudGFzeSBldmVyISEh").decode("utf-8")))
                print("{}\n\n".format(b64decode("VGhlIHNpbXVsYXRpb24gd2lsbCByZXN1bWUgc2hvcnRseS4=").decode("utf-8")))
                print("{}\n\n".format(b64decode("SWYgeW91IHdhbnQgdG8gb3B0IG91dCBvZiB0aGlzIGluIHRoZSBmdXR1cmUsIHlvdSBjYW4gaW5jbHVkZSBgZGVidWdfZW5hYmxlZD1GYWxzZWAgaW4geW91ciBgcnVuKClgLg==").decode("utf-8")))

                playsound(sound=path)
        except Exception:
            pass
