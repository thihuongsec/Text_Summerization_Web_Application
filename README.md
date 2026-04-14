# Xây dựng ứng dụng web giúp tóm tắt văn bản dựa trên mô hình ngôn ngữ lớn LLMs
Với mục tiêu là xây dựng một ứng dụng web có khả năng tóm tắt văn bản tiếng Việt hiệu quả, cho phép người dùng tải lên file văn bản, url của một trang web hoặc nhập dữ liệu trực tiếp trên trường nhập liệu.

## Thiết kế hệ thống
<img width="925" height="929" alt="image" src="https://github.com/user-attachments/assets/5633d636-54d2-4d74-a0b3-1e4e795cee0f" />

## Yêu cầu và hướng dẫn cài đặt
### Yêu cầu
* Cài đặt Visual Code Studio, Python package tối thiểu 3.8 trở lên.
* Cài đặt Ollama, lựa chọn mô hình Gemma3 bản 4B và tải về.
* Cấu hình máy: tối thiểu ram 8Gb, ổ nhớ SSD tối thiểu 30Gb.
* Cài sẵn các thư viện và framework sau bằng công cụ pip install
### Hướng dẫn cài đặt
#### 1. Cài đặt Ollama
[Link download](https://apidog.com/vi/blog/how-to-download-and-use-ollama-vi/)

<img width="1006" height="344" alt="image" src="https://github.com/user-attachments/assets/2cf04e7d-0735-44a8-8989-13ff1635522a" />

Kết quả khi run ollama thành công, mở trình duyệt web để kiểm tra: [](http://localhost:11434/)

<img width="791" height="286" alt="image" src="https://github.com/user-attachments/assets/5725bdd6-79b7-4545-a68f-d6c02e6f2660" />

Tải modul LLMs về máy: `ollama run gemma3:4b`

<img width="959" height="138" alt="image" src="https://github.com/user-attachments/assets/f1f0bafb-a2a0-42dc-bf7b-ba2fe18fecc3" />

#### 2. Tạo môi trường ảo và kích hoạt
* `python -m venv SUMMERIZE_ENVIRONMENT`
* `scripts\activate`
#### 3. Truy cập môi trường ảo và code.
* Ngôn ngữ lựa chọn: Python, php
* Framework: Django
* Database: SQLite
* Giao diện sau khi hoàn tất

<img width="975" height="519" alt="image" src="https://github.com/user-attachments/assets/c673336e-aaec-4be9-b8f5-b0123839bdfa" />

## Kiểm thử chức năng
* Chức năng nhập văn bản và tóm tắt
<img width="754" height="685" alt="image" src="https://github.com/user-attachments/assets/753fb87d-70e3-4c40-b2c5-4d08f0d08396" />

* Chức năng tải file lên (docx, txt, pdf) và tóm tắt
<img width="778" height="643" alt="image" src="https://github.com/user-attachments/assets/22f82535-fd67-4770-847e-ab1bf9a9827c" />

* Chức năng dán url web để tóm tắt trang
<img width="765" height="384" alt="image" src="https://github.com/user-attachments/assets/d4f42f54-69e9-45fa-9914-b1f1299aef90" />

## Kết quả
* Chức năng nhập văn bản: []()
* Chức năng upload file: []()
* Chức năng dán url web: []()

## License
