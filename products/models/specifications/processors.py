from products.models.specifications.base import BenchmarkSpecification
from collections import defaultdict


class Processor(BenchmarkSpecification):
    name = "Processor"



    @staticmethod
    def collect_benchmarks():
        url = "https://browser.geekbench.com/processor-benchmarks"
        soup = BenchmarkSpecification.get_soup(url)
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

    def __str__(self):
        return "<Processor %s>" % self.value
