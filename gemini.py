import streamlit as st
import google.generativeai as genai
import PyPDF2
import io

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def main():
    st.set_page_config(page_title="사내 학습 제도 안내 챗봇")
    
    st.title("🎓 사내 학습 제도 안내 챗봇")
    st.markdown("---")
    
    # 사이드바에 API 키 입력
    with st.sidebar:
        st.header("설정")
        api_key = st.text_input("Google API 키를 입력하세요:", type="password")
        st.markdown("---")
        uploaded_file = st.file_uploader("사내 학습 제도 PDF 파일을 업로드하세요", type=['pdf'])
    
    if api_key:
        genai.configure(api_key=api_key)
        
        if uploaded_file is not None:
            # PDF 내용을 세션 상태에 저장
            if 'pdf_content' not in st.session_state:
                st.session_state.pdf_content = extract_text_from_pdf(uploaded_file)
                st.success("PDF 파일이 성공적으로 업로드되었습니다!")
            
            # 채팅 기록 초기화
            if 'chat_history' not in st.session_state:
                st.session_state.chat_history = []
            
            # 채팅 인터페이스
            st.markdown("### 💬 사내 학습 제도에 대해 궁금한 점을 물어보세요!")
            
            # 이전 대화 내용 표시
            for chat in st.session_state.chat_history:
                if chat['role'] == 'user':
                    st.write(f"🙋‍♂️ **질문**: {chat['content']}")
                else:
                    st.write(f"🤖 **답변**: {chat['content']}")
            
            # 사용자 입력
            user_question = st.text_input("질문을 입력하세요:", key="user_input")
            
            if user_question:
                try:
                    # Gemini 모델 설정
                    model = genai.GenerativeModel('gemini-pro')
                    
                    # 프롬프트 작성
                    prompt = f"""
                    당신은 사내 학습 제도 안내 챗봇입니다. 
                    다음 문서 내용을 바탕으로 질문에 친절하고 정확하게 답변해주세요.
                    
                    문서 내용:
                    {st.session_state.pdf_content}
                    
                    질문: {user_question}
                    """
                    
                    # 응답 생성
                    response = model.generate_content(prompt)
                    
                    # 채팅 기록 저장
                    st.session_state.chat_history.append({"role": "user", "content": user_question})
                    st.session_state.chat_history.append({"role": "assistant", "content": response.text})
                    
                    # 페이지 새로고침
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {str(e)}")
        
        else:
            st.info("👈 사이드바에서 PDF 파일을 업로드해주세요.")
    else:
        st.warning("👈 사이드바에서 API 키를 입력해주세요.")

if __name__ == "__main__":
    main()