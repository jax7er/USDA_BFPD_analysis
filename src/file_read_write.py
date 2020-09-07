import pickle
from os import mkdir, path


# data from USDA Branded Food Products Database (BFPD), August 2018
data_folder = "data"

raw_data_folder = path.join(data_folder, "raw")
raw_ext = "csv"
raw_foods_file_name = path.join(raw_data_folder, "Products") + f".{raw_ext}"
raw_nutrients_file_name = path.join(raw_data_folder, "Nutrients") + f".{raw_ext}"
raw_derivations_file_name = path.join(raw_data_folder, "Derivation_Code_Description") + f".{raw_ext}"

processed_data_folder = path.join(data_folder, "processed")
processed_ext = "pkl"
foods_file_name = path.join(processed_data_folder, "foods") + f".{processed_ext}"
nutrients_file_name = path.join(processed_data_folder, "nutrients") + f".{processed_ext}"
derivations_file_name = path.join(processed_data_folder, "derivations") + f".{processed_ext}"


'''
foods: {
    id1: {
        name: "...",
	    ingredients:{
            main: ["ing1", ...],
            ...: [...],
            ...
	    },
        nutrients: {
            id1: "...",
            ...
        }
    },
    id2: {...},
    ...
}

nutrients: {
    id1: "name1",
    ...
}
'''


def read_raw():
    def open_raw(n):
        return open(n, "r", encoding="utf-8")

    foods_dict = {}
    derivations_dict = {}
    nutrients_dict = {}

    with open_raw(raw_foods_file_name) as read_f:
        header = read_f.readline()

        for i, line in enumerate(read_f):
            if not line or '"' not in line:
                continue

            line_split = [x.strip() for x in line.lower().split('"')[1::2]]
            
            food_ndb_num = line_split[0]
            food_name = line_split[1]
            food_ingredients = line_split[7]

            ingredients_names = []
            ingredients_lists = []
            
            for ing_split in food_ingredients.replace(".", "").split(":"):
                if "ingredients" in ing_split:
                    pre_ingredients = ing_split.split("ingredients")[0]
                    
                    if "," not in pre_ingredients:
                        ingredients_names.append(pre_ingredients.strip())
                    else:
                        last_comma = pre_ingredients.rfind(",")

                        ingredients_names.append(pre_ingredients[last_comma + 1:].strip())
                        ingredients_lists.append(pre_ingredients[:last_comma].strip())
                elif "%" in ing_split:
                    last_comma = ing_split.rfind(",")

                    ingredients_names.append(ing_split[last_comma + 1:].strip())
                    ingredients_lists.append(ing_split[:last_comma].strip())
                else:
                    ingredients_lists.append(ing_split)

                if len(ingredients_lists) > len(ingredients_names):
                    ingredients_names.append("main")

            for list_i, list_str in enumerate(ingredients_lists):
                if "(" in list_str:
                    list_str_formatted = list_str\
                        .replace("*", "")\
                        .replace("(", "),")\
                        .replace("),", "!")\
                        .replace(")", "")

                    list_split = [s.strip() for s in list_str_formatted.split("!")]

                    whole_ingredients = [[item.strip() for item in list_csv.split(",")]
                                         for list_csv in list_split[0::2]]
                    partial_ingredients = [[item.strip() for item in list_csv.split(",")]
                                           for list_csv in list_split[1::2]]

                    ingredients_and_parts = {}

                    for ing_list_i, part_ing_list in enumerate(partial_ingredients):
                        whole_ing_name = whole_ingredients[ing_list_i][-1]

                        ingredients_and_parts[whole_ing_name] = \
                            part_ing_list \
                            if len(part_ing_list) > 1 \
                            else part_ing_list[0]

                        del whole_ingredients[ing_list_i][-1]

                    main_ingredients = [item for ingr_list in whole_ingredients for item in ingr_list]

                    if main_ingredients:
                        ingredients_and_parts["main"] = main_ingredients

                    ingredients_lists[list_i] = ingredients_and_parts
                else:
                    list_split = list_str.split(",")

                    if len(list_split) > 1:
                        ingredients_lists[list_i] = [item.strip() for item in list_split]
                    elif len(list_split) == 1:
                        ingredients_lists[list_i] = list_str.strip()

            foods_dict[food_ndb_num] = {"name": food_name}
            
            if len(ingredients_lists) > 1:
                foods_dict[food_ndb_num]["ingredients"] = {
                    list_name: ing_list
                    for list_name, ing_list
                    in zip(ingredients_names, ingredients_lists)
                }
            elif len(ingredients_lists) == 1:
                foods_dict[food_ndb_num]["ingredients"] = ingredients_lists[0]
            else:
                foods_dict[food_ndb_num]["ingredients"] = []

    for ndb_num in foods_dict:
        foods_dict[ndb_num]["nutrients"] = {}

    with open_raw(raw_nutrients_file_name) as read_f:
        header = read_f.readline()

        for line in read_f:
            data = line.split('"')[1::2]

            ndb_num = data[0]
            nutrient_code = int(data[1])

            if ndb_num in foods_dict:
                amount_per_100g = float(data[4])

                if amount_per_100g > 0:
                    derivation_code = data[3]
                    amount_units = data[5]

                    foods_dict[ndb_num]["nutrients"][nutrient_code] = {
                        "derivation_code": derivation_code,
                        "amount_per_100g": amount_per_100g,
                        "amount_units": amount_units
                    }

            if nutrient_code not in nutrients_dict:
                nutrient_name = data[2]

                nutrients_dict[nutrient_code] = nutrient_name

    with open_raw(raw_derivations_file_name) as read_f:
        for line in read_f:
            code, description = line.split('"')[1::2]

            derivations_dict[code] = description

    return foods_dict, nutrients_dict, derivations_dict


def read_processed():
    def read_data(n):
        with open(n, "rb") as read_f:
            return pickle.load(read_f)

    foods_dict = read_data(foods_file_name)
    nutrients_dict = read_data(nutrients_file_name)
    derivations_dict = read_data(derivations_file_name)

    return foods_dict, nutrients_dict, derivations_dict


def write_processed(foods_dict, nutrients_dict, derivations_dict):
    try:
        mkdir(processed_data_folder)
    except FileExistsError:
        pass

    def write_data(d, n):
        with open(n, "wb") as write_f:
            pickle.dump(d, write_f, 0)

    write_data(nutrients_dict, nutrients_file_name)
    write_data(derivations_dict, derivations_file_name)
    write_data(foods_dict, foods_file_name)
