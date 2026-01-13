import os
import streamlit as st
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# 1) .env を読み込む（OPENAI_API_KEY を使えるようにする）
load_dotenv()

# 2) 画面設定
st.set_page_config(page_title="専門家AI相談アプリ", page_icon="🤖")
st.title("🤖 専門家AI相談アプリ")

st.write("""
このアプリでは、**専門家の種類**を選んでAIに相談できます。

### 使い方
1. ラジオボタンで専門家を選択  
2. 質問・相談内容を入力  
3. 「送信」を押すとAIが回答します
""")

# 3) APIキー確認（無いと動かないのでここで止める）
if not os.getenv("OPENAI_API_KEY"):
    st.error("OPENAI_API_KEY が設定されていません。.env を確認してください。")
    st.stop()

# 4) 専門家選択（ラジオ）
expert = st.radio(
    "専門家を選択してください",
    ["A：やさしいプログラミング講師", "B：ビジネス戦略コンサルタント"]
)

# 5) 入力フォーム（1つ）
user_input = st.text_input("質問・相談内容を入力してください（例：Streamlitって何？）")

# 6) 条件：入力テキスト＋選択値を受け取り、回答文字列を返す関数
def ask_llm(text: str, expert_type: str) -> str:
    if expert_type.startswith("A"):
        system_message = (
            "あなたはやさしいプログラミング講師です。"
            "中学生にもわかる言葉で、短い具体例を交えて説明してください。"
        )
    else:
        system_message = (
            "あなたはビジネス戦略コンサルタントです。"
            "結論→理由→具体例→次の行動、の順で簡潔に答えてください。"
        )

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=text),
    ]

    response = llm.invoke(messages)
    return response.content

# 7) 実行ボタン → 画面に表示
if st.button("送信"):
    if not user_input.strip():
        st.warning("質問内容を入力してください。")
    else:
        with st.spinner("AIが回答中..."):
            answer = ask_llm(user_input, expert)
        st.subheader("回答")
        st.write(answer)
