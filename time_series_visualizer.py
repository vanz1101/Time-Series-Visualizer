import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.set_index('date')

# Clean data
df = df[(df['value'] > df['value'].quantile(0.025)) &(df['value'] < df['value'].quantile(0.975))]


def draw_line_plot():
  
    # Draw line plot
  fig, ax = plt.subplots(figsize=(19, 10), dpi=100)
  plt.plot(df,color = 'red')
  plt.xlabel('Date')
  plt.ylabel('Page Views')
  plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
  

    # Save image and return fig (don't change this part)
  fig.savefig('line_plot.png')
  return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
  df_bar = df.copy()

  df_bar['Years'] = df_bar.index.year
  df_bar['Months'] = df_bar.index.month_name()

  df_bar = pd.DataFrame(df_bar.groupby(["Years","Months"],sort = False)["value"].mean().round().astype(int))

  df_bar = df_bar.rename(columns={"value": "Average Page Views"})
  df_bar = df_bar.reset_index()
  missing_data = {"Years": [2016, 2016, 2016, 2016],
                  "Months": ['January', 'February', 'March', 'April'],
                  "Average Page Views": [0, 0, 0, 0]}

  df_bar = pd.concat([pd.DataFrame(missing_data) , df_bar])

    # Draw bar plot
  fig = plt.subplots(figsize = (19,10),dpi = 100)

  sns.barplot(df_bar, x = 'Years', y = 'Average Page Views', hue = 'Months',palette = 'tab10')
  
    # chart.set_xticklabels(chart.get_xticklabels(), rotation=90, horizontalalignment='center')
  plt.xticks(rotation = 90)
    # Save image and return fig (don't change this part)
  fig[0].savefig('bar_plot.png')
  return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
  df_box = df.copy()
  df_box.reset_index(inplace = True)
  df_box['Year'] = [x.year for x in df_box.date]
  df_box['Month'] = [x.strftime('%b') for x in df_box.date]

    # Draw box plots (using Seaborn)
  fig, ax = plt.subplots(1, 2, figsize=(32, 10), dpi=100)

    # Yearly boxplot
  sns.boxplot(df_box,x='Year',y='value',ax = ax[0])
  ax[0].set_ylabel('Page Views')
  ax[0].set_title('Year-wise Box Plot (Trend)')

    # Monthly boxplot
  month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
  sns.boxplot(df_box,x='Month',y='value',ax =ax[1],order = month_order)
  ax[1].set_title('Month-wise Box Plot (Seasonality)')
  ax[1].set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
  fig.savefig('box_plot.png')
  return fig