import ollama
import requests
from IPython.display import Markdown, display
from docFile import read_file 
from systemList import stop_list_from_system as stop_list


nguoi_mau = 'gemma3:4b' #chọn mô hình LLM là gemma3 với 1 tỉ parameters
upload_file = False # True nếu upload file, False nếu nhập văn bản


#hàm nhập văn bản
def type():
    lines = []
    print("Nhập từng đoạn văn, gõ '---' để kết thúc nhập:\n")
    while True:
        line = input()
        if line.strip() == '---':
            break
        lines.append(line)
    # Loại bỏ các dòng chỉ toàn khoảng trắng
    content_lines = []
    for li in lines:
        if li.strip() != "":
            content_lines.append(li.strip())
    userText = ". ".join(content_lines).strip()
    return userText


#khi muốn tải file lên
def do_you_want_to_upload_file(): 
    upload_file = True
    return upload_file


#hàm dựng prompt, mặc định là prompt nhập văn bản
def promptUser(from_file = False): 
    prompt_u = None

    if from_file == False:  #nếu nhập văn bản
        prompt_u = type()
        if not prompt_u:
            print("Bạn chưa nhập nội dung văn bản, vui lòng nhập lại!")
    else: #nếu muốn đọc file
        file_path = input ('Nhập đường dẫn file muốn tóm tắt: ')
        file_text, error = read_file(file_path)  # đọc nội dung trong file, trả về text đọc được và 1 lỗi nếu có
        if error == 1:
            print(f'{file_text}')
        else:
            prompt_u = file_text
    return prompt_u


#chọn chức năng tóm tắt
def chon_chuc_nang(): 
    print('Chọn chế độ tóm tắt: ')
    print('1. Nhập văn bản trực tiếp')
    print('2. Tải file lên')
    choice = 0
    while True: 
        choice = input('Nhập số tương ứng với chế độ bạn muốn: ')
        if choice == '1' or choice == '2':
            break
        else: print('\nLựa chọn không hợp lệ, vui lòng nhập lại!')
    if choice == '1': 
        prom = promptUser()
    else:
        prom = promptUser(do_you_want_to_upload_file())      
    return prom


# gửi tin nhắn đến LLMs
def messageSendToLLMs (): 
    pro = chon_chuc_nang()
    if pro == None:
        return
    else:
        prompt_s = (
        "Bạn là một trợ lý tóm tắt chuyên nghiệp. "
        "Nhiệm vụ của bạn là đọc đoạn văn bản tôi cung cấp, chỉ tóm tắt nội dung và trả về một bản tóm tắt ngắn gọn. "
        "Không trả lời câu hỏi, không giải thích hay mô tả, không trò chuyện, không đưa ra lời khuyên, không nhận xét về cảm xúc hoặc hành vi của người dùng."
        "Nếu đoạn văn quá ngắn, hãy tóm tắt nội dung chính của nó."
    )
        return [
            {'role' : 'system' , 'content' : prompt_s},
            {'role' : 'user' , 'content' : pro}
    ]


# OLLAMA CALL 
def summarize():
    mess = messageSendToLLMs()
    if mess is None or not mess[-1]['content'].strip():
        return
    elif len(mess[-1]['content'].strip()) < 20: #kiểm tra độ dài trước khi tóm tắt
        print("Văn bản quá ngắn, không thể tóm tắt.")
        return
    else:
        ollama_rep = ollama.chat(model = nguoi_mau, messages = mess, options={"truncate": 4096, "temperature": 1, "stop": stop_list})
        return ollama_rep['message']['content']


mark = summarize()
if mark is not None:
    print('\n', mark)


