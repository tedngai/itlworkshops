---
layout: post
title: Data Visualization for History of Art and Design - Processing the MoMA Collection
description: Pandas, Plotly, Regular Expression
image: 
---
<hr />
## Project Description
This data visualization module is inspired by MoMA's [data dump](https://github.com/MuseumofModernArt/collection){:target="_blank"} in 2015. MoMA had release the database of their collection which contains over 130,000 pieces of artwork over the timespan of 150 years. In this session, we will learn to visualise MoMA collection similar to what [Oliver Roeder](https://fivethirtyeight.com/features/a-nerds-guide-to-the-2229-paintings-at-moma/){:target="_blank"} had done at [FiveThirtyEight](https://fivethirtyeight.com/){:target="_blank"}, perhaps we will even take it further. This session will allow us to dive into Pandas, Plot.ly, and python regular expression a lot more and get into some of the more intermediate level of data processing. In the course this this workshop, we will try to re-create some of Oliver's visualizations such as these.

<iframe width="100%" height="500" frameborder="0" scrolling="no" src="//plot.ly/~prattitl/66.embed"></iframe>
<iframe width="100%" height="500" frameborder="0" scrolling="no" src="//plot.ly/~prattitl/103.embed"></iframe>
***

# Step 1
### Import Libraries and Data

This workshop module assumes you have already installed all the necessary python libraries, if you have not done so, please go back to the previous module. What we will need for this session is Plotly and Pandas, and we will run the entire session on Jupyter.  

First import all the libraries by executing the following code.

```python
import plotly.graph_objs as go
import plotly.express as px
from collections import defaultdict
import pandas as pd
```

Import the csv file by executing the following code.

```python
df_moma = pd.read_csv('https://github.com/MuseumofModernArt/collection/blob/master/Artworks.csv')
```

If you want to speed things up a little, download the csv file to your local drive and place it in the same folder as where you're running Jupyter Notebook, then execute this code.

```python
df_moma = pd.read_csv('./MoMAArtworks.csv')
```

Execute **df_moma.info()** to see what's inside this variable.

```
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 138118 entries, 0 to 138117
Data columns (total 29 columns):
Title                 138079 non-null object
Artist                136662 non-null object
ConstituentID         136662 non-null object
ArtistBio             132559 non-null object
Nationality           136662 non-null object
BeginDate             136662 non-null object
EndDate               136662 non-null object
Gender                136662 non-null object
Date                  135743 non-null object
Medium                127156 non-null object
Dimensions            127253 non-null object
CreditLine            135354 non-null object
AccessionNumber       138118 non-null object
Classification        138118 non-null object
Department            138118 non-null object
```
The RangeIndex shows there is a total of 138,118 entries in the dataset. It also lists the number of non-null items in each column. Non-null objects has a value of  **NaN**. In computer science lingo, it means **"not a number"**, which also means there is an invalid record in the dataset. So before we begin to do anything beyond this, we need to for fill those records up with something else other than a **NaN** because it will cause issues with Pandas and Python down the line (unless we write more code to handle the errors). We use a function call **fillna** to replace any **NaN** value with something we designate.

```python
df_moma[['Artist','Nationality','BeginDate',
         'Gender','Medium']] = df_moma[['Artist','Nationality','BeginDate',
'Gender','Medium']].fillna(value='Unknown')
```

This line of code lets us look into each of these columns and find any **NaN** values and replace them with the word **"Unknown"**. We're now ready to move forward with more advanced date processing techniques.

***

# Step 2
### Data Processing

Now that we have imported the whole 130,000 records of MoMA's collection, say we want to see which is their largest collection, we can do something like - look at every record and see what "Medium" it uses and count them all. And finally give me a sorted result which tells me what is their biggest collection is based on the Medium.

You can explore this easily with a **pandas** function

```python
df_moma['Medium'].value_counts()
```
And you should see something like this

