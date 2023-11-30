import panel as pn
from sklearn.datasets import load_wine
import pandas as pd
import hvplot.pandas
import warnings
warnings.filterwarnings("ignore")

########################### LOAD DATASET ##################
wine = load_wine()
wine_df = pd.DataFrame(wine.data, columns=wine.feature_names)
wine_df["WineType"] = [wine.target_names[t] for t in wine.target]

################################# CREATE CHARTS ############################
def create_hist(sel_feature):
    return wine_df.hvplot.hist(y=sel_feature, by="WineType",
                                bins=50, height=400).opts(active_tools=[])

def create_scatter_chart(x_axis, y_axis):
    return wine_df.hvplot.scatter(x=x_axis, y=y_axis, color="WineType",
                                  size=100, alpha=0.9, height=400).opts(active_tools=[])

def create_bar_chart(sel_cols):
    avg_wine_df = wine_df.groupby("WineType").mean().reset_index()
    return avg_wine_df.hvplot.bar(x="WineType", y=sel_cols, bar_width=0.8,
                                  rot=45, height=400).opts(active_tools=[])

def create_corr_heatmap():
    wine_corr = wine_df.corr(numeric_only=True)
    return wine_corr.hvplot.heatmap(cmap="Blues", rot=45, height=500).opts(active_tools=[])

############################# WIDGETS & CALLBACK ###########################################
# https://tabler-icons.io/
button1 = pn.widgets.Button(name="Introduction", button_type="warning", icon="file-info", styles={"width": "100%"})
button2 = pn.widgets.Button(name="Dataset", button_type="warning", icon="clipboard-data", styles={"width": "100%"})
button3 = pn.widgets.Button(name="Distribution", button_type="warning", icon="chart-histogram", styles={"width": "100%"})
button4 = pn.widgets.Button(name="Relationship", button_type="warning", icon="chart-dots-filled", styles={"width": "100%"})
button5 = pn.widgets.Button(name="Avg Features", button_type="warning", icon="chart-bar", styles={"width": "100%"})
button6 = pn.widgets.Button(name="Correlation", button_type="warning", icon="chart-treemap", styles={"width": "100%"})

dist_feature = pn.widgets.Select(name="Feature", options=wine.feature_names)

x_axis = pn.widgets.Select(name="X-Axis", options=wine.feature_names)
y_axis = pn.widgets.Select(name="Y-Axis", options=wine.feature_names, value="malic_acid")

multi_select = pn.widgets.MultiSelect(name="Ingredients", options=wine.feature_names,
                                      value=["alcohol", "malic_acid", "ash"])
def show_page(page_key):
    main_area.clear()
    main_area.append(mapping[page_key])

button1.on_click(lambda event: show_page("Page1"))
button2.on_click(lambda event: show_page("Page2"))
button3.on_click(lambda event: show_page("Page3"))
button4.on_click(lambda event: show_page("Page4"))
button5.on_click(lambda event: show_page("Page5"))
button6.on_click(lambda event: show_page("Page6"))

############################ CREATE PAGE LAYOUT ##################################
def CreatePage1():
    descr = "\n".join([line.replace("\t", "") for line in wine.DESCR[19:550].split("\n") if line.strip()])
    return pn.Column(pn.pane.Markdown(descr, width=550),
                     align="center")

def CreatePage2(df):
    return pn.Column(
        pn.pane.Markdown("## Dataset Explorer"),
        pn.pane.DataFrame(df, height=450, width=850),
        align="center",
    )

def CreatePage3():
    return pn.Column(
        pn.pane.Markdown("## Explore Distribution of Features"),
        dist_feature,
        pn.bind(create_hist, dist_feature),
        align="center",
    )

def CreatePage4():
    return pn.Column(
        pn.pane.Markdown("## Explore Relationship Between Features"),
        pn.Row(x_axis, y_axis),
        pn.bind(create_scatter_chart, x_axis, y_axis),
        align="center",
    )

def CreatePage5():
    return pn.Column(
        pn.pane.Markdown("## Explore Avg Values of Features per Wine Type"),
        multi_select,
        pn.bind(create_bar_chart, multi_select),
        align="center",
    )

def CreatePage6():
    return pn.Column(
        pn.pane.Markdown("## Features Correlation Heatmap"),
        create_corr_heatmap(),
        align="center",
    )

mapping = {
    "Page1": CreatePage1(),
    "Page2": CreatePage2(wine_df),
    "Page3": CreatePage3(),
    "Page4": CreatePage4(),
    "Page5": CreatePage5(),
    "Page6": CreatePage6(),
}

#################### SIDEBAR LAYOUT ##########################
sidebar = pn.Column(pn.pane.Markdown("## Pages"), button1, button2, button3, button4, button5, button6,
					styles={"width": "100%", "padding": "15px"})

#################### MAIN AREA LAYOUT ##########################
main_area = pn.Column(mapping["Page1"], styles={"width":"100%"})

###################### APP LAYOUT ##############################
template = pn.template.BootstrapTemplate(
    title=" Multi-Page Web App",
    sidebar=[sidebar],
    main=[main_area],
    header_background="black", 
    site="CoderzColumn", logo="cc.png", theme=pn.template.DarkTheme,
    sidebar_width=250, ## Default is 330
    busy_indicator=None,
)

# Serve the Panel app
template.servable()
