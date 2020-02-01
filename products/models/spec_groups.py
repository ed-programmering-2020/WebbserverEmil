from django.contrib.contenttypes.models import ContentType
from django.db import models
import re


class SpecGroup(models.Model):
    name = models.CharField("name", max_length=32)
    standard = models.CharField("standard", max_length=32, null=True)
    rank_group = models.BooleanField("rank group", default=False)
    content_type = models.ForeignKey(ContentType, editable=False, on_delete=models.SET_NULL, null=True)

    def process_number(self, value):
        value = value.split(" ")[0]
        value = re.sub("[^0-9]", "", value)
        return int(value)

    def process_text(self, value):
        return value.lower()

    def get_rank(self, value):
        for i, panel_type in enumerate(self.types):
            if panel_type in value:
                return i
        return 0

    def save(self, *args, **kwargs):
        if not self.content_type:
            self.content_type = ContentType.objects.get_for_model(self.__class__)
            super(SpecGroup, self).save(*args, **kwargs)

    def as_inherited_model(self):
        content_type = self.content_type
        model = content_type.model_class()
        return model.objects.first()

    def __str__(self):
        return "<SpecGroup %s>" % self.name


class RefreshRate(SpecGroup):
    @classmethod
    def create(cls):
        return cls(name="RefreshRate", standard="60", rank_group=True).save()

    def process_value(self, value):
        if not value:
            return int(self.standard)
        else:
            return self.process_number(value)

    def is_bigger(self, first, second):
        return first > second

    def is_equal(self, first, second):
        return first == second


class PanelType(SpecGroup):
    types = ["ips", "va", "tn"]

    @classmethod
    def create(cls):
        return cls(name="PanelType", standard="tn", rank_group=True).save()

    def process_value(self, value):
        if not value:
            return self.standard
        else:
            return self.process_text(value)

    def is_bigger(self, first, second):
        first, second = self.get_rank(first), self.get_rank(second)
        return first > second

    def is_equal(self, first, second):
        first, second = self.get_rank(first), self.get_rank(second)
        return first == second


class ScreenSize(SpecGroup):
    @classmethod
    def create(cls):
        return cls(name="ScreenSize", rank_group=False).save()

    def process_value(self, value):
        if not value:
            return None
        else:
            return self.process_number(value)


