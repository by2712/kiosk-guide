import streamlit as st
import json
import os

if (os.path.exists('petition_save.json') and
    os.path.getsize('petition_save.json') > 0):
    with open('petition_save.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
else:
    data = []

st.title('민원톡 자연어 저장 페이지')
st.write('타이핑한 자연어를 json파일에 저정하는 에이전트입니다')

with st.form('민원입력', clear_on_submit=True):
    name = st.text_input('성명', '')
    birth = st.text_input('생년월일', '')
    content = st.text_input('필요한 민원서류 또는 업무', '')
    btn_submitted, btn_cleared = st.columns(2)
    submitted = btn_submitted.form_submit_button('확인')
    cleared = btn_cleared.form_submit_button('저장된 자료 초기화')

for item in data:
    col1, col2, col3 = st.columns(3)
    col1.write(item['name'])
    col2.write(item['birth'])
    col3.write(item['content'])

if submitted:
    dic_append = {
        'name' : name,
        'birth' : birth,
        'content' : content
    }

    data.append(dic_append)

    with open('petition_save.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

    st.rerun()

if cleared:
    data = []

    with open('petition_save.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

    st.rerun()
