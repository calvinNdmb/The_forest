import noise
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


def create_noise(nx: float, ny: float, octaves: int, persistence: float, lacunarity: int) -> np.ndarray:

    val = noise.pnoise2(
        nx,
        ny,
        octaves=octaves,
        persistence=persistence,
        lacunarity=lacunarity,
        repeatx=1024,
        repeaty=1024,
        base=9
    )
    pixel_val = (val + 1) / 2 * 255
    # Discrétisation
    if pixel_val <= 25:
        pixel_val = 0
    elif pixel_val <= 50 and pixel_val > 25:
        pixel_val = 50
    elif pixel_val <= 75 and pixel_val > 50:
        pixel_val = 75
    elif pixel_val <= 100 and pixel_val > 75:
        pixel_val = 100
    elif pixel_val <= 125 and pixel_val > 100:
        pixel_val = 125
    elif pixel_val <= 150 and pixel_val > 125:
        pixel_val = 150
    elif pixel_val <= 175 and pixel_val > 150:
        pixel_val = 175
    elif pixel_val <= 200 and pixel_val > 175:
        pixel_val = 200
    elif pixel_val <= 225 and pixel_val > 200:
        pixel_val = 225
    elif pixel_val <= 250 and pixel_val > 225:
        pixel_val = 250
            
    return pixel_val

def graphiques(number_of_tree_vivants, number_of_seeds, mean_age, mean_rayons_tops, 
               mean_energies, mean_energies_solaires, mean_hauteurs):
    """Trace plusieurs graphiques sur une seule figure pour analyser l'évolution."""
    x = np.arange(len(number_of_tree_vivants))  # Axe X basé sur les périodes
    fig, axs = plt.subplots(3, 2, figsize=(14, 12))  # 3 lignes, 2 colonnes de graphiques

    # Graphique 1 : Nombre d'arbres vivants
    axs[0, 0].plot(x, number_of_tree_vivants, label="Nombre d'arbres vivants", linestyle='-', linewidth=2)
    axs[0, 0].plot(x, number_of_seeds, label="Nombre de graines", linestyle='--', linewidth=2)
    axs[0, 0].set_title("Nombre d'arbres vivants et de graines")
    axs[0, 0].set_xlabel("Temps (en périodes de 100 jours)")
    axs[0, 0].set_ylabel("Nombre")
    axs[0, 0].legend()
    axs[0, 0].grid(True)

    # Graphique 2 : Âge moyen
    x = np.arange(len(mean_age))
    axs[0, 1].plot(x, mean_age, label="Âge moyen", linestyle='-', linewidth=2, color='orange')
    axs[0, 1].set_title("Âge moyen des arbres")
    axs[0, 1].set_xlabel("Temps (en périodes de 100 jours)")
    axs[0, 1].set_ylabel("Âge")
    axs[0, 1].legend()
    axs[0, 1].grid(True)

    # Graphique 3 : Rayon moyen des canopées
    axs[1, 0].plot(x, mean_rayons_tops, label="Rayon moyen des canopées", linestyle='-', linewidth=2, color='green')
    axs[1, 0].set_title("Rayon moyen des canopées")
    axs[1, 0].set_xlabel("Temps (en périodes de 100 jours)")
    axs[1, 0].set_ylabel("Rayon")
    axs[1, 0].legend()
    axs[1, 0].grid(True)

    # Graphique 4 : Énergie moyenne
    axs[1, 1].plot(x, mean_energies, label="Énergie moyenne", linestyle='-', linewidth=2, color='red')
    axs[1, 1].set_title("Énergie moyenne des arbres")
    axs[1, 1].set_xlabel("Temps (en périodes de 100 jours)")
    axs[1, 1].set_ylabel("Énergie")
    axs[1, 1].legend()
    axs[1, 1].grid(True)

    # Graphique 5 : Énergie solaire moyenne
    axs[2, 0].plot(x, mean_energies_solaires, label="Énergie solaire moyenne", linestyle='-', linewidth=2, color='purple')
    axs[2, 0].set_title("Énergie solaire moyenne des arbres")
    axs[2, 0].set_xlabel("Temps (en périodes de 100 jours)")
    axs[2, 0].set_ylabel("Énergie solaire")
    axs[2, 0].legend()
    axs[2, 0].grid(True)

    # Graphique 6 : Hauteur moyenne
    axs[2, 1].plot(x, mean_hauteurs, label="Hauteur moyenne", linestyle='-', linewidth=2, color='blue')
    axs[2, 1].set_title("Hauteur moyenne des arbres")
    axs[2, 1].set_xlabel("Temps (en périodes de 100 jours)")
    axs[2, 1].set_ylabel("Hauteur")
    axs[2, 1].legend()
    axs[2, 1].grid(True)

    # Ajuster l'espacement
    plt.tight_layout()
    plt.savefig("graphiques_complets.png")
    plt.show()

