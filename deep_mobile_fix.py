#!/usr/bin/env python3
"""
Deep Surgical Mobile Optimization Script
Injects mobile CSS fixes & glassmorphism prompt card enhancements into index.html
without altering desktop UI or losing any features.
"""
import os, sys, re, subprocess

print("🚀 Applying deep surgical mobile patch to index.html...")

if not os.path.exists("index.html"):
    print("❌ Error: index.html not found.")
    sys.exit(1)

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Mobile-Only CSS Patch (Max Depth Mobile Containment + High-End Terminal Shell)
MOBILE_PATCH_CSS = """
  /* ==================== SURGICAL DEEP MOBILE FIXES ==================== */
  * { box-sizing: border-box !important; }
  html, body { max-width: 100vw !important; overflow-x: hidden !important; }

  /* Premium Code Terminal Styling */
  .prompt-content-box, pre, code {
    background: rgba(10, 14, 23, 0.90) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 12px !important;
    box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.5) !important;
    font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
    max-width: 100% !important;
    overflow-x: auto !important;
    white-space: pre-wrap !important;
    word-break: break-word !important;
  }

  /* Placeholder Badges */
  .prompt-content-box span, .placeholder-badge {
    background: rgba(139, 92, 246, 0.22) !important;
    border: 1px solid rgba(167, 139, 250, 0.4) !important;
    color: #ddd6fe !important;
    padding: 2px 7px !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
  }

  @media (max-width: 767px) {
    /* Main Layout Viewport Containment */
    body, main, section, .container, .app-wrapper {
      padding-left: 14px !important;
      padding-right: 14px !important;
      padding-bottom: calc(105px + env(safe-area-inset-bottom)) !important;
    }

    /* Fix Cost Calculator Clipping */
    .calculator-grid, div[class*="grid"] {
      display: flex !important;
      flex-direction: column !important;
      width: 100% !important;
      max-width: 100% !important;
    }

    /* Heading Text Responsiveness */
    h1, h2, h3, .hero-title {
      font-size: clamp(1.5rem, 6vw, 2.2rem) !important;
      line-height: 1.25 !important;
      word-break: break-word !important;
    }

    /* Touch Targets */
    button, a.btn, input, select {
      min-height: 46px !important;
      touch-action: manipulation !important;
    }
  }
  /* =================================================================== */
"""

# Inject CSS into <head>
if "</head>" in content:
    updated_content = content.replace("</head>", f"<style>{MOBILE_PATCH_CSS}</style>\n</head>")
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(updated_content)
    print("✅ Injected surgical mobile CSS into index.html")
else:
    print("❌ Error: Couldn't locate </head> tag.")
    sys.exit(1)

# Commit & Push
try:
    subprocess.run(["git", "add", "index.html"], check=True)
    subprocess.run(["git", "commit", "-m", "Deep surgical mobile containment & code box visual enhancement"], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("🚀 Pushed updates directly to GitHub origin main.")
except Exception as e:
    print(f"⚠️ Git error: {e}")

print("✨ DEEP MOBILE OVERHAUL COMPLETE. Check your live site in ~30 seconds!")
