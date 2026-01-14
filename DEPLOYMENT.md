# DEPLOYMENT GUIDE

## 🚀 Deploy Backend lên Railway

1. **Tạo tài khoản Railway**
   - Vào https://railway.app
   - Login bằng GitHub

2. **Deploy Backend**
   ```bash
   # Push code lên GitHub trước
   git add .
   git commit -m "Ready for deployment"
   git push
   ```

3. **Trên Railway:**
   - Click "New Project"
   - Chọn "Deploy from GitHub repo"
   - Chọn repo của bạn
   - **Settings:**
     - Root Directory: `backend`
     - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Railway sẽ tự động detect Python và install requirements.txt

4. **Copy Backend URL**
   - Railway sẽ cho URL dạng: `https://tool-hub-backend.up.railway.app`
   - Copy URL này

---

## 🌐 Deploy Frontend lên Vercel

1. **Update Backend URL**
   - Mở file `frontend/.env.production`
   - Paste Railway URL vào:
     ```
     VITE_API_URL=https://tool-hub-backend.up.railway.app
     ```
   - Commit và push:
     ```bash
     git add frontend/.env.production
     git commit -m "Update production API URL"
     git push
     ```

2. **Tạo tài khoản Vercel**
   - Vào https://vercel.com
   - Login bằng GitHub

3. **Deploy Frontend**
   - Click "Add New Project"
   - Chọn repo của bạn
   - **Settings:**
     - Framework Preset: Vite
     - Root Directory: `frontend`
     - Build Command: `npm run build`
     - Output Directory: `dist`
   - Click "Deploy"

4. **Vercel sẽ cho URL:**
   - `https://your-app.vercel.app`
   - Mở URL này để xem website!

---

## ✅ Checklist

- [ ] Backend deploy lên Railway thành công
- [ ] Copy Railway URL
- [ ] Update `frontend/.env.production` với Railway URL
- [ ] Push code lên GitHub
- [ ] Frontend deploy lên Vercel thành công
- [ ] Test website: mở Vercel URL, kiểm tra tools hiển thị đầy đủ

---

## 🔧 Troubleshooting

**Lỗi: Frontend không kết nối được backend**
- Check Railway URL trong `.env.production` đã đúng chưa
- Check Railway backend có đang chạy không (xem logs)
- Check CORS trong `backend/main.py` (đã set allow_origins=["*"])

**Lỗi: Railway không start**
- Check `backend/requirements.txt` có đầy đủ dependencies
- Check Railway logs để xem lỗi gì

**Update tools:**
- Edit `config/tools.yaml`
- Push lên GitHub
- Railway và Vercel tự động redeploy (1-2 phút)
