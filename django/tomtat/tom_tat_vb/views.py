from django.shortcuts import render, redirect
import ollama
from docFile import read_file
from systemList import stop_list_from_system as stop_list
import os
from .models import Data
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.urls import reverse

nguoi_mau = 'gemma3:4b'

def handle_text_input(lines):
    # Loại bỏ các dòng chỉ toàn khoảng trắng
    content_lines = [li.strip() for li in lines if li.strip() != ""]
    userText = ". ".join(content_lines).strip()
    return userText

def split_text(text, chunk_size=4000, chunk_overlap=200):
    # Chia text thành các đoạn nhỏ, không cắt ở giữa từ
    chunks = []
    start = 0
    length = len(text)
    while start < length:
        end = min(start + chunk_size, length)
        # Đảm bảo không cắt giữa từ
        if end < length:
            while end > start and text[end-1] not in [' ', '\n', '.', '?', '!']:
                end -= 1
            if end == start:
                end = min(start + chunk_size, length)  # Nếu không tìm được, cứ cắt luôn
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - chunk_overlap  # overlap
        if start < 0:
            start = 0
    return chunks

def giao_dien(request):
    summary = ''
    error = ''
    input_text = ''
    input_url = ''
    dochinhxac = 70  # Độ chính xác mặc định
    output_length = 'medium'
    style = 'academic'
    if request.method == 'POST':
        mode = request.POST.get('mode', 'text')
        dochinhxac = int(request.POST.get('dochinhxac', 80))
        output_length = request.POST.get('output_length', 'medium')
        style = request.POST.get('style', 'academic')
        user_input = ''
        if mode == 'file' and request.FILES.get('file_upload'):
            file = request.FILES['file_upload']
            upload_dir = os.path.join(os.path.dirname(__file__), '../../upLoad')
            upload_dir = os.path.abspath(upload_dir)
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, file.name)
            with open(file_path, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            file_text, err = read_file(file_path)
            if err == 1 or not file_text or file_text.strip() == "":
                error = file_text or "File rỗng, không thể trích xuất nội dung."
            else:
                user_input = file_text
        elif mode == 'url':
            input_url = request.POST.get('input_url', '').strip()
            if not input_url:
                error = "Bạn chưa nhập URL, vui lòng nhập lại!"
            else:
                try:
                    import requests
                    from bs4 import BeautifulSoup
                    resp = requests.get(input_url, timeout=10)
                    resp.encoding = resp.apparent_encoding
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    # Lấy nội dung chính (ưu tiên thẻ article, nếu không lấy toàn bộ text)
                    article = soup.find('article')
                    if article:
                        user_input = article.get_text(separator=' ', strip=True)
                    else:
                        user_input = soup.get_text(separator=' ', strip=True)
                    # Kiểm tra nội dung thực sự có ý nghĩa hay không
                    if not user_input or len(user_input.strip()) < 30:
                        error = "Không thể trích xuất văn bản trong URL này."
                    else:
                        # Nếu chỉ có 1 dòng hoặc chỉ là tiêu đề, cũng báo lỗi
                        lines = [line.strip() for line in user_input.split('\n') if line.strip()]
                        if len(lines) <= 1 and len(user_input.strip()) < 60:
                            error = "Không thể trích xuất văn bản trong URL này."
                except Exception as e:
                    error = f"Lỗi khi lấy nội dung từ URL: {e}"
        else:
            input_text = request.POST.get('input_text', '')
            lines = input_text.split('\n')
            user_input = handle_text_input(lines)
            if not user_input:
                error = "Không có nội dung để tóm tắt, vui lòng nhập lại!"
        # Nếu không có lỗi, gọi Ollama
        if not error and user_input and len(user_input.strip()) >= 30:
            def get_prompt(dochinhxac, output_length, style):
                length_map = {
                    'short': 'Hãy tóm tắt thật ngắn gọn, chỉ giữ lại ý chính nhất, tối đa 3-5 câu.',
                    'medium': 'Hãy tóm tắt với độ dài trung bình, giữ lại các ý chính quan trọng, tối đa 8-12 câu.',
                    'long': 'Hãy tóm tắt chi tiết, đầy đủ ý chính, sát với nội dung gốc, tối đa 15-20 câu.'
                }
                style_map = {
                    'academic': 'Viết theo phong cách học thuật, trang trọng, rõ ràng, súc tích. Bắt chước mẫu sau: Hệ thống giám sát mạng được triển khai nhằm phát hiện và xử lý các cuộc tấn công mạng trong thời gian thực. Bằng cách tích hợp các thuật toán học máy, hệ thống có thể phân tích luồng dữ liệu và nhận diện các hành vi bất thường, qua đó hỗ trợ cảnh báo sớm các mối đe dọa tiềm ẩn.',
                    'funny': 'Viết theo phong cách vui vẻ, hài hước, thân thiện, dễ tiếp cận. Bắt chước mẫu sau: Hệ thống này giống như một chú chó canh cổng mạng – ngửi thấy mùi khả nghi là sủa lên ngay! Nó dùng bộ não AI để soi từng luồng dữ liệu, và nếu phát hiện điều gì lạ lạ… thì kẻ tấn công nên biết điều mà biến!',
                    'creative': 'Viết theo phong cách sáng tạo, mới mẻ, sinh động, truyền cảm hứng. Bắt chước mẫu sau Trong thế giới số ồn ào, có một vệ sĩ âm thầm đứng gác: gã quan sát viên không bao giờ ngủ. Hắn lắng nghe từng nhịp dữ liệu, nhìn sâu vào dòng sông số, và khi có kẻ lạ lén lút bước vào… hắn đã biết từ hơi thở đầu tiên.',
                    'professional': 'Viết theo phong cách chuyên nghiệp, nghiêm túc, chính xác, phù hợp với môi trường công việc. Bắt chước mẫu sau: Hệ thống sử dụng AI để giám sát và phát hiện tấn công mạng theo thời gian thực, giúp tổ chức phản ứng kịp thời với rủi ro an ninh mạng.'
                }
                length_instruction = length_map.get(output_length, length_map['short'])
                style_instruction = style_map.get(style, style_map['creative'])
                
                if dochinhxac >= 80:
                    accuracy_instruction = "Giữ lại khoảng 70% từ khoá, ý chính và cấu trúc của bản gốc."
                elif dochinhxac >= 60:
                    accuracy_instruction = "Giữ lại khoảng 50% từ khoá, ý chính quan trọng của bản gốc."
                elif dochinhxac >= 40:
                    accuracy_instruction = "Giữ lại khoảng 30% từ khoá, ý chính quan trọng nhất của bản gốc."
                else:
                    accuracy_instruction = "Chỉ giữ lại ý chính nhất, không cần bám sát từ ngữ gốc."
                return (
                    "Bạn là một trợ lý tóm tắt chuyên nghiệp. Có 10 năm kinh nghiệm làm tóm tắt nội dung cho một công ty chuyên xử lí văn bản."
                    "Nhiệm vụ của bạn là đọc đoạn văn bản tôi cung cấp và trả về bản tóm tắt tiếng Việt. "
                    f"Tóm tắt theo yêu cầu sau: Độ chính xác so với input: {accuracy_instruction} {length_instruction} {style_instruction}"
                    "Bạn không trả lời câu hỏi, không giải thích hay mô tả, không trò chuyện, không đưa ra lời khuyên, không nhận xét về cảm xúc hoặc hành vi của tôi."
                    "Trình bày bản tóm tắt theo dạng văn bản thuần túy, không có định dạng HTML hay Markdown."
                )
            # Nếu input quá dài, chia nhỏ và tóm tắt từng phần
            if len(user_input) > 4000:
                chunks = split_text(user_input, chunk_size=4000, chunk_overlap=200)
                chunk_summaries = []
                for chunk in chunks:
                    prompt_s = get_prompt(dochinhxac, output_length, style)
                    messages = [
                        {'role': 'system', 'content': prompt_s},
                        {'role': 'user', 'content': chunk}
                    ]
                    try:
                        ollama_rep = ollama.chat(
                            model=nguoi_mau,
                            messages=messages,
                            options={"truncate": 4096, "temperature": 1, "stop": stop_list}
                        )
                        chunk_summaries.append(ollama_rep['message']['content'])
                    except Exception as e:
                        error = f"Lỗi khi tóm tắt đoạn văn bản: {e}"
                        break
                if not error:
                    # Tổng hợp lại các tóm tắt nhỏ thành 1 bản tóm tắt chung
                    summary_input = '\n'.join(chunk_summaries)
                    prompt_final = get_prompt(dochinhxac, output_length, style)
                    messages_final = [
                        {'role': 'system', 'content': prompt_final},
                        {'role': 'user', 'content': summary_input}
                    ]
                    try:
                        ollama_rep = ollama.chat(
                            model=nguoi_mau,
                            messages=messages_final,
                            options={"truncate": 4096, "temperature": 1, "stop": stop_list}
                        )
                        summary = ollama_rep['message']['content']
                    except Exception as e:
                        error = f"Lỗi khi tổng hợp tóm tắt: {e}"
            else:
                prompt_s = get_prompt(dochinhxac, output_length, style)
                messages = [
                    {'role': 'system', 'content': prompt_s},
                    {'role': 'user', 'content': user_input}
                ]
                try:
                    ollama_rep = ollama.chat(
                        model=nguoi_mau,
                        messages=messages,
                        options={"truncate": 4096, "temperature": 1, "stop": stop_list}
                    )
                    summary = ollama_rep['message']['content']
                except Exception as e:
                    error = f"Lỗi khi gọi Ollama: {e}"
            if not error:
                # Lưu lịch sử vào database
                Data.objects.create(data_input=user_input, data_output=summary)
                # Lưu vào session và redirect để tránh lặp bản ghi khi reload
                request.session['summary'] = summary
                request.session['input_text'] = input_text
                request.session['input_url'] = input_url
                request.session['dochinhxac'] = dochinhxac
                request.session['output_length'] = output_length
                request.session['style'] = style
                request.session['error'] = ''
                return redirect('giao_dien')
        elif not error and user_input and len(user_input.strip()) < 20:
            error = "Văn bản quá ngắn, không thể tóm tắt."
        if error:
            request.session['summary'] = ''
            request.session['input_text'] = input_text
            request.session['input_url'] = input_url
            request.session['error'] = error
            return redirect('giao_dien')
    else:
        # Lấy kết quả từ session nếu có
        summary = request.session.pop('summary', '')
        input_text = request.session.pop('input_text', '')
        input_url = request.session.pop('input_url', '')
        dochinhxac = request.session.pop('dochinhxac', 80)
        output_length = request.session.pop('output_length', 'medium')
        style = request.session.pop('style', 'academic')
        error = request.session.pop('error', '')
    # Lấy lịch sử tóm tắt
    history = Data.objects.order_by('-id')[:10]
    return render(request, 'tom_tat_vb/giao_dien.html', {
        'summary': summary,
        'input_text': input_text,
        'input_url': input_url,
        'dochinhxac': dochinhxac,
        'output_length': output_length,
        'style': style,
        'error': error,
        'history': history
    })

def delete_history(request, id):
    if request.method == 'POST':
        try:
            Data.objects.filter(id=id).delete()
        except Exception:
            pass
    return HttpResponseRedirect(reverse('giao_dien'))
