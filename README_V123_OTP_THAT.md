# V12.3 - Gửi OTP thật về số điện thoại

Bản này đã tích hợp **gửi OTP thật** qua nhà cung cấp SMS. Mặc định tôi cấu hình theo hướng **eSMS** vì phù hợp dùng tại Việt Nam; ngoài ra code cũng có sẵn nhánh **Twilio Verify**.

## 1) Chuẩn bị cấu hình
- Copy file `.env.example` thành `.env`
- Điền khóa API của nhà cung cấp SMS

### Nếu dùng eSMS
- `ESMS_API_KEY`
- `ESMS_SECRET_KEY`
- `ESMS_BRANDNAME`
- `OTP_PROVIDER=esms`

### Nếu dùng Twilio Verify
- `OTP_PROVIDER=twilio`
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_VERIFY_SERVICE_SID`

## 2) Chạy hệ thống
```powershell
.\deploy\02_CAI_THU_VIEN.bat
.\deploy\01_KHOI_DONG_HE_THONG.bat
```

## 3) Lưu ý quan trọng
- **Không có API key/secret thì không thể gửi OTP thật**.
- Với số điện thoại Việt Nam, eSMS là lựa chọn thực tế hơn cho triển khai nội bộ/cơ quan.
- Nếu dùng Twilio để gửi SMS về Việt Nam, cần tuân thủ yêu cầu brand/application name trong nội dung tin nhắn. Twilio cũng khuyến nghị sender đã đăng ký cho Việt Nam. citeturn0search25turn0search16
- eSMS cung cấp API key/secret để tích hợp SMS API và có tài liệu gửi OTP/SMS Brandname. citeturn0search2turn0search5turn0search7