```
Gelatin silver print	15399
Lithograph		7842
Albumen silver print	4854
Pencil on paper		1831
Letterpress		1680
...  
```
The square bracket defines the column name, you can try using different column names to explore the dataset. Now, because the list of medium types is long and the screen does not show everything, we will need to find a way to access all the other items. 

Since Pandas restricts how many rows of data it shows, we will need to do a little work-around.

```python
med_keys = df_moma['Medium'].value_counts().keys().to_list()
med_values = df_moma['Medium'].value_counts().to_list()
df_medium = pd.DataFrame(list(zip(med_keys, med_values)),
                         columns =['Medium', 'Count'])
df_medium.to_csv('MoMA_MediumCounts.csv', index=False)
```
What we have done is to we created a new pandas dataframe only based on the medium value and the medium count, and we exported it out as a csv file so we can look at it with another program like Excel.

We can also plot this as a graph with the following code.  Bear in mind that we have over 20k medium types so it would be quite unlikely we can fit everything within the screen and potentially get some sort of error. Therefore we limit the amount of medium type to show to 20 with the code **.head(n=20)**.

```python
fig = px.bar(df_medium.head(n=20), x='Medium', y='Count')
fig.show()
```
![test image size](../../assets/images/moma/fig02.png){:height="70%" width="70%" .center-image}

You can also graph this with the following code.

```python
fig = px.bar(df_medium.head(n=20), template='seaborn', x='Medium', y='Count')
fig.write_image("./fig01.png", width=1800, height=900)
fig.show()
```
![test image size](../../assets/images/moma/fig01.png){:height="70%" width="70%" .center-image}

So now we know the largest collection MoMA has is photography. But let's say you want to look for specific **keywords** in the collection that you would associate with paintings like paint, oil, canvas...etc,  you can do something like this.

```python
searchfor = ['paint','oil','canvas','Casein']
df_medium[df_medium['Medium'].str.contains('|'.join(searchfor))]
```

Now let's try to use the same method of finding duplicates to see which artist has the largest number of work at MoMA.

```python
artist_keys = df_moma['Artist'].value_counts().keys().to_list()
artist_values = df_moma['Artist'].value_counts().to_list()
df_artist = pd.DataFrame({'Artist':artist_keys, 'Counts':artist_values})
df_artist
```
![test image size](../../assets/images/moma/fig03.png){:height="70%" width="70%" .center-image}

We can also single out individual artist and look at the variety of work based on medium. For example, we can specifically look at the Picasso collection and see which medium the museum has the most.


```python
searchfor = ['Picasso']
df_picasso = df_moma[df_moma['Artist'].str.contains('|'.join(searchfor))]

grouped = df_picasso[['Medium','Artist', ]].groupby(['Medium',]).count().reset_index()
grouped.sort_values('Artist', ascending=False)
```
![test image size](../../assets/images/moma/fig04.png){:height="70%" width="70%" .center-image}

So it turns out, MoMA has over one thousand pieces of art work by Picasso and almost 25% of that are litographic work!


***

# Step 3
### MoMA Collection by Size

