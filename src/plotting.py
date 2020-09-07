import matplotlib as mpl
import matplotlib.pyplot as plt


# speed up plotting by using the fast style to render plots
mpl.style.use('fast')


def _plot_init(title):
    fig = plt.figure()    
    fig.suptitle(title)
    
    ax = plt.gca()
    
    return fig, ax


def _plot_show():
    return plt.show()


def plot_bars(titles, all_plot_foods, all_nutrient_ids):
    num_plots = len(titles)

    if num_plots != len(all_plot_foods) or num_plots != len(all_nutrient_ids):
        print("Input arrays are not the same length")
        return

    for plot_i in range(num_plots):
        title = titles[plot_i]
        plot_foods = all_plot_foods[plot_i]
        nutrient_id = all_nutrient_ids[plot_i]

        fig, ax = _plot_init(title)

        for count, food in enumerate(plot_foods):
            # TODO all foods should have nutrients
            try:
                food_nutrients = food["nutrients"]

                if nutrient_id in food_nutrients:
                    ax.bar(count, food_nutrients[nutrient_id]["amount_per_100g"])
            except KeyError as e:
                print(e)

        ax.set_xticks([x for x in range(len(plot_foods))])
        ax.set_xticklabels([food["name"].replace(" ", "\n") for food in plot_foods])

        ax.set_ylabel([food["nutrients"][nutrient_id]["amount_units"]
                       for food in plot_foods
                       if "nutrients" in food][0])

    _plot_show()
