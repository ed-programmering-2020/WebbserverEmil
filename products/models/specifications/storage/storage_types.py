from products.models.specifications.base import SpecifiedSpecification


class StorageType(SpecifiedSpecification):
    name = "Hårddisktyp"
    specified_values = [["emmc"], ["hdd"], ["ssd"]]
