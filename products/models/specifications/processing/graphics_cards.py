from products.models.specifications.base import BenchmarkSpecification


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
