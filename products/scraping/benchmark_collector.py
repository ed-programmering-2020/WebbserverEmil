from products.models import Benchmark, SpecGroup
from collections import defaultdict
from bs4 import BeautifulSoup
import requests


class Collector:
    def __init__(self):
        self.collect_processors()
        self.collect_graphics_cards()

    def get_soup(self, url):
        fp = requests.get(url)
        html_doc = fp.text
        return BeautifulSoup(html_doc, "html.parser")

    def save_benchmarks(self, benchmarks, spec_group):
        for i, benchmark in enumerate(benchmarks):
            name, __ = benchmark
            score = len(benchmarks) - i

            try:
                benchmark = Benchmark.objects.get(name=name)
                benchmark.score = score
                benchmark.save()
            except Benchmark.DoesNotExist:
                Benchmark.objects.create(name=name, score=score, spec_group=spec_group)

    def collect_processors(self):
        url = "https://browser.geekbench.com/processor-benchmarks"
        soup = self.get_soup(url)
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

                    if score < average_score or (score == average_score and scores[0] > processor_scores[saved_name][0]):
                        processors.insert(i, processor_package)
                        break
                    elif i == (len(processors) - 1):
                        processors.append(processor_package)
                        break

        self.save_benchmarks(processors, SpecGroup.objects.get(name="Processor"))

    def collect_graphics_cards(self):
        url = "https://benchmarks.ul.com/compare/best-gpus"
        soup = self.get_soup(url)
        graphics_card_scores = []

        # Get all scores
        graphics_cards = soup.find("tbody").find_all("tr")
        for i, graphics_card in enumerate(graphics_cards):
            score = len(graphics_cards) - i
            name = graphics_card.find("a")

            if name:
                name = name.get_text().strip().lower()
                if "1060-" in name:
                    name.replace("1060-", "1060 ")

                graphics_card_package = (name, score)
                graphics_card_scores.append(graphics_card_package)

        self.save_benchmarks(graphics_card_scores, SpecGroup.objects.get(name="GraphicsCard"))
