import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np

# Create figure for Twitter header (1500x500)
fig, ax = plt.subplots(1, 1, figsize=(15, 5))
ax.set_xlim(0, 1500)
ax.set_ylim(0, 500)
ax.axis('off')

# Background gradient effect
gradient = np.linspace(0, 1, 256).reshape(1, -1)
gradient = np.vstack((gradient, gradient))
ax.imshow(gradient, aspect='auto', cmap='Purples', alpha=0.3, 
          extent=[0, 1500, 0, 500])

# Main background
bg = patches.Rectangle((0, 0), 1500, 500, facecolor='#667eea', alpha=0.9)
ax.add_patch(bg)

# Decorative circles
circle1 = plt.Circle((200, 400), 100, color='#764ba2', alpha=0.3)
circle2 = plt.Circle((1300, 100), 150, color='#764ba2', alpha=0.2)
circle3 = plt.Circle((750, 250), 80, color='white', alpha=0.1)
ax.add_patch(circle1)
ax.add_patch(circle2)
ax.add_patch(circle3)

# Main text
ax.text(750, 350, 'SEO BOT', fontsize=72, fontweight='bold', 
        color='white', ha='center', va='center')
ax.text(750, 250, 'AI-Powered Article Generator', fontsize=28, 
        color='white', ha='center', va='center', alpha=0.9)
ax.text(750, 180, 'Create SEO-optimized content in minutes', fontsize=20, 
        color='white', ha='center', va='center', alpha=0.8)

# Website
ax.text(750, 100, 'seo-bot-qrk9.onrender.com', fontsize=18, 
        color='white', ha='center', va='center', alpha=0.7, style='italic')

# Save
import os
banner_path = os.path.expanduser('~/.openclaw/workspace/seo_bot/banner.png')
plt.tight_layout()
plt.savefig(banner_path, dpi=100, 
            bbox_inches='tight', pad_inches=0, facecolor='#667eea')
plt.close()

print('Banner saved: banner.png')
