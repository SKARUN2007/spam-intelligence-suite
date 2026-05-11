# 🚀 Deployment Guide: Spam Intelligence Suite

Follow these steps to host your Expert/Master level Spam Classifier in the cloud.

## 1. Prepare your GitHub Repository
1. Create a new repository on GitHub.
2. Initialize git in your local project folder:
   ```bash
   git init
   git add .
   git commit -m "Initial commit for cloud deployment"
   ```
3. Push your code to GitHub.

---

## 2. Host the Backend (Render.com)
1. Log in to [Render](https://render.com).
2. Click **New +** > **Web Service**.
3. Connect your GitHub repository.
4. Set the following:
   - **Environment**: `Docker`
   - **Region**: Choose one closest to you.
5. Go to **Settings** > **Environment Variables** and add:
   - `ALLOWED_ORIGINS`: `https://your-frontend-domain.vercel.app` (Add this after setting up Vercel)
   - `DATA_DIR`: `/data`
6. Go to **Settings** > **Disks** and click **Add Disk**:
   - **Name**: `spam-data`
   - **Mount Path**: `/data`
   - **Size**: `1GB` (Free tier is fine)
7. Deploy! Your backend URL will look like `https://spam-checker-api.onrender.com`.

---

## 3. Host the Frontend (Vercel)
1. Log in to [Vercel](https://vercel.com).
2. Click **Add New** > **Project**.
3. Import your GitHub repository.
4. **Important**: In the "Root Directory" settings, ensure it points to the `frontend/` folder.
5. Expand **Environment Variables** and add:
   - `NEXT_PUBLIC_API_URL`: `https://your-render-backend-url.onrender.com`
6. Click **Deploy**.

---

## 📝 Post-Deployment Note
Once Vercel gives you a URL (e.g., `https://spam-forensics.vercel.app`), remember to go back to **Render** and update the `ALLOWED_ORIGINS` environment variable to match that URL. This ensures your backend only accepts requests from your own frontend.

Congratulations! Your Master-Level Spam Forensics Suite is now live!
