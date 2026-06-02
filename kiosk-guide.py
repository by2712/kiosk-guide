import pandas as pd
import streamlit as st

df = pd.read_excel('무인민원발급기_증명서_목록.xlsx')

st.title('민원톡')
st.write('자연어를 입력 받아 적합한 증명서를 표시합니다')

with st.form('입력창', clear_on_submit=True):
    content = st.text_input('발급을 원하시는 증명서 또는 관련 업무를 입력해주세요')
    btn_submitted, btn_cancel = st.columns(2)
    submitted = btn_submitted.form_submit_button('확인', use_container_width=True)
    cancel = btn_cancel.form_submit_button('취소', use_container_width=True)

if submitted:
    df_results = df[df['키워드'].str.contains(content)]
    df_results.index += 1

    # rows_count = len(df_results)
        
    for r, result in enumerate(df_results['증명서']):
        col1, col2 = st.columns([1, 5])
        col1.markdown(f'**{r+1}**')
        col2.button(result, use_container_width=True)

elif cancel:
    pass
