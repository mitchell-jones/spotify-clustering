# Spotify Clustering
Applying K-means clustering (PCA and no-PCA) to my Spotify Liked Songs to create new playlists

Steps:
- Authenticate with Spotify API
- Download data of all of my liked songs, with audio features (provided by Spotify)
- Fit k-means clustering and find optimal number of clusters using intertia
- Visualize cluster means
- Use custom gridSearch to explore PCA & Inertia
- Send a cluster to new playlist for user
