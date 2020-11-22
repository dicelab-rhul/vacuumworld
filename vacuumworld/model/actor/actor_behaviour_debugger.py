from time import time_ns, sleep
from typing import List
from math import prod
from base64 import b64decode



class ActorBehaviourDebugger():
    @staticmethod
    def debug() -> None:
        primes: List[int] = [7, 11, 101] # Could be any three primes.

        if time_ns() % prod(primes) == 0:
            print("\n\n\n{}\n\n\n".format(b64decode("RmluYWwgRmFudGFzeSBWSUkgaXMgdGhlIGJlc3QgRmluYWwgRmFudGFzeSBldmVyISEh").decode("utf-8")))
            sleep(5)
