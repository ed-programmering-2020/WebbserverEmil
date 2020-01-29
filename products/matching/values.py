from products.matching import spec_evaluators


class LaptopValues:
    def __init__(self):
        self.values = {
            "battery capacity": [],
            "processor": spec_evaluators.processors,
            "graphics card": spec_evaluators.graphics_cards,
            "memory": [],
            "disk type": spec_evaluators.disk_types,
            "storage size": [],
            "resolution": [],
            "panel type": spec_evaluators.panel_types,
            "refresh rate": []
        }
        self.biases = {
            "general": {
                "battery capacity": 1,
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
                "battery capacity": 1,
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
            "battery": ["battery capacity"],
            "performance": ["processor", "graphics card", "memory", "disk type"],
            "storage": ["storage size"],
            "screen": ["resolution", "panel type", "refresh rate"]
        }