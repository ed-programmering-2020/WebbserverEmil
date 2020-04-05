from products.models.specifications.base import SpecifiedSpecification


class StorageType(SpecifiedSpecification):
    name = "Hårddisktyp"
    specified_values = [["emmc"], ["hdd"], ["ssd"]]

    def __str__(self):
        return "<StorageType %s>" % self.formatted_value
