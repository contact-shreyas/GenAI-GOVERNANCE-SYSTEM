# Docker Desktop Installation Guide

Since the automated installation is taking too long due to the large installer file (586 MB), please manually install Docker Desktop:

## Manual Installation Steps

1. **Download Docker Desktop**
   - Visit: https://www.docker.com/products/docker-desktop
   - Click "Download for Windows"
   - This downloads: `Docker Desktop Installer.exe` (≈586 MB)

2. **Run the Installer**
   - Double-click `Docker Desktop Installer.exe`
   - Administrator privileges required
   - Keep all default options selected
   - Check "Install required Windows components for WSL2" if prompted

3. **Complete Installation**
   - Click "Install" and wait 3-5 minutes
   - Restart your computer when prompted
   - Docker Desktop will launch on startup (icon in system tray)

4. **Verify Installation**
   ```powershell
   docker --version
   docker run hello-world
   ```

## Time Estimate
- Download: 2-5 minutes (depending on internet speed)
- Installation: 3-5 minutes
- Restart: 1-2 minutes
- **Total: 6-12 minutes**

## Once Docker is Installed

Run the full application:

```powershell
cd "d:\GenAI GOVERNANCE LAYER FOR HIGHER EDUCATION"
docker-compose up --build
```

The build will take 10-15 minutes on first run (compiling Python wheels, installing npm packages).

## Troubleshooting

If you see "500 Internal Server Error":
1. Check Docker Desktop is running (icon in system tray)
2. Right-click Docker icon → "Restart Docker engine"
3. Wait 30 seconds, then retry

If installation hangs:
1. Kill the installer: `taskkill /F /IM Docker\ Desktop.exe`
2. Download the latest version directly from docker.com
3. Run with elevated privileges

---

**Current Project Status**: ✅ All files ready, waiting for Docker installation
