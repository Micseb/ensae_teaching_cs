"""
@brief      test log(time=1000s)
@author     Xavier Dupre
"""

import sys
import os
import unittest


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
    import pyquickhelper as skip____
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
    import pyquickhelper as skip____


try:
    import pyensae as skip_____
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..",
                "..",
                "pyensae",
                "src")))
    if path not in sys.path:
        sys.path.append(path)
    import pyensae as skip_____


from pyquickhelper.loghelper.flog import fLOG
from pyquickhelper.pycode import is_travis_or_appveyor


class TestSkipExampleKerasMNIST(unittest.TestCase):

    def test_theano_logreg(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        if is_travis_or_appveyor():
            # it requires latex
            return

        from src.ensae_teaching_cs.examples.keras_mnist import keras_mnist_data, keras_build_mnist_model, keras_fit, keras_predict
        fLOG("data")
        (X_train, Y_train), (X_test, Y_test) = keras_mnist_data()
        fLOG("model", Y_train.shape)
        model = keras_build_mnist_model(Y_train.shape[1], fLOG=fLOG)
        fLOG("fit")
        keras_fit(model, X_train, Y_train, X_test, Y_test, batch_size=128,
                  nb_classes=None, nb_epoch=1, fLOG=fLOG)
        fLOG("predict")
        score = keras_predict(model, X_test, Y_test)
        fLOG(score.shape)
        fLOG(score[:5])


if __name__ == "__main__":
    unittest.main()
