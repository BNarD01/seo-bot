# 快速解决 - 删除重建仓库

## 步骤 1：删除 GitHub 仓库
1. 打开 https://github.com/BNarD01/seo-bot
2. 点击 Settings（设置）
3. 拉到最下面 Danger Zone
4. 点击 Delete this repository
5. 输入 `BNarD01/seo-bot` 确认删除

## 步骤 2：重新创建仓库
1. 点击 New Repository
2. Repository name: `seo-bot`
3. 选 Public
4. **重要：不要勾选 Add a README file**
5. 点击 Create repository

## 步骤 3：推送代码
在终端执行：
```bash
cd ~/.openclaw/workspace/seo_bot
git remote remove origin
git remote add origin https://github.com/BNarD01/seo-bot.git
git branch -M main
git push -u origin main
```

这样就干净了，没有历史提交的问题！
