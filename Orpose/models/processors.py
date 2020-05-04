from django.db import models
from collections import defaultdict
from bs4 import BeautifulSoup
import requests


class BaseProcessor(models.Model):
    score = models.DecimalField("score", max_digits=6, decimal_places=4, null=True)
    value = models.CharField("value", null=True, max_length=128)

    class Meta:
        abstract = True

    @staticmethod
    def get_soup(url):
        fp = requests.get(url)
        html_doc = fp.text
        return BeautifulSoup(html_doc, "html.parser")

    @staticmethod
    def collect_benchmarks():
        raise NotImplementedError

    @classmethod
    def find_existing(cls, value):
        return cls.objects.filter(value__icontains=value).first()

    @classmethod
    def rank(cls):
        benchmarks = sorted(cls.collect_benchmarks(), key=lambda tup: tup[1])
        min_score, max_score = benchmarks[0][1], benchmarks[-1][1]
        for name, score in benchmarks:
            specification, __ = cls.objects.get_or_create(value=name)
            specification.score = (score - min_score) / max_score * 5
            specification.save()


class Processor(BaseProcessor):
    name = "Processor"

    @staticmethod
    def collect_benchmarks():
        url = "https://browser.geekbench.com/processor-benchmarks"
        soup = BaseProcessor.get_soup(url)
        processor_scores = defaultdict()

        # Get all scores
        tables = soup.find_all("table")
        for table in tables:
            processors = table.find_all("tr")

            for i, processor in enumerate(processors):
                score = len(processors) - i
                name = processor.find("a")

                if name:
                    name = name.get_text().strip().replace("-", " ").lower()

                    if "iris " in name:
                        name = name.replace("iris ", "")

                    if name in processor_scores:
                        processor_scores[name].append(score)
                    else:
                        processor_scores[name] = [score]

        # Combine scores
        processors = []
        for name, scores in processor_scores.copy().items():
            average_score = scores[0] + scores[1]
            processor_package = (name, average_score)

            if len(processors) == 0:
                processors.append(processor_package)
            else:
                for i, processor in enumerate(processors):
                    saved_name, score = processor

                    if score < average_score or (
                            score == average_score and scores[0] > processor_scores[saved_name][0]
                    ):
                        processors.insert(i, processor_package)
                        break
                    elif i == (len(processors) - 1):
                        processors.append(processor_package)
                        break

        return processors


class GraphicsCard(BaseProcessor):
    name = "Grafikkort"

    @staticmethod
    def collect_benchmarks():
        url = "https://www.notebookcheck.net/Mobile-Graphics-Cards-Benchmark-List.844.0.html?type=&sort=&showClassDescription=1&deskornote=2&archive=1&perfrating=1&or=0&showBars=1&3dmark13_ice_gpu=1&3dmark13_cloud_gpu=1&3dmark13_fire_gpu=1&3dmark11_gpu=1&gpu_fullname=1&architecture=1&pixelshaders=1&vertexshaders=1&corespeed=1&boostspeed=1&memoryspeed=1&memorybus=1&memorytype=1"
        soup = BaseProcessor.get_soup(url)
        graphics_card_scores = []

        # Get all scores
        elements = soup.find_all("tr")
        for element in elements:
            # Get name and score elements
            score = element.find("span", {"class": "bl_med_val_5_0"})
            name = element.find("td", {"class": "fullname"})
            if score is None or name is None:
                continue

            score = score.get_text().replace("~", "")
            if score is not "":
                if score[-1] is "%":
                    score = score[:-3]
                score = float(score)

                name = name.get_text().strip().lower()
                if "1060-" in name:
                    name = name.replace("1060-", "1060 ")
                if "(" in name:
                    name = name.split(" (")[0]

                graphics_card_scores.append((name, score))

        return graphics_card_scores
