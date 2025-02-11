import streamlit as st
from services.image_search import ImageSearch

st.title("VV表情包搜索器")

search_engine = ImageSearch()
user_input = st.text_input("请输入搜索关键词", "")

if user_input:
    results = search_engine.search(user_input)
    
    if results:
        st.write("找到以下匹配的表情包：")
        for i, result in enumerate(results, 1):
            st.image(result, caption=f"结果 {i}", use_column_width=True)
    else:
        st.warning("未找到匹配的表情包") 