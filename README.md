# Movie Recommender

App develoved with [Streamlit](https://streamlit.io/) using the [Movie-Lens dataset](https://www.kaggle.com/rounakbanik/the-movies-dataset)

![](demo.gif)

<p align="center">
<a href="https://movie-recommender-streamlit.herokuapp.com/" target="blank">
    <img align="center" src="https://img.shields.io/badge/LINK TO HEROKU-6762A6?style=for-the-badge&logo=heroku&logoColor=white"/>
</a>  

## Usage

0. Install [anaconda](https://www.anaconda.com/products/individual).

1. Create a virtual environment:

```bash
conda create -n env_recommender_streamlit python=3.7
conda activate env_recommender_streamlit
```
2. Clone this repository

```bash
git clone https://github.com/jmonsalverodilla/Recommender-Systems.git
cd Recommender-Systems
```

3. Install requirements:

```bash
pip install -r requirements.txt
```

4. Run the app:

```bash
streamlit run main.py --server.runOnSave True
```

## License

This repo is under the [MIT License](LICENSE).