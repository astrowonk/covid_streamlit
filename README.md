## Covid Case Counts with Streamlit

### [See the app running live here on Streamlit Cloud](https://covidcases.streamlitapp.com).

This is the source code for the [streamlit](https://streamlit.io) version of my [Covid Case Growth dash app](https://github.com/astrowonk/covid_dash), which you can see running live [here](https://marcoshuerta.com/dash/covid/).

The Dash version runs via [uwsgi](https://marcoshuerta.com/hugo/posts/deploying-uwsgi-for-dash/) on a Digital Ocean droplet with the data rebuilt daily into a SQlite database.

Because of the file size limitations of github (which Streamlit cloud hosting uses), the entire sqlite database can't be stored in this repository. I have developed a [private api in Flask](https://github.com/astrowonk/covid_dash/blob/main/rest_api.py) that serves the data from my existing sqlite database to this app when it runs live.
