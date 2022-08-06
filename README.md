## Covid Case Counts with Streamlit

### [See the app running live here on Streamlit Cloud](https://astrowonk-covid-streamlit-covid-streamlit-eis1xz.streamlitapp.com).

This is the source code for the [streamlit](https://streamlit.io) version of my [Covid Case Growth dash app](https://github.com/astrowonk/covid_dash), which you can see running live [here](https://marcoshuerta.com/dash/covid/).

The Dash version runs via [uwsgi](https://marcoshuerta.com/hugo/posts/deploying-uwsgi-for-dash/) on a Digital Ocean droplet with the data rebuilt daily into a SQlite database.

Because of the file size limitations of github (which Streamlit cloud hosting uses), the entire sqlite database can't be stored in this repository. I have developed a [private api in Flask](https://github.com/astrowonk/covid_dash/tree/api) that serves the data from the sqlite database to this app when it runs live.
