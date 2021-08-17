MMU Gain Prediction Visualization Using Dash

 

Files, features 설명

-       File location:

        /home/sujin/PycharmProjects/hayung_dash

-       Necessary directories and files:

    1.   mmu_gain_webapp.py

      -        메인 파일

    2.   functions1.py (helper functions)

      -        predict_gain(contents, filename, filename1, filename2)

        model, input 파일 로드하고 예측한 csv 파일을 df로 리턴

      -        input_parse_contents(contents)

        input (.feather) 파일의 데이터를 읽고 df로 리턴

      -        empty_png()

        이전에 만들었던 shap value png 파일들을 모두 삭제

      -        plot_shap(filename1, filename2, gaintype, shaplist)
  

    3.  functions2.py (helper functions)

      -        get_max(mydf, gaintype)

      -        gain_pred_file()

      -        column_name(gaintype)

      -        filter_df(df, gaintype, range, circle, band, interference)