def search_graphique_kmeans(data):
    """
    Applique le K-means sur les données et affiche les résultats.
    
    :param data: np.ndarray, données 2D pour le clustering
    :param n_clusters: int, nombre de clusters
    """
    kmeans_kwargs = {
        "init": "random",
        "n_init": 10,
        "random_state": 1,
        }
    sse = []
    for k in range(1, 10):
        kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
        kmeans.fit(data)
        sse.append(kmeans.inertia_)

    #visualize results
    plt.plot(range(1, 10), sse)
    plt.xticks(range(1, 10))
    plt.xlabel("Number of Clusters")
    plt.ylabel("SSE")
    plt.savefig("graphiques_means.png")
    plt.show()

def show_kmeans(data, n_clusters=3):
    kmeans_kwargs = {
        "init": "random",
        "n_init": 10,
        "random_state": 1,
        }
    kmeans = KMeans(n_clusters=n_clusters, **kmeans_kwargs)
    clusters = kmeans.fit_predict(data)

    # Add cluster labels to the data
    data['Cluster'] = clusters

    # Scatter plot
    plt.figure(figsize=(8, 6))
    for cluster in range(3):
        data = data[data['Cluster'] == cluster]
        plt.scatter(data['rayon_top'], data['hauteur'], label=f'Cluster {cluster}')

    # Mark cluster centers
    centers = kmeans.cluster_centers_
    plt.scatter(centers[:, 0], centers[:, 1], s=200, c='red', label='Centroids', marker='X')

    plt.xlabel('rayon_top')
    plt.ylabel('hauteur')
    plt.title('Scatter Plot of Clusters')
    plt.legend()
    plt.savefig("kmeans2D.png")
    plt.show()

def show_kmeans_3d(data, n_clusters=3):
    kmeans_kwargs = {
        "init": "random",
        "n_init": 10,
        "random_state": 1,
        }
    kmeans = KMeans(n_clusters=n_clusters, **kmeans_kwargs)
    clusters = kmeans.fit_predict(data)

    # Add cluster labels to the data
    data['Cluster'] = clusters
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    for cluster in range(n_clusters):
        cluster_data = data[data['Cluster'] == cluster]
        ax.scatter(cluster_data['rayon_top'], cluster_data['hauteur'], cluster_data['nutriments'], label=f'Cluster {cluster}')

    centers = kmeans.cluster_centers_
    ax.scatter(centers[:, 0], centers[:, 1], centers[:, 2], s=200, c='red', label='Centroids', marker='X')

    ax.set_xlabel('rayon_top')
    ax.set_ylabel('hauteur')
    ax.set_zlabel('nutriments')
    ax.set_title('3D Scatter Plot of Clusters')
    ax.legend()
    plt.savefig("kmeans3D.png")
    plt.show()

def show_kmeans_3d_2(data, n_clusters=3):
    kmeans_kwargs = {
        "init": "random",
        "n_init": 10,
        "random_state": 1,
        }
    kmeans = KMeans(n_clusters=n_clusters, **kmeans_kwargs)
    clusters = kmeans.fit_predict(data)

    # Add cluster labels to the data
    data['Cluster'] = clusters
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    for cluster in range(n_clusters):
        cluster_data = data[data['Cluster'] == cluster]
        ax.scatter(cluster_data['rayon_top'], cluster_data['coeff_stockage'], cluster_data['favorite_groth'], label=f'Cluster {cluster}')

    centers = kmeans.cluster_centers_
    ax.scatter(centers[:, 0], centers[:, 1], centers[:, 2], s=200, c='red', label='Centroids', marker='X')

    ax.set_xlabel('rayon_top')
    ax.set_ylabel('hauteur')
    ax.set_zlabel('nutriments')
    ax.set_title('3D Scatter Plot of Clusters')
    ax.legend()
    plt.savefig("kmeans3D.png")
    plt.show()

