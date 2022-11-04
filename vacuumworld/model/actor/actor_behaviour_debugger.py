from time import time_ns
from typing import List
from math import prod
from base64 import b64decode
from playsound import playsound

import os


class ActorBehaviourDebugger():
    DEBUG_ENABLED: bool = True

    @staticmethod
    def debug() -> None:
        try:
            primes: List[int] = [7, 11, 101]  # Could be any three primes.

            if ActorBehaviourDebugger.DEBUG_ENABLED and time_ns() % prod(primes) == 0:
                vw_path: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                path: str = os.path.join(vw_path, b64decode("cmVz").decode("utf-8"), b64decode("c291bmRz").decode("utf-8"), b64decode("ZGVidWcubXAz").decode("utf-8"))

                assert os.path.exists(path)

                print("\n\n\n{}\n\n\n".format(b64decode("RmluYWwgRmFudGFzeSBWSUkgaXMgdGhlIGJlc3QgRmluYWwgRmFudGFzeSBldmVyISEh").decode("utf-8")))
                print("{}\n\n\n".format(b64decode("VGhlIHNpbXVsYXRpb24gd2lsbCByZXN1bWUgc2hvcnRseS4=").decode("utf-8")))

                playsound(sound=path)
        except Exception:
            pass
