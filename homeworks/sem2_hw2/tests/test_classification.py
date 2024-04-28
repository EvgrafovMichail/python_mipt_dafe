import sklearn.datasets as skd
from visualisation.visualize import visualize_classification


def test_vis_class():
    points, labels = skd.make_classification(
        n_samples=400,
        n_features=2,
        n_classes=4,
        n_clusters_per_class=1,
        n_redundant=0
    )

    visualize_classification(points, labels, ["red", "green", "blue", "yellow"])
