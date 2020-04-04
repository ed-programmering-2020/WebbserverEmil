from products.models.specifications.base import SpecifiedSpecification


class StorageType(SpecifiedSpecification):
    name = "Hårddisktyp"
    types = ["emmc", "hdd", "ssd"]

    def __str__(self):
        return "<StorageType %s>" % self.value
