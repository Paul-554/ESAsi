import numpy as np

def kronecker_product(*matrices):
    """
    Compute the Kronecker product of a sequence of matrices.
    :param matrices: Two or more numpy arrays.
    :return: Kronecker product as a numpy array.
    """
    result = matrices[0]
    for m in matrices[1:]:
        result = np.kron(result, m)
    return result

def kronecker_factorized_prior(mean_list, cov_list):
    """
    Construct a multivariate normal prior with Kronecker-factorized covariance.
    :param mean_list: List of 1D numpy arrays (means for each factor).
    :param cov_list: List of 2D numpy arrays (covariance for each factor).
    :return: mean (1D array), covariance (2D array)
    """
    # Compute the full mean vector as the Kronecker product of means
    mean = mean_list[0]
    for m in mean_list[1:]:
        mean = np.kron(mean, m)
    # Compute the full covariance as the Kronecker product of covariances
    cov = cov_list[0]
    for c in cov_list[1:]:
        cov = np.kron(cov, cov)
    return mean, cov

def sample_kronecker_prior(mean_list, cov_list, n_samples=1, random_state=None):
    """
    Draw samples from a Kronecker-factorized multivariate normal prior.
    :param mean_list: List of 1D numpy arrays (means for each factor).
    :param cov_list: List of 2D numpy arrays (covariance for each factor).
    :param n_samples: Number of samples to draw.
    :param random_state: Optional numpy random state.
    :return: Samples as a 2D numpy array (n_samples, total_dim).
    """
    mean, cov = kronecker_factorized_prior(mean_list, cov_list)
    rng = np.random.default_rng(random_state)
    return rng.multivariate_normal(mean, cov, size=n_samples)

def kronecker_logpdf(x, mean_list, cov_list):
    """
    Compute the log probability density of x under a Kronecker-factorized prior.
    :param x: 1D numpy array (flattened sample).
    :param mean_list: List of 1D numpy arrays (means for each factor).
    :param cov_list: List of 2D numpy arrays (covariance for each factor).
    :return: Log probability density (float).
    """
    mean, cov = kronecker_factorized_prior(mean_list, cov_list)
    size = mean.shape[0]
    diff = x - mean
    try:
        inv_cov = np.linalg.inv(cov)
        logdet = np.linalg.slogdet(cov)[1]
    except np.linalg.LinAlgError:
        # For large Kronecker products, use logdet and solve via Cholesky if possible
        raise ValueError("Covariance matrix is singular or ill-conditioned.")
    log_prob = -0.5 * (np.dot(diff, np.dot(inv_cov, diff)) + logdet + size * np.log(2 * np.pi))
    return log_prob

# Example usage:
if __name__ == "__main__":
    # Define two factors
    mean1 = np.zeros(2)
    mean2 = np.ones(3)
    cov1 = np.eye(2)
    cov2 = 2 * np.eye(3)
    # Kronecker product prior
    mean, cov = kronecker_factorized_prior([mean1, mean2], [cov1, cov2])
    print("Kronecker mean:", mean)
    print("Kronecker covariance shape:", cov.shape)
    # Draw samples
    samples = sample_kronecker_prior([mean1, mean2], [cov1, cov2], n_samples=5)
    print("Samples:\n", samples)
    # Log probability of a sample
    logp = kronecker_logpdf(samples[0], [mean1, mean2], [cov1, cov2])
    print("Log probability of first sample:", logp)
