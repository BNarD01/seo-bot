import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np

# Create figure
fig, ax = plt.subplots(1, 1, figsize=(8, 8))
ax.set_xlim(0, 400)
ax.set_ylim(0, 400)
ax.axis('off')

# Background circle with gradient effect
circle = plt.Circle((200, 200), 180, color='#667eea', alpha=0.9)
ax.add_patch(circle)

# Inner circle for depth
circle2 = plt.Circle((200, 200), 170, color='#764ba2', alpha=0.3)
ax.add_patch(circle2)

# Robot icon (simplified)
# Head
head = plt.Circle((200, 260), 40, color='white', alpha=0.9)
ax.add_patch(head)
# Eyes
eye1 = plt.Circle((185, 270), 8, color='#667eea')
eye2 = plt.Circle((215, 270), 8, color='#667eea')
ax.add_patch(eye1)
ax.add_patch(eye2)
# Antenna
ax.plot([200, 200], [300, 330], color='white', linewidth=4)
antenna = plt.Circle((200, 335), 8, color='white')
ax.add_patch(antenna)

# Body
body = FancyBboxPatch((170, 190), 60, 50, boxstyle="round,pad=0.02", 
                       facecolor='white', edgecolor='white', alpha=0.9)
ax.add_patch(body)

# Text
ax.text(200, 140, 'SEO BOT', fontsize=36, fontweight='bold', 
        color='white', ha='center', va='center')
ax.text(200, 100, 'AI Article Generator', fontsize=14, 
        color='white', ha='center', va='center', alpha=0.9)

# Save
plt.tight_layout()
import os
logo_path = os.path.expanduser('~/.openclaw/workspace/seo_bot/logo.png')
plt.savefig(logo_path, dpi=150, 
            bbox_inches='tight', pad_inches=0, facecolor='none')
plt.close()

print('Logo saved: logo.png')
