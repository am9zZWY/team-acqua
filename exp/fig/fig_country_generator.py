import os

import matplotlib.pyplot as plt
from tueplots.constants.color import rgb

from src.aquastat_utils import get_aquastat, SOURCE_TEXT
from src.utils import save_fig

FIG_PATH = 'fig_country'

# ENTER YOUR COUNTRY HERE
# ========================
RELEVANT_COUNTRY = 'Peru'
FILTER_COUNTRIES = []

RELEVANT_VARS = ["% of agricultural GVA produced by irrigated agriculture",
                 "% of agricultural water managed area equipped for irrigation",
                 "% of area equipped for full control irrigation actually irrigated",
                 "% of area equipped for irrigation by desalinated water",
                 "% of area equipped for irrigation by direct use of  treated municipal wastewater",
                 "% of area equipped for irrigation by direct use of agricultural drainage water ",
                 "% of area equipped for irrigation by direct use of non-treated municipal wastewater",
                 "% of area equipped for irrigation by groundwater ",
                 "% of area equipped for irrigation by mixed surface water and groundwater",
                 "% of area equipped for irrigation by surface water", "% of area equipped for irrigation drained",
                 "% of area equipped for irrigation power irrigated", "% of area equipped for irrigation salinized",
                 "% of irrigation potential equipped for irrigation",
                 "% of the agricultural holdings with irrigation managed by women",
                 "% of the area equipped for irrigation actually irrigated",
                 "% of the area equipped for irrigation managed by women",
                 "% of the cultivated area equipped for irrigation", "% of total country area cultivated",
                 "% of total cultivated area drained", "% of total grain production irrigated",
                 "Agricultural water withdrawal",
                 "Agricultural water withdrawal as % of total renewable water resources",
                 "Agricultural water withdrawal as % of total water withdrawal", "Agriculture, value added (% GDP)",
                 "Agriculture, value added to GDP", "Arable land area",
                 "Area equipped for full control irrigation: actually irrigated",
                 "Area equipped for full control irrigation: localized irrigation",
                 "Area equipped for full control irrigation: sprinkler irrigation",
                 "Area equipped for full control irrigation: surface irrigation",
                 "Area equipped for full control irrigation: total",
                 "Area equipped for irrigation by desalinated water",
                 "Area equipped for irrigation by direct use of agricultural drainage water",
                 "Area equipped for irrigation by direct use of non-treated municipal wastewater ",
                 "Area equipped for irrigation by direct use of not treated municipal wastewater",
                 "Area equipped for irrigation by direct use of treated municipal wastewater",
                 "Area equipped for irrigation by groundwater",
                 "Area equipped for irrigation by mixed surface water and groundwater",
                 "Area equipped for irrigation by surface water", "Area equipped for irrigation drained",
                 "Area equipped for irrigation: actually irrigated",
                 "Area equipped for irrigation: equipped lowland areas",
                 "Area equipped for irrigation: spate irrigation", "Area equipped for irrigation: total",
                 "Area equipped for power irrigation (surface water or groundwater)", "Area salinized by irrigation",
                 "Area waterlogged by irrigation", "Capacity of the municipal wastewater treatment facilities",
                 "Collected municipal wastewater", "Cultivated area (arable land + permanent crops)",
                 "Cultivated wetlands and inland valley bottoms non-equipped", "Dam capacity per capita",
                 "Dependency ratio", "Desalinated water produced", "Direct use of agricultural drainage water",
                 "Direct use of not treated municipal wastewater for irrigation purposes",
                 "Direct use of treated municipal wastewater",
                 "Direct use of treated municipal wastewater for irrigation purposes",
                 "Environmental Flow Requirements",
                 "Exploitable: irregular renewable surface water", "Exploitable: regular renewable groundwater",
                 "Exploitable: regular renewable surface water", "Exploitable: total renewable surface water",
                 "Flood occurrence (WRI)", "Flood recession cropping area non-equipped", "Fresh groundwater withdrawal",
                 "Fresh surface water withdrawal", "GDP Deflator (2015)", "GDP per capita",
                 "Gender Inequality Index (GII) [equality = 0; inequality = 1)", "Gross Domestic Product (GDP)",
                 "Groundwater produced internally", "Groundwater: accounted inflow",
                 "Groundwater: accounted outflow to other countries", "Groundwater: entering the country (total)",
                 "Groundwater: leaving the country to other countries (total)",
                 "Harvested irrigated permanent crop area: Bananas", "Harvested irrigated permanent crop area: Citrus",
                 "Harvested irrigated permanent crop area: Cocoa beans",
                 "Harvested irrigated permanent crop area: Coconuts", "Harvested irrigated permanent crop area: Coffee",
                 "Harvested irrigated permanent crop area: Grapes",
                 "Harvested irrigated permanent crop area: Grass and Fodder",
                 "Harvested irrigated permanent crop area: Oil palm", "Harvested irrigated permanent crop area: Olives",
                 "Harvested irrigated permanent crop area: Other crops",
                 "Harvested irrigated permanent crop area: Other fruits",
                 "Harvested irrigated permanent crop area: Plantains",
                 "Harvested irrigated permanent crop area: Rubber",
                 "Harvested irrigated permanent crop area: Tea", "Harvested irrigated permanent crop area: Total",
                 "Harvested irrigated temporary crop area: Barley", "Harvested irrigated temporary crop area: Cassava",
                 "Harvested irrigated temporary crop area: Cotton", "Harvested irrigated temporary crop area: Flowers",
                 "Harvested irrigated temporary crop area: Fodder",
                 "Harvested irrigated temporary crop area: Groundnuts",
                 "Harvested irrigated temporary crop area: Leguminous crops",
                 "Harvested irrigated temporary crop area: Maize", "Harvested irrigated temporary crop area: Millet",
                 "Harvested irrigated temporary crop area: Other cereals",
                 "Harvested irrigated temporary crop area: Other crops",
                 "Harvested irrigated temporary crop area: Other roots and tubers",
                 "Harvested irrigated temporary crop area: Potatoes", "Harvested irrigated temporary crop area: Rice",
                 "Harvested irrigated temporary crop area: Sesame", "Harvested irrigated temporary crop area: Sorghum",
                 "Harvested irrigated temporary crop area: Soybeans",
                 "Harvested irrigated temporary crop area: Sugar beet",
                 "Harvested irrigated temporary crop area: Sugarcane",
                 "Harvested irrigated temporary crop area: Sunflower",
                 "Harvested irrigated temporary crop area: Sweet potatoes",
                 "Harvested irrigated temporary crop area: Tobacco", "Harvested irrigated temporary crop area: Total",
                 "Harvested irrigated temporary crop area: Vegetables",
                 "Harvested irrigated temporary crop area: Wheat",
                 "Human Development Index (HDI) [highest = 1]", "Industrial water withdrawal",
                 "Industrial water withdrawal as % of total water withdrawal", "Industry, value added to GDP",
                 "Interannual variability (WRI)", "Irrigated cropping intensity", "Irrigation potential",
                 "Irrigation water requirement", "Irrigation water withdrawal",
                 "Long-term average annual precipitation in depth", "Long-term average annual precipitation in volume",
                 "MDG 7.5. Freshwater withdrawal as % of total renewable water resources", "Municipal water withdrawal",
                 "Municipal water withdrawal as % of total withdrawal", "National Rainfall Index (NRI)",
                 "Non-irrigated cultivated area drained", "Not treated municipal wastewater",
                 "Not treated municipal wastewater discharged (secondary water)",
                 "Number of municipal wastewater treatment facilities",
                 "Number of people undernourished (3-year average)", "Overlap between surface water and groundwater",
                 "Overlap: between surface water and groundwater", "Permanent crops area",
                 "Permanent meadows and pastures irrigated", "Population affected by water related disease",
                 "Population density", "Prevalence of undernourishment (3-year average)",
                 "Produced municipal wastewater", "Ratio between rainfed and irrigated yields", "Rural population",
                 "Rural population with access to safe drinking-water (JMP)",
                 "SDG 6.4.1. Industrial Water Use Efficiency", "SDG 6.4.1. Irrigated Agriculture Water Use Efficiency",
                 "SDG 6.4.1. Services Water Use Efficiency", "SDG 6.4.1. Water Use Efficiency",
                 "SDG 6.4.2. Water Stress", "Seasonal variability (WRI)", "Services, value added to GDP",
                 "Surface water produced internally", "Surface water: accounted flow of border rivers",
                 "Surface water: accounted inflow", "Surface water: entering the country (total)",
                 "Surface water: inflow not submitted to treaties", "Surface water: inflow secured through treaties",
                 "Surface water: inflow submitted to treaties",
                 "Surface water: leaving the country to other countries (total)",
                 "Surface water: outflow to other countries not submitted to treaties",
                 "Surface water: outflow to other countries secured through treaties",
                 "Surface water: outflow to other countries submitted to treaties",
                 "Surface water: total external renewable", "Surface water: total flow of border rivers",
                 "Total agricultural water managed area", "Total area of the country (excl. coastal water)",
                 "Total cultivated area drained", "Total dam capacity", "Total exploitable water resources",
                 "Total freshwater withdrawal", "Total harvested irrigated crop area (full control irrigation)",
                 "Total internal renewable water resources (IRWR)",
                 "Total internal renewable water resources per capita", "Total population",
                 "Total population with access to safe drinking-water (JMP)", "Total renewable groundwater",
                 "Total renewable surface water", "Total renewable water resources",
                 "Total renewable water resources per capita", "Total water withdrawal",
                 "Total water withdrawal per capita", "Treated municipal wastewater",
                 "Treated municipal wastewater discharged (secondary water)", "Urban population",
                 "Urban population with access to safe drinking-water (JMP)",
                 "Water resources: total external renewable", "Water withdrawal for aquaculture",
                 "Water withdrawal for cooling of thermoelectric plants",
                 "Water withdrawal for livestock (watering and cleaning)"]

