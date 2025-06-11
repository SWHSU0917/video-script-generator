# utils.py
#import ssl_session
#import wikipedia.wikipedia  # ✅ 一定要 import 這個名稱

# ✅ 強制替換掉 requests.get
#wikipedia.wikipedia.requests.get = ssl_session.get
#print("Using patched requests.get:", wikipedia.wikipedia.requests.get)

from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper
from opencc import OpenCC
#import httpx

# 1. 獲得影片標題
# 2. 呼叫維基百科的API, 獲得相關訊息
# 3. 獲得影片的腳本內容
def generate_script(subject, video_length, creativity, api_key, api_model):
    title_template = ChatPromptTemplate.from_messages(
        [
            ("human", "請將'{subject}'這個主題的影片想一個吸引人的標題")
        ]
    )
    script_template = ChatPromptTemplate.from_messages(
        [
            (
                "human",
                """你是一位經營影片頻道的 YouTuber。請根據以下的標題與相關資訊，撰寫一支短影音的腳本。
                影片標題：{title}，影片長度：約 {duration} 分鐘，腳本內容請盡量符合影片時長。
                要求開頭要吸引目光，中段提供實用有料的內容，結尾則加入讓人驚喜的元素。
                腳本格式請依照【開頭、中段、結尾】三部分撰寫。
                整體風格要輕鬆有趣，能夠吸引年輕族群的注意力。
                腳本內容請不要有大陸用語，請以台灣繁體中文完全述說. 例如不要說短影音, 或者其他用語.
                你可以參考以下從維基百科搜尋到的資訊，僅擷取與主題相關的部分使用，無關的請忽略。:
                ```{wikipedia_search}```"""
            )
        ]
    )

    # 建立一個不驗證 SSL 憑證的 http client（⚠️ 測試用）
    #http_client = httpx.Client(verify=False)

    # 用 OpenAI 新版 SDK 初始化 client，整合所有參數
    model = ChatOpenAI(
        #model="gpt-4o-mini",
        model=api_model,
        temperature=creativity,
        #openai_api_key="sk-nkiTvXkslQzRogUF3574De012a124fCd829564Cf79F143C3",
        openai_api_key=api_key,
        openai_api_base="https://free.v36.cm/v1/",
        default_headers={"x-foo": "true"},
        #http_client=http_client,
    )

    title_chain = title_template | model
    title = title_chain.invoke({"subject": subject}).content

    search = WikipediaAPIWrapper(lang="zh")
    search_result = search.run(subject)

    cc = OpenCC('s2t')  # 簡體轉繁體
    search_big5_result = cc.convert(search_result)

    script_chain = script_template | model
    script_chain_response = script_chain.invoke({
        "title": subject,
        "duration": video_length,
        "wikipedia_search": search_big5_result
    })
    script = script_chain_response.content

    return search_big5_result, title, script

# print(generate_script("五月天", 1, 0.7, "sk-nkiTvXkslQzRogUF3574De012a124fCd829564Cf79F143C3"))