import streamlit as st
import random
from services.image_search import ImageSearch
from config.settings import Config

# 页面配置
st.set_page_config(
    page_title="VV表情包搜索器",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

default_api_key = Config.SILICON_API_KEY
search_engine = ImageSearch()

# 搜索框提示语列表
SEARCH_PLACEHOLDERS = [
    "如何看待Deepseek？",
    "如何看待六代机？",
    "如何看待VVQuery？",
    "如何看待张维为？",
    "如何看待...？",
]

st.title("VV表情包搜索器")

# 初始化session state
if 'placeholder' not in st.session_state:
    st.session_state.placeholder = random.choice(SEARCH_PLACEHOLDERS)
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""
if 'n_results' not in st.session_state:
    st.session_state.n_results = 5
if 'api_key' not in st.session_state:
    st.session_state.api_key = default_api_key

# 搜索函数
def search():
    if not st.session_state.search_query:
        return
    try:
        with st.spinner('Searching'):
            results = search_engine.search(
                st.session_state.search_query, 
                st.session_state.n_results,
                st.session_state.api_key
            )
            return results if results else []
    except Exception as e:
        st.sidebar.error(f"搜索失败: {e}")
        return []

# 回调函数
def on_input_change():
    st.session_state.search_query = st.session_state.user_input
    st.session_state.results = search()

def on_slider_change():
    st.session_state.n_results = st.session_state.n_results_widget
    if st.session_state.search_query:
        st.session_state.results = search()

def on_api_key_change():
    st.session_state.api_key = st.session_state.api_key_input

# 侧边栏搜索区域
with st.sidebar:
    st.title("🔍 VV智能回应")
    user_input = st.text_input(
        "请输入搜索关键词", 
        value=st.session_state.search_query,
        placeholder=st.session_state.placeholder,
        key="user_input",
        on_change=on_input_change
    )
    
    api_key = st.text_input(
        "请输入 SILICON API Key", 
        value=st.session_state.api_key,
        type="password",
        key="api_key_input",
        on_change=on_api_key_change
    )
    
    n_results = st.slider(
        "选择展示的结果数量", 
        1, 30, 
        value=st.session_state.n_results,
        key="n_results_widget",
        on_change=on_slider_change
    )
    
    search_button = st.button("搜索", use_container_width=True, on_click=on_input_change)

# 主区域显示
if not st.session_state.get("results"):
    # 初始页面显示欢迎信息
    st.title("👋 Welcome！")
    st.markdown("""
                在左侧的侧边栏输入或者点击左上角的箭头以开始。
                """)
else:
    # 显示搜索结果
    results = st.session_state.results
    if results:
        # 使用列布局显示图片
        cols = st.columns(3)  # 在一行中显示3张图片
        for i, result in enumerate(results):
            with cols[i % 3]:
                st.image(result, use_container_width=True)
    else:
        st.sidebar.warning("未找到匹配的表情包") 

# 添加页脚
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
    
    🌟 关注我 | Follow Me 🌟
    
    👨‍💻 [GitHub](https://github.com/DanielZhangyc) · 
    📺 [哔哩哔哩](https://space.bilibili.com/165404794) · 
    📝 [博客](https://www.xy0v0.top/)
    </div>
    """, 
    unsafe_allow_html=True
) 