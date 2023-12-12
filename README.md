# 1) MMU Gain Prediction Visualization Using Dash

 

## Files, features explanation

### File location:

        /home/@@@@@/PycharmProjects/hayung_dash

### Necessary directories and files:

#### 1.   mmu_gain_webapp.py

      -        main file of the project

#### 2.   functions1.py (helper functions)

      -        predict_gain(contents, filename, filename1, filename2)

          loads the *model*, *input* files and returns the predicted csv file to *df* 

      -        input_parse_contents(contents)

          reads the data from the *input (.feather)* file and return to *df* 

      -        empty_png()

          deletes all the previous shap value png files

      -        plot_shap(filename1, filename2, gaintype, shaplist)
  

#### 3.  functions2.py (helper functions)

      -        get_max(mydf, gaintype)

      -        gain_pred_file()

      -        column_name(gaintype)

      -        filter_df(df, gaintype, range, circle, band, interference)





# 2) MMU Gain Prediction Visualization Project OJT

####   1. Apply filters for the user to start the Visualization

     -        Input file button to upload the *input* and *model* files to the web app 

     -        Radio items to select *Gain type* 

     -        Range slider to set a range on *Gain*

     -        Multi-dropdown to select *Circle* and *Bands*

####   2.  Sort the filtered data by *gain* value and visualize in table, bar charts

####   3.  Create a button for the user to export the filted data from the table into a csv file

####   4.  Create a SHAP value chart once a certain data on Table chart is selected

####   5. Create a bubble map to easily visualize the data from the table chart at one sight table 

####   6. Simple layout (using dash bootstrap components)

####   7. Let the app create a gain prediction file once the *input* and *model* files are uploaded
