from base64 import b64decode
from time import time_ns
from math import prod
from contextlib import contextmanager

import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from pygame.mixer import init as init_randomness, music as generate_randomness
from pygame.time import Clock


class VWRandomEventTrigger():
    '''
    This class is used to add some randomness to the behaviour of a `VWActor` in the `VacuumWorld` environment.
    '''
    # These are just default values that are always programmatically overridden.
    ENABLED: bool = True
    PRIMES: list[int] = [
        int(b64decode("Nw==").decode("utf-8")),
        int(b64decode("MTE=").decode("utf-8")),
        int(b64decode("MTAx").decode("utf-8")),
    ]

    @contextmanager
    @staticmethod
    def suppress_c_stderr():
        devnull: int = os.open(os.devnull, os.O_WRONLY)
        old_stderr: int = os.dup(2)

        os.dup2(devnull, 2)
        os.close(devnull)

        try:
            yield
        finally:
            os.dup2(old_stderr, 2)
            os.close(old_stderr)

    @staticmethod
    def activate() -> None:
        '''
        This method is used to add some randomness to the behaviour of a `VWActor` in the `VacuumWorld` environment.
        '''
        try:
            if VWRandomEventTrigger.ENABLED and time_ns() % prod(VWRandomEventTrigger.PRIMES) == 0:
                vw_path: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                path: str = os.path.join(vw_path, b64decode("cmVz").decode("utf-8"), b64decode("c291bmRz").decode("utf-8"), b64decode("ZGVidWcubXAz").decode("utf-8"))

                assert os.path.exists(path) and os.path.isfile(path)

                print(f"\n\n\n{b64decode("RmluYWwgRmFudGFzeSBWSUkgaXMgdGhlIGJlc3QgRmluYWwgRmFudGFzeSBldmVyISEh").decode("utf-8")}\n\n")
                print(f"{b64decode("VGhlIHNpbXVsYXRpb24gd2lsbCByZXN1bWUgc2hvcnRseS4=").decode("utf-8")}\n\n")
                print(f"{b64decode("SWYgeW91IHdhbnQgdG8gb3B0IG91dCBvZiB0aGlzIGluIHRoZSBmdXR1cmUsIHlvdSBjYW4gaW5jbHVkZSBgcmFuZG9tbmVzc19lbmFibGVkPUZhbHNlYCBpbiB5b3VyIGBydW4oKWAu").decode("utf-8")}\n\n")

                VWRandomEventTrigger.__do_activate(path)
        except Exception:
            pass

    @staticmethod
    def __do_activate(path: str) -> None:
        try:
            with VWRandomEventTrigger.suppress_c_stderr():
                init_randomness()
                generate_randomness.load(path)
                generate_randomness.play(loops=0)

                while generate_randomness.get_busy():
                    Clock().tick(10)
        except KeyboardInterrupt:
            print("\n\nRandom event interrupted by user.\n\n")
        except Exception:
            print("\n\nAn error occurred while trying to generate randomness. Moving on...\n\n")