# Get the dataframe
df = get_aquastat()
raw_df = get_aquastat(raw=True)
print(df.head())

# Format dataframe
var_unit_map = raw_df[['Variable', 'Unit']].drop_duplicates().set_index('Variable').to_dict()['Unit']

# Extract relevant variables and drop all NaN
data = df[['Country', 'Year', *RELEVANT_VARS]]
if FILTER_COUNTRIES:
    data = data[data['Country'].isin(FILTER_COUNTRIES)]
data = data.dropna()

# Define colors
colors = [rgb.tue_blue, rgb.tue_red, rgb.tue_green, rgb.tue_orange]

for single_variable in RELEVANT_VARS:

    thiss = [single_variable]

    # Iterate over unique countries in the dataset
    for country in df['Country'].unique():

        if country != RELEVANT_COUNTRY:
            continue

        # Filter data for the current country
        country_data = df[df['Country'] == country]
        years = country_data['Year']
        years_range = [min(years), max(years)]

        # Create a figure and an axes
        fig, ax = plt.subplots()

        # Set the title
        ax.set_title('{} in {} ({}-{})'.format(" and\n".join(thiss), country, years_range[0], years_range[1]),
                     fontsize=10, pad=10,
                     color=rgb.tue_darkblue)

        # Grid
        ax.grid(True, which='both', color=rgb.tue_gray, linestyle='--', alpha=0.5)

        # X-axis
        ax.set_xlabel('year')
        ax.xaxis.set_ticks_position('both')
        ax.xaxis.set_minor_locator(plt.MultipleLocator(1))

        for (index, variable) in enumerate(thiss):
            if variable not in df.columns:
                continue

            data = country_data[variable]

            # Plotting
            color = colors[index % len(colors)]
            ax.plot(years, data, marker='o', linestyle='-', color=color, linewidth=1, markersize=3)

            # Y-axis
            ax.set_ylabel(var_unit_map[variable])
            ax.yaxis.set_ticks_position('both')

            # Add a legend
            ax.legend(thiss, loc='upper left', frameon=False)

            # Add source
            ax.text(0.99, 0.01, SOURCE_TEXT, transform=ax.transAxes, fontsize=8, ha='right',
                    color=rgb.tue_gray)

            # Save the figure
            save_fig(fig, fig_name=f'{country}_{variable}', fig_path=os.path.join(FIG_PATH, country))

            # Close the plot to avoid displaying it in the loop
            plt.close()

print("Plots saved!")

# %%
