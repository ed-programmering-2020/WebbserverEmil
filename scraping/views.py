from rest_framework.response import Response
from rest_framework import generics


class WebsitesAPI(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        website = Website.query.filter_by(has_run=False).first()
        if not website:
            websites = Website.query.all()
            for site in websites:
                site.has_run = False

            website = websites[0]
        website.has_run = True

        return Response({})


class ProductsAPI(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):

        # Website data
        website = request.data.get("website")
        id = request.data.get("id")

        # Product data
        name = request.data.get("title")
        price = re.sub("\D", "", str(request.data.get("price")))
        image = request.data.get("image")
        specs = request.data.get("specifications")
        category = request.data.get("category")

        # Find/Create product
        product = Product.query.filter_by(name=name).first()
        if product == None:
            word_list = name.split(" ")
            products = Product.query.all()

            best_ratio = 0
            best_product = 0
            group_list = []
            for product in products:
                nme = product.name
                prod_word_list = nme.split(" ")
                ratio = SequenceMatcher(lambda x: x not in "1234567890", name, nme).ratio()
                ratio_min = 0.95 if len(nme) >= 10 else 0.90

                if ratio > best_ratio and ratio >= ratio_min:
                    best_ratio = ratio
                    best_product = product

                matching_words = []
                for word in word_list:
                    for prod_word in prod_word_list:
                        if prod_word == word: matching_words.append(word)

                group_words = []
                for i in range(1, len(matching_words)):
                    for n in range(len(matching_words) - i + 1):
                        word = " ".join(matching_words[n:i + n])
                        group_words.append(word)

                group_models = []
                for word in group_words:
                    group = NameGroup.query.filter_by(name=word).first()
                    if group == None: group = NameGroup(name=word)
                    if product not in group.products: group.products.append(product)

                    group_models.append(group)

                rnge = len(group_models)
                for i in range(rnge - 1):
                    for n in range(1 + i, rnge):
                        group_models[i].name_groups.append(group_models[n])
                        group_models[n].name_groups.append(group_models[i])

                group_list.extend(group_models)

            if best_ratio == 0:
                product = Product(name=name)
            else:
                product = best_product

            for group in group_list:

                if product not in group.products: group.products.append(product)

            product.specifications = specs

            category_name = ""
            if "category" in request.args:
                category_name = request.args.get("category")

            matches = 0
            best_matches = 0
            best_collection = 0

            collection = Collection.query.filter_by(name=category_name).first()
            print(collection)
            if collection == None:

                collections = Collection.query.all()
                for col in collections:
                    prods = random.shuffle(col.products)

                    if prods != None:
                        if len(prods) >= 10:
                            rnge = 10
                        else:
                            rnge = len(prods)

                        for i in range(rnge):
                            prod = prods[i]

                            amount_of_specs = len(specs)

                            if len(prod.specifications) < amount_of_specs:
                                amount_of_specs = len(prod.specifications)

                            for spec_key, spec_value in prod.specifications.items():
                                best_ratio = 0

                                for s_key, s_value in specs.items():
                                    ratio = SequenceMatcher(lambda x: x not in "1234567890", spec_key, s_key).ratio()

                                    if ratio > best_ratio and ratio >= 0.95:
                                        best_ratio = ratio

                                if best_ratio != 0:
                                    matches = matches + 1

                            if amount_of_specs >= 10:
                                match_ratio = 0.8
                            else:
                                match_ratio = 0.75

                            if matches > best_matches and matches >= (amount_of_specs * match_ratio):
                                best_collection = col

                            matches = 0

                if best_collection != 0:
                    collection = best_collection
                else:
                    collection = Collection()

                product.collection = collection

            if category_name != None and collection.name != None:
                collection.name = category_name

            print(collection)

        if "price" in request.args:
            product.websites = (website, price)
        else:
            product.websites = (website, 0)

        print(product.websites)

        return Response({})
