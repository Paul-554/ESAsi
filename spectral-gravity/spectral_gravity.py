import numpy as np

# Define the critical density (in kg/m^3)
rho_c = 8.5e-27

def space_time_response(density, k=10):
    """
    Calculate clumping and expansion factors for a given density.
    Args:
        density (float or np.array): Local density (kg/m^3)
        k (float): Sharpness of the transition (default 10)
    Returns:
        clumping (float or np.array): Clumping factor (0 to 1)
        expansion (float or np.array): Expansion factor (0 to 1)
    """
    eta = density / rho_c
    clumping = 1 / (1 + np.exp(-k * (eta - 1)))
    expansion = 1 - clumping
    return clumping, expansion
