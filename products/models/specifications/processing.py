from .base import BaseSpecification, BenchmarkSpecification
from collections import defaultdict


class GraphicsCard(BaseSpecification, BenchmarkSpecification):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = self.process_number(value)

    @staticmethod
    def collect_benchmarks():
        url = "https://benchmarks.ul.com/compare/best-gpus"
        soup = super().get_soup(url)
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

        super().save_benchmarks(graphics_card_scores, GraphicsCard)

    def __str__(self):
        return "<GraphicsCard %s>" % self._value


class Processor(BaseSpecification, BenchmarkSpecification):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = self.process_number(value)

    @staticmethod
    def collect_benchmarks():
        url = "https://browser.geekbench.com/processor-benchmarks"
        soup = super().get_soup(url)
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

                    if score < average_score or (
                            score == average_score and scores[0] > processor_scores[saved_name][0]
                    ):
                        processors.insert(i, processor_package)
                        break
                    elif i == (len(processors) - 1):
                        processors.append(processor_package)
                        break

        super().save_benchmarks(processors, Processor)

    def __str__(self):
        return "<Processor %s>" % self._value
