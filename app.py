import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from palmerpenguins import load_penguins
from shiny.express import ui, input, render

# --- 1. Data Loading ---
penguins = load_penguins()

# --- 2. User Interface (UI) Definition ---
ui.page_opts(title="Interactive Data Visualizations", fillable=True)

with ui.sidebar():
    ui.input_slider("selected_number_of_bins", "Number of Bins", 0, 100, 20)

    ui.hr()
    ui.h6("Penguin Plot Filters")

    all_species = ["All"] + sorted(penguins["species"].dropna().unique().tolist())
    ui.input_select("selected_species", "Select Species", choices=all_species, selected="All")


# --- 3. Server Logic and Output Definitions ---

@render.plot(alt="Histogram using the selected number of bins for random data")
def plot_histogram():
    data = np.random.randn(800)
    plt.hist(data, bins=input.selected_number_of_bins(), density=True, color="darkorange", edgecolor="black")

    plt.title("Frequency Distribution of Randomly Generated Data")
    plt.xlabel("Value")
    plt.ylabel("Density")


@render.plot(alt="Scatterplot of Penguin Flipper Length vs Body Mass")
def penguin_scatter():
    selected_species = input.selected_species()

    if selected_species == "All":
        filtered_penguins = penguins
    else:
        filtered_penguins = penguins[penguins["species"] == selected_species]

    sns.scatterplot(
        data=filtered_penguins,
        x="flipper_length_mm",
        y="body_mass_g",
        hue="species",
        style="sex",
        palette={"Adelie": "red", "Chinstrap": "blue", "Gentoo": "green"}
    )

    plt.title(f"Penguin Flipper Length vs Body Mass by Species and Sex ({selected_species})")
    plt.xlabel("Flipper Length (mm)")
    plt.ylabel("Body Mass (g)")
