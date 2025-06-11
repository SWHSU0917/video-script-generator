import streamlit as st
from utils import generate_script

st.title("影片腳本產生器")

with st.sidebar:
    openai_api_model = st.text_input("請輸入OpenAI 模型:")
    openai_api_key = st.text_input("請輸入OpenAI API密鑰: ", type="password")
    st.markdown("[獲取OpenAI API密鑰](https://platform.openai.com/account/api-keys)")

subject = st.text_input("請輸入影片的主題")
video_length = st.number_input("請輸入影片的長度(單位: 分鐘)", min_value=0.1, step=0.1)
creativity = st.slider("請輸入影片腳本的創造力(數字小說明更嚴謹, 數字大說明更多樣)", min_value=0.0, max_value=1.0, value=0.2, step=0.1)

submit = st.button("產生腳本")


if submit and not openai_api_model:
    st.info("請輸入你的OpenAI模型")
    st.stop()
if submit and not openai_api_key:
    st.info("請輸入你的OpenAI API密鑰")
    st.stop()
if submit and not subject:
    st.info("請輸入影片的主題")
    st.stop()
if submit and not video_length >= 0.1:
    st.info("影片長度需要大於或等於0.1分鐘")
    st.stop()
if submit:
    with st.spinner(("AI正在思考中, 請等候...")):
        search_result, title, script = generate_script(subject, video_length, creativity, openai_api_key, openai_api_model)
    st.success("影片腳本已產生! ")

    st.subheader("影片標題: ")
    st.write(title)

    st.subheader("影片腳本: ")
    st.write(script)

    with st.expander("維基百科搜索結果: "):
        st.info(search_result)