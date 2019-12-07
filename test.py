if __name__ == "__main__":
    products = [
      [13000, 1080, 60, "IPS", 256, 76, 16, "SSD"],
      [16000, 2160, 60, "IPS", 128, 60, 8, "HDD"],
      [14000, 1440, 120, "TN", 512, 30, 16, "SSD"],
      [13000, 1080, 120, "TN", 256, 90, 8, "HDD"]
    ]

    pts = ["IPS", "TN"]
    sts = ["SSD", "HDD"]

    values = []
    for i in range(len(products)):
      for ind, val in enumerate(products[i]):
        if ind == 3:
          val = pts.index(val)
        elif ind == 7:
          val = sts.index(val)

        if (len(values) - 1) < ind:
          values.append([(i, val)])
        else:
          for i_i, l in enumerate(values[ind]):
            if type(l) == list:
              l = l[0]

            i_l, v_l = l
            if val > v_l:
              values[ind].insert(i_i, (i, val))
              break
            elif val == v_l:
              if type(values[ind][i_i]) == list:
                values[ind][i_i].append((i, val))
              else:
                values[ind][i_i] = [values[ind][i_i], (i, val)]
              break
            elif i_i == (len(values[ind]) - 1):
              values[ind].append([(i, val)])
              break

    prod_values = {}

    def save_value(i_val, i_inverse):
        i_val = str(i_val)

        if i_val in prod_values.keys():
            prod_values[i_val] = prod_values[i_val] + i_inverse
        else:
            prod_values[i_val] = i_inverse


    prices = values[0]
    values.pop(0)
    for t in values:
        for i, val in enumerate(t):
            i_inverse = len(t) - i
            if type(val) == list:
                for sub_val in val:
                    i_val, val_val = sub_val
                    save_value(i_val, i_inverse)
            else:
                i_val, val_val = val
                save_value(i_val, i_inverse)

    print(prod_values)

    def divide_by_price_value(i_val, price):
        i, price = price
        i = str(i)
        prod_values[i] = prod_values[i] / (price / 1000)

    for i, price in enumerate(prices):
        if type(price) == list:
            for sub_price in price:
                divide_by_price_value(i, sub_price)
        else:
            divide_by_price_value(i, price)


    print(prod_values)
