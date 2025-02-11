import streamlit as st
from services.image_search import ImageSearch
from config.settings import Config

default_api_key = Config.SILICON_API_KEY

st.title("VV表情包搜索器")

search_engine = ImageSearch()
user_input = st.text_input("请输入搜索关键词", "")

api_key = st.text_input("请输入 SILICON API Key", value=default_api_key, type="password")
n_results = st.slider("选择展示的结果数量", 1, 10, 5)

if user_input:
    results = search_engine.search(user_input, n_results, api_key)
    
    if results:
        st.write("找到以下匹配的表情包：")
        for i, result in enumerate(results, 1):
            st.image(result, caption=f"结果 {i}")
    else:
        st.warning("未找到匹配的表情包") 