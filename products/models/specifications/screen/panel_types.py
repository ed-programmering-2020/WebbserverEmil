from products.models.specifications.base import SpecifiedSpecification


class PanelType(SpecifiedSpecification):
    name = "Paneltyp"
    specified_values = [["tn"], ["va"], ["ips", "retina"], ["oled"]]