processors = [
    '9980HK',
    '9880H',
    '8950HK',
    '2186M',
    '2276M',
    '2145',
    '9850H',
    '9750H',
    '2176M',
    '8850H',
    '8750H',
    '8809G',
    '9400H',
    '10710U',
    '1535M',
    '8400H',
    '8709G',
    '8706G',
    '8705G',
    '7920HQ',
    '9300H',
    '1505M',
    '8300H',
    '1575M',
    '4940MX',
    '7820HQ',
    '7820HK',
    '6920HQ',
    '1545M',
    '5950HQ',
    '4930MX',
    '1535M',
    '6970HQ',
    '7700HQ',
    '8305G',
    '1515M',
    '1505M',
    '6870HQ',
    '4980HQ',
    '4910MQ',
    '8559U',
    '1068G7',
    '8557U',
    '5850HQ',
    '3940XM',
    '8269U',
    '5700HQ',
    '5750HQ',
    '6820HK',
    '8279U',
    '6820HQ',
    '6770HQ',
    '8259U',
    '8257U',
    '4900MQ',
    '4960HQ',
    '6700HQ',
    '4810MQ',
    '4870HQ',
    '3750H',
    '3700U',
    '3780U',
    'PRO 3700U',
    '8650U',
    '3920XM',
    '4800MQ',
    '8665U',
    '4950HQ',
    '4860HQ',
    '4720HQ',
    '3840QM',
    '4850HQ',
    '4710HQ',
    '4710MQ',
    '1065G7',
    '8565U',
    '4770HQ',
    '1035G7',
    '1035G4',
    '3820QM',
    '7440HQ',
    '1035G1',
    '1060G7',
    '1034G1',
    '8365U',
    '10510U',
    '3740QM',
    '3720QM',
    '4700HQ',
    '4700MQ',
    '4760HQ',
    '4722HQ',
    '8265U',
    '10210U',
    '2800H',
    '2960XM',
    '2700U',
    'PRO 2700U',
    '3550H',
    '3500U',
    '3580U',
    'PRO 3500U',
    '7567U',
    '8550U',
    '2600H',
    '1030G7',
    '1030G4',
    '1005G1',
    '7660U',
    '7600U',
    '4712HQ',
    '4712MQ',
    '4750HQ',
    '3635QM',
    '3630QM',
    '4702HQ',
    '4702MQ',
    '2860QM',
    '2920XM',
    '3615QM',
    '3610QM',
    '7300HQ',
    '6440HQ',
    '3632QM',
    '6350HQ',
    '6300HQ',
    '8350U',
    '1000G4',
    '1000G1',
    '8250U',
    '2500U',
    'PRO 2500U',
    '8100H',
    '2760QM',
    '7287U',
    '10110U',
    'SQ1'
    '7560U',
    '8cx',
    '8145U',
    '2820QM',
    '3612QM',
    '2720QM',
    '2675QM',
    '2670QM',
    '6567U',
    '7360U',
    '7267U',
    '3300U',
    'PRO 3300U',
    '2300U',
    'PRO 2300U',
    '7500U',
    '8130U',
    '5350H',
    '7300U',
    '2635QM',
    '2630QM',
    '6287U',
    '5557U',
    '4610M',
    '4600M',
    '4340M',
    '5287U',
    '7260U',
    '6267U',
    '4578U',
    '4210H',
    '4330M',
    '3540M',
    '4200H',
    '4558U',
    '8121U',
    '5257U',
    '4308U',
    '4310M',
    '6600U',
    '6650U',
    '6560U',
    '7200U',
    '4300M',
    '7100H',
    '3520M',
    '6500U',
    '5600U',
    '5650U',
    '6360U',
    '4210M',
    '6300U',
    '4288U',
    '4278U',
    '3380M',
    '3360M',
    '4200M',
    '3340M',
    '2640M',
    '5500U',
    '5550U',
    '6260U',
    '3320M',
    '4258U',
    '3230M',
    '10510Y',
    '2620M',
    '4600U',
    '4650U',
    '7167U',
    '8109U',
    '6198DU',
    '6200U',
    '10310Y',
    '10210Y',
    '7130U',
    '6167U',
    '6100H',
    '5300U',
    '3687U',
    '5350U',
    '4510U',
    '3210M',
    '8500Y',
    '2540M',
    '10110Y',
    '3667U',
    '4500U',
    '4550U',
    '7Y75',
    '8210Y',
    '8200Y',
    '4310U',
    '4360U',
    '9830P',
    '3537U',
    '3200U',
    '2200U',
    'PRO 2200U',
    '5200U',
    '5250U',
    '4300U',
    '4350U',
    '9830B',
    '2520M',
    '5157U',
    '8100Y',
    '7Y57',
    '7Y54',
    '6405U',
    '6157U',
    '7100U',
    '300U',
    '6100U',
    '4110M',
    '7Y32',
    'N5030',
    '9800P',
    '9800B',
    '2450M',
    '3517U',
    '4100M',
    '2435M',
    '2430M',
    '5405U',
    '4415U',
    '4000M',
    '4100E',
    '3130M',
    '2415M',
    '2410M',
    '7Y30',
    '3437U',
    '9720P',
    '9700P',
    '8800P',
    '8800B',
    '4210U',
    '4260U',
    '9620P',
    '3965U',
    '3120M',
    '3427U',
    '4402E',
    '6Y75',
    '4200U',
    '4250U',
    '5020U',
    '7020U',
    '9600P',
    '9600B',
    '3110M',
    '7600P',
    '4405U',
    '2649M',
    '5010U',
    '4417U',
    '5015U',
    '6006U',
    '5205U',
    '2370M',
    '5005U',
    '2350M',
    '2348M',
    '3337U',
    '6Y57',
    '6Y54',
    '8700P',
    '8700B',
    '4610Y',
    '2629M',
    '2677M',
    '7400P',
    '3560M',
    '2330M',
    '2328M',
    '2030M',
    '3550M',
    '3317U',
    '8600P',
    '8600B',
    '7200P',
    '5750M',
    '5757M',
    '2637M',
    '2657M',
    '3689Y',
    '2020M',
    '4158U',
    '3825U',
    '4120U',
    '2970M',
    '4300Y',
    '4302Y',
    'B980',
    '5Y71',
    '4030U',
    '4025U',
    '4205U',
    '3865U',
    '4600M',
    '4657M',
    '2312M',
    '2310M',
    '2308M',
    '2557M',
    '5745M',
    '5550M',
    '5557M',
    '6Y30',
    '5Y51',
    '5Y70',
    'N5000',
    '7500',
    '850',
    '7350B',
    '1020E',
    '5Y31',
    'N4120',
    'M-5Y10c',
    '5Y10a',
    '5Y10',
    '2617M',
    '3439Y',
    '9425',
    '9420e',
    '9420',
    '4202Y',
    '4220Y',
    '4100U',
    '4425Y',
    '3227U',
    '9410',
    '4210Y',
    '2467M',
    '3339Y',
    '4010U',
    '4005U',
    '4415Y',
    '3217U',
    '7300',
    '7150B',
    '4405Y',
    '4200Y',
    'B970',
    '3765U',
    'N4200',
    '2950M',
    '7410',
    '7100',
    '4102E',
    '4030Y',
    '835',
    '3550MX',
    'N4100',
    '1020M',
    '4410Y',
    '3965Y',
    'B960',
    '3805U',
    '4020Y',
    '4012Y',
    '6410',
    '7310',
    '6310',
    '3755U',
    '3215U',
    'B950',
    '3530MX',
    '2537M',
    '3510MX',
    '2127U',
    'B940',
    '1005M',
    '7210',
    '3430MX',
    '3558U',
    '9225',
    '9220',
    '9220C',
    '3556U',
    '2117U',
    '1000M',
    '1037U',
    '2981U',
    '2980U',
    '3520M',
    '9210',
    '4655M',
    '4500M',
    '4557M',
    '3410MX',
    '3500M',
    '3420M',
    '5545M',
    '3400M',
    'N4020',
    '4555M',
    'B840',
    '5350M',
    '5357M',
    'N4000',
    'N3540',
    '5200',
    'N3450',
    'N3710',
    'Z8750',
    'B830',
    '3330MX',
    '5150M',
    '4400M',
    'J2900',
    '4300M',
    'N3530',
    '1017U',
    '3205U',
    'B820',
    'N3700',
    'J2850',
    'N3520',
    'J1900',
    'Z8700',
    '9120',
    '9120C',
    '4010Y',
    '9010',
    '7110',
    '6210',
    '8500P',
    '8500B',
    'Z8550',
    'Z3795',
    'Z3785',
    'Z3775',
    'Z3775D',
    'Z3770',
    'E3950',
    'Z8500',
    'N2940',
    'N3160',
    '2957U',
    '2955U',
    'J3355',
    'N3350',
    '1007U',
    'N3150',
    'N2930',
    'J1850',
    'N3510',
    'B815',
    'B810',
    'N2920',
    '3229Y',
    '2377M',
    '2375M',
    '2367M',
    '2365M',
    '5100',
    '5050',
    '5000',
    '6110',
    'E3845',
    '6700T',
    '3310MX',
    '3320M',
    'Z8350',
    'Z8300',
    '997',
    '1047UE',
    '3800',
    '3000M',
    '987',
    '887',
    'B800',
    '2357M',
    'E2 9000',
    'A4 3300M',
    'A4 3305M',
    '7050B',
    'A6 7000',
    'AMD A6-5345M',
    'J1800',
]

