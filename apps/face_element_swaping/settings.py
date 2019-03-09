from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors

PERCENT_OF_NEAREST_NEIGHBOURS = 0.01
CLASSIFIERS = {

    "kNN": KNeighborsClassifier,
    "NearestNeighbors": NearestNeighbors
}
DEFAULT_CLASSIFIER = CLASSIFIERS["NearestNeighbors"]