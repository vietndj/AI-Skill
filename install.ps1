# ==============================================================================
# AI SKILL - ONE-CLICK INSTALLER (Windows PowerShell)
# ==============================================================================

$RepoUrl = "https://github.com/vietndj/AI-Skill.git"
$TargetDir = "$env:USERPROFILE\.gemini\config\skills"
$TempDir = "$env:USERPROFILE\.gemini\.ai-skill-temp"

Write-Host ""
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host " 🚀 CAI DAT BO KY NANG ANTIGRAVITY AI - AI SKILL" -ForegroundColor Green
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Tao thu muc config neu chua co
if (!(Test-Path -Path $TargetDir)) {
    New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null
}

# 2. Tai hoac cap nhat tu GitHub
if (Test-Path -Path "$TempDir\.git") {
    Write-Host "🔄 Dang dong bo cap nhat phien ban moi nhat tu GitHub..." -ForegroundColor Blue
    Set-Location $TempDir
    git fetch --all --quiet
    git reset --hard origin/main --quiet
} else {
    Write-Host "📥 Dang tai bo ky nang ve may..." -ForegroundColor Blue
    if (Test-Path -Path $TempDir) { Remove-Item -Recurse -Force $TempDir }
    git clone --depth 1 $RepoUrl $TempDir --quiet
}

# 3. Sao chep vao thu muc skills cua Antigravity
Write-Host "📂 Dang sao chep cac ky nang vao Antigravity..." -ForegroundColor Blue
Copy-Item -Path "$TempDir\skills\*" -Destination $TargetDir -Recurse -Force

# 4. Dem so luong ky nang
$Count = (Get-ChildItem -Directory -Path $TargetDir).Count

Write-Host ""
Write-Host "✅ CAI DAT THANH CONG! DA DONG BO $Count KY NANG VAO HE THONG." -ForegroundColor Green
Write-Host "👉 Vi tri luu tru: $TargetDir" -ForegroundColor Yellow
Write-Host ""
Write-Host "------------------------------------------------------" -ForegroundColor Cyan
Write-Host "💡 CACH SU DUNG TREN ANTIGRAVITY:" -ForegroundColor Green
Write-Host "1. Khoi dong lai hoac mo Antigravity IDE."
Write-Host "2. Gui link video hoac chat cac cau lenh thuc chien:"
Write-Host "   - Phan tich video: 'Phan tich video nay giup toi: <link instagram/tiktok>'"
Write-Host "   - Phan tich podcast: 'PODCAST <link youtube>'"
Write-Host "   - Tai nhac: 'TAI NHAC : <link>' hoac 'Tai nhac bai nay <link>'"
Write-Host "   - Nen video 1080p: 'nen1080 <duong dan file video>'"
Write-Host "   - Bang phan canh: 'BANG PHAN CANH cho kich ban sau: ...'"
Write-Host "   - Loc van mau: 'LOC van mau doan van nay: ...'"
Write-Host "------------------------------------------------------" -ForegroundColor Cyan
Write-Host ""