For this exercise we will go back to what [Oliver Roeder](https://fivethirtyeight.com/features/a-nerds-guide-to-the-2229-paintings-at-moma/){:target="_blank"} had done at [FiveThirtyEight](https://fivethirtyeight.com/){:target="_blank"} and look at the visualization that compare the size of the artwork in the collection.

Again we'll start fresh with a new notebook and import all the libraries. 

```python
import plotly.graph_objs as go
from collections import defaultdict
import pandas as pd
import re, datetime
```

And we bring in the csv file.

```python
df_moma = pd.read_csv('https://github.com/MuseumofModernArt/collection/blob/master/Artworks.csv')
```

```python
df_moma = pd.read_csv('./MoMAArtworks.csv')
```

And again, let's clean up all the missing values. 

```python
df_moma[['Artist','Nationality','Date','BeginDate','Gender','DateAcquired']] = df_moma[['Artist','Nationality','Date','BeginDate','Gender','DateAcquired']].fillna(value='Unknown')
```

Remember that there're over 130,000 records and it's simply not feasible to visualize every single item in the collection, we will make an arbitrary decision and say the visualization will be based on their classification, and in this case, the architecture collection. You can change this to what ever you want. Say if you want to look at the sizes of all of Picasso's work, it's the same procedure.

First look at how many classifications there are that are related to architecture. To do that we use the same value_counts() function as before.

```python
df_moma['Classification'].value_counts().head(n=10)
```
<iframe width="100%" height="500" frameborder="0" scrolling="no" src="//plot.ly/~prattitl/111.embed"></iframe>

From this list you can see there is a Mies van der Rohe Archive, an architecture collection, and a Frank Lloyd Wright Archive, all related to architecture. So we'll create a new dataframe that would use those terms as filter words. 

![test image size](../../assets/images/moma/fig05.png){:height="70%" width="70%" .center-image}

```python
searchfor = ['Mies van der Rohe Archive','Architecture','Frank Lloyd Wright Archive']
df_moma_archi = df_moma[df_moma['Classification'].str.contains('|'.join(searchfor))]
```

Since we know we will base our on the Height and Width columns, we need to ensure we don't have any missing data. 

```python
df_moma_archi_hasSize = df_moma_archi[~df_moma_archi['Height (cm)'].isnull() & 
                                     ~df_moma_archi['Width (cm)'].isnull()]
```

Now the data should be ready to pass to Plotly.

```python
fig = px.scatter(df_moma_archi_hasSize, template='seaborn', x='Width (cm)', y='Height (cm)',
                hover_data=['Artist','Title','DateAcquired'], width=800, height=400)
fig.show()
```

<iframe width="100%" height="500" frameborder="0" scrolling="no" src="//plot.ly/~prattitl/70.embed"></iframe>
Now let's not stop here because we only got a scatter plot, but we want to actually see the rectangles. To have plotly draw shapes, we'll need to learn about the syntax. For a deep dive into Plot.ly shapes, click here.

<center><button class="button special fit">
		<a href="https://plot.ly/python/shapes/" target="blank">Deep Dive: Plot.ly Shapes</a>
</button></center><br>

Essentially we learn that shapes are drawn in the layout section rather than in the data section. And shapes are drawn as a dictionary like this. Dictionary is a type of data structure in Python. For a deep dive on the subject, click here.

<center><button class="button special fit">
		<a href="https://www.w3schools.com/python/python_dictionaries.asp" target="blank">Deep Dive: Python Dictionary</a>
</button></center><br>



```python
df_placeholder = df_moma_archi_hasSize

hovertext = []
rects = []
for i,row in df_placeholder.iterrows():
    hovertext.append(row['Artist'] + '<br>' + row['DateAcquired']+ '<br>' + row['Title'] )
    keys = ['type','xref','yref','x0','y0','x1','y1','line','fillcolor']
    values = ['rect','x','y',0,0,
              row['Width (cm)'],
              row['Height (cm)'],
              {'color': 'rgb(200,200,200)','width':1,},
              'rgba(55,55,55,0.1)']
    rects.append(dict(zip(keys,values)))

trace = go.Scatter(
        y = df_placeholder['Height (cm)'].tolist(),
        x = df_placeholder['Width (cm)'].tolist(),
        mode = 'markers',
        text = hovertext,
        marker = dict(
            size = 2,
            color = 'rgba(255, 0, 0, .3)',
            ) 
        )

layout = go.Layout(
    title = 'MoMA Drawing Size<br>'+ '<br>' + str(len(df_placeholder)),
    hovermode = 'closest',
    yaxis = dict(
            title = 'Height (cm)',
            ticklen = 5,
            zeroline = True,
            gridwidth = 1,
            ),
    xaxis = dict(
            title = 'Width (cm)',
            ticklen = 5,
            gridwidth = 1,
            ),
    shapes = rects,
    showlegend = False,
    )

fig = go.Figure(data = [trace], layout=layout)

fig.show()
```

<iframe width="100%" height="500" frameborder="0" scrolling="no" src="//plot.ly/~prattitl/66.embed"></iframe>

***

# Step 4
### Date Created VS Date Aquired
We are diving deeper and deeper into data processing with Pandas as we continue to work with the same data set. This next exercise will dive right into one of the graphs 
[Oliver Roeder](https://fivethirtyeight.com/features/a-nerds-guide-to-the-2229-paintings-at-moma/){:target="_blank"} had done at [FiveThirtyEight](https://fivethirtyeight.com/){:target="_blank"} in which he graphed the year in which a painting had been painted versus the year in which the painted had been acquired by MoMA. It's a simple idea but to actually create this graph, it's anything but simple. We will have to rely on everything we have learned so far and more!

Let's open up a new notebook start fresh, and import the following packages.

```python
import plotly.graph_objs as go
from collections import defaultdict
import pandas as pd
import re, datetime
```

Import the CSV file as we did before, again, your choice if you want to load it remotely or locally.

```python
df_moma = pd.read_csv('https://github.com/MuseumofModernArt/collection/blob/master/Artworks.csv')
```

```python
df_moma = pd.read_csv('./MoMAArtworks.csv')
```

And again, let's clean up all the missing values which is represented by **NaN** and fill that with the text **Unknown**. For more on how to work with **Missing Data** in Pandas, click here.

<center><button  class="button special fit">
		<a href="https://pandas.pydata.org/pandas-docs/stable/user_guide/missing_data.html" target="blank">Deep Dive: Pandas Missing Data</a>
</button></center>

```python
df_moma[['Artist','Nationality','Date','BeginDate','Gender','DateAcquired']] = df_moma[['Artist','Nationality','Date','BeginDate','Gender','DateAcquired']].fillna(value='Unknown')
```

Now let's look at the 2 column of data we're interested in working with, DateAcquired and Date (assuming it is the date the work was produced), and you should see something like the following.

```python
df_moma[['DateAcquired','Date']]
```

<iframe width="100%" height="500" frameborder="0" scrolling="no" src="https://plot.ly/~prattitl/101.embed"></iframe>

Immediately we notice that the date format is diffent between the 2 columns. And even within each column, there are a lot of inconsistensies in the format. This is one of the quintessential task in data science - understanding how data needs to be structured so computer language can make sense of it. And now our task is to search through and clear data for inconsistencies. 

To do that let's talk through what the approach is, and simplify the problem by only looking at one of the columns first. The Date Acquired seems to be a bit more consistent at first glance, it seems most of the rows have this xxxx-xx-xx format. So let's take a deeper look into this.

```python
for row in (df_moma.DateAcquired):
    q = re.search(r'(\d{4})-(\d{1,2})-(\d{1,2})$', row)
    if not q:
        print(row)
```

<iframe width="100%" height="500" frameborder="0" scrolling="no" src="//plot.ly/~prattitl/105.embed"></iframe>
**df_moma.DateAcquired** is a short form to only show the DataAcquired column of the df_moma dataframe. It can also be written as **df_moma['DateAcquired']**, it'll give us the same thing. The **for row in x** loop goes into every single row of data. **q = re.search(r'(\d{4})-(\d{1,2})-(\d{1,2})$', row)** is to use a very powerful function call **Regular Expression** to sift through the data looking for patterns. Regular Expression is a rabbit hole, it was invented in the 1950s as a mathematical formal language and people have built search engines and word processors with it. For a deeper understanding, I'd recommend doing a more extensive reading on this subject. For a deeper look at how to use it pragmatically with python, click the following link.

<center><button class="button special fit">
		<a href="https://www.dataquest.io/blog/regex-cheatsheet/" target="blank">Deep Dive: Regular Expression</a>
</button></center><br>

But let's try to break it down so we have a basic understanding. 

`re.search(r'(\d{4})-(\d{1,2})-(\d{1,2})$', row)` is made up of `re.search(a,b)`, which is to look for pattern a inside b. The `r''` quote is a convention that defines everything within the quotes are "raw" strings. `\d` is any digit between 0-9. Used along with `{4}` will look for any 4 digits repeated 4 times. `\d{1,2}` means look for digits repeated 1 to 2 times. So in human language, look for this pattern, digits that has been repeated 4 times, then a hyphen, then 1 to 2 digits, then another hyphen, then another 1 to 2 digits. Put this whole thing under a variable **q** means, if the search is positive, return True and store that in **q**. 

Thus, `if not q:` means if the pattern didn't match, then `print(row)` show me the result. 

So from the results we see a lot of **Unknown**, but unless we go through each entry one by one, we can't be sure if that is the only deviation, so let's add to the funciton and identify all the unique variations. 

```python
dateAcquired_nullValue = []
for row in (df_moma.DateAcquired):
    q = re.search(r'(\d{4})-(\d{1,2})-(\d{1,2})$', row)
    if not q:
        print(row)
        dateAcquired_nullValue.append(row)
```

We first create an empty list and inside the loop, pass all the values that doesn't match the pattern into the variable. So we end with a list of all the deviations. We then use a function to look for unique values.

```python
def list_duplicates(seq):
    result = []
    for item in seq:
        if item not in result:
            result.append(item)
    return result

list_duplicates(dateAcquired_nullValue)
```

Here, a **list_duplicate** function is created to look for unique items. And low and behold, we get this as a result - `['Unknown', '1977-08', '1975-01', '1994', '1961']`. So other than Unknown, we also have 2 other date format we have to account for.

Now the **Date** column seems like it's a lot more complex. Just by scrolling through the data we can already see there is **xxxx, xxxx-xx, c. xxxx, c. xxxx-xx, xxxx-xxxx**... so we will have to come up with another **regular expression pattern** to sift through that data. 

```python
date_nullValue = []
for row in (df_moma.Date):
    q = re.search(r'^.*(\d{4}).*', row)
    if not q:
        print(row)
        date_nullValue.append(row)
```

For this search pattern `re.search(r'^.*(\d{4}).*', row)`, we can just concentrate on this part `^.*(\d{4}).*`. `^` forces the search pattern right at the start of the string. `.` is any character and `*` is repeated however many times. So reading this together `^.*(\d{4})` is it looks for a 4 digit number and ignore anything that comes before, `^.*(\d{4}).*` thus, adding another `.*` after that is to say, look for a 4 digit code and ignore anything that comes before and after. 

```python
def list_duplicates(seq):
    result = []
    for item in seq:
        if item not in result:
            result.append(item)
    return result

list_duplicates(date_nullValue)
```

You should see a big list of deviations that would be very hard to sift through without the use of regular expression.

Now that we know the data has these many inconsistencies, let's get rid of them. But as a general practice, we don't necessarily want to delete records. Instead, we can create a copy of the data with a filter so we get a clean dataset. To do this we first create 2 lists that contains all the inconsistent date formats.

```python
dateAcquired_nullValueDup = list_duplicates(dateAcquired_nullValue)
date_nullValueDup = list_duplicates(date_nullValue)
```

We're essentially just repeating the same function earlier but now passing the results into a new variable. Then we do this.

```python
df_moma_known = df_moma[~df_moma['DateAcquired'].isin(dateAcquired_nullValueDup)]
```

Let's break it down again. `dateAcquired_nullValueDup` is a list of filter words. `df_moma['DateAcquired'].isin()` is a way to pass the column of data and see if any of the rows is in whatever has been passed into `isin()`. So essentially this will give a list of True False value showing us all the records that is in that filter list. However, we want a record that is not in the filter list, so we add that little `~` tilda in front. 

So we have reduced the dataframe by using a list of keywords as filter. Now let's do that again with the other list. 

```python
df_moma_known_known = df_moma_known[~df_moma_known['Date'].isin(date_nullValueDup)]
```

Now although we have cleaned up the data by eliminated all the null or unknown value records, we have yet to change the date format to something that can be used. Since we can say for sure that the year is the only consistent value between the 2 columns, we need to find a way to extract that information. We'll do it with regular expression again. 

 ```python
 datePatternToExtract = r'^.*(\d{4}).*'
dateAcquiredPatternToExtract = r'^(\d{4}).*'
df_moma_known_known['DateCreated'] = df_moma_known_known['Date'].str.extract(datePatternToExtract)
df_moma_known_known['DateAcquiredFormtted'] = df_moma_known_known['DateAcquired'].str.extract(dateAcquiredPatternToExtract)
 ```

For this part, we're using a native Pandas function **str.extract** in combination with regular expression to create a new column with the proper year value. We first create 2 patterns, 1 for the Date column and the other for the Date Acquired column. The patter is very similar except for the beginning. Then we created 2 new columns and pass all the extracted values there. 

When you execute this, you might get an error message that reads something like this,

```python
A value is trying to be set on a copy of a slice from a DataFrame.
Try using .loc[row_indexer,col_indexer] = value instead
```

You can ignore the message and move on. The last step in cleaning up the date format is to get rid of a single row of data that has the wrong date. The acquisition date says it's from the 1200's but you know that can't be correct because the museum didn't exist. Execute this code to get rid that specific record. 

`df_moma_known_known.drop(129985, inplace=True)`

Since there're still over 120,000 records, let's further filter the data and then do the visualization. 

```python
medium = []
for dup in sorted(list_duplicates(df_moma_known_known['Medium'].astype(str))):
    medium.append([dup[0], len(dup[1])])
labels = ['Medium', 'Number Of Artwork']
df_medium = pd.DataFrame.from_records(medium, columns=labels)
df_medium.sort_values('Number Of Artwork', ascending=False)
```

<iframe width="100%" height="500" frameborder="0" scrolling="no" src="//plot.ly/~prattitl/109.embed"></iframe>
You can choose to filter the records in different ways but let's say for now we will do it by medium. We'll first make a list of all the medium and show its collection size. Then say we will make a few new dataframes based on medium.

```python
df_Gelatin = df_moma_known_known[df_moma_known_known['Medium']=='Gelatin silver print']
df_Lithograph = df_moma_known_known[df_moma_known_known['Medium']=='Lithograph']
df_Oil = df_moma_known_known[df_moma_known_known['Medium']=='Oil on canvas']
df_Albumen = df_moma_known_known[df_moma_known_known['Medium']=='Albumen silver print']
```

Now to create the actual graph, we'll use a place holder variable so if you want to change to a different medium, you just need to change the first variable. 

```python
df_placeholder = df_Oil
trace = go.Scatter(
        y = df_placeholder['DateAcquiredFormtted'].tolist(),
        x = df_placeholder['DateCreated'].tolist(),
        mode = 'markers',
        text = df_placeholder['Title'].tolist(),
        marker = dict(
            size = 10,
            color = 'rgba(200, 200, 200, .3)',
            ) 
        )

layout = go.Layout(
    title = '<b>MoMA Year Acquired VS Year Created</b><br>'+ df_placeholder.iloc[0]['Medium'] +'<br>' + str(len(df_placeholder)),
    hovermode = 'closest',
    yaxis = dict(
            title = 'Date Acquired',
            ticklen = 5,
            zeroline = True,
            gridwidth = 2,
            ),
    xaxis = dict(
            title = 'Date Created',
            ticklen = 5,
            gridwidth = 2,
            ),
    showlegend = False,
    )

fig = go.Figure(data = [trace], layout=layout)

fig.show()
```

<iframe width="100%" height="500" frameborder="0" scrolling="no" src="//plot.ly/~prattitl/103.embed"></iframe>
Congratulations for completing this step. Now you're ready to move on to the next step. 


***

# Summary

### What You have Learned

* How to create and assign value to a variable
* How to create and assign values a list
* How to create and assign values a list of lists
* How to bring data into Python as text or csv files 
* How to create and use a counter
* How to write a basic function
* How to call a basic function
* Basic loop structure - how to use for-loops
* How to import packages in Python
* How to use basic functions of packages like Pandas, Plotly, BeautifulSoup
* How to create interactive plots with Plotly.