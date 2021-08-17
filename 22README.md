# samsung2020


-        MMU Gain Prediction Visualization Layout 간단하게 정리 후 구현 시작

   1. 사용자가 Visualization을 시작하기 위해 필요한 filter 적용

     -        Web app 에 Input & model 파일을 upload 할 수 있는 input file button

     -        Gain type 등을 선택 할 수 있는 Radio items

     -        Gain 의 range 를 적용시키기 위한 Range slider

     -        사용자가 원하는 Circle & Band 를 선택 할 수 있는 Multi-dropdown

   2.  그리고 그 필터 처리된 자료를 gain 순으로 sort 하여 table, bar chart로 표현

   3.  사용자가 적용한 필터에 해당되는 Table 자료를 csv file로 export 하는 버튼 제작

-       Dash library에 다양한 기능, 함수들이 있어서 이것저것 구경할 수 있어서 좋았다. 예를 들자면, 1년 전만 해도 사용자가 만든 data를 export하는 built-in 기능이 없었으나, 최신 버전 dash에서 built-in export button이 나와 사용자들이 더욱 쉽게 접근할 수 있게 되었다.


-       Table chart에 있는 데이터를 누를 시 그에 해당되는 SHAP value chart들을 구현

-       추가 구현: table 에 있는 자료를 한눈에 보기 쉬운 bubble map로 표현하기

-       레이아웃을 더욱 깔끔하게 정리 (dash bootstrap components 사용)

-       input & model 파일을 upload 할 때 앱이 스스로 하나의 gain prediction file 을 만들 수 있도록 구현
