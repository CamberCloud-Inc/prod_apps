# Import required libraries for data processing and visualization
import numpy as np
import matplotlib.pyplot as plt
import pyvista as pv
from scipy.interpolate import griddata
from matplotlib.path import Path
from scipy.spatial import ConvexHull

# ============================================================================
# LOAD AND PROCESS VTK DATA FROM POTENTIALFOAM SIMULATION
# ============================================================================

# Load the potential flow solution and cylinder boundary
# AFTER `from matplotlib.path import Path` …
from pathlib import Path as FS        # avoid the name clash with matplotlib.Path
run = next(d for d in FS('VTK').iterdir() if d.is_dir())  # first sub-folder
mesh     = pv.read(run / 'internal.vtu')
cylinder = pv.read(run / 'boundary' / 'cylinder.vtp')

# Extract cell centers and velocity data from the potential flow solution
cells = mesh.cell_centers()
centres = cells.points[:, :2]          # 2D cell-center coordinates (N×2)
U = mesh.cell_data["U"][:, :2]         # Velocity components from potential flow [u, v] (N×2)

# ============================================================================
# CREATE CYLINDER BOUNDARY POLYGON FOR MASKING
# ============================================================================

# Extract 2D cylinder boundary points and create convex hull
c2d = cylinder.points[:, :2]
hull = ConvexHull(c2d)
poly = c2d[hull.vertices]              # Ordered boundary vertices
poly_path = Path(poly)                 # Create matplotlib Path for inside/outside tests

# Remove cell centers that are inside the cylinder body
keep = ~poly_path.contains_points(centres)
centres, U = centres[keep], U[keep]

# ============================================================================
# INTERPOLATE TO REGULAR GRID FOR STREAMLINE VISUALIZATION
# ============================================================================

# Create regular rectangular grid for streamline plotting
nx = ny = 300  # Grid resolution
xi = np.linspace(centres[:,0].min(), centres[:,0].max(), nx)
yi = np.linspace(centres[:,1].min(), centres[:,1].max(), ny)
X, Y = np.meshgrid(xi, yi)

# Interpolate velocity components from unstructured to structured grid
u = griddata(centres, U[:,0], (X, Y), method='linear')  # x-velocity component
v = griddata(centres, U[:,1], (X, Y), method='linear')  # y-velocity component

# Apply cylinder mask to grid (remove points inside cylinder)
inside = poly_path.contains_points(np.c_[X.ravel(), Y.ravel()]).reshape(X.shape)
u[inside] = v[inside] = np.nan  # Set interior points to NaN
speed = np.hypot(u, v)              # Calculate velocity magnitude

# ============================================================================
# CREATE POTENTIAL FLOW STREAMLINE VISUALIZATION
# ============================================================================

# Create streamline plot showing smooth potential flow patterns
plt.figure(figsize=(6, 6))
plt.streamplot(X, Y, u, v, 
               color=speed,           # Color streamlines by velocity magnitude
               cmap='viridis',        # Use viridis colormap
               density=1.5,           # Streamline density
               linewidth=1)           # Line thickness

# Draw cylinder outline
poly_closed = np.vstack([poly, poly[0]])   # Close the polygon
plt.plot(poly_closed[:,0], poly_closed[:,1], 'k', lw=1.5)

# Format plot for clean presentation
plt.axis('equal')      # Equal aspect ratio to preserve geometry
plt.axis('off')        # Hide axes for cleaner scientific visualization
plt.tight_layout()     # Optimize layout
plt.title('Potential Flow Around Cylinder\n(Smooth streamlines, no separation)', 
          fontsize=12, pad=20)
plt.show()