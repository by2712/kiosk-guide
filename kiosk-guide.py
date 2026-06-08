import pandas as pd
import streamlit as st
import anthropic

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
    list_a = df_results['연번'].tolist()

    client = anthropic.Anthropic(api_key=st.secrets['ANTHROPIC_API_KEY'])

    msg = ", ".join(df.apply(lambda x: f"{x['연번']}-{x['증명서']}", axis=1))

    response = client.messages.create(
        model = 'claude-sonnet-4-6',
        max_tokens = 100,
        system = '아래 목록에서만 골라서 연번만 쉼표로 답해. 다른말은 하지마.',
        messages = [{
            'role' : 'user',
            'content' : f'목록 : {msg}\n질문 : {content}'
        }]
    )

    result_text = response.content[0].text

    try:
        list_b = [int(x.strip()) for x in result_text.split(',')]
    except:
        list_b = []

    final_list = list(set(list_a + list_b))     # set : 중복값 제거, 자료형 set 형태

    df_final = df[df['연번'].isin(final_list)]

        
    for r, result in enumerate(df_final['증명서']):
        col1, col2 = st.columns([1, 5])
        col1.markdown(f'**{r+1}**')     # ** : 마크다운 볼드체 문법
        col2.button(result, use_container_width=True)

elif cancel:
    pass
