import csv, random, time, os, requests
from io import StringIO
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates

load_dotenv()
app = FastAPI(title="Đảng ủy xã Ea Kiết - Quản lý nhiệm vụ V12.5")
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

ROLE_CATALOG = [
    {"name":"admin","desc":"Quản trị hệ thống","perm":"Toàn quyền, quản lý người dùng, cấu hình, sao lưu"},
    {"name":"thường trực","desc":"Vai trò Thường trực Đảng ủy","perm":"Xem tổng hợp, giao việc, phê duyệt, đánh giá"},
    {"name":"văn phòng","desc":"Văn phòng Đảng ủy","perm":"Tiếp nhận công văn, tạo việc, báo cáo, nhắc việc"},
    {"name":"ban xây dựng đảng","desc":"Ban xây dựng Đảng","perm":"Quản lý công việc lĩnh vực xây dựng Đảng, đảng viên, tổ chức"},
    {"name":"UBKT","desc":"Ủy ban kiểm tra","perm":"Quản lý nhiệm vụ kiểm tra, giám sát, kết luận, theo dõi khắc phục"},
    {"name":"chuyên viên","desc":"Chuyên viên","perm":"Nhận việc, cập nhật tiến độ, báo cáo"},
]
USERS = [
    {"username":"admin","password":"123456","full_name":"Quản trị hệ thống","role":"admin","phone":"0912345678","status":"Hoạt động","email":"admin@eakiet.local"},
    {"username":"thuongtruc","password":"123456","full_name":"Thường trực Đảng ủy","role":"thường trực","phone":"0978123456","status":"Hoạt động","email":"tt@eakiet.local"},
    {"username":"vanphong","password":"123456","full_name":"Văn phòng Đảng ủy","role":"văn phòng","phone":"0987123456","status":"Hoạt động","email":"vp@eakiet.local"},
    {"username":"bandx","password":"123456","full_name":"Ban xây dựng Đảng","role":"ban xây dựng đảng","phone":"0965123456","status":"Hoạt động","email":"bdx@eakiet.local"},
    {"username":"ubkt","password":"123456","full_name":"Ủy ban kiểm tra","role":"UBKT","phone":"0932123456","status":"Hoạt động","email":"ubkt@eakiet.local"},
]
ASSIGNMENTS = [
    {"title":"Rà soát hồ sơ đảng viên quý III","description":"Kiểm tra, bổ sung hồ sơ đảng viên còn thiếu","category":"Xây dựng Đảng","priority":"Cao","due_date":"2026-07-30","assignee_username":"bandx","status":"Đang thực hiện","progress":"55%"},
    {"title":"Báo cáo công tác kiểm tra 6 tháng","description":"Hoàn thiện báo cáo UBKT 6 tháng đầu năm","category":"UBKT","priority":"Cao","due_date":"2026-07-25","assignee_username":"ubkt","status":"Chờ duyệt","progress":"90%"},
]
AUDIT_LOGS = [{"time":"vừa xong","text":"Khởi tạo gói V12.5 giao diện đẹp"}]
OTP_STORE = {}
NOTICES = [
    {"title":"Nhắc tiến độ nhiệm vụ tháng","content":"Các bộ phận cập nhật tiến độ nhiệm vụ trước 16h thứ Sáu hàng tuần."},
    {"title":"Kiểm tra hồ sơ đảng viên","content":"Ban xây dựng Đảng rà soát hồ sơ còn thiếu trong tháng này."}
]

def current_user(request: Request):
    username = request.cookies.get("auth_user")
    return next((u for u in USERS if u["username"] == username), None) if username else None

def guard(request: Request):
    return None if current_user(request) else RedirectResponse("/login", status_code=303)

def otp_expire_seconds(): return int(os.getenv("OTP_EXPIRE_SECONDS", "300"))
def send_sms_esms(phone: str, content: str):
    url = "https://rest.esms.vn/MainService.svc/json/SendMultipleMessage_V4_post_json/"
    payload = {"ApiKey": os.getenv("ESMS_API_KEY",""), "SecretKey": os.getenv("ESMS_SECRET_KEY",""), "Content": content, "Phone": phone, "SmsType": int(os.getenv("ESMS_SMS_TYPE","2")), "Brandname": os.getenv("ESMS_BRANDNAME", os.getenv("OTP_SENDER_NAME","EAKIET"))}
    r = requests.post(url, json=payload, timeout=20)
    return r.status_code, r.text
