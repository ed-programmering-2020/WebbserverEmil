from .base import BenchmarkSpecification
from collections import defaultdict


class GraphicsCard(BenchmarkSpecification):
    name = "Grafikkort"

    @staticmethod
    def collect_benchmarks():
        url = "https://www.notebookcheck.net/Mobile-Graphics-Cards-Benchmark-List.844.0.html?type=&sort=&showClassDescription=1&deskornote=2&archive=1&perfrating=1&or=0&showBars=1&3dmark13_ice_gpu=1&3dmark13_cloud_gpu=1&3dmark13_fire_gpu=1&3dmark11_gpu=1&gpu_fullname=1&architecture=1&pixelshaders=1&vertexshaders=1&corespeed=1&boostspeed=1&memoryspeed=1&memorybus=1&memorytype=1"
        soup = BenchmarkSpecification.get_soup(url)
        graphics_card_scores = []

        # Get all scores
        elements = soup.find_all("tr")
        for element in elements:
            # Get name and score elements
            score = element.find("span", {"class": "gg_pos"})
            name = element.find("td", {"class": "fullname"})
            if score is None or name is None:
                continue

            # Format values
            score = int(score.get_text())
            name = name.get_text().strip().lower()
            if "1060-" in name:
                name = name.replace("1060-", "1060 ")
            if "(" in name:
                name = name.split(" (")[0]

            graphics_card_scores.append((name, score))

        return graphics_card_scores

    def __str__(self):
        return "<GraphicsCard %s>" % self.value


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
