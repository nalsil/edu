import streamlit as st
import openai
import time
from openai import OpenAI
import json

# Streamlit 페이지 설정
st.set_page_config(page_title="OpenAI Assistant Chatbot", page_icon="🤖")
st.title("OpenAI Assistant Chatbot")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

# API 키 입력 섹션
api_key = st.text_input("OpenAI API Key를 입력하세요:", type="password")

if api_key:
    # OpenAI 클라이언트 설정
    client = OpenAI(api_key=api_key)
    assistant_id = "asst_6kv6EB0EsMT7HjIXfdZgpfci"

    # 새 스레드 생성 (첫 실행시)
    if st.session_state.thread_id is None:
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id

    # 메시지 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력
    if prompt := st.chat_input("메시지를 입력하세요."):
        # 사용자 메시지 표시
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Assistant에 메시지 전송
        message = client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content=prompt
        )

        # 실행 생성 및 응답 대기
        run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=assistant_id
        )

        # 실행 완료 대기
        with st.spinner('응답을 생성하고 있습니다...'):
            while run.status != 'completed':
                time.sleep(1)
                run = client.beta.threads.runs.retrieve(
                    thread_id=st.session_state.thread_id,
                    run_id=run.id
                )

        # 응답 메시지 가져오기
        messages = client.beta.threads.messages.list(
            thread_id=st.session_state.thread_id
        )

        # 최신 응답 표시
        # assistant_message = messages.data[0].content[0].text.value
        assistant_message = messages
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})
        with st.chat_message("assistant"):
            st.markdown(assistant_message)

else:
    st.warning("계속하려면 OpenAI API 키를 입력하세요.")