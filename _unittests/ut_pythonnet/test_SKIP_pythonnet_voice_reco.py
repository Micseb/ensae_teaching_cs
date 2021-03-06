"""
@brief      test log(time=1s)
"""

import sys
import os
import unittest
import warnings


try:
    import src
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..")))
    if path not in sys.path:
        sys.path.append(path)
    import src

try:
    import pyquickhelper as skip_
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..",
                "..",
                "pyquickhelper",
                "src")))
    if path not in sys.path:
        sys.path.append(path)
    import pyquickhelper as skip_

from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import is_travis_or_appveyor


class TestSKIPPythonnetVoiceReco(unittest.TestCase):
    """
    This API is not reliable.
    The free account has probably stopped.
    """

    def test_voice_reco(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        wav = os.path.join(os.path.abspath(
            os.path.dirname(__file__)), "data", "output.wav")

        if is_travis_or_appveyor():
            # no keys
            return

        import keyring
        subkey = keyring.get_password(
            "cogser", os.environ["COMPUTERNAME"] + "voicereco")

        if subkey is None:
            warnings.warn("No available key for access Voice Recognition.")
            return

        if sys.platform.startswith("win"):
            from src.ensae_teaching_cs.pythonnet import vocal_recognition

            with open(wav, "rb") as f:
                content = f.read()

            try:
                res = vocal_recognition(subkey, memwav=content)
            except Exception as e:
                if "Audio device error encountered" in str(e):
                    # maybe the script is running on a virtual machine (no
                    # Audia device)
                    if os.environ["USERNAME"] == "ensaestudent" or \
                       os.environ["USERNAME"] == "vsxavierdupre" or \
                       os.environ["USERNAME"] == "vsxavierdupre" or \
                       ("DOUZE2016" in os.environ["COMPUTERNAME"]) or \
                       os.environ["USERNAME"] == "appveyor" or \
                       "paris" in os.environ["COMPUTERNAME"].lower() or \
                       os.environ["USERNAME"].endswith("$"):  # anonymous Jenkins configuration
                        # I would prefer to catch a proper exception
                        # it just exclude one user only used on remotre
                        # machines
                        return
                raise Exception(
                    "USERNAME: " + os.environ.get("USERNAME", "-")) from e

            fLOG(res)
            self.assertTrue(isinstance(res, dict))

            res = vocal_recognition(subkey, filename=wav)
            fLOG(res)
            self.assertTrue(isinstance(res, dict))
            for k, v in res.items():
                fLOG(k, v)
                if "results" == k:
                    for _ in v:
                        fLOG(_)


if __name__ == "__main__":
    unittest.main()