graphics_cards = [
    "rtx 6000",
    "rtx 5000",
    "rtx 5000 max-q"
    "rtx 2080",
    "gtx 1080 sli",
    "gtx 1070 sli",
    "rtx 2080 max-q",
    "rtx 2070",
    "gtx 1080",
    "rtx 4000",
    "rtx 4000 max-q",
    "rtx 2070 max-q",
    "rtx 3000",
    "rtx 3000 max-q",
    "rtx 2060",
    "p5200",
    "gtx 1080 max-q",
    "gtx 1070",
    "p4200",
    "p5000",
    "gtx 1660 ti",
    "gtx 1070 max-q",
    "gtx 1660 ti max-q",
    "p5000 max-q",
    "gtx 980",
    "m5500",
    "p4000",
    "t2000",
    "t2000 max-q",
    "gtx 1060",
    "rx 5000m",
    "pro 5500m",
    "p4000 max-q",
    "P3200",

    "RX 580X",

    "RX 580",

    "Vega Mobile",

    "Pro 5300M",

    "RX 5300M",

    "Quadro P3000",

    "GTX 1650",

    "GTX 1060 Max-Q",

    "P3000 Max-Q",

    "RX 480",

    "WX 7100",

    "RX 570X",

    "RX 570",

    "RX 470",

    "GTX 1650 Max-Q",

    "Quadro T1000",

    "T1000 Max-Q",

    "GTX 980M",

    "Vega M GH",

    "Pro Vega 20",

    "Quadro M5000M",

    "GTX 1050 Ti",

    "P2000",

    "P2000 Max-Q",

    "M4000M",

    "GTX 970M",

    "R9 M395X",

    "GTX 1050 Ti Max-Q",

    "Vega M GL",

    "Pro Vega 16",

    "R9 M485",

    "R9 M295X",

    "R9 M390",

    "M3000M",

    "GTX 1050",

    "Xe DG1",

    "FirePro W7170M",

    "R9 M395",

    "GTX 880M",

    "GTX 1050 Max-Q",

    "K5100M",

    "P1000",

    "WX 4150",

    "GTX 965M",

    "RX 560X",

    "RX 560",

    "M2200",

    "RX 460",

    "R9 M390",

    "FirePro M6100",

    "Pro 560X",

    "Pro 560",

    "Pro 460",

    "WX 4130",

    "GTX 960M",

    "Quadro M1200",

    "Quadro P620",

    "RX 550X",

    "RX 550",

    "RX 640",

    "WX 3200",

    "Pro 555X",

    "Pro 555",

    "Pro 455",

    "Radeon 630",

    "P600",

    "MX250",

    "MX150",

    "M2000M",

    "K5000M",

    "K4100M",

    "RX 540X",

    "WX 2100",

    "RX 540",

    "WX 3100",

    "GTX 860M",

    "GTX 950M",

    "Pro 450",

    "R9 M470X",

    "R9 M385X",

    "P520",

    "GTX 850M",

    "M1000M",

    "M620",

    "945M",

    "K4000M",

    "P500",

    "Graphics G7",

    "Vega 10",

    "Graphics P580",

    "Graphics 580",

    "R9 M470",

    "K3100M",

    "FirePro W5170M",

    "R9 M370X",

    "Vega 9",

    "940M",

    "FirePro W5130M",

    "K3000M",

    "FirePro M6000",

    "FirePro M5100",

    "MX230",

    "K2100M",

    "GT 755M ",

    "845M",

    "R9 M265",

    "R7 M465",

    "FirePro W4170M",

    "GT 750M",

    "Graphics 6200",

    "MX130",

    "940MX",

    "M520",

    "K1100M",

    "Vega 8",

    "940M",

    "Graphics G4",

    "930MX",

    "A12X Bionic",

    "M600M",

    "FirePro W4190M",

    "R9 M375",

    "Graphics 655",

    "M445",

    "M500M",

    "840M",

    "GT 745M",

    "Graphics 5200",

    "GT 740M",

    "Graphics 650",

    "930M",

    "Graphics 550",

    "Radeon 530",

    "Radeon 625",

    "Graphics 645",

    "A13 Bionic",

    "830M",

    "MX110",

    "Graphics 640",

    "920MX",

    "Graphics 540",

    "A12 Bionic",

    "A11 Bionic",

    "Imagination A10X",

    "K2000M",

    "GT 735M",

    "825M",

    "FirePro M4000",

    "GT 730M",

    "M4100",

    "R7 M460",

    "R7 M360",

    "920M",

    "R8 M445DX",

    "Radeon 620",

    "R7 M440",

    "R7 M340",

    "Radeon 520",

    "Radeon 610",

    "Vega 6",

    "Graphics 530",

    "Graphics P530",

    "Tegra X1",

    "Graphics 620",

    "Graphics 620",

    "Adreno 685",

    "Adreno 680",

    "Graphics 5600",

    "R6 M255DX",

    "K1000M",

    "HD 8650G",

    "R5 M330",

    "R5 M430",

    "R5 M255",

    "Vega 3",

    "910M",

    "820M",

    "Graphics 520",

    "Graphics 6100",

    "GT 720M",

    "Adreno 650",

    "R5 M320",

    "R5 M315",

    "R5 M420",

    "Imagination A10",

    "Graphics 6000",

    "K610M",

    "Graphics 5100",

    "Graphics 4600",

    "Graphics 5500",

    "Mali-G76",

    "Adreno 640",

    "Adreno 630",

    "Mali-G76",

    "Adreno 540",

    "Mali-G72",

    "Mali-G71",

    "Graphics 617",

    "Graphics 615",

    "710M",

    "7660G",

    "Graphics 5000",

    "HD 8550G",

    "Adreno 530",

    "GXA6850",

    "ULP K1",

    "Imagination A9",

    "GT7600",

    "Mali-T880",

    "Mali-G76",

    "Graphics 515",

    "Graphics 4400",

    "Graphics 610",

    "HD 8610G",

    "Graphics 510",

    "Graphics 605",

    "Graphics 505",

    "Graphics 5300",

    "Graphics 4000",

    "Mali-T760",

    "Mali-G71",

    "Adreno 430",

    "Graphics 4200",

    "HD 8450G",

    "HD 8400",

    "Mali-G72",

    "Mali-T880",

    "HD 8350G",

    "HD 8330",

    "Graphics 600",

    "Graphics 500",

    "Mali-T760",

    "Mali-T880",

    "Graphics 405",

    "Graphics 400",

    "GX6450",

    "Adreno 420",

    "Adreno 418",

    "Mali-G51",

    "GE8320",

    "GE8300",

    "GE8100",

    "Adreno 618",

    "Adreno 616",

    "HD 8280",

    "HD 8240",

    "HD 8250",

    "HD 8210",

    "Adreno 612",

    "Adreno 610",

    "Adreno 512",

    "Adreno 510",

    "Adreno 330",

    "G6430",

    "GX6250",

    "G6400",

    "Mali-T628",

    "Mali-T760",

    "HD 7340",

    "HD 7310",

    "HD 8180",

    "HD 7290",

    "SGX554MP",

    "Mali-T628",

    "Adreno 508",

    "Adreno 506",

    "Adreno 505",

    "Adreno 504",

    "Mali-T860",

    "Mali-T83",

    "Mali-T604",

    "Tegra 4",

    "G6200",

    "Adreno 405",

    "Mali-T830",

    "GE8322",

    "SGX543M",

    "Mali-T624",

    "Adreno 320",

    "Mali-T760",

    "Mali-T72",

    "Mali-450",

    "Mali-T830",

    "SGX543MP",

    "SGX543MP2",

    "SGX545",

    "SGX544MP2",

    "Mali-T720",

    "SGX544",

    "Adreno 308",

    "Adreno 306",

    "Adreno 305",

    "Adreno 304",

    "Mali-T720",

    "GC7000UL",

    "Adreno 302",

    "Adreno 225",

    "GC4000",

    "Mali-400",

    "Adreno 220",

    "GC1000+",

    "Mali-400",

    "Mali-400",

    "Tegra 2",

    "SGX540",

    "Adreno 205",

    "Adreno 203",

    "GC800",

    "SGX535",

    "SGX531",

    "SGX530",

    "Adreno 200",

    "Mali-200",
]

disk_types = [
    "ssd",
    "hdd"
]
