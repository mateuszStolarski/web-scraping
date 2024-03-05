import logging

import pandas as pd
import streamlit as st
from pymongo import MongoClient
from settings.base import AppSettings

st.header("Welcome to the Streamlit web-scrapping demo ✨")

_settings = AppSettings()
_client = MongoClient(_settings.connection_string)
_databse = _client["scrapper"]
_collections = _databse.list_collection_names()

logging.info(_collections)
if _collections:
    option = st.selectbox(
        "Choose data source",
        tuple(_collections),
    )

    collection = _databse[option]
    df = pd.DataFrame(
        list(
            collection.find(
                {},
                {"_id": 0, "likes": 1, "number_of_comments": 1},
            )
        )
    )

    min_likes, max_likes = min(df["likes"]), max(df["likes"])
    min_comments, max_comments = min(df["number_of_comments"]), max(
        df["number_of_comments"]
    )

    likes = st.slider(
        "Range - number of likes:",
        min_value=min_likes,
        max_value=max_likes,
        value=(min_likes, max_likes),
    )

    comments = st.slider(
        "Range - number of comments:",
        min_value=min_comments,
        max_value=max_comments,
        value=(min_comments, max_comments),
    )

    df = pd.DataFrame(
        list(
            collection.find(
                {
                    "likes": {"$gte": likes[0], "$lte": likes[1]},
                    "number_of_comments": {"$gte": comments[0], "$lte": comments[1]},
                },
                {
                    "_id": 0,
                    "index": 0,
                },
            )
        )
    )
    st.dataframe(df)
