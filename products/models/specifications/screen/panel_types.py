from products.models.specifications.base import SpecifiedSpecification


class PanelType(SpecifiedSpecification):
    name = "Paneltyp"
    specified_values = [["tn"], ["va"], ["ips", "retina"], ["oled"]]

    def __str__(self):
        return "<PanelType %s>" % self.formatted_value