def send_otp_real(phone: str, otp: str):
    return send_sms_esms(phone, f"[EAKIET] Ma OTP dat lai mat khau cua ban la {otp}. Hieu luc {otp_expire_seconds()//60} phut.")
def verify_otp_local(phone: str, otp: str):
    s = OTP_STORE.get(phone)
    if not s: return False, "Không tìm thấy OTP"
    if time.time() - s["created"] > otp_expire_seconds(): return False, "OTP đã hết hạn"
    if s["otp"] != otp: return False, "OTP không đúng"
    return True, "OK"

def stats_for(user):
    mine = [a for a in ASSIGNMENTS if a["assignee_username"] == user["username"]]
    return {
        "users": len(USERS),
        "tasks": len(ASSIGNMENTS),
        "mine": len(mine),
        "done": len([a for a in ASSIGNMENTS if a["status"] == "Hoàn thành"]),
    }

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request, msg: str = ""):
    return templates.TemplateResponse("login.html", {"request": request, "msg": msg})

@app.post("/login")
async def do_login(username: str = Form(...), password: str = Form(...)):
    user = next((u for u in USERS if u["username"] == username and u["password"] == password and u["status"] == "Hoạt động"), None)
    if not user: return RedirectResponse("/login?msg=Sai tài khoản hoặc mật khẩu", status_code=303)
    resp = RedirectResponse("/", status_code=303); resp.set_cookie("auth_user", user["username"], httponly=True, samesite="lax"); return resp

@app.get("/logout")
def logout():
    resp = RedirectResponse("/login?msg=Đã đăng xuất", status_code=303); resp.delete_cookie("auth_user"); return resp

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    g = guard(request)
    if g: return g
    me = current_user(request)
    return templates.TemplateResponse("dashboard.html", {"request": request, "me": me, "stats": stats_for(me), "tasks": ASSIGNMENTS[:10], "notices": NOTICES, "logs": AUDIT_LOGS[:8]})

@app.get("/users", response_class=HTMLResponse)
def users_page(request: Request):
    g = guard(request)
    if g: return g
    return templates.TemplateResponse("users.html", {"request": request, "users": USERS, "roles": ROLE_CATALOG, "me": current_user(request)})

@app.post("/users/create")
async def create_user(request: Request, full_name: str = Form(...), username: str = Form(...), phone: str = Form(...), role: str = Form(...), email: str = Form(""), status: str = Form("Hoạt động"), password: str = Form("123456")):
    g = guard(request)
    if g: return g
    USERS.append({"username": username, "password": password, "full_name": full_name, "role": role, "phone": phone, "email": email, "status": status})
    AUDIT_LOGS.insert(0, {"time":"vừa xong","text":f"Tạo người dùng mới: {full_name}"})
    return RedirectResponse("/users", status_code=303)

@app.get("/roles", response_class=HTMLResponse)
def roles_page(request: Request):
    g = guard(request)
    if g: return g
    return templates.TemplateResponse("roles.html", {"request": request, "roles": ROLE_CATALOG, "me": current_user(request)})

@app.get("/assign", response_class=HTMLResponse)
def assign_page(request: Request):
    g = guard(request)
    if g: return g
    me = current_user(request)
    my_tasks = [a for a in ASSIGNMENTS if a["assignee_username"] == me["username"]]
    return templates.TemplateResponse("assign.html", {"request": request, "users": USERS, "assignments": ASSIGNMENTS, "my_tasks": my_tasks, "me": me})

@app.post("/assign/direct")
async def assign_direct(request: Request, title: str = Form(...), description: str = Form(...), category: str = Form("Công tác Đảng"), priority: str = Form("Cao"), due_date: str = Form(...), assignee: str = Form(...)):
    g = guard(request)
    if g: return g
    ASSIGNMENTS.insert(0, {"title": title, "description": description, "category": category, "priority": priority, "due_date": due_date, "assignee_username": assignee, "status":"Đang thực hiện","progress":"0%"})
    AUDIT_LOGS.insert(0, {"time":"vừa xong","text":f"Giao nhiệm vụ: {title} → {assignee}"})
    return RedirectResponse("/assign", status_code=303)

