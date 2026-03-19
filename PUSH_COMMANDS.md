# SEO Bot - GitHub 推送命令

## 在电脑上执行以下命令：

```bash
cd ~/.openclaw/workspace/seo_bot

# 添加远程仓库
git remote add origin https://github.com/BNarD01/seo-bot.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

## 如果提示登录：
- 输入你的 GitHub 用户名
- 密码用 Personal Access Token（不是 GitHub 密码）

## 生成 Token（如果需要）：
1. GitHub → Settings → Developer settings
2. Personal access tokens → Tokens (classic)
3. Generate new token
4. 勾选 repo 权限
5. 复制 token 当密码用

## 推送成功后：
告诉我，我帮你部署到 Vercel！
