from docx import Document 
import pdfplumber
import textract  
import os 

def read_file(file_path):
    try:
        file_extension = os.path.splitext(file_path)[1].lower()

        if file_extension == '.docx' :
            doc = Document(file_path)
            text_docx = []
            for para in doc.paragraphs:
                text_docx.append(para.text)
            content = '. '.join(text_docx).strip()
            if not content:
                return 'File rỗng, không thể trích xuất nội dung', 1
            else:
                print ('Nội dung trong file: ', content)
                return content, 0
        
        elif file_extension == '.txt':
            with open(file_path, 'r', encoding='utf-8') as faifai:
                text_txt = faifai.read().strip()
                if not text_txt:
                    return 'File rỗng, không thể trích xuất nội dung', 1
                else:
                    print('Nội dung trong file: ',text_txt)
                    return text_txt, 0
                
        elif file_extension == '.pdf':
            try:
                with pdfplumber.open(file_path) as pdf:
                    text_pdf = []
                    for page in pdf.pages:
                        text_page = page.extract_text()
                        text_pdf.append(text_page)
                content = '. '.join([t for t in text_pdf if t]).strip()
                if not content:
                    return 'File rỗng, không thể trích xuất nội dung', 1
                else:
                    print('Nội dung trong file: ', content)
                    return content, 0
            except Exception:
                return 'xin lỗi, chúng tôi không thể trích xuất văn bản từ file PDF này', 1
        else:
            return f'Định dạnh file {file_extension} không được hỗ trợ.', 1
    except Exception as e:
        return 'Lỗi {e}, bạn hãy thử lại hoặc thử một file khác', 1

#read_file('D:\TP HCM.txt') 
