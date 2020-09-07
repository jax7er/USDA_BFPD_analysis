def resolve_multiple_matches(matches):
    max_index = len(matches) - 1

    print(f"Multiple matches found, enter index of desired result (0 to {max_index}):")
    print("\n".join(f"\t{i}: {v}" for i, v in enumerate(matches)))

    while True:
        index = input("")

        if index.isnumeric() and 0 <= int(index) <= max_index:
            return int(index)
        else:
            print(f"Invalid index, enter a value between 0 and {max_index}")


def get_user_foods(foods, plot_food_ids):
    def print_foods():
        print("Current foods to plot:")
        print("\t" + "\n".join(sorted(["\t" + foods[plot_food_id]['name'] for plot_food_id in plot_food_ids])))

    if plot_food_ids:
        print_foods()

    find_exact_match = True

    while True:
        no_foods = len(plot_food_ids) == 0

        if no_foods:
            clear_quit_text = "Quit: q"
        else:
            clear_quit_text = "Clear list: c"

        if find_exact_match:
            find_exact_text = "on"
        else:
            find_exact_text = "off"

        find_food = input(f"Find food:\n"
                          f"\tToggle exact ({find_exact_text}): !\n"
                          f"\t{clear_quit_text}\n"
                          f"\tContinue: <Enter>\n").lower()

        if find_food == "":
            break
        elif find_food == "!":
            find_exact_match = not find_exact_match
            continue
        elif find_food == "q" and no_foods:
            return None
        elif find_food == "c" and not no_foods:
            plot_food_ids = []
            continue

        found_list = []

        for food_id in foods:
            food_name = foods[food_id]["name"].lower()

            if find_exact_match:
                if food_name == find_food:
                    # check an exact match isn't already in the found list
                    if not any([food_name == foods[already_found_id]["name"] for already_found_id in found_list]):
                        found_list.append(food_id)
            else:
                find_food_i = food_name.find(find_food)

                if find_food_i > -1:
                    if find_food_i == 0 or food_name[find_food_i - 1] == " ":
                        end_i = find_food_i + len(find_food)

                        if end_i == len(food_name) or food_name[end_i] == " ":
                            found_list.append(food_id)

        if len(found_list) == 0:
            print("Can't find " + find_food)
        else:
            if len(found_list) == 1:
                found_id = found_list[0]
            else:
                found_names = [foods[food_id]["name"] for food_id in found_list]

                found_id = found_list[resolve_multiple_matches(found_names)]

            if found_id in plot_food_ids:
                plot_food_ids.remove(found_id)
            else:
                plot_food_ids.append(found_id)

            print_foods()

    return plot_food_ids


def get_user_nutrient(nutrients):
    def print_nutrients():
        print("Available nutrients:")
        print("\n".join(sorted("\t" + [nutrients[nut_id] for nut_id in nutrients])))

    print_nutrients()

    while True:
        find_nutrient = input("Find nutrient:\n\tQuit: q\n").lower()

        if find_nutrient == "":
            print("Enter a search term")
            continue
        elif find_nutrient == "q":
            return None

        found_list = []

        for nutrient_id in nutrients:
            nutrient_name = nutrients[nutrient_id].lower()

            find_nutrient_i = nutrient_name.find(find_nutrient)

            if find_nutrient_i == 0 or (find_nutrient_i > 0 and nutrient_name[find_nutrient_i - 1] == " "):
                found_list.append(nutrient_id)

        if len(found_list) == 0:
            print("Can't find " + find_nutrient)
            print_nutrients()
        else:
            if len(found_list) == 1:
                return found_list[0]
            else:
                found_names = [nutrients[nutrient_id] for nutrient_id in found_list]

                return found_list[resolve_multiple_matches(found_names)]
