class LaptopWeights:
    def __init__(self):
        self.usages = {
            "general": {
                "battery time": 1,
                "weight": 1,
                "processor": 1,
                "graphics card": 1,
                "memory": 1,
                "disk type": 1,
                "storage size": 1,
                "resolution": 1,
                "panel type": 1,
                "refresh rate": 1
            },
            "gaming": {
                "battery time": 1,
                "weight": 1,
                "processor": 1,
                "graphics card": 1,
                "memory": 1,
                "disk type": 1,
                "storage size": 1,
                "resolution": 1,
                "panel type": 1,
                "refresh rate": 1
            }
        }
        self.priority_groups = {
            "weight": ["weight"],
            "battery": ["battery time"],
            "performance": ["processor", "graphics card", "memory", "disk type"],
            "storage": ["storage size"],
            "screen": ["resolution", "panel type", "refresh rate"]
        }
