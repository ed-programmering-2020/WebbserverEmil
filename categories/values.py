from categories import specs


class LaptopValues:
    @staticmethod
    def get_values(self):
        return {
            "battery capacity": [],
            "processor": specs.processors,
            "graphics card": specs.graphics_cards,
            "memory": [],
            "disk type": specs.disk_types,
            "storage size": [],
            "resolution": [],
            "panel type": specs.panel_types,
            "refresh rate": []
        }

    @staticmethod
    def get_biases(self):
        return {
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

    @staticmethod
    def get_priority_groups(self):
        return {
            "battery": ["battery capacity"],
            "performance": ["processor", "graphics card", "memory", "disk type"],
            "storage": ["storage size"],
            "screen": ["resolution", "panel type", "refresh rate"]
        }