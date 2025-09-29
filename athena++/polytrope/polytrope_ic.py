#!/usr/bin/env python3
"""
Generate initial conditions for polytrope star simulation
Solves the Lane-Emden equation for polytropic stellar structure
"""

import numpy as np
import h5py
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

def lane_emden_derivatives(xi, y, n):
    """
    Derivatives for the Lane-Emden equation
    d²θ/dξ² = -θ^n - (2/ξ)dθ/dξ

    Where y[0] = θ, y[1] = dθ/dξ
    """
    theta, dtheta_dxi = y

    # Ensure theta is non-negative for power operation
    theta = max(theta, 0.0)

    if xi == 0 or xi < 1e-10:
        # At the center, use L'Hôpital's rule
        d2theta_dxi2 = -theta**n / 3.0
    else:
        d2theta_dxi2 = -theta**n - (2.0/xi) * dtheta_dxi

    return [dtheta_dxi, d2theta_dxi2]

def solve_lane_emden(n, xi_max=10.0, num_points=1000):
    """
    Solve the Lane-Emden equation for polytropic index n
    """
    # Initial conditions at center (xi = 0)
    # θ(0) = 1, dθ/dξ(0) = 0
    y0 = [1.0, 0.0]

    # Create xi array (avoid xi=0 for numerical stability)
    xi = np.linspace(1e-6, xi_max, num_points)

    # Solve the ODE
    sol = solve_ivp(lambda xi, y: lane_emden_derivatives(xi, y, n),
                   [xi[0], xi[-1]], y0, t_eval=xi,
                   method='RK45', rtol=1e-8, atol=1e-10)

    # Only return successful solution points
    if sol.success:
        return sol.t, sol.y[0], sol.y[1]  # xi, theta, dtheta_dxi
    else:
        raise RuntimeError("Lane-Emden equation solver failed")

def create_polytrope_profile(n=1.5, rho_c=1.0, R_star=1.0, nr=128):
    """
    Create density and pressure profiles for polytrope star
    """
    # Solve Lane-Emden equation
    xi, theta, dtheta_dxi = solve_lane_emden(n, xi_max=10.0)

    # Find stellar surface (where theta first becomes zero or negative)
    surface_idx = np.where(theta <= 0)[0]
    if len(surface_idx) > 0:
        xi_1 = xi[surface_idx[0]]
        theta_1 = theta[surface_idx[0]]
    else:
        # If theta doesn't reach zero, use the point where it's minimum
        min_idx = np.argmin(theta)
        xi_1 = xi[min_idx]
        theta_1 = theta[min_idx]

    print(f"Stellar surface at xi_1 = {xi_1:.4f}")

    # Create radial grid for simulation
    r = np.linspace(0, R_star * 2, nr)  # Extend beyond stellar radius

    # Scale factor relating dimensionless radius to physical radius
    alpha = R_star / xi_1

    # Initialize arrays
    rho = np.zeros(nr)
    pressure = np.zeros(nr)

    # Interpolate Lane-Emden solution onto radial grid
    for i, radius in enumerate(r):
        xi_val = radius / alpha

        if xi_val <= xi_1:  # Inside the star
            # Interpolate theta
            theta_val = np.interp(xi_val, xi, theta)
            theta_val = max(theta_val, 0)  # Ensure non-negative

            # Density and pressure from polytropic relations
            rho[i] = rho_c * theta_val**n

            # For gamma = 1 + 1/n, P = K * rho^gamma
            # We set K such that pressure is continuous
            K = 1.0 / ((n + 1) * rho_c**(1/n))
            pressure[i] = K * rho[i]**(1 + 1/n)

        else:  # Outside the star (vacuum or atmosphere)
            rho[i] = 1e-6  # Small background density
            pressure[i] = 1e-6  # Small background pressure

    return r, rho, pressure

def write_athena_initial_conditions(filename, r, rho, pressure, v_r=None):
    """
    Write initial conditions in format suitable for Athena++
    """
    nr = len(r)

    # Default to zero radial velocity if not provided
    if v_r is None:
        v_r = np.zeros(nr)

    # Create output data
    data = {
        'radius': r,
        'density': rho,
        'pressure': pressure,
        'velocity_r': v_r,
        'velocity_theta': np.zeros(nr),
        'velocity_phi': np.zeros(nr)
    }

    # Write to HDF5 file
    with h5py.File(filename, 'w') as f:
        for key, value in data.items():
            f.create_dataset(key, data=value)

        # Add metadata
        f.attrs['polytrope_index'] = 1.5
        f.attrs['stellar_mass'] = 1.0
        f.attrs['stellar_radius'] = 1.0
        f.attrs['central_density'] = 1.0

    print(f"Initial conditions written to {filename}")

def plot_polytrope_profile(r, rho, pressure):
    """
    Plot the polytrope density and pressure profiles
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    ax1.plot(r, rho, 'b-', linewidth=2)
    ax1.set_xlabel('Radius')
    ax1.set_ylabel('Density')
    ax1.set_title('Polytrope Density Profile')
    ax1.grid(True)
    ax1.set_yscale('log')

    ax2.plot(r, pressure, 'r-', linewidth=2)
    ax2.set_xlabel('Radius')
    ax2.set_ylabel('Pressure')
    ax2.set_title('Polytrope Pressure Profile')
    ax2.grid(True)
    ax2.set_yscale('log')

    plt.tight_layout()
    plt.savefig('polytrope_profile.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Profile plot saved as polytrope_profile.png")

if __name__ == "__main__":
    # Generate polytrope initial conditions
    print("Generating polytrope star initial conditions...")

    # Parameters
    polytrope_index = 1.5
    central_density = 1.0
    stellar_radius = 1.0
    num_radial_points = 128

    # Create profile
    r, rho, pressure = create_polytrope_profile(
        n=polytrope_index,
        rho_c=central_density,
        R_star=stellar_radius,
        nr=num_radial_points
    )

    # Write initial conditions
    write_athena_initial_conditions('polytrope_ic.h5', r, rho, pressure)

    # Plot profile
    plot_polytrope_profile(r, rho, pressure)

    print("Polytrope initial conditions generation complete!")