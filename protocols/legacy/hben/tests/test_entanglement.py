import unittest
import numpy as np
from core.entanglement_ops import kronecker_product, kronecker_factorized_prior, sample_kronecker_prior, kronecker_logpdf

class TestEntanglementOps(unittest.TestCase):
    def setUp(self):
        self.mean1 = np.array([0.0, 1.0])
        self.mean2 = np.array([1.0, -1.0])
        self.cov1 = np.eye(2)
        self.cov2 = 2 * np.eye(2)

    def test_kronecker_product(self):
        A = np.array([[1, 2], [3, 4]])
        B = np.array([[0, 5], [6, 7]])
        result = kronecker_product(A, B)
        self.assertEqual(result.shape, (4, 4))
        self.assertTrue(np.allclose(result[0:2, 0:2], A[0,0]*B))

    def test_kronecker_factorized_prior(self):
        mean, cov = kronecker_factorized_prior([self.mean1, self.mean2], [self.cov1, self.cov2])
        self.assertEqual(mean.shape[0], 4)
        self.assertEqual(cov.shape, (4, 4))
        self.assertTrue(np.allclose(np.diag(cov), 2.0))

    def test_sample_kronecker_prior(self):
        samples = sample_kronecker_prior([self.mean1, self.mean2], [self.cov1, self.cov2], n_samples=10)
        self.assertEqual(samples.shape, (10, 4))

    def test_kronecker_logpdf(self):
        mean, cov = kronecker_factorized_prior([self.mean1, self.mean2], [self.cov1, self.cov2])
        x = mean + np.random.normal(0, 0.1, size=mean.shape)
        logp = kronecker_logpdf(x, [self.mean1, self.mean2], [self.cov1, self.cov2])
        self.assertIsInstance(logp, float)

if __name__ == '__main__':
    unittest.main()
