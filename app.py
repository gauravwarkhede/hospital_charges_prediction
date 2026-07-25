"""
===============================================================================
MEDICO.AI - PREMIUM 3D F1 TELEMETRY EDITION (MODERN CLEAN UI)
===============================================================================
Advanced Predictive Analytics Engine for Hospital Charges
Features: 11 Premium F1 Themes, Clean Modern Layout, Neumorphic 3D UI, 
Mouse-Tracking Tilt Physics, Chart.js, SQLite Persistence, and ML Engine.
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
<html lang="en" data-theme="mercedes">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Medico.AI | Premium 3D Pit Wall</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800;900&family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        /* ================= CSS VARIABLES & 3D THEMES ================= */
        :root {
            --sidebar-width: 280px;
            --card-radius: 12px; /* Sharper corners inspired by clean e-com UI */
            --transition-fast: all 0.25s cubic-bezier(0.25, 0.8, 0.25, 1);
            --transition-smooth: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
            --font-head: 'Montserrat', sans-serif;
            --font-body: 'Inter', sans-serif;
        }

        /* 11 Premium 3D Formula 1 Themes (Neumorphic Tuned) */
        [data-theme="mercedes"] {
            --bg-base: #14171A; --bg-card-light: #1a1e22; --bg-card-dark: #0e1012;
            --shadow-outer: 15px 15px 30px #0b0d0e, -15px -15px 30px #1d2126;
            --shadow-inner: inset 8px 8px 16px #0b0d0e, inset -8px -8px 16px #1d2126;
            --accent-primary: #00A19C; --accent-secondary: #C8CCCE; --text-main: #ffffff; --text-muted: #8c9298;
        }
        [data-theme="mclaren"] {
            --bg-base: #121212; --bg-card-light: #181818; --bg-card-dark: #0c0c0c;
            --shadow-outer: 15px 15px 30px #080808, -15px -15px 30px #1c1c1c;
            --shadow-inner: inset 8px 8px 16px #080808, inset -8px -8px 16px #1c1c1c;
            --accent-primary: #FF8000; --accent-secondary: #474747; --text-main: #ffffff; --text-muted: #999999;
        }
        [data-theme="redbull"] {
            --bg-base: #0B1221; --bg-card-light: #0e182c; --bg-card-dark: #080c16;
            --shadow-outer: 15px 15px 30px #060911, -15px -15px 30px #101b31;
            --shadow-inner: inset 8px 8px 16px #060911, inset -8px -8px 16px #101b31;
            --accent-primary: #FDB927; --accent-secondary: #CC1E4A; --text-main: #ffffff; --text-muted: #8A9CAE;
        }
        [data-theme="ferrari"] {
            --bg-base: #171111; --bg-card-light: #1e1616; --bg-card-dark: #100c0c;
            --shadow-outer: 15px 15px 30px #0b0808, -15px -15px 30px #231a1a;
            --shadow-inner: inset 8px 8px 16px #0b0808, inset -8px -8px 16px #231a1a;
            --accent-primary: #EF1A2D; --accent-secondary: #FFDF00; --text-main: #ffffff; --text-muted: #A37A7A;
        }
        [data-theme="williams"] {
            --bg-base: #0A1424; --bg-card-light: #0d1a2f; --bg-card-dark: #070e19;
            --shadow-outer: 15px 15px 30px #050a12, -15px -15px 30px #0f1e36;
            --shadow-inner: inset 8px 8px 16px #050a12, inset -8px -8px 16px #0f1e36;
            --accent-primary: #00A3E0; --accent-secondary: #FFFFFF; --text-main: #ffffff; --text-muted: #7A99B8;
        }
        [data-theme="astonmartin"] {
            --bg-base: #0D1C16; --bg-card-light: #11251d; --bg-card-dark: #09130f;
            --shadow-outer: 15px 15px 30px #060e0a, -15px -15px 30px #142a22;
            --shadow-inner: inset 8px 8px 16px #060e0a, inset -8px -8px 16px #142a22;
            --accent-primary: #CEDC00; --accent-secondary: #00665E; --text-main: #ffffff; --text-muted: #80998F;
        }
        [data-theme="haas"] {
            --bg-base: #161616; --bg-card-light: #1d1d1d; --bg-card-dark: #0f0f0f;
            --shadow-outer: 15px 15px 30px #0a0a0a, -15px -15px 30px #222222;
            --shadow-inner: inset 8px 8px 16px #0a0a0a, inset -8px -8px 16px #222222;
            --accent-primary: #E6002B; --accent-secondary: #FFFFFF; --text-main: #ffffff; --text-muted: #999999;
        }
        [data-theme="alpine"] {
            --bg-base: #0F1722; --bg-card-light: #141e2d; --bg-card-dark: #0a1017;
            --shadow-outer: 15px 15px 30px #070b10, -15px -15px 30px #172334;
            --shadow-inner: inset 8px 8px 16px #070b10, inset -8px -8px 16px #172334;
            --accent-primary: #FD4BC7; --accent-secondary: #005094; --text-main: #ffffff; --text-muted: #8A9CAE;
        }
        [data-theme="cadillac"] {
            --bg-base: #141414; --bg-card-light: #1b1b1b; --bg-card-dark: #0d0d0d;
            --shadow-outer: 15px 15px 30px #090909, -15px -15px 30px #1f1f1f;
            --shadow-inner: inset 8px 8px 16px #090909, inset -8px -8px 16px #1f1f1f;
            --accent-primary: #D4AF37; --accent-secondary: #FFFFFF; --text-main: #ffffff; --text-muted: #A3A3A3;
        }
        [data-theme="audi"] {
            --bg-base: #1A1A1C; --bg-card-light: #222225; --bg-card-dark: #121213;
            --shadow-outer: 15px 15px 30px #0d0d0d, -15px -15px 30px #27272b;
            --shadow-inner: inset 8px 8px 16px #0d0d0d, inset -8px -8px 16px #27272b;
            --accent-primary: #F50537; --accent-secondary: #C0C0C0; --text-main: #ffffff; --text-muted: #999999;
        }
        [data-theme="sauber"] {
            --bg-base: #111411; --bg-card-light: #161a16; --bg-card-dark: #0c0e0c;
            --shadow-outer: 15px 15px 30px #080a08, -15px -15px 30px #1a1e1a;
            --shadow-inner: inset 8px 8px 16px #080a08, inset -8px -8px 16px #1a1e1a;
            --accent-primary: #00E701; --accent-secondary: #FFFFFF; --text-main: #ffffff; --text-muted: #809980;
        }

        /* ================= BASE STYLES & LAYOUT ================= */
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background-color: var(--bg-base); color: var(--text-main); font-family: var(--font-body);
            min-height: 100vh; overflow-x: hidden; display: flex; transition: background-color 0.5s ease;
        }

        /* Animations */
        @keyframes popIn { 0% { opacity: 0; transform: scale(0.95) translateY(40px); } 100% { opacity: 1; transform: scale(1) translateY(0); } }
        @keyframes slideInRight { from { opacity: 0; transform: translateX(50px); } to { opacity: 1; transform: translateX(0); } }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

        /* ================= SIDEBAR ================= */
        .sidebar {
            width: var(--sidebar-width); height: 100vh; position: fixed; top: 0; left: 0;
            background: linear-gradient(145deg, var(--bg-card-light), var(--bg-card-dark));
            box-shadow: 10px 0px 30px rgba(0,0,0,0.5); padding: 3rem 2rem;
            display: flex; flex-direction: column; z-index: 100; border-right: 1px solid rgba(255,255,255,0.02);
        }
        .brand { display: flex; align-items: center; gap: 15px; margin-bottom: 4rem; cursor: pointer; }
        .brand-text { font-family: var(--font-head); font-size: 2.2rem; font-weight: 900; letter-spacing: -1px; text-transform: uppercase; line-height: 1;}
        
        .nav-menu { display: flex; flex-direction: column; gap: 10px; flex: 1; }
        .nav-item {
            padding: 1.2rem 1.5rem; border-radius: var(--card-radius); cursor: pointer; display: flex; align-items: center; gap: 15px;
            font-weight: 700; color: var(--text-muted); transition: var(--transition-fast);
            text-transform: uppercase; font-size: 0.85rem; letter-spacing: 1.5px; font-family: var(--font-head);
            border: 1px solid transparent;
        }
        .nav-item:hover, .nav-item.active {
            color: var(--text-main); border-color: rgba(255,255,255,0.1);
            background: rgba(255,255,255,0.03); transform: translateX(5px);
        }
        .nav-item.active i { color: var(--accent-primary); }

        .theme-selector { margin-top: auto; }
        .theme-selector label { display: block; font-size: 0.75rem; margin-bottom: 12px; color: var(--text-muted); text-transform: uppercase; font-weight: 800; letter-spacing: 2px;}
        .theme-select {
            appearance: none; width: 100%; 
            background: var(--bg-base); box-shadow: var(--shadow-inner);
            color: var(--text-main); border: none; padding: 1.2rem; border-radius: var(--card-radius);
            font-family: var(--font-head); font-weight: 800; font-size: 0.9rem; outline: none; cursor: pointer; transition: var(--transition-fast); text-transform: uppercase;
        }
        .theme-select:hover { color: var(--accent-primary); }
        .theme-select option { background-color: var(--bg-base); color: #fff; font-family: var(--font-body); }

        /* ================= MAIN CONTENT ================= */
        .main-content { margin-left: var(--sidebar-width); flex: 1; padding: 4rem 5rem; width: calc(100% - var(--sidebar-width)); perspective: 1800px; }
        
        .header-title { margin-bottom: 4rem; animation: fadeIn 0.8s ease backwards; }
        .header-title h1 { font-family: var(--font-head); font-size: 4rem; text-transform: uppercase; font-weight: 900; margin-bottom: 10px; letter-spacing: -2px; line-height: 1.1; text-shadow: 10px 10px 20px rgba(0,0,0,0.5);}
        .header-title p { color: var(--text-muted); font-size: 1.2rem; font-weight: 500; letter-spacing: 1px;}
        .header-accent { color: var(--accent-primary); }

        .dashboard-grid { display: grid; grid-template-columns: repeat(12, 1fr); gap: 3rem; }

        /* Clean Modern 3D Cards */
        .glass-card {
            background: linear-gradient(145deg, var(--bg-card-light), var(--bg-card-dark));
            box-shadow: var(--shadow-outer); border-radius: var(--card-radius); padding: 3rem; 
            transition: transform 0.1s ease, box-shadow 0.3s ease; position: relative;
            transform-style: preserve-3d; animation: popIn 0.8s cubic-bezier(0.16, 1, 0.3, 1) backwards; 
            border: 1px solid rgba(255,255,255,0.03);
        }
        
        .glass-card:nth-child(1) { animation-delay: 0.1s; }
        .glass-card:nth-child(2) { animation-delay: 0.2s; }
        .glass-card:nth-child(3) { animation-delay: 0.3s; }
        .glass-card:nth-child(4) { animation-delay: 0.4s; }

        .card-header {
            display: flex; align-items: center; justify-content: space-between; font-family: var(--font-head); font-size: 1.5rem; font-weight: 900;
            color: var(--text-main); margin-bottom: 2.5rem; text-transform: uppercase; letter-spacing: 1px;
            transform: translateZ(25px); /* Stronger 3D pop */
        }
        
        /* Grid Placements */
        .input-card { grid-column: span 7; }
        .result-card { grid-column: span 5; }
        .chart-card { grid-column: span 6; height: 450px; display: flex; flex-direction: column; }
        .chart-container { flex: 1; position: relative; width: 100%; height: 100%; transform: translateZ(15px); }
        .table-card { grid-column: span 12; }

        /* ================= FORMS & INPUTS ================= */
        .form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 2.5rem; transform: translateZ(15px); }
        .form-group { display: flex; flex-direction: column; gap: 12px; }
        .form-group.full { grid-column: 1 / -1; }
        
        label { font-size: 0.8rem; font-weight: 800; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1.5px; font-family: var(--font-head); }
        
        .input-elem {
            appearance: none; background: var(--bg-base); box-shadow: var(--shadow-inner); border: 1px solid transparent;
            padding: 1.2rem 1.5rem; border-radius: 8px; color: var(--text-main); font-family: var(--font-body); font-weight: 600; font-size: 1rem; transition: var(--transition-fast); outline: none;
        }
        select.input-elem {
            background-image: url("data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%238c9298%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E");
            background-repeat: no-repeat; background-position: right 1.5rem top 50%; background-size: 0.8rem auto; text-transform: uppercase; font-family: var(--font-head); font-weight: 800;
        }
        .input-elem:focus { border-color: var(--accent-primary); }
        
        .slider-flex { display: flex; align-items: center; gap: 20px; background: var(--bg-base); box-shadow: var(--shadow-inner); padding: 1rem 1.5rem; border-radius: 8px; }
        .slider-flex input[type="range"] { flex: 1; accent-color: var(--accent-primary); cursor: pointer; height: 6px; background: rgba(255,255,255,0.1); outline: none; border-radius: 5px;}
        .slider-val { font-family: var(--font-head); font-size: 1.4rem; font-weight: 900; color: var(--text-main); width: 50px; text-align: right; }

        /* Solid E-com style Button */
        .btn-main {
            grid-column: 1 / -1; padding: 1.5rem; border: none; border-radius: 8px;
            background: var(--accent-primary); box-shadow: 0 10px 20px rgba(0,0,0,0.4); 
            color: #fff; font-family: var(--font-head); font-size: 1.1rem; font-weight: 900; letter-spacing: 2px;
            cursor: pointer; transition: var(--transition-fast); margin-top: 1.5rem; text-transform: uppercase;
            transform: translateZ(35px);
        }
        .btn-main:hover { filter: brightness(1.15); transform: translateZ(40px) translateY(-3px); box-shadow: 0 15px 25px rgba(0,0,0,0.5); }
        .btn-main:active { transform: translateZ(15px) translateY(2px); box-shadow: 0 5px 10px rgba(0,0,0,0.5); }

        /* ================= RESULT DISPLAY ================= */
        .cost-display {
            text-align: center; padding: 3rem 1rem; border-radius: 12px;
            background: var(--bg-base); box-shadow: var(--shadow-inner); margin-bottom: 2.5rem;
            transform: translateZ(20px); border-top: 4px solid var(--accent-primary);
        }
        .cost-value { font-family: var(--font-head); font-size: 4.5rem; font-weight: 900; color: var(--text-main); margin: 1rem 0; letter-spacing: -3px; }
        
        .badge { display: inline-block; padding: 0.8rem 2rem; border-radius: 4px; font-family: var(--font-head); font-size: 0.85rem; font-weight: 900; text-transform: uppercase; letter-spacing: 2px; }
        .badge.success { background: #10b981; color: #fff; }
        .badge.warning { background: #f59e0b; color: #fff; }
        .badge.danger { background: #f43f5e; color: #fff; }

        .breakdown-item {
            display: flex; justify-content: space-between; align-items: center; padding: 1.5rem;
            background: var(--bg-base); box-shadow: var(--shadow-outer); border-radius: 8px; margin-bottom: 15px;
            transition: var(--transition-fast); font-weight: 700; font-size: 0.85rem; text-transform: uppercase; font-family: var(--font-head); letter-spacing: 1px;
            transform: translateZ(15px); border-left: 4px solid var(--accent-primary);
        }
        .breakdown-item:hover { transform: translateZ(25px) translateX(10px); color: var(--accent-primary);}
        .breakdown-item strong { font-family: var(--font-head); font-size: 1.25rem; color: var(--text-main); }

        /* ================= DATA TABLE ================= */
        .styled-table { width: 100%; border-collapse: separate; border-spacing: 0 15px; margin-top: 1rem; transform: translateZ(15px); }
        .styled-table th { padding: 1rem 1.5rem; text-align: left; color: var(--text-muted); font-weight: 900; text-transform: uppercase; font-size: 0.8rem; font-family: var(--font-head); letter-spacing: 2px; border-bottom: 1px solid rgba(255,255,255,0.05);}
        .styled-table td { padding: 1.5rem; background: var(--bg-base); font-weight: 600; font-family: var(--font-body); }
        .styled-table tr td:first-child { border-top-left-radius: 8px; border-bottom-left-radius: 8px; box-shadow: inset 5px 5px 10px rgba(0,0,0,0.3); }
        .styled-table tr td:last-child { border-top-right-radius: 8px; border-bottom-right-radius: 8px; box-shadow: inset -5px 5px 10px rgba(0,0,0,0.3); }
        .styled-table tr { box-shadow: var(--shadow-outer); transition: var(--transition-fast); }
        .styled-table tr:hover { transform: scale(1.02) translateY(-3px); }

        .btn-refresh {
            background: transparent; border: 2px solid var(--text-muted); padding: 0.8rem 1.5rem; border-radius: 8px;
            color: var(--text-muted); font-family: var(--font-head); font-weight: 900; cursor: pointer; text-transform: uppercase; transition: var(--transition-fast); font-size: 0.8rem; letter-spacing: 1px;
        }
        .btn-refresh:hover { border-color: var(--accent-primary); color: var(--accent-primary); }

        /* ================= TOAST NOTIFICATIONS ================= */
        .toast-container { position: fixed; bottom: 40px; right: 40px; z-index: 1000; display: flex; flex-direction: column; gap: 15px; }
        .toast {
            background: var(--bg-base); box-shadow: var(--shadow-outer); border-radius: 8px;
            padding: 1.5rem 2rem; animation: slideInRight 0.4s cubic-bezier(0.25, 0.8, 0.25, 1) forwards; 
            display: flex; align-items: center; gap: 15px; font-weight: 900; font-family: var(--font-head); text-transform: uppercase; font-size: 0.95rem; color: var(--text-main);
            border-left: 6px solid var(--accent-primary);
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
            <div class="brand-text">MEDICO<span style="color:var(--accent-primary)">.AI</span></div>
        </div>
        <nav class="nav-menu">
            <div class="nav-item active">Telemetry Matrix</div>
            <div class="nav-item">Visual Cortex</div>
            <div class="nav-item">Sector Logs</div>
            <div class="nav-item">Pit Settings</div>
        </nav>
        <div class="theme-selector">
            <label>Constructor Theme</label>
            <select id="themeSelect" class="theme-select" onchange="changeTheme(this.value)">
                <option value="mercedes">Mercedes AMG</option>
                <option value="mclaren">McLaren Papaya</option>
                <option value="redbull">Red Bull Racing</option>
                <option value="ferrari">Scuderia Ferrari</option>
                <option value="williams">Williams Racing</option>
                <option value="astonmartin">Aston Martin</option>
                <option value="haas">Haas F1</option>
                <option value="alpine">Alpine F1</option>
                <option value="cadillac">Cadillac Racing</option>
                <option value="audi">Audi Sport</option>
                <option value="sauber">Kick Sauber</option>
            </select>
        </div>
    </aside>

    <!-- MAIN CONTENT -->
    <main class="main-content">
        <div class="header-title">
            <h1>Diagnostic<br><span class="header-accent">Cost Telemetry</span></h1>
            <p>Modern Machine Learning Estimation Matrix</p>
        </div>

        <div class="dashboard-grid">
            
            <!-- INPUT FORM -->
            <div class="glass-card input-card" data-tilt>
                <div class="card-header">
                    <span>Clinical Profile</span>
                </div>
                <form id="predictForm" onsubmit="handlePrediction(event)">
                    <div class="form-grid">
                        <div class="form-group full">
                            <label>Patient Age: <span id="ageVal" style="color:var(--accent-primary)">35</span></label>
                            <div class="slider-flex">
                                <input type="range" id="age" min="18" max="100" value="35" oninput="document.getElementById('ageVal').innerText = this.value">
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
                            Initiate Projection
                        </button>
                    </div>
                </form>
            </div>

            <!-- RESULT CARD -->
            <div class="glass-card result-card" data-tilt>
                <div class="card-header">
                    <span>Projection Output</span>
                </div>
                <div class="cost-display">
                    <div style="color: var(--text-muted); text-transform: uppercase; font-size: 0.9rem; font-weight: 800; font-family: var(--font-head); letter-spacing: 2px;">Estimated Total Charge</div>
                    <div class="cost-value" id="costOutput">---</div>
                    <div id="riskBadge" class="badge warning" style="display:none;">Awaiting Data</div>
                </div>
                <div id="breakdownList">
                    <p style="text-align:center; color: var(--text-muted); margin-top: 2.5rem; font-weight: 700; font-family:var(--font-head); text-transform:uppercase;">Input data to view 3D breakdown.</p>
                </div>
            </div>

            <!-- CHARTS SECTION -->
            <div class="glass-card chart-card" data-tilt>
                <div class="card-header"><span>Age vs Cost Trajectory</span></div>
                <div class="chart-container"><canvas id="lineChart"></canvas></div>
            </div>
            
            <div class="glass-card chart-card" data-tilt>
                <div class="card-header"><span>Cost Distribution Profile</span></div>
                <div class="chart-container"><canvas id="doughnutChart"></canvas></div>
            </div>

            <!-- HISTORY TABLE -->
            <div class="glass-card table-card" data-tilt>
                <div class="card-header">
                    <span>Historic Telemetry Logs</span>
                    <button class="btn-refresh" onclick="loadHistory()">Refresh Logs</button>
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
                            <tr><td colspan="6" style="text-align:center; font-family:var(--font-head); font-weight:800; text-transform:uppercase;">Loading records...</td></tr>
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

        // --- 3D TILT EFFECT LOGIC ---
        document.querySelectorAll('[data-tilt]').forEach(card => {
            card.addEventListener('mousemove', e => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left; 
                const y = e.clientY - rect.top;
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                const rotateX = ((y - centerY) / centerY) * -4; // Max 4 deg rotation
                const rotateY = ((x - centerX) / centerX) * 4;
                
                card.style.transform = `perspective(1200px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.01, 1.01, 1.01)`;
                card.style.transition = 'transform 0.1s ease';
            });

            card.addEventListener('mouseleave', () => {
                card.style.transform = 'perspective(1200px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
                card.style.transition = 'transform 0.5s cubic-bezier(0.25, 0.8, 0.25, 1)';
            });
        });

        // Toast Notification System
        function showToast(message, type = 'success') {
            const box = document.getElementById('toastBox');
            const toast = document.createElement('div');
            toast.className = 'toast';
            const icon = type === 'success' ? '<i class="fa-solid fa-check" style="color:var(--accent-primary); font-size:1.4rem;"></i>' : '<i class="fa-solid fa-xmark" style="color:#f43f5e; font-size:1.4rem;"></i>';
            toast.innerHTML = `${icon} <span>${message}</span>`;
            box.appendChild(toast);
            setTimeout(() => { toast.style.opacity = '0'; toast.style.transform = 'translateX(50px) scale(0.9)'; setTimeout(() => toast.remove(), 400); }, 3500);
        }

        // Theme Management
        function changeTheme(theme) {
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('medico_premium_f1_theme', theme);
            setTimeout(renderCharts, 200); // Re-render charts with new colors
        }

        // Setup on load
        window.addEventListener('DOMContentLoaded', () => {
            const savedTheme = localStorage.getItem('medico_premium_f1_theme');
            if (savedTheme) {
                document.getElementById('themeSelect').value = savedTheme;
                document.documentElement.setAttribute('data-theme', savedTheme);
            } else {
                document.getElementById('themeSelect').value = "mercedes";
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
                const easeProgress = 1 - Math.pow(1 - progress, 4); // Quartic ease out
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
            btn.innerHTML = 'PROCESSING...';
            
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
                    showToast('Projection Generated');
                    
                    // Animate number
                    const costEl = document.getElementById('costOutput');
                    animateValue(costEl, 0, data.charge_val, 1500);
                    
                    // Update Badge
                    const badge = document.getElementById('riskBadge');
                    badge.style.display = 'inline-block';
                    badge.innerText = `${data.risk_metrics.risk_level} Risk (Score: ${data.risk_metrics.risk_score})`;
                    badge.className = `badge ${data.risk_metrics.badge_color}`;
                    
                    // Breakdown List
                    let html = '';
                    currentBreakdown = data.risk_metrics.breakdown;
                    let delay = 0;
                    for (const [key, val] of Object.entries(currentBreakdown)) {
                        html += `<div class="breakdown-item" style="animation: slideInRight 0.4s ease backwards; animation-delay: ${delay}s"><span>${key}</span><strong>$${val.toLocaleString(undefined, {minimumFractionDigits:2})}</strong></div>`;
                        delay += 0.1;
                    }
                    document.getElementById('breakdownList').innerHTML = html;
                    
                    // Refresh components
                    renderCharts();
                    loadHistory();
                } else {
                    showToast(data.error, 'error');
                }
            } catch(err) {
                showToast('Connection Failed.', 'error');
            } finally {
                btn.innerHTML = 'Initiate Projection';
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
                    tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; font-family:var(--font-head); font-weight:800; text-transform:uppercase;">No logs found.</td></tr>';
                    return;
                }
                
                data.records.forEach(row => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td><span style="color:var(--text-muted); font-size:0.85rem; font-family:var(--font-head); font-weight:800;">${row.timestamp}</span></td>
                        <td style="font-family:var(--font-head); font-weight:800;">${row.age}</td>
                        <td style="font-family:var(--font-head); font-weight:800;">${row.bmi}</td>
                        <td><span style="color:${row.smoker==='yes' ? '#f43f5e' : '#10b981'}; font-weight:900; font-family:var(--font-head); text-transform:uppercase;">${row.smoker}</span></td>
                        <td style="text-transform:uppercase; font-family:var(--font-head); font-weight:800;">${row.region}</td>
                        <td style="font-weight:900; font-family: var(--font-head); color:var(--text-main); font-size: 1.1rem;">$${row.charge.toLocaleString(undefined,{minimumFractionDigits:2})}</td>
                    `;
                    tbody.appendChild(tr);
                });
            } catch(err) {
                console.error("Failed to load telemetry logs");
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
            const fontHead = getCss('--font-head');

            // --- Line Chart (Age Trend) ---
            if(lineChartObj) lineChartObj.destroy();
            const lineCtx = document.getElementById('lineChart').getContext('2d');

            lineChartObj = new Chart(lineCtx, {
                type: 'line',
                data: {
                    labels: chartDataCache.age_trend.labels,
                    datasets: [
                        { label: 'Smoker Baseline', data: chartDataCache.age_trend.smoker_cost, borderColor: sec, borderDash: [5, 5], tension: 0.4, borderWidth: 3 },
                        { label: 'Non-Smoker Trajectory', data: chartDataCache.age_trend.non_smoker_cost, borderColor: prim, backgroundColor: prim.replace(')', ', 0.15)').replace('rgb', 'rgba'), fill: true, tension: 0.4, borderWidth: 4 }
                    ]
                },
                options: {
                    responsive: true, maintainAspectRatio: false,
                    plugins: { legend: { labels: { color: textMain, font: {family: fontHead, weight: 800} } } },
                    scales: {
                        x: { ticks: { color: textMuted, font: {family: fontHead, weight:800} }, grid: { display: false } },
                        y: { ticks: { color: textMuted, font: {family: fontHead, weight:800} }, grid: { color: 'rgba(255,255,255,0.05)' } }
                    },
                    elements: { point: { radius: 0, hitRadius: 10, hoverRadius: 8, backgroundColor: prim, borderColor: '#fff', borderWidth: 2 } } 
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
                            prim, sec, '#555555', '#222222'
                        ],
                        borderWidth: 4,
                        borderColor: getCss('--bg-base'),
                        hoverOffset: 15,
                        borderRadius: 5
                    }]
                },
                options: {
                    responsive: true, maintainAspectRatio: false,
                    cutout: '75%',
                    animation: { animateScale: true, animateRotate: true },
                    plugins: {
                        legend: { position: 'right', labels: { color: textMain, font: {family: fontHead, weight: 800}, padding: 25 } }
                    },
                    layout: { padding: 10 }
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
DB_PATH = "medico_core_v3_premium_clean.db"
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
    print("🚀 MEDICO.AI V7 SERVER BOOTING...")
    print("==================================================")
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
