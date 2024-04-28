class DistanceMetrics:
    MANHATTAN = L1 = "MANHATTAN"
    CLASSIC = L2 = "CLASSIC_DISTANCE"


class DiagramTypes:
    """supports only: violin, hist, boxplot."""
    VIOLIN = "violin"
    HIST = "hist"
    BOXPLOT = "boxplot"

    @staticmethod
    def contains(value: str) -> bool:
        return value in (
            DiagramTypes.VIOLIN,
            DiagramTypes.HIST,
            DiagramTypes.BOXPLOT
        )


DEFAULT_FILE_SAVE_NAME = "visualisation_result.png"
