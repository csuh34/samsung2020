MMU Gain Prediction Visualization Using Dash

 

Files, features explanation

-       File location:

        /home/sujin/PycharmProjects/hayung_dash

-       Necessary directories and files:

    1.   mmu_gain_webapp.py

      -        main file of the project

    2.   functions1.py (helper functions)

      -        predict_gain(contents, filename, filename1, filename2)

          loads the *model*, *input* files and returns the predicted csv file to *df* 

      -        input_parse_contents(contents)

          reads the data from the *input (.feather)* file and return to *df* 

      -        empty_png()

          deletes all the previous shap value png files

      -        plot_shap(filename1, filename2, gaintype, shaplist)
  

    3.  functions2.py (helper functions)

      -        get_max(mydf, gaintype)

      -        gain_pred_file()

      -        column_name(gaintype)

      -        filter_df(df, gaintype, range, circle, band, interference)
