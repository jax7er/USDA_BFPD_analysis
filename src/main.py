from file_read_write import read_raw, read_processed, write_processed
from cmd_ui import get_user_foods, get_user_nutrient
from plotting import plot_bars
from random import choice, choices


def main():
    try:
        print("Loading processed data...")
        foods, nutrients, derivations = read_processed()
    except (FileNotFoundError, EOFError) as e:
        print(f"Failed ({e}), reading data from raw files...")
        foods, nutrients, derivations = read_raw()

        print("Saving processed data...")
        write_processed(foods, nutrients, derivations)

    plot_food_ids = []

    while True:
        user_in = ""
        while user_in.lower() not in ["y", "n"]:
            user_in = input("Random plots?\n\tYes: y\n\tNo: n\n")

        if user_in == "y":
            num_plots = 5
            num_foods = 10
            all_plot_food_ids = []
            all_nutrient_ids = []

            for _ in range(num_plots):
                while True:
                    try:
                        # get foods with at least 1 common nutrient
                        while True:
                            plot_food_ids = choices(list(foods.keys()), k=num_foods)

                            nutrient_id_set = set.intersection(*[set(foods[food_id]["nutrients"]) for food_id in plot_food_ids])
                            if nutrient_id_set:
                                break
                            
                        nutrient_id = choice(list(nutrient_id_set))

                        # check all foods with nutrient have more than zero g/100g
                        if all(foods[food_id]["nutrients"][nutrient_id]["amount_per_100g"] > 0 for food_id in plot_food_ids):
                            break
                    except KeyError as e:
                        #TODO some foods don't have a "nutrients" key but they should
                        print(e)
                        pass

                all_plot_food_ids.append(plot_food_ids)
                all_nutrient_ids.append(nutrient_id)
        else:
            all_plot_food_ids = get_user_foods(foods, plot_food_ids)
            if all_plot_food_ids is None:
                return

            all_nutrient_ids = get_user_nutrient(nutrients)
            if all_nutrient_ids is None:
                return

        all_plot_foods = [[foods[food_id] for food_id in plot_food_ids] for plot_food_ids in all_plot_food_ids]
        all_plot_titles = [nutrients[nutrient_id] + " per 100g" for nutrient_id in all_nutrient_ids]
        plot_bars(all_plot_titles, all_plot_foods, all_nutrient_ids)


if __name__ == "__main__":
    main()
    print("Quitting...")
