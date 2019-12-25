class LaptopCustomizer:
    sub_header = "Hitta den bästa bärbara datorn efter dina krav och preferenser"

    customization_settings = [
        {
            "type": "select",
            "name": "usage",
            "title": "Välj användningsområde för din laptop",
            "options": [
                {
                    "title": "Allmänt",
                    "name": "general"
                }, {
                    "title": "Gaming",
                    "name": "gaming"
                }
            ]
        }, {
            "type": "slider",
            "name": "price",
            "title": "Välj budget för laptopen (kr)",
            "step": 100,
            "min": 0,
            "max": 20000,
        }, {
            "type": "slider",
            "name": "size",
            "step": 1,
            "title": "Vilken skärmstorlek ska laptopen ha? (tum)",
            "min": 10,
            "max": 18
        }, {
            "type": "priorities",
            "valuePoints": 20,
            "title": "Vad är viktigast för din laptop? (Höj/sänk)",
            "priorities": [
                {
                    "title": "Batteri",
                    "name": "battery"
                }, {
                    "title": "Prestanda",
                    "name": "performance"
                }, {
                    "title": "Utrymme",
                    "name": "storage"
                }, {
                    "title": "Skärm",
                    "name": "screen"
                }
            ]
        }
    ]
