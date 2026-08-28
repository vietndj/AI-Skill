# ==============================================================================
# AI FACE CLONE PRO - 1-CLICK DEDICATED INSTALLER FOR WINDOWS (PowerShell)
# ==============================================================================

$ErrorActionPreference = "Stop"

$RepoUrl = "https://github.com/vietndj/AI-Skill.git"
$GeminiDir = Join-Path $HOME ".gemini"
$TargetSkillsDir = Join-Path $GeminiDir "config\skills"
$TargetSkillDir = Join-Path $TargetSkillsDir "ai-face-clone"
$TempCloneDir = Join-Path $GeminiDir ".ai-skill-temp"
$AvatarDir = Join-Path $GeminiDir "avatar_photos"

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host " 👤 CÀI ĐẶT SKILL: AI FACE CLONE PRO CHO ANTIGRAVITY (WINDOWS)" -ForegroundColor Magenta
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Tạo thư mục
if (!(Test-Path $TargetSkillsDir)) { New-Item -ItemType Directory -Path $TargetSkillsDir -Force | Out-Null }
if (!(Test-Path $AvatarDir)) { New-Item -ItemType Directory -Path $AvatarDir -Force | Out-Null }

# 2. Tải hoặc cập nhật từ GitHub
if (Test-Path (Join-Path $TempCloneDir ".git")) {
    Write-Host "🔄 Đang đồng bộ cập nhật từ GitHub repo..." -ForegroundColor Blue
    Set-Location $TempCloneDir
    git fetch --all --quiet
    git reset --hard origin/main --quiet
} else {
    Write-Host "📥 Đang tải gói kỹ năng AI Face Clone..." -ForegroundColor Blue
    if (Test-Path $TempCloneDir) { Remove-Item -Recurse -Force $TempCloneDir }
    git clone --depth 1 $RepoUrl $TempCloneDir --quiet
}

# 3. Sao chép skill
Write-Host "📂 Đang thiết lập cấu hình skill vào Antigravity..." -ForegroundColor Blue
if (!(Test-Path $TargetSkillDir)) { New-Item -ItemType Directory -Path $TargetSkillDir -Force | Out-Null }
Copy-Item -Path (Join-Path $TempCloneDir "skills\ai-face-clone\*") -Destination $TargetSkillDir -Recurse -Force

Write-Host ""
Write-Host "✅ CÀI ĐẶT THÀNH CÔNG SKILL AI FACE CLONE PRO TRÊN WINDOWS!" -ForegroundColor Green
Write-Host "👉 Thư mục lưu ảnh chân dung mẫu của bạn: $AvatarDir" -ForegroundColor Yellow
Write-Host ""
Write-Host "----------------------------------------------------------------------" -ForegroundColor Cyan
Write-Host "🎯 HƯỚNG DẪN 3 BƯỚC SỬ DỤNG:" -ForegroundColor Green
Write-Host " 1. Copy 3-5 ảnh chân dung rõ mặt của bạn vào: $AvatarDir"
Write-Host " 2. Khởi động lại Antigravity IDE."
Write-Host " 3. Mở khung chat và gõ: 'Setup hồ sơ khuôn mặt của tôi'"
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""
