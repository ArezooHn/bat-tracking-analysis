import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
from sklearn.neighbors import KernelDensity
import numpy as np
import os

def run_kde_analysis(df, bandwidth=0.01, output_path="outputs/figures/kde_map.png"):
    """
    اجرای تحلیل KDE روی داده‌های خفاش‌ها
    """
    coords = df[['location-long', 'location-lat']].dropna().values
    kde = KernelDensity(bandwidth=bandwidth, kernel='gaussian')
    kde.fit(coords)

    x_min, x_max = coords[:, 0].min(), coords[:, 0].max()
    y_min, y_max = coords[:, 1].min(), coords[:, 1].max()
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 100),
                         np.linspace(y_min, y_max, 100))
    grid_coords = np.vstack([xx.ravel(), yy.ravel()]).T

    density = np.exp(kde.score_samples(grid_coords))
    density = density.reshape(xx.shape)

    plt.figure(figsize=(8, 6))
    plt.imshow(density, cmap='hot', extent=[x_min, x_max, y_min, y_max], origin='lower')
    plt.scatter(coords[:, 0], coords[:, 1], s=2, color='blue', alpha=0.5, label="Bat locations")
    plt.colorbar(label="Bat density")
    plt.legend()
    plt.title("Bat Activity Hotspots (KDE)")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()