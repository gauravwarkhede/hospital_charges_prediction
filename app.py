"""
===============================================================================
MEDICO.AI - ENTERPRISE SINGLE-FILE ARCHITECTURE (RENDER READY)
===============================================================================
Advanced Predictive Analytics Engine for Hospital Charges
Features: 16 Dynamic Themes (including Netflix), Glassmorphism UI, 
Smooth Animations, Chart.js Integrations, SQLite Persistence.
===============================================================================
"""

import os
import sqlite3
import uuid
import pickle
import datetime
import warnings
import numpy as np
from flask import Flask, request, jsonify, render_template_string

warnings.filterwarnings("ignore", category=UserWarning)

# =============================================================================
# 1. FRONTEND UI EMBEDDED (HTML/CSS/JS)
# =============================================================================

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" data-theme="netflix-dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Medico.AI | Advanced Health Analytics</title>
    <!-- Modern Bold Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800;900&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        /* ================= CSS VARIABLES & THEMES ================= */
        :root {
            --sidebar-width: 280px;
            --glass-blur: blur(20px);
            --card-radius: 20px;
            --transition-fast: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            --transition-smooth: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
            --font-head: 'Montserrat', sans-serif;
            --font-body: 'Inter', sans-serif;
        }

        /* 16 Custom Themes (Added Netflix Dark) */
        [data-theme="netflix-dark"] { --bg-base: #000000; --bg-card: rgba(20, 20, 20, 0.85); --border-glow: rgba(229, 9, 20, 0.5); --accent-primary: #e50914; --accent-secondary: #b20710; --text-main: #ffffff; --text-muted: #a3a3a3; }
        [data-theme="cyberpunk"] { --bg-base: #080c14; --bg-card: rgba(13, 20, 36, 0.75); --border-glow: rgba(0, 240, 255, 0.3); --accent-primary: #00f0ff; --accent-secondary: #8b5cf6; --text-main: #f8fafc; --text-muted: #64748b; }
        [data-theme="solar-golden"] { --bg-base: #0f0d0a; --bg-card: rgba(28, 23, 16, 0.8); --border-glow: rgba(245, 158, 11, 0.35); --accent-primary: #f59e0b; --accent-secondary: #d97706; --text-main: #fffbeb; --text-muted: #a1a1aa; }
        [data-theme="purple-magic"] { --bg-base: #0e0a1a; --bg-card: rgba(25, 18, 45, 0.8); --border-glow: rgba(168, 85, 247, 0.35); --accent-primary: #a855f7; --accent-secondary: #c084fc; --text-main: #faf5ff; --text-muted: #988aae; }
        [data-theme="ice-sapphire"] { --bg-base: #06111e; --bg-card: rgba(12, 30, 52, 0.75); --border-glow: rgba(56, 189, 248, 0.35); --accent-primary: #38bdf8; --accent-secondary: #0284c7; --text-main: #f0f9ff; --text-muted: #64748b; }
        [data-theme="emerald-bio"] { --bg-base: #04140d; --bg-card: rgba(10, 36, 24, 0.8); --border-glow: rgba(16, 185, 129, 0.35); --accent-primary: #10b981; --accent-secondary: #059669; --text-main: #ecfdf5; --text-muted: #6ee7b7; }
        [data-theme="crimson-velvet"] { --bg-base: #14060a; --bg-card: rgba(36, 12, 18, 0.8); --border-glow: rgba(244, 63, 94, 0.35); --accent-primary: #f43f5e; --accent-secondary: #e11d48; --text-main: #fff1f2; --text-muted: #fda4af; }
        [data-theme="deep-space"] { --bg-base: #030308; --bg-card: rgba(15, 15, 32, 0.85); --border-glow: rgba(99, 102, 241, 0.35); --accent-primary: #6366f1; --accent-secondary: #4f46e5; --text-main: #eef2ff; --text-muted: #818cf8; }
        [data-theme="sunset-synth"] { --bg-base: #120a17; --bg-card: rgba(32, 16, 42, 0.8); --border-glow: rgba(249, 115, 22, 0.35); --accent-primary: #f97316; --accent-secondary: #ec4899; --text-main: #fff7ed; --text-muted: #fdba74; }
        [data-theme="matrix-obsidian"] { --bg-base: #050a05; --bg-card: rgba(10, 25, 12, 0.85); --border-glow: rgba(34, 197, 94, 0.35); --accent-primary: #22c55e; --accent-secondary: #16a34a; --text-main: #f0fdf4; --text-muted: #86efac; }
        [data-theme="solar-light"] { --bg-base: #f1f5f9; --bg-card: rgba(255, 255, 255, 0.9); --border-glow: rgba(14, 165, 233, 0.3); --accent-primary: #0284c7; --accent-secondary: #6366f1; --text-main: #0f172a; --text-muted: #475569; }
        [data-theme="formula-grid"] { --bg-base: #111111; --bg-card: rgba(26, 26, 26, 0.85); --border-glow: rgba(255, 40, 0, 0.4); --accent-primary: #ff2800; --accent-secondary: #a61a00; --text-main: #ffffff; --text-muted: #8c8c8c; }
        [data-theme="neon-paddock"] { --bg-base: #0a0a0a; --bg-card: rgba(15, 15, 15, 0.8); --border-glow: rgba(255, 135, 0, 0.4); --accent-primary: #ff8700; --accent-secondary: #00e5ff; --text-main: #f4f4f4; --text-muted: #737373; }
        [data-theme="oceanic"] { --bg-base: #001220; --bg-card: rgba(0, 31, 63, 0.75); --border-glow: rgba(0, 255, 204, 0.3); --accent-primary: #00ffcc; --accent-secondary: #0074d9; --text-main: #e6f7ff; --text-muted: #80c1ff; }
        [data-theme="nebula"] { --bg-base: #1a0b2e; --bg-card: rgba(45, 19, 77, 0.8); --border-glow: rgba(255, 0, 128, 0.4); --accent-primary: #ff0080; --accent-secondary: #7928ca; --text-main: #f9ebff; --text-muted: #b886ee; }
        [data-theme="monolith"] { --bg-base: #1c1c1c; --bg-card: rgba(45, 45, 45, 0.9); --border-glow: rgba(255, 255, 255, 0.2); --accent-primary: #ffffff; --accent-secondary: #888888; --text-main: #f0f0f0; --text-muted: #a0a0a0; }

        /* ================= BASE STYLES & LAYOUT ================= */
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background-color: var(--bg-base); color: var(--text-main); font-family: var(--font-body);
            min-height: 100vh; overflow-x: hidden; display: flex; transition: var(--transition-smooth);
            background-image: radial-gradient(circle at 10% 10%, rgba(255,255,255,0.015) 0%, transparent 60%),
                              radial-gradient(circle at 90% 90%, var(--border-glow) 0%, transparent 50%);
        }

        /* Animations */
        @keyframes slideUp { from { opacity: 0; transform: translateY(40px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes slideInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes pulseGlow { 0% { box-shadow: 0 0 10px var(--border-glow); } 100% { box-shadow: 0 0 30px var(--accent-primary); } }
        @keyframes slideInRight { from { opacity: 0; transform: translateX(50px); } to { opacity: 1; transform: translateX(0); } }

        /* ================= SIDEBAR ================= */
        .sidebar {
            width: var(--sidebar-width); height: 100vh; position: fixed; top: 0; left: 0;
            background: var(--bg-card); backdrop-filter: var(--glass-blur);
            border-right: 1px solid var(--border-glow); padding: 2.5rem 1.5rem;
            display: flex; flex-direction: column; z-index: 100; transition: var(--transition-smooth);
        }
        .brand { display: flex; align-items: center; gap: 15px; margin-bottom: 3.5rem; cursor: pointer; transition: var(--transition-fast); }
        .brand:hover { transform: scale(1.05); }
        .brand-logo {
            width: 48px; height: 48px; border-radius: 14px;
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
            display: flex; align-items: center; justify-content: center; font-size: 1.3rem; color: #fff;
            animation: pulseGlow 3s infinite alternate; box-shadow: 0 0 15px var(--border-glow);
        }
        .brand-text { font-family: var(--font-head); font-size: 1.5rem; font-weight: 900; letter-spacing: 1px; }
        
        .nav-menu { display: flex; flex-direction: column; gap: 12px; flex: 1; }
        .nav-item {
            padding: 1.1rem 1.2rem; border-radius: 14px; cursor: pointer; display: flex; align-items: center; gap: 14px;
            font-weight: 600; color: var(--text-muted); transition: var(--transition-fast); border: 1px solid transparent;
        }
        .nav-item:hover, .nav-item.active {
            background: rgba(255, 255, 255, 0.08); color: var(--accent-primary);
            border-color: var(--border-glow); transform: translateX(8px);
        }

        /* Sleek Dropdown */
        .theme-selector { margin-top: auto; }
        .theme-selector label { display: block; font-size: 0.8rem; margin-bottom: 10px; color: var(--text-muted); text-transform: uppercase; font-weight: 700; letter-spacing: 1px;}
        .theme-select {
            appearance: none; width: 100%; background: rgba(0,0,0,0.3) url("data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%23FFFFFF%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E") no-repeat right 1rem top 50%;
            background-size: 0.8rem auto; color: var(--text-main); border: 1px solid rgba(255,255,255,0.15); padding: 1rem 1.2rem; border-radius: 14px;
            font-family: var(--font-body); font-weight: 600; font-size: 0.95rem; outline: none; cursor: pointer; transition: var(--transition-fast);
        }
        .theme-select:hover, .theme-select:focus { border-color: var(--accent-primary); box-shadow: 0 0 15px var(--border-glow); background-color: rgba(0,0,0,0.5); }
        .theme-select option { background-color: #1a1a1a; color: #fff; }

        /* ================= MAIN CONTENT ================= */
        .main-content { margin-left: var(--sidebar-width); flex: 1; padding: 3rem 4rem; width: calc(100% - var(--sidebar-width)); }
        
        .header-title { margin-bottom: 2.5rem; animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1); }
        .header-title h1 { font-family: var(--font-head); font-size: 2.8rem; text-transform: uppercase; font-weight: 900; margin-bottom: 8px; letter-spacing: -1px; }
        .header-title p { color: var(--text-muted); font-size: 1.15rem; font-weight: 400; }

        .dashboard-grid { display: grid; grid-template-columns: repeat(12, 1fr); gap: 2rem; }

        /* Cards */
        .glass-card {
            background: var(--bg-card); backdrop-filter: var(--glass-blur); border: 1px solid rgba(255,255,255,0.05);
            border-radius: var(--card-radius); padding: 2rem; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3); 
            transition: var(--transition-smooth); position: relative; overflow: hidden; animation: slideUp 0.8s ease backwards;
        }
        .glass-card:hover { border-color: var(--border-glow); transform: translateY(-8px); box-shadow: 0 30px 60px rgba(0,0,0,0.5), 0 0 30px var(--border-glow); }
        .glass-card:nth-child(1) { animation-delay: 0.1s; }
        .glass-card:nth-child(2) { animation-delay: 0.2s; }
        .glass-card:nth-child(3) { animation-delay: 0.3s; }
        .glass-card:nth-child(4) { animation-delay: 0.4s; }
        .glass-card:nth-child(5) { animation-delay: 0.5s; }

        .card-header {
            display: flex; align-items: center; justify-content: space-between; font-family: var(--font-head); font-size: 1.2rem; font-weight: 800;
            color: var(--accent-primary); border-bottom: 2px dashed rgba(255,255,255,0.1); padding-bottom: 1.2rem; margin-bottom: 1.8rem; text-transform: uppercase; letter-spacing: 0.5px;
        }
        
        /* Grid Placements */
        .input-card { grid-column: span 7; }
        .result-card { grid-column: span 5; }
        .chart-card { grid-column: span 6; height: 380px; display: flex; flex-direction: column; }
        .chart-container { flex: 1; position: relative; width: 100%; height: 100%; }
        .table-card { grid-column: span 12; }

        /* ================= FORMS & INPUTS ================= */
        .form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.8rem; }
        .form-group { display: flex; flex-direction: column; gap: 10px; animation: slideInUp 0.6s ease backwards; }
        .form-group:nth-child(1) { animation-delay: 0.15s; }
        .form-group:nth-child(2) { animation-delay: 0.25s; }
        .form-group:nth-child(3) { animation-delay: 0.35s; }
        .form-group:nth-child(4) { animation-delay: 0.45s; }
        .form-group:nth-child(5) { animation-delay: 0.55s; }
        .form-group:nth-child(6) { animation-delay: 0.65s; }
        .form-group.full { grid-column: 1 / -1; }
        
        label { font-size: 0.85rem; font-weight: 800; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; font-family: var(--font-head); }
        .input-elem {
            appearance: none; background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 1rem 1.2rem; border-radius: 12px; color: var(--text-main); font-family: var(--font-body); font-weight: 500; font-size: 1rem; transition: var(--transition-fast); outline: none;
        }
        select.input-elem {
            background-image: url("data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%23FFFFFF%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E");
            background-repeat: no-repeat; background-position: right 1rem top 50%; background-size: 0.7rem auto;
        }
        select.input-elem option { background-color: #1a1a1a; color: #fff; }
        .input-elem:focus { border-color: var(--accent-primary); box-shadow: 0 0 15px var(--border-glow); background: rgba(255,255,255,0.08); transform: translateY(-2px); }
        
        .slider-flex { display: flex; align-items: center; gap: 15px; }
        .slider-flex input[type="range"] { flex: 1; accent-color: var(--accent-primary); cursor: pointer; transition: var(--transition-fast); }
        .slider-flex input[type="range"]:hover { filter: brightness(1.2); }
        .slider-val { font-family: var(--font-head); font-size: 1.2rem; font-weight: 800; color: var(--accent-primary); width: 45px; text-align: right; }

        .btn-main {
            grid-column: 1 / -1; padding: 1.2rem; border: none; border-radius: 14px;
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
            color: #fff; font-family: var(--font-head); font-size: 1.15rem; font-weight: 900; letter-spacing: 1px;
            cursor: pointer; box-shadow: 0 10px 25px var(--border-glow); transition: var(--transition-smooth);
            margin-top: 1.5rem; text-transform: uppercase; animation: slideInUp 0.6s ease backwards; animation-delay: 0.75s;
        }
        .btn-main:hover { transform: translateY(-4px) scale(1.02); box-shadow: 0 20px 40px var(--accent-primary); filter: brightness(1.2); }
        .btn-main:active { transform: translateY(0) scale(0.98); }

        /* ================= RESULT DISPLAY ================= */
        .cost-display {
            text-align: center; padding: 2.5rem 1rem; border-radius: 16px;
            background: rgba(0, 0, 0, 0.4); border: 1px solid rgba(255,255,255,0.05); margin-bottom: 2rem;
            transition: var(--transition-smooth);
        }
        .cost-display:hover { border-color: var(--border-glow); box-shadow: inset 0 0 20px var(--border-glow); }
        .cost-value { font-family: var(--font-head); font-size: 4rem; font-weight: 900; color: var(--accent-primary); margin: 0.5rem 0; text-shadow: 0 0 35px var(--border-glow); letter-spacing: -2px; }
        
        .badge { display: inline-block; padding: 0.6rem 1.8rem; border-radius: 30px; font-family: var(--font-head); font-size: 0.95rem; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; }
        .badge.success { background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid #10b981; }
        .badge.warning { background: rgba(245, 158, 11, 0.15); color: #f59e0b; border: 1px solid #f59e0b; }
        .badge.danger { background: rgba(244, 63, 94, 0.15); color: #f43f5e; border: 1px solid #f43f5e; }

        .breakdown-item {
            display: flex; justify-content: space-between; align-items: center; padding: 1.2rem;
            background: rgba(255, 255, 255, 0.03); border-radius: 12px; margin-bottom: 12px;
            border-left: 4px solid var(--accent-primary); transition: var(--transition-fast);
            font-weight: 600;
        }
        .breakdown-item:hover { background: rgba(255, 255, 255, 0.08); transform: translateX(8px); box-shadow: 0 5px 15px rgba(0,0,0,0.3); }
        .breakdown-item strong { font-family: var(--font-head); font-size: 1.1rem; }

        /* ================= DATA TABLE ================= */
        .styled-table { width: 100%; border-collapse: collapse; margin-top: 1.5rem; }
        .styled-table th, .styled-table td { padding: 1.2rem; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.08); }
        .styled-table th { color: var(--text-muted); font-weight: 800; text-transform: uppercase; font-size: 0.85rem; font-family: var(--font-head); letter-spacing: 1px;}
        .styled-table tr { transition: var(--transition-fast); }
        .styled-table tr:hover { background: rgba(255,255,255,0.05); transform: scale(1.01); }

        /* ================= TOAST NOTIFICATIONS ================= */
        .toast-container { position: fixed; bottom: 30px; right: 30px; z-index: 1000; display: flex; flex-direction: column; gap: 12px; }
        .toast {
            background: var(--bg-card); border-left: 5px solid var(--accent-primary); border-radius: 12px;
            padding: 1.2rem 1.8rem; box-shadow: 0 15px 40px rgba(0,0,0,0.6); backdrop-filter: var(--glass-blur);
            animation: slideInRight 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards; display: flex; align-items: center; gap: 14px; font-weight: 700; font-family: var(--font-head);
        }
        
        /* Responsive */
        @media (max-width: 1200px) { .input-card, .result-card { grid-column: span 12; } }
        @media (max-width: 992px) { .chart-card { grid-column: span 12; } .sidebar { display: none; } .main-content { margin-left: 0; width: 100%; padding: 2rem; } }
    </style>
</head>
<body>

    <!-- SIDEBAR -->
    <aside class="sidebar">
        <div class="brand">
            <div class="brand-logo"><i class="fa-solid fa-heart-pulse"></i></div>
            <div class="brand-text">MEDICO<span style="color:var(--accent-primary)">.AI</span></div>
        </div>
        <nav class="nav-menu">
            <div class="nav-item active"><i class="fa-solid fa-wand-magic-sparkles"></i> Predictor Engine</div>
            <div class="nav-item"><i class="fa-solid fa-chart-pie"></i> Visual Analytics</div>
            <div class="nav-item"><i class="fa-solid fa-database"></i> Patient Database</div>
            <div class="nav-item"><i class="fa-solid fa-gear"></i> System Settings</div>
        </nav>
        <div class="theme-selector">
            <label><i class="fa-solid fa-palette"></i> Interface Theme</label>
            <select id="themeSelect" class="theme-select" onchange="changeTheme(this.value)">
                <option value="netflix-dark">Netflix Dark (Red)</option>
                <option value="cyberpunk">Cyberpunk Neon</option>
                <option value="formula-grid">Formula Grid (Racing)</option>
                <option value="neon-paddock">Neon Paddock</option>
                <option value="deep-space">Deep Space</option>
                <option value="solar-golden">Solar Golden</option>
                <option value="purple-magic">Purple Magic</option>
                <option value="ice-sapphire">Ice Sapphire</option>
                <option value="emerald-bio">Emerald Bio</option>
                <option value="crimson-velvet">Crimson Velvet</option>
                <option value="matrix-obsidian">Matrix Obsidian</option>
                <option value="oceanic">Oceanic Depths</option>
                <option value="nebula">Cosmic Nebula</option>
                <option value="sunset-synth">Sunset Synth</option>
                <option value="monolith">Dark Monolith</option>
                <option value="solar-light">Solar Light (Day)</option>
            </select>
        </div>
    </aside>

    <!-- MAIN CONTENT -->
    <main class="main-content">
        <div class="header-title">
            <h1>Diagnostic Cost Prediction</h1>
            <p>Enter patient parameters to run the Machine Learning estimation model.</p>
        </div>

        <div class="dashboard-grid">
            
            <!-- INPUT FORM -->
            <div class="glass-card input-card">
                <div class="card-header">
                    <span><i class="fa-solid fa-sliders"></i> Clinical Parameters</span>
                    <i class="fa-solid fa-microchip"></i>
                </div>
                <form id="predictForm" onsubmit="handlePrediction(event)">
                    <div class="form-grid">
                        <div class="form-group full">
                            <label>Patient Age: <span id="ageVal" style="color:var(--accent-primary)">35</span></label>
                            <div class="slider-flex">
                                <input type="range" id="age" min="18" max="100" value="35" oninput="document.getElementById('ageVal').innerText = this.value">
                                <span class="slider-val"><i class="fa-solid fa-cake-candles"></i></span>
                            </div>
                        </div>
                        <div class="form-group">
                            <label>Biological Sex</label>
                            <select id="sex" class="input-elem">
                                <option value="male">Male</option>
                                <option value="female">Female</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Tobacco Use</label>
                            <select id="smoker" class="input-elem">
                                <option value="no">Non-Smoker</option>
                                <option value="yes">Smoker</option>
                            </select>
                        </div>
                        <div class="form-group full">
                            <label>Body Mass Index (BMI): <span id="bmiVal" style="color:var(--accent-primary)">26.5</span></label>
                            <div class="slider-flex">
                                <input type="range" id="bmi" min="15.0" max="55.0" step="0.1" value="26.5" oninput="document.getElementById('bmiVal').innerText = this.value">
                                <span class="slider-val"><i class="fa-solid fa-weight-scale"></i></span>
                            </div>
                        </div>
                        <div class="form-group">
                            <label>Dependents / Children</label>
                            <input type="number" id="children" class="input-elem" min="0" max="10" value="0">
                        </div>
                        <div class="form-group">
                            <label>Geographic Region</label>
                            <select id="region" class="input-elem">
                                <option value="southeast">Southeast</option>
                                <option value="southwest">Southwest</option>
                                <option value="northeast">Northeast</option>
                                <option value="northwest">Northwest</option>
                            </select>
                        </div>
                        <button type="submit" class="btn-main" id="submitBtn">
                            <i class="fa-solid fa-bolt"></i> Generate Estimation
                        </button>
                    </div>
                </form>
            </div>

            <!-- RESULT CARD -->
            <div class="glass-card result-card">
                <div class="card-header">
                    <span><i class="fa-solid fa-receipt"></i> Financial Projection</span>
                    <i class="fa-solid fa-file-invoice-dollar"></i>
                </div>
                <div class="cost-display">
                    <div style="color: var(--text-muted); text-transform: uppercase; font-size: 0.9rem; font-weight: 800; font-family: var(--font-head); letter-spacing: 1px;">Total Estimated Charge</div>
                    <div class="cost-value" id="costOutput">---</div>
                    <div id="riskBadge" class="badge warning" style="display:none;">Awaiting Data</div>
                </div>
                <div id="breakdownList">
                    <p style="text-align:center; color: var(--text-muted); margin-top: 2.5rem; font-weight: 500;">Submit parameters to view financial breakdown.</p>
                </div>
            </div>

            <!-- CHARTS SECTION -->
            <div class="glass-card chart-card">
                <div class="card-header"><span><i class="fa-solid fa-chart-line"></i> Age vs Cost Trajectory</span></div>
                <div class="chart-container"><canvas id="lineChart"></canvas></div>
            </div>
            
            <div class="glass-card chart-card">
                <div class="card-header"><span><i class="fa-solid fa-chart-pie"></i> Cost Breakdown Distribution</span></div>
                <div class="chart-container"><canvas id="doughnutChart"></canvas></div>
            </div>

            <!-- HISTORY TABLE -->
            <div class="glass-card table-card">
                <div class="card-header">
                    <span><i class="fa-solid fa-clock-rotate-left"></i> Recent Estimations Ledger</span>
                    <button onclick="loadHistory()" style="background:rgba(255,255,255,0.05); padding: 0.5rem 1rem; border-radius: 8px; border:1px solid rgba(255,255,255,0.1); color:var(--text-main); font-family: var(--font-head); font-weight: 700; cursor:pointer; transition: var(--transition-fast);"><i class="fa-solid fa-rotate-right" style="color:var(--accent-primary)"></i> Refresh</button>
                </div>
                <div style="overflow-x:auto;">
                    <table class="styled-table">
                        <thead>
                            <tr>
                                <th>Timestamp</th>
                                <th>Age</th>
                                <th>BMI</th>
                                <th>Smoker</th>
                                <th>Region</th>
                                <th>Est. Charge</th>
                            </tr>
                        </thead>
                        <tbody id="historyTableBody">
                            <tr><td colspan="6" style="text-align:center;">Loading records...</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </main>

    <!-- Toasts -->
    <div class="toast-container" id="toastBox"></div>

    <script>
        // Global Chart Instances
        let lineChartObj = null;
        let doughnutChartObj = null;
        let currentBreakdown = null;

        // Toast Notification System
        function showToast(message, type = 'success') {
            const box = document.getElementById('toastBox');
            const toast = document.createElement('div');
            toast.className = 'toast';
            const icon = type === 'success' ? '<i class="fa-solid fa-circle-check" style="color:#10b981; font-size:1.2rem;"></i>' : '<i class="fa-solid fa-triangle-exclamation" style="color:#f43f5e; font-size:1.2rem;"></i>';
            toast.innerHTML = `${icon} <span>${message}</span>`;
            box.appendChild(toast);
            setTimeout(() => { toast.style.opacity = '0'; toast.style.transform = 'translateX(50px)'; setTimeout(() => toast.remove(), 400); }, 3500);
        }

        // Theme Management
        function changeTheme(theme) {
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('medico_theme', theme);
            setTimeout(renderCharts, 150); // Re-render charts with new colors
        }

        // Setup on load
        window.addEventListener('DOMContentLoaded', () => {
            const savedTheme = localStorage.getItem('medico_theme');
            if (savedTheme) {
                document.getElementById('themeSelect').value = savedTheme;
                document.documentElement.setAttribute('data-theme', savedTheme);
            } else {
                document.getElementById('themeSelect').value = "netflix-dark";
            }
            loadAnalyticsData();
            loadHistory();
        });

        // CSS Variable Helper
        function getCss(variable) {
            return getComputedStyle(document.documentElement).getPropertyValue(variable).trim();
        }

        // Counter Animation
        function animateValue(obj, start, end, duration) {
            let startTimestamp = null;
            const step = (timestamp) => {
                if (!startTimestamp) startTimestamp = timestamp;
                const progress = Math.min((timestamp - startTimestamp) / duration, 1);
                // Ease out cubic
                const easeProgress = 1 - Math.pow(1 - progress, 3);
                const current = easeProgress * (end - start) + start;
                obj.innerHTML = "$" + current.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits:2});
                if (progress < 1) { window.requestAnimationFrame(step); }
            };
            window.requestAnimationFrame(step);
        }

        // Form Submission
        async function handlePrediction(e) {
            e.preventDefault();
            const btn = document.getElementById('submitBtn');
            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Processing...';
            
            const payload = {
                age: document.getElementById('age').value,
                sex: document.getElementById('sex').value,
                bmi: document.getElementById('bmi').value,
                children: document.getElementById('children').value,
                smoker: document.getElementById('smoker').value,
                region: document.getElementById('region').value
            };

            try {
                const res = await fetch('/api/predict', { method: 'POST', body: JSON.stringify(payload) });
                const data = await res.json();
                
                if(data.success) {
                    showToast('Prediction generated successfully!');
                    
                    // Animate number
                    const costEl = document.getElementById('costOutput');
                    animateValue(costEl, 0, data.charge_val, 1200);
                    
                    // Update Badge
                    const badge = document.getElementById('riskBadge');
                    badge.style.display = 'inline-block';
                    badge.innerText = `${data.risk_metrics.risk_level} Risk (Score: ${data.risk_metrics.risk_score})`;
                    badge.className = `badge ${data.risk_metrics.badge_color}`;
                    
                    // Breakdown List
                    let html = '';
                    currentBreakdown = data.risk_metrics.breakdown;
                    for (const [key, val] of Object.entries(currentBreakdown)) {
                        html += `<div class="breakdown-item"><span>${key}</span><strong>$${val.toLocaleString(undefined, {minimumFractionDigits:2})}</strong></div>`;
                    }
                    document.getElementById('breakdownList').innerHTML = html;
                    
                    // Refresh components
                    renderCharts();
                    loadHistory();
                } else {
                    showToast(data.error, 'error');
                }
            } catch(err) {
                showToast('Server connection failed.', 'error');
            } finally {
                btn.innerHTML = '<i class="fa-solid fa-bolt"></i> Generate Estimation';
            }
        }

        // Load History Table
        async function loadHistory() {
            try {
                const res = await fetch('/api/history');
                const data = await res.json();
                const tbody = document.getElementById('historyTableBody');
                tbody.innerHTML = '';
                
                if(data.records.length === 0) {
                    tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;">No records found.</td></tr>';
                    return;
                }
                
                data.records.forEach(row => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td><span style="color:var(--text-muted); font-size:0.85rem">${row.timestamp}</span></td>
                        <td>${row.age}</td>
                        <td>${row.bmi}</td>
                        <td><span style="color:${row.smoker==='yes' ? '#f43f5e' : '#10b981'}; font-weight:700;">${row.smoker.toUpperCase()}</span></td>
                        <td><span style="text-transform:capitalize;">${row.region}</span></td>
                        <td style="font-weight:800; font-family: var(--font-head); color:var(--accent-primary)">$${row.charge.toLocaleString(undefined,{minimumFractionDigits:2})}</td>
                    `;
                    tbody.appendChild(tr);
                });
            } catch(err) {
                console.error("Failed to load history");
            }
        }

        // Global data cache for charts
        let chartDataCache = null;

        async function loadAnalyticsData() {
            try {
                const res = await fetch('/api/analytics');
                chartDataCache = await res.json();
                renderCharts();
            } catch(err) { console.error("Analytics load failed"); }
        }

        function renderCharts() {
            if(!chartDataCache) return;
            
            const prim = getCss('--accent-primary');
            const sec = getCss('--accent-secondary');
            const textMain = getCss('--text-main');
            const textMuted = getCss('--text-muted');
            const fontFamily = getCss('--font-body');

            // --- Line Chart (Age Trend) ---
            if(lineChartObj) lineChartObj.destroy();
            const lineCtx = document.getElementById('lineChart').getContext('2d');
            
            // Gradient fill
            let gradientFill = lineCtx.createLinearGradient(0, 0, 0, 400);
            gradientFill.addColorStop(0, prim.replace('rgb', 'rgba').replace(')', ', 0.3)'));
            gradientFill.addColorStop(1, 'rgba(0,0,0,0)');

            lineChartObj = new Chart(lineCtx, {
                type: 'line',
                data: {
                    labels: chartDataCache.age_trend.labels,
                    datasets: [
                        { label: 'Smoker Base', data: chartDataCache.age_trend.smoker_cost, borderColor: sec, borderDash: [5, 5], tension: 0.4 },
                        { label: 'Non-Smoker Trend', data: chartDataCache.age_trend.non_smoker_cost, borderColor: prim, backgroundColor: gradientFill, fill: true, tension: 0.4 }
                    ]
                },
                options: {
                    responsive: true, maintainAspectRatio: false,
                    plugins: { legend: { labels: { color: textMain, font: {family: fontFamily, weight: 600} } } },
                    scales: {
                        x: { ticks: { color: textMuted, font: {family: fontFamily} }, grid: { display: false } },
                        y: { ticks: { color: textMuted, font: {family: fontFamily} }, grid: { color: 'rgba(255,255,255,0.05)' } }
                    }
                }
            });

            // --- Doughnut Chart (Breakdown) ---
            if(doughnutChartObj) doughnutChartObj.destroy();
            const pieCtx = document.getElementById('doughnutChart').getContext('2d');
            
            let dLabels = ['Base', 'Age', 'BMI', 'Lifestyle'];
            let dData = [2500, 1500, 500, 0]; // Defaults
            
            if(currentBreakdown) {
                dLabels = Object.keys(currentBreakdown);
                dData = Object.values(currentBreakdown);
            }

            doughnutChartObj = new Chart(pieCtx, {
                type: 'doughnut',
                data: {
                    labels: dLabels,
                    datasets: [{
                        data: dData,
                        backgroundColor: [
                            prim, sec, getCss('--border-glow'), '#ffffff'
                        ],
                        borderWidth: 0,
                        hoverOffset: 15
                    }]
                },
                options: {
                    responsive: true, maintainAspectRatio: false,
                    cutout: '75%',
                    animation: { animateScale: true, animateRotate: true },
                    plugins: {
                        legend: { position: 'right', labels: { color: textMain, font: {family: fontFamily, weight: 600}, padding: 20 } }
                    }
                }
            });
        }
    </script>
</body>
</html>
"""

# =============================================================================
# 2. CONFIGURATION & DATABASE ARCHITECTURE
# =============================================================================

MODEL_PATH = "Practice.pkl"
DB_PATH = "medico_core_v2.db"
FEATURE_NAMES = ['age', 'sex', 'bmi', 'children', 'smoker', 'region']

# Encoding Maps
SEX_MAP = {'female': 0, 'male': 1}
SMOKER_MAP = {'no': 0, 'yes': 1}
REGION_MAP = {'northeast': 0, 'northwest': 1, 'southeast': 2, 'southwest': 3}

class DatabaseCore:
    """Handles SQLite persistence for patient prediction ledgers."""
    def __init__(self, db_file):
        self.db_file = db_file
        self._boot_sequence()
        
    def _get_conn(self):
        # check_same_thread=False allows Flask multithreading on Render/AWS
        conn = sqlite3.connect(self.db_file, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn
        
    def _boot_sequence(self):
        try:
            with self._get_conn() as conn:
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS predictions (
                        id TEXT PRIMARY KEY,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        age REAL, sex TEXT, bmi REAL, children INTEGER, 
                        smoker TEXT, region TEXT, charge REAL
                    )
                ''')
                conn.commit()
        except Exception as e:
            print(f"[DB ERROR] Initialization failed: {e}")

    def insert_record(self, data_dict, estimated_charge):
        try:
            with self._get_conn() as conn:
                conn.execute('''
                    INSERT INTO predictions (id, age, sex, bmi, children, smoker, region, charge)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    str(uuid.uuid4()), data_dict['age'], data_dict['sex'], data_dict['bmi'], 
                    data_dict['children'], data_dict['smoker'], data_dict['region'], estimated_charge
                ))
                conn.commit()
        except Exception as e:
            print(f"[DB ERROR] Insert failed: {e}")

    def fetch_recent(self, limit=10):
        try:
            with self._get_conn() as conn:
                cur = conn.execute('SELECT * FROM predictions ORDER BY timestamp DESC LIMIT ?', (limit,))
                rows = cur.fetchall()
                # Format timestamps for UI
                result = []
                for r in rows:
                    d = dict(r)
                    dt = datetime.datetime.strptime(d['timestamp'], '%Y-%m-%d %H:%M:%S')
                    d['timestamp'] = dt.strftime('%b %d, %H:%M')
                    result.append(d)
                return result
        except Exception as e:
            print(f"[DB ERROR] Fetch failed: {e}")
            return []

db_engine = DatabaseCore(DB_PATH)


# =============================================================================
# 3. MACHINE LEARNING ENGINE
# =============================================================================

class MLManager:
    """Manages the Scikit-Learn model loading and preprocessing."""
    def __init__(self):
        self.model = None
        self._load_binary()
        
    def _load_binary(self):
        if os.path.exists(MODEL_PATH):
            try:
                with open(MODEL_PATH, "rb") as f:
                    self.model = pickle.load(f)
                print(f"[ML ENGINE] Successfully loaded primary weights from {MODEL_PATH}")
                return
            except Exception as e:
                print(f"[ML ENGINE] Warning: Unpickle failed ({e}). Booting fallback.")
        else:
            print(f"[ML ENGINE] Warning: {MODEL_PATH} missing. Booting fallback.")
            
        self._generate_fallback()

    def _generate_fallback(self):
        """Generates an in-memory regression model to prevent crashes."""
        from sklearn.linear_model import LinearRegression
        # Synthetic dataset reflecting general insurance parameters
        X = np.array([
            [19,0,27.9,0,1,3], [18,1,33.7,1,0,2], [28,1,33.0,3,0,2],
            [33,1,22.7,0,0,1], [32,1,28.8,0,0,1], [31,0,25.7,0,1,2],
            [46,0,33.4,1,0,2], [37,0,27.7,3,0,1], [37,1,29.8,2,0,0],
            [60,0,25.8,0,0,1], [25,1,26.2,0,0,0], [62,0,26.2,0,1,2]
        ])
        y = np.array([
            16884, 1725, 4449, 21984, 3866, 37566, 
            8240, 7281, 6406, 28923, 2721, 27808
        ])
        self.model = LinearRegression().fit(X, y)
        print("[ML ENGINE] Fallback Linear Regression active.")

    def parse_inputs(self, raw_json):
        """Sanitizes JSON inputs to numpy arrays safely."""
        age = float(raw_json.get('age', 30))
        sex_raw = str(raw_json.get('sex')).lower()
        sex = SEX_MAP.get(sex_raw, 1)
        
        bmi = float(raw_json.get('bmi', 25.0))
        children = int(raw_json.get('children', 0))
        
        smoker_raw = str(raw_json.get('smoker')).lower()
        smoker = SMOKER_MAP.get(smoker_raw, 0)
        
        region_raw = str(raw_json.get('region')).lower()
        region = REGION_MAP.get(region_raw, 2)
        
        features = np.array([[age, sex, bmi, children, smoker, region]])
        clean_dict = {
            'age': age, 'sex': sex_raw, 'bmi': bmi, 
            'children': children, 'smoker': smoker_raw, 'region': region_raw
        }
        return features, clean_dict

    def run_inference(self, features):
        """Executes the prediction."""
        raw = self.model.predict(features)[0]
        return float(max(1500.0, raw)) # Ensure base minimum logic

ml_engine = MLManager()


# =============================================================================
# 4. ADVANCED RISK & FINANCIAL ANALYTICS
# =============================================================================

def calculate_detailed_risk(inputs, total_charge):
    """Calculates categorical risk and reverse-engineers cost drivers."""
    age = inputs['age']
    bmi = inputs['bmi']
    is_smoker = (inputs['smoker'] == 'yes')
    
    # 1. Base Score calculation (0-100)
    score = 15
    if age > 55: score += 25
    elif age > 40: score += 15
    
    if bmi > 35: score += 25
    elif bmi > 30: score += 15
    elif bmi > 25: score += 5
    
    if is_smoker: score += 35
    
    score = min(100, max(0, score))
    
    # 2. Risk Tiers
    if score < 30:
        level, color = "Low", "success"
    elif score < 65:
        level, color = "Moderate", "warning"
    else:
        level, color = "High/Critical", "danger"
        
    # 3. Financial Breakdown Proportions
    base = total_charge * 0.15
    smoker_tax = total_charge * 0.45 if is_smoker else 0
    age_tax = (age / 100) * total_charge * 0.25
    bmi_tax = max(0, (bmi - 25) / 20) * total_charge * 0.15
    
    # Normalize to ensure sum equals total exactly
    calculated_sum = base + smoker_tax + age_tax + bmi_tax
    diff = total_charge - calculated_sum
    base += diff 
    
    return {
        'risk_score': int(score),
        'risk_level': level,
        'badge_color': color,
        'breakdown': {
            'Hospital Base Fee': round(base, 2),
            'Age Demographic Factor': round(age_tax, 2),
            'BMI Health Index': round(bmi_tax, 2),
            'Tobacco Surcharge': round(smoker_tax, 2)
        }
    }


# =============================================================================
# 5. FLASK WEB SERVER ROUTING
# =============================================================================

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index_ui():
    """Serves the massive integrated UI."""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """Main inference endpoint."""
    try:
        req_data = request.get_json(force=True)
        features, clean_data = ml_engine.parse_inputs(req_data)
        
        # ML Prediction
        charge = ml_engine.run_inference(features)
        
        # Save to DB
        db_engine.insert_record(clean_data, charge)
        
        # Analytics
        risk_data = calculate_detailed_risk(clean_data, charge)
        
        return jsonify({
            'success': True,
            'charge_val': charge,
            'risk_metrics': risk_data
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/history', methods=['GET'])
def api_history():
    """Returns the latest DB records for the UI table."""
    records = db_engine.fetch_recent(limit=10)
    return jsonify({'success': True, 'records': records})

@app.route('/api/analytics', methods=['GET'])
def api_analytics():
    """Provides synthetic generation for Chart.js rendering."""
    ages = list(range(18, 65, 4))
    return jsonify({
        'age_trend': {
            'labels': ages,
            'non_smoker_cost': [3000 + (a**1.35) * 45 for a in ages],
            'smoker_cost': [17000 + (a**1.4) * 60 for a in ages]
        }
    })

# =============================================================================
# 6. SERVER EXECUTION (RENDER CONFIGURATION INCLUDED)
# =============================================================================

if __name__ == '__main__':
    print("==================================================")
    print("🚀 MEDICO.AI V4 SERVER BOOTING...")
    print("==================================================")
    
    # This automatically grabs the port Render assigns, or defaults to 5000 locally
    port = int(os.environ.get("PORT", 5000))
    
    # Threaded=True handles multiple UI requests smoothly
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
