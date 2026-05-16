1, Tải Ollama trên ollama.com, chọn hệ điều hành phù hợp
2, Sau khi tải xong mở cmd trên máy tính, cài mô hình ngôn ngữ gemma (hoặc mô hình khác tuy chọn) với câu lệnh
        ollama run <tên mô hình>, với model gemma thì sẽ là: ollama run gemma3 
3, Sau khi tải model xong, cmd sẽ hiện dòng: send me a message, lúc này có thể gõ bất cứ một yêu cầu gì rồi enter xem nó có trả về kết quả oke ko
4, tắt cmd, rồi mở lại cmd gõ: ollama serve (để bật dịch vụ)
5, kiểm tra ollama đã được bật chưa khi truy cập vào link: http://localhost:11434/ 
    nếu nó hiện dòng chữ: ollama is running nghĩa là thành công



6, Tạo môi trường ảo (đối với folder em gửi nó đã có tất cả trong đó rồi, anh chỉ việc tạo môi trường ảo rồi open folder đấy trong môi trương ảo anh vừa tạo)
    bước 1: tạo môi trường ảo qua cmd -> python -m venv <tên thư mục sẽ chứa môi trg ảo>
    bước 2: khởi động môi trường ảo bằng -> scripts\activate trong cmd
    bước 3: sau đó gõ: code .
        cửa sổ sẽ chuyển hướng qua vscode, tạo môi trường ảo thành công!
    bước 4: mở terminal trong vscode vừa mở, pip install ollama vào môi trường ảo và tải về các thư viện cần cho dự án -> pip install <tên thư viện> 
            các thư viện cần tải em để trong tệp requirment.txt và requirment-dev.txt, anh tìm và install hết. 
            chương trình em đang chạy trên jupiter, anh chạy file summerize.ipynb nha, tìm nút run all ở trên nhé
            trước đó anh cần chọn kernel cho môi trường ảo, thì anh kiểm tra python anh đang dùng là phiên bản gì, rồi gõ tìm trên vscode
           
           

Các câu lệnh có thể có ích:
pip install -r <tên file txt> -> tự động tải về các thư viện đã liệt kê trong file này
pip freeze -> xem các thư viện đã cài trong môi trường hiện tại
pip show <tên thư viện> -> hiển thị thông tin về thư viện đó
deactivate -> tắt môi trường ảo
ctrl + C -> tắt môi trường ảo (ollama) an toàn khi không dùng 