@app.post("/assign/file")
async def assign_file(request: Request, task_file: UploadFile = File(...)):
    g = guard(request)
    if g: return g
    rows = list(csv.DictReader(StringIO((await task_file.read()).decode("utf-8-sig", errors="ignore"))))
    for row in reversed(rows):
        ASSIGNMENTS.insert(0, {"title": row.get("title",""), "description": row.get("description",""), "category": row.get("category",""), "priority": row.get("priority",""), "due_date": row.get("due_date",""), "assignee_username": row.get("assignee_username",""), "status":"Đang thực hiện","progress":"0%"})
    AUDIT_LOGS.insert(0, {"time":"vừa xong","text":f"Nhập file giao việc {len(rows)} nhiệm vụ"})
    return RedirectResponse("/assign", status_code=303)

@app.post("/assign/update-progress")
async def update_progress(request: Request, idx: int = Form(...), progress: str = Form(...), status: str = Form(...)):
    g = guard(request)
    if g: return g
    if 0 <= idx < len(ASSIGNMENTS):
        ASSIGNMENTS[idx]["progress"] = progress
        ASSIGNMENTS[idx]["status"] = status
        AUDIT_LOGS.insert(0, {"time":"vừa xong","text":f"Cập nhật tiến độ nhiệm vụ: {ASSIGNMENTS[idx]['title']} -> {progress}"})
    return RedirectResponse("/assign", status_code=303)

@app.get("/sample-task-file")
def sample_task_file():
    return FileResponse("deploy/mau_giao_viec_hang_loat.csv", filename="mau_giao_viec_hang_loat.csv")

@app.get("/system", response_class=HTMLResponse)
def system_page(request: Request):
    g = guard(request)
    if g: return g
    return templates.TemplateResponse("system.html", {"request": request, "me": current_user(request), "logs": AUDIT_LOGS[:20]})

@app.get("/profile", response_class=HTMLResponse)
def profile_page(request: Request, msg: str = ""):
    g = guard(request)
    if g: return g
    return templates.TemplateResponse("profile.html", {"request": request, "me": current_user(request), "msg": msg})

@app.post("/profile/change-password")
async def change_password(request: Request, old_password: str = Form(...), new_password: str = Form(...), confirm_password: str = Form(...)):
    g = guard(request)
    if g: return g
    me = current_user(request)
    if me["password"] != old_password:
        return RedirectResponse("/profile?msg=Mật khẩu cũ không đúng", status_code=303)
    if new_password != confirm_password:
        return RedirectResponse("/profile?msg=Xác nhận mật khẩu không khớp", status_code=303)
    me["password"] = new_password
    return RedirectResponse("/profile?msg=Đổi mật khẩu thành công", status_code=303)

@app.get("/forgot-password", response_class=HTMLResponse)
def forgot_password_page(request: Request, msg: str = ""):
    return templates.TemplateResponse("forgot_password.html", {"request": request, "msg": msg})

@app.post("/forgot-password/send-otp")
async def send_otp(phone: str = Form(...)):
    otp = str(random.randint(100000, 999999)); OTP_STORE[phone] = {"otp": otp, "created": time.time()}
    try:
        status_code, resp = send_otp_real(phone, otp)
        return RedirectResponse(f"/forgot-password?msg={'Đã gửi OTP tới số ' + phone if 200 <= status_code < 300 else 'Gửi OTP thất bại: ' + resp[:120]}", status_code=303)
    except Exception as e:
        return RedirectResponse(f"/forgot-password?msg=Lỗi gửi OTP: {e}", status_code=303)

@app.post("/forgot-password/verify")
async def verify_otp(phone: str = Form(...), otp: str = Form(...), new_password: str = Form(...), confirm_password: str = Form(...)):
    if new_password != confirm_password: return RedirectResponse("/forgot-password?msg=Mật khẩu xác nhận không khớp", status_code=303)
    ok, msg = verify_otp_local(phone, otp)
    if not ok: return RedirectResponse(f"/forgot-password?msg={msg}", status_code=303)
    for u in USERS:
        if u["phone"] == phone: u["password"] = new_password
    OTP_STORE.pop(phone, None)
    return RedirectResponse("/login?msg=Đặt lại mật khẩu thành công", status_code=303)