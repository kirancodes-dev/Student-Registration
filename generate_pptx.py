#!/usr/bin/env python3
"""
Generate a professional 16:9 PowerPoint Presentation (.pptx) with 14 slides
Features:
- Sapthagiri University logo on the top right of all pages (matching background)
- Names and SRNs of all 3 members on all slides
- Clean, premium Navy & Gold themed slide layout
- Highly visual design using shapes, tables, blocks, and indicators
"""

import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# Brand Colors
NAVY = RGBColor(0, 49, 126)      # #00317e
GOLD = RGBColor(212, 175, 55)    # #D4AF37
DARK_GRAY = RGBColor(28, 28, 30) # #1C1C1E
LIGHT_GRAY = RGBColor(242, 242, 247) # #F2F2F7
WHITE = RGBColor(255, 255, 255)  # #FFFFFF
MUTED_GRAY = RGBColor(110, 110, 115) # #6E6E73
SUCCESS_GREEN = RGBColor(16, 185, 129) # #10B981

LOGO_PATH = "static/logo.png"

def create_presentation():
    # Initialize Presentation
    prs = Presentation()
    
    # Set to widescreen 16:9 aspect ratio
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    blank_layout = prs.slide_layouts[6] # Blank slide
    
    # 👥 Team Members info
    members_text = "Keerthana GP (24SUUBECS0914)  |  Keerthana BS (23SUUBECS0909)  |  Kiran M Biradar (24SUUBECS0937)"
    
    # Helper: Set slide background to white (so logo matches background)
    def set_white_background(slide):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = WHITE

    # Helper: Add Logo at top right
    def add_logo(slide, is_title_slide=False):
        if os.path.exists(LOGO_PATH):
            if is_title_slide:
                # Place larger logo on title slide
                slide.shapes.add_picture(LOGO_PATH, Inches(4.5), Inches(1.5), width=Inches(4.33))
            else:
                # Standard top right logo
                slide.shapes.add_picture(LOGO_PATH, Inches(10.5), Inches(0.25), width=Inches(2.5))

    # Helper: Add Footer on content slides
    def add_footer(slide):
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(11.7), Inches(0.4))
        tf = footer_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_bottom = tf.margin_right = 0
        p = tf.paragraphs[0]
        p.text = f"Student Hub  |  Sapthagiri University  |  {members_text}"
        p.font.name = "Arial"
        p.font.size = Pt(9.5)
        p.font.color.rgb = MUTED_GRAY
        p.alignment = PP_ALIGN.CENTER

    # Helper: Add standard slide template
    def add_content_slide(title_text):
        slide = prs.slides.add_slide(blank_layout)
        set_white_background(slide)
        add_logo(slide)
        add_footer(slide)
        
        # Slide Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(9.5), Inches(0.8))
        tf = title_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_bottom = tf.margin_right = 0
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = "Arial"
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = NAVY
        
        # Gold Accent Line below title
        line = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.15), Inches(11.7), Inches(0.04)
        )
        line.fill.solid()
        line.fill.fore_color.rgb = GOLD
        line.line.color.rgb = GOLD
        
        return slide

    # ==========================================
    # SLIDE 1: Title Slide
    # ==========================================
    slide_1 = prs.slides.add_slide(blank_layout)
    set_white_background(slide_1)
    add_logo(slide_1, is_title_slide=True)
    
    # Title & Subtitle Card (Bottom half of title slide)
    title_box = slide_1.shapes.add_textbox(Inches(0.8), Inches(3.2), Inches(11.7), Inches(1.8))
    tf = title_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_bottom = tf.margin_right = 0
    
    p1 = tf.paragraphs[0]
    p1.text = "STUDENT HUB"
    p1.font.name = "Arial"
    p1.font.size = Pt(48)
    p1.font.bold = True
    p1.font.color.rgb = NAVY
    p1.alignment = PP_ALIGN.CENTER
    
    p2 = tf.add_paragraph()
    p2.text = "Premium Online Student Registration System"
    p2.font.name = "Arial"
    p2.font.size = Pt(22)
    p2.font.bold = True
    p2.font.color.rgb = GOLD
    p2.alignment = PP_ALIGN.CENTER
    p2.space_before = Pt(8)

    # Presenter / Author Details
    presenter_box = slide_1.shapes.add_textbox(Inches(0.8), Inches(5.2), Inches(11.7), Inches(1.8))
    tf_pres = presenter_box.text_frame
    tf_pres.word_wrap = True
    tf_pres.margin_left = tf_pres.margin_top = tf_pres.margin_bottom = tf_pres.margin_right = 0
    
    p_pres_title = tf_pres.paragraphs[0]
    p_pres_title.text = "DEVELOPMENT TEAM"
    p_pres_title.font.name = "Arial"
    p_pres_title.font.size = Pt(11)
    p_pres_title.font.bold = True
    p_pres_title.font.color.rgb = MUTED_GRAY
    p_pres_title.alignment = PP_ALIGN.CENTER
    
    team = [
        ("Keerthana GP", "24SUUBECS0914"),
        ("Keerthana BS", "23SUUBECS0909"),
        ("Kiran M Biradar", "24SUUBECS0937")
    ]
    
    for name, srn in team:
        p_member = tf_pres.add_paragraph()
        p_member.text = f"{name}  ({srn})"
        p_member.font.name = "Arial"
        p_member.font.size = Pt(13.5)
        p_member.font.bold = True
        p_member.font.color.rgb = DARK_GRAY
        p_member.alignment = PP_ALIGN.CENTER
        p_member.space_before = Pt(4)

    # ==========================================
    # SLIDE 2: Executive Summary
    # ==========================================
    slide_2 = add_content_slide("Executive Summary")
    
    # Left Content Box
    left_box = slide_2.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(7.5), Inches(4.8))
    tf_left = left_box.text_frame
    tf_left.word_wrap = True
    tf_left.margin_left = tf_left.margin_top = tf_left.margin_bottom = tf_left.margin_right = 0
    
    p = tf_left.paragraphs[0]
    p.text = "The modern higher education landscape demands automated, paperless, and secure administration systems. Student Hub provides a production-ready solution."
    p.font.name = "Arial"
    p.font.size = Pt(18)
    p.font.color.rgb = DARK_GRAY
    p.space_after = Pt(20)
    
    bullets = [
        "🌐 Digital Transformation: Replaces manual, physical registry routines with secure online registration.",
        "🔒 Self-Contained Assets: Standardized local asset hosting (fonts, styles) guarantees CSP security compliance.",
        "⚡ Integrated Workflow: Merges registration, dashboard trackers, dynamic courses search, and admin charts.",
        "📊 Dynamic Database Adapters: Runs SQLite in development environments and transitions easily to production-ready MySQL."
    ]
    for pt in bullets:
        p = tf_left.add_paragraph()
        p.text = pt
        p.font.name = "Arial"
        p.font.size = Pt(15)
        p.font.color.rgb = DARK_GRAY
        p.space_before = Pt(12)

    # Right Card: Objectives
    right_card = slide_2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(1.8), Inches(3.7), Inches(4.4))
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = LIGHT_GRAY
    right_card.line.color.rgb = GOLD
    right_card.line.width = Pt(1.5)
    
    rc_text = slide_2.shapes.add_textbox(Inches(9.1), Inches(2.1), Inches(3.1), Inches(3.8))
    tf_rc = rc_text.text_frame
    tf_rc.word_wrap = True
    p = tf_rc.paragraphs[0]
    p.text = "PROJECT MISSION"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(16)
    
    mission_pts = [
        ("Speed", "Optimize client forms to complete in under 3 minutes."),
        ("Security", "Implement strict CSP and Bcrypt encryptions."),
        ("Compliance", "Create transparent request audit logging trails."),
        ("Adaptability", "Design database-agnostic backend models.")
    ]
    for title, desc in mission_pts:
        p = tf_rc.add_paragraph()
        p.text = f"✔ {title}"
        p.font.name = "Arial"
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = GOLD
        p.space_before = Pt(8)
        
        p = tf_rc.add_paragraph()
        p.text = desc
        p.font.name = "Arial"
        p.font.size = Pt(11.5)
        p.font.color.rgb = DARK_GRAY

    # ==========================================
    # SLIDE 3: Problem Statement
    # ==========================================
    slide_3 = add_content_slide("The Problem Statement")
    
    problems = [
        ("📁 Heavy Paperwork & Admin Overload", "Manual, paper-based student registrations cause massive administrative workloads and high processing delays.", Inches(0.8), Inches(1.8)),
        ("🛑 CSRF & Session Vulnerabilities", "Insecure registration web applications risk session hijacking, credential leaks, and data breaches.", Inches(6.8), Inches(1.8)),
        ("⚡ High User Friction & Dropouts", "Complex, single-page application forms without real-time validations result in validation failures and high dropout rates.", Inches(0.8), Inches(4.3)),
        ("🔌 Third-Party Assets Dependency", "Loading UI symbols/fonts via public CDNs leaves portals open to CSP failures, tracking, and offline loading crashes.", Inches(6.8), Inches(4.3))
    ]
    
    for title, desc, left, top in problems:
        card = slide_3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.7), Inches(2.1))
        card.fill.solid()
        card.fill.fore_color.rgb = LIGHT_GRAY
        card.line.color.rgb = RGBColor(239, 68, 68) # Red border for problems
        card.line.width = Pt(1)
        
        tb = slide_3.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), Inches(5.3), Inches(1.8))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = NAVY
        p.space_after = Pt(6)
        
        p = tf.add_paragraph()
        p.text = desc
        p.font.name = "Arial"
        p.font.size = Pt(13)
        p.font.color.rgb = DARK_GRAY

    # ==========================================
    # SLIDE 4: Proposed Solution
    # ==========================================
    slide_4 = add_content_slide("The Proposed Solution: Student Hub")
    
    solutions = [
        ("⚡ Streamlined 4-Step Form", "Replaces complex inputs with a clean wizard interface, keeping cognitive load low and completing files in 3 mins.", Inches(0.8), Inches(1.8)),
        ("🔒 Multi-Layered Cryptography", "Implements Bcrypt hashes, WTForms CSRF validation, Separate session managers, and custom JWT tokens.", Inches(6.8), Inches(1.8)),
        ("🌐 100% Local CSP Integration", "Assets like the Material Symbols font file are self-hosted inside static folders, removing external dependencies.", Inches(0.8), Inches(4.3)),
        ("📈 Centralized Admin Dashboard", "Provides administrators with real-time sortable tables, candidate editors, CSV exports, and dynamic stats.", Inches(6.8), Inches(4.3))
    ]
    
    for title, desc, left, top in solutions:
        card = slide_4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.7), Inches(2.1))
        card.fill.solid()
        card.fill.fore_color.rgb = LIGHT_GRAY
        card.line.color.rgb = SUCCESS_GREEN # Green border for solutions
        card.line.width = Pt(1)
        
        tb = slide_4.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), Inches(5.3), Inches(1.8))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = NAVY
        p.space_after = Pt(6)
        
        p = tf.add_paragraph()
        p.text = desc
        p.font.name = "Arial"
        p.font.size = Pt(13)
        p.font.color.rgb = DARK_GRAY

    # ==========================================
    # SLIDE 5: System Architecture
    # ==========================================
    slide_5 = add_content_slide("System Architecture")
    
    layers = [
        ("📂 VISUAL LAYER", "Client-Side", [
            "HTML5 semantic structures",
            "CSS3 custom variables theme",
            "Vanilla JS state engine",
            "Local Material Symbols font",
            "Responsive viewport adapter"
        ], Inches(0.8)),
        ("⚙️ LOGIC LAYER", "Server-Side", [
            "Flask 3.0 controller routing",
            "SQLAlchemy ORM adapter",
            "Bcrypt passwords generator",
            "JWT secure API tokens",
            "Request Audit Logging (audit.py)"
        ], Inches(4.8)),
        ("🗄️ STORAGE LAYER", "Database Engine", [
            "SQLite for local testing",
            "MySQL 8+ for production setup",
            "Candidate/Admin schemas",
            "Uniqueness indexes on DB",
            "Relational catalog tables"
        ], Inches(8.8))
    ]
    
    for title, subtitle, points, left in layers:
        card = slide_5.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, Inches(1.8), Inches(3.75), Inches(4.4))
        card.fill.solid()
        card.fill.fore_color.rgb = LIGHT_GRAY
        card.line.color.rgb = GOLD
        card.line.width = Pt(1.5)
        
        tb = slide_5.shapes.add_textbox(left + Inches(0.15), Inches(2.0), Inches(3.45), Inches(4.0))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = NAVY
        
        p = tf.add_paragraph()
        p.text = subtitle
        p.font.name = "Arial"
        p.font.size = Pt(12)
        p.font.italic = True
        p.font.color.rgb = GOLD
        p.space_after = Pt(14)
        
        for pt in points:
            p = tf.add_paragraph()
            p.text = f"• {pt}"
            p.font.name = "Arial"
            p.font.size = Pt(13)
            p.font.color.rgb = DARK_GRAY
            p.space_before = Pt(8)

    # ==========================================
    # SLIDE 6: 4-Step Registration Process (Part 1)
    # ==========================================
    slide_6 = add_content_slide("Registration Process: Steps 1 & 2")
    
    # Progress visual bar
    bar_bg = slide_6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.7), Inches(0.15))
    bar_bg.fill.solid()
    bar_bg.fill.fore_color.rgb = LIGHT_GRAY
    bar_bg.line.fill.background()
    
    bar_fill = slide_6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.85), Inches(0.15))
    bar_fill.fill.solid()
    bar_fill.fill.fore_color.rgb = GOLD
    bar_fill.line.fill.background()
    
    # Step 1 Card
    card1 = slide_6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.4))
    card1.fill.solid()
    card1.fill.fore_color.rgb = LIGHT_GRAY
    card1.line.color.rgb = NAVY
    card1.line.width = Pt(1)
    
    tb1 = slide_6.shapes.add_textbox(Inches(1.0), Inches(2.1), Inches(5.2), Inches(4.0))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "STEP 1: PERSONAL INFORMATION"
    p1.font.name = "Arial"
    p1.font.size = Pt(18)
    p1.font.bold = True
    p1.font.color.rgb = NAVY
    p1.space_after = Pt(14)
    
    pt1s = [
        "👥 Full Identity Fields: First and Last Name entries.",
        "📅 Date of Birth Validation: Enforces appropriate age validations.",
        "✉️ Email Verification: Validates format on form focus and checks uniqueness on the DB.",
        "📞 Phone Formatter: Enforces correct local phone number formatting patterns."
    ]
    for pt in pt1s:
        p = tf1.add_paragraph()
        p.text = pt
        p.font.name = "Arial"
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_GRAY
        p.space_before = Pt(10)
        
    # Step 2 Card
    card2 = slide_6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.9), Inches(5.6), Inches(4.4))
    card2.fill.solid()
    card2.fill.fore_color.rgb = LIGHT_GRAY
    card2.line.color.rgb = NAVY
    card2.line.width = Pt(1)
    
    tb2 = slide_6.shapes.add_textbox(Inches(7.1), Inches(2.1), Inches(5.2), Inches(4.0))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = "STEP 2: MAILING ADDRESS"
    p2.font.name = "Arial"
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = NAVY
    p2.space_after = Pt(14)
    
    pt2s = [
        "🏠 Street Address: Simple, auto-completable single line field.",
        "🏙️ City & State Inputs: Splits local municipal registry areas.",
        "🔢 ZIP / Postal Code Match: Ensures correct numeric zip codes (regex check).",
        "🌐 Country Selection: Standardized drop-down listing for foreign admissions."
    ]
    for pt in pt2s:
        p = tf2.add_paragraph()
        p.text = pt
        p.font.name = "Arial"
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_GRAY
        p.space_before = Pt(10)

    # ==========================================
    # SLIDE 7: 4-Step Registration Process (Part 2)
    # ==========================================
    slide_7 = add_content_slide("Registration Process: Steps 3 & 4")
    
    # Progress visual bar
    bar_bg = slide_7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.7), Inches(0.15))
    bar_bg.fill.solid()
    bar_bg.fill.fore_color.rgb = LIGHT_GRAY
    bar_bg.line.fill.background()
    
    bar_fill = slide_7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.7), Inches(0.15))
    bar_fill.fill.solid()
    bar_fill.fill.fore_color.rgb = GOLD
    bar_fill.line.fill.background()
    
    # Step 3 Card
    card3 = slide_7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.4))
    card3.fill.solid()
    card3.fill.fore_color.rgb = LIGHT_GRAY
    card3.line.color.rgb = NAVY
    card3.line.width = Pt(1)
    
    tb3 = slide_7.shapes.add_textbox(Inches(1.0), Inches(2.1), Inches(5.2), Inches(4.0))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    p3 = tf3.paragraphs[0]
    p3.text = "STEP 3: ACADEMIC DETAILS"
    p3.font.name = "Arial"
    p3.font.size = Pt(18)
    p3.font.bold = True
    p3.font.color.rgb = NAVY
    p3.space_after = Pt(14)
    
    pt3s = [
        "🎓 High School Reference: Logs previous educational history.",
        "📅 Graduation Year: Collects year details to enforce entry parameters.",
        "🔬 Selected Major: Drops down options (Computer Science, Data Science, etc.).",
        "🕒 Enrollment Type: Choice between Full-Time and Part-Time status."
    ]
    for pt in pt3s:
        p = tf3.add_paragraph()
        p.text = pt
        p.font.name = "Arial"
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_GRAY
        p.space_before = Pt(10)
        
    # Step 4 Card
    card4 = slide_7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.9), Inches(5.6), Inches(4.4))
    card4.fill.solid()
    card4.fill.fore_color.rgb = LIGHT_GRAY
    card4.line.color.rgb = NAVY
    card4.line.width = Pt(1)
    
    tb4 = slide_7.shapes.add_textbox(Inches(7.1), Inches(2.1), Inches(5.2), Inches(4.0))
    tf4 = tb4.text_frame
    tf4.word_wrap = True
    p4 = tf4.paragraphs[0]
    p4.text = "STEP 4: ACCOUNT CREATION"
    p4.font.name = "Arial"
    p4.font.size = Pt(18)
    p4.font.bold = True
    p4.font.color.rgb = NAVY
    p4.space_after = Pt(14)
    
    pt4s = [
        "🔑 Password Constraints: Enforces 8+ characters, letters, and numbers.",
        "📈 Strength Meter Indicator: Visual meter displays password difficulty.",
        "📃 Terms Agreement check: Ensures compliance with terms and regulations.",
        "🎓 Dynamic ID Generation: Auto-generates registration key `STU-2026-XXXX`."
    ]
    for pt in pt4s:
        p = tf4.add_paragraph()
        p.text = pt
        p.font.name = "Arial"
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_GRAY
        p.space_before = Pt(10)

    # ==========================================
    # SLIDE 8: Student Dashboard & User Experience
    # ==========================================
    slide_8 = add_content_slide("Student Dashboard & User Experience")
    
    left_box = slide_8.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(7.5), Inches(4.8))
    tf_left = left_box.text_frame
    tf_left.word_wrap = True
    tf_left.margin_left = tf_left.margin_top = tf_left.margin_bottom = tf_left.margin_right = 0
    
    p = tf_left.paragraphs[0]
    p.text = "Upon sign-in, students access a personalized portal designed to track their application status and manage their details."
    p.font.name = "Arial"
    p.font.size = Pt(18)
    p.font.color.rgb = DARK_GRAY
    p.space_after = Pt(14)
    
    student_pts = [
        "⭕ Profile Completion Ring: Dynamic SVG ring calculating completeness of inputs.",
        "🌓 Interactive Theme Selector: Dark and Light theme toggle, saving selection in `localStorage`.",
        "📚 Course Catalogs Search: Allows query lookup of available classes and code numbers.",
        "✏️ Direct Profile Updates: Edit address, phone, and enrollment options anytime."
    ]
    for pt in student_pts:
        p = tf_left.add_paragraph()
        p.text = pt
        p.font.name = "Arial"
        p.font.size = Pt(15)
        p.font.color.rgb = DARK_GRAY
        p.space_before = Pt(10)
        
    # Right visual box: Confetti & Success details
    right_card = slide_8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(1.8), Inches(3.7), Inches(4.4))
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = LIGHT_GRAY
    right_card.line.color.rgb = GOLD
    right_card.line.width = Pt(1.5)
    
    rc_text = slide_8.shapes.add_textbox(Inches(9.1), Inches(2.1), Inches(3.1), Inches(3.8))
    tf_rc = rc_text.text_frame
    tf_rc.word_wrap = True
    
    p = tf_rc.paragraphs[0]
    p.text = "UX INTERACTIONS"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(16)
    
    ux_pts = [
        ("🎉 Confetti Canvas", "Sparks a celebratory canvas animation upon successful registration."),
        ("📋 One-Click Copy", "Copies the auto-generated student ID with dynamic status labels."),
        ("🔔 Auto-Dismiss Alerts", "Clean JavaScript toasts slides up and auto-fades in 5 seconds.")
    ]
    for num, desc in ux_pts:
        p = tf_rc.add_paragraph()
        p.text = f"✔ {num}"
        p.font.name = "Arial"
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = GOLD
        p.space_before = Pt(6)
        
        p = tf_rc.add_paragraph()
        p.text = desc
        p.font.name = "Arial"
        p.font.size = Pt(11.5)
        p.font.color.rgb = DARK_GRAY

    # ==========================================
    # SLIDE 9: Admin Control Center
    # ==========================================
    slide_9 = add_content_slide("Admin Control Center")
    
    left_box = slide_9.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(7.5), Inches(4.8))
    tf_left = left_box.text_frame
    tf_left.word_wrap = True
    tf_left.margin_left = tf_left.margin_top = tf_left.margin_bottom = tf_left.margin_right = 0
    
    p = tf_left.paragraphs[0]
    p.text = "The Administrative interface handles institutional workflows, candidate verification, and exports."
    p.font.name = "Arial"
    p.font.size = Pt(18)
    p.font.color.rgb = DARK_GRAY
    p.space_after = Pt(14)
    
    admin_pts = [
        "🔍 Real-time Search: Instant server queries matching student names, emails, or IDs.",
        "🔢 Multi-Column Sorting: Sort dynamic tabular records by Date, Major, or ID.",
        "📝 Candidate Detail Editors: Override graduation details, enrollment status, or majors.",
        "📥 CSV Directory Exporter: One-click export download of the student roster."
    ]
    for pt in admin_pts:
        p = tf_left.add_paragraph()
        p.text = pt
        p.font.name = "Arial"
        p.font.size = Pt(15)
        p.font.color.rgb = DARK_GRAY
        p.space_before = Pt(10)

    # Right Card: Access Details
    right_card = slide_9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(1.8), Inches(3.7), Inches(4.4))
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = LIGHT_GRAY
    right_card.line.color.rgb = NAVY
    right_card.line.width = Pt(1.5)
    
    rc_text = slide_9.shapes.add_textbox(Inches(9.1), Inches(2.1), Inches(3.1), Inches(3.8))
    tf_rc = rc_text.text_frame
    tf_rc.word_wrap = True
    
    p = tf_rc.paragraphs[0]
    p.text = "ADMIN PORTAL INFO"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = GOLD
    p.space_after = Pt(14)
    
    admin_details = [
        ("🔒 Endpoint Location", "https://f0e3e2dbe03207.lhr.life/admin"),
        ("📧 Default Email", "admin@school.com"),
        ("🔑 Default Password", "Admin123!"),
        ("🛡️ Session Lock", "Flask Session Cookie: Lax + Secure")
    ]
    for label, val in admin_details:
        p = tf_rc.add_paragraph()
        p.text = f"• {label}"
        p.font.name = "Arial"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = NAVY
        
        p = tf_rc.add_paragraph()
        p.text = val
        p.font.name = "Courier New" if "@" in val or "/" in val else "Arial"
        p.font.size = Pt(11.5)
        p.font.color.rgb = DARK_GRAY
        p.space_after = Pt(4)

    # ==========================================
    # SLIDE 10: Admin Analytics & Business Intelligence
    # ==========================================
    slide_10 = add_content_slide("Admin Analytics & KPI Cards")
    
    left_box = slide_10.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(7.5), Inches(4.8))
    tf_left = left_box.text_frame
    tf_left.word_wrap = True
    tf_left.margin_left = tf_left.margin_top = tf_left.margin_bottom = tf_left.margin_right = 0
    
    p = tf_left.paragraphs[0]
    p.text = "Administrators gain access to a dedicated business intelligence layer, enabling visual insights into student admissions metrics."
    p.font.name = "Arial"
    p.font.size = Pt(18)
    p.font.color.rgb = DARK_GRAY
    p.space_after = Pt(14)
    
    kpi_pts = [
        "📊 Dynamically Served KPIs: Displays Total Registrations, Majors distribution count, and active schedules.",
        "📡 Stats API Endpoint (/api/stats): Dynamic JSON route returning real-time student numbers to the landing page.",
        "📈 Chart.js Charting Interface: Administrative screens render real-time majors breakdown graphs.",
        "📉 Interactive Major Filtering: Click elements in Chart.js legends to filter candidate records."
    ]
    for pt in kpi_pts:
        p = tf_left.add_paragraph()
        p.text = pt
        p.font.name = "Arial"
        p.font.size = Pt(15)
        p.font.color.rgb = DARK_GRAY
        p.space_before = Pt(10)
        
    # Right Box: API Response Block
    right_card = slide_10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(1.8), Inches(3.7), Inches(4.4))
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = DARK_GRAY
    right_card.line.color.rgb = GOLD
    right_card.line.width = Pt(1.5)
    
    rc_text = slide_10.shapes.add_textbox(Inches(9.0), Inches(2.0), Inches(3.3), Inches(4.0))
    tf_rc = rc_text.text_frame
    tf_rc.word_wrap = True
    
    p = tf_rc.paragraphs[0]
    p.text = "API JSON SAMPLE (/api/stats)"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = GOLD
    p.space_after = Pt(10)
    
    code = (
        "{\n"
        '  "status": "success",\n'
        '  "total_students": 20,\n'
        '  "majors": {\n'
        '    "Computer Science": 8,\n'
        '    "Data Science": 5,\n'
        '    "Electrical": 4,\n'
        '    "Mechanical": 3\n'
        "  },\n"
        '  "types": {\n'
        '    "Full-Time": 14,\n'
        '    "Part-Time": 6\n'
        "  }\n"
        "}"
    )
    p = tf_rc.add_paragraph()
    p.text = code
    p.font.name = "Courier New"
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(0, 255, 0) # Green code text
    p.line_spacing = 1.1

    # ==========================================
    # SLIDE 11: Security & Compliance System
    # ==========================================
    slide_11 = add_content_slide("Production Security & Compliance")
    
    sec_details = [
        ("🔐 Cryptographic Password Protection", "User passwords undergo hashing using the blowfish Bcrypt algorithm (work factor: 12) before database write.", Inches(0.8), Inches(1.8)),
        ("🛡️ Content Security Policy (CSP)", "Rigid HTTP security policies restrict resource downloads exclusively to 'self' and approved endpoints, preventing injections.", Inches(6.8), Inches(1.8)),
        ("🚫 Rate-Limiter Interceptor", "Protects authentication interfaces against dictionary attacks. Registers max 10 attempts/hour per IP.", Inches(0.8), Inches(4.3)),
        ("📜 Cross-Site Request Forgery (CSRF)", "Flask-WTForms forces cryptographic signature checks on every POST payload, neutralizing CSRF attacks.", Inches(6.8), Inches(4.3))
    ]
    
    for title, desc, left, top in sec_details:
        card = slide_11.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, Inches(5.7), Inches(2.1))
        card.fill.solid()
        card.fill.fore_color.rgb = LIGHT_GRAY
        card.line.color.rgb = GOLD
        card.line.width = Pt(1)
        
        tb = slide_11.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), Inches(5.3), Inches(1.8))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = NAVY
        p.space_after = Pt(6)
        
        p = tf.add_paragraph()
        p.text = desc
        p.font.name = "Arial"
        p.font.size = Pt(12.5)
        p.font.color.rgb = DARK_GRAY

    # ==========================================
    # SLIDE 12: Audit Logging & Middleware
    # ==========================================
    slide_12 = add_content_slide("Audit Logging & Middleware")
    
    left_box = slide_12.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(7.5), Inches(4.8))
    tf_left = left_box.text_frame
    tf_left.word_wrap = True
    tf_left.margin_left = tf_left.margin_top = tf_left.margin_bottom = tf_left.margin_right = 0
    
    p = tf_left.paragraphs[0]
    p.text = "Student Hub logs every critical operation in the server logs (audit.py) to meet corporate compliance standards."
    p.font.name = "Arial"
    p.font.size = Pt(18)
    p.font.color.rgb = DARK_GRAY
    p.space_after = Pt(14)
    
    audit_pts = [
        "📋 Session Isolation: Keeps Administrator and Student credentials separated at the controller layer.",
        "🖥️ Audit Logs: Writes time, operation context, client IP, and target candidate IDs for all admin edits.",
        "🧹 Input Sanitizer: Filter classes inspect all inbound strings to wipe out SQL injections and HTML tags.",
        "🔓 JWT Authentication: Endpoint controller decorator `@token_required` validates student API sessions."
    ]
    for pt in audit_pts:
        p = tf_left.add_paragraph()
        p.text = pt
        p.font.name = "Arial"
        p.font.size = Pt(15)
        p.font.color.rgb = DARK_GRAY
        p.space_before = Pt(10)
        
    # Right box: Code sample
    right_card = slide_12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(1.8), Inches(3.7), Inches(4.4))
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = DARK_GRAY
    right_card.line.color.rgb = GOLD
    right_card.line.width = Pt(1.5)
    
    rc_text = slide_12.shapes.add_textbox(Inches(9.0), Inches(2.0), Inches(3.3), Inches(4.0))
    tf_rc = rc_text.text_frame
    tf_rc.word_wrap = True
    
    p = tf_rc.paragraphs[0]
    p.text = "LOG FORMAT SAMPLE"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = GOLD
    p.space_after = Pt(10)
    
    log_sample = (
        "2026-05-24 10:45:01 [INFO]\n"
        "AuditLog: {\n"
        '  "request_id": "8a32-9b2f",\n'
        '  "user_id": 14,\n'
        '  "action": "UPDATE_PROFILE",\n'
        '  "ip": "127.0.0.1",\n'
        '  "timestamp": "10:45:01",\n'
        '  "details": {\n'
        '    "student_id": "STU-2026-A3",\n'
        '    "status": "active"\n'
        "  }\n"
        "}"
    )
    p = tf_rc.add_paragraph()
    p.text = log_sample
    p.font.name = "Courier New"
    p.font.size = Pt(10.5)
    p.font.color.rgb = RGBColor(0, 255, 255) # Cyan code text
    p.line_spacing = 1.1

    # ==========================================
    # SLIDE 13: Full Technology Stack
    # ==========================================
    slide_13 = add_content_slide("The Technology Stack")
    
    # Table data
    rows = 7
    cols = 3
    table_shape = slide_13.shapes.add_table(rows, cols, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.5))
    table = table_shape.table
    
    table.columns[0].width = Inches(2.2)
    table.columns[1].width = Inches(3.8)
    table.columns[2].width = Inches(5.7)
    
    headers = ["Layer", "Technology Used", "Role in Student Hub"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        for p in cell.text_frame.paragraphs:
            p.font.bold = True
            p.font.size = Pt(15)
            p.font.color.rgb = GOLD
            p.alignment = PP_ALIGN.CENTER
            
    tech_stack = [
        ("Backend logic", "Python / Flask 3.0", "Handles HTTP endpoints, controller mapping, and route lifecycle."),
        ("ORM / Database", "SQLAlchemy 2.0 / SQLite & MySQL", "Relational database models mapping. Dev fallback utilizes SQLite."),
        ("UI Styling", "CSS3 / Custom Variable Design", "Apple-inspired styling, glassmorphism cards, and Dark/Light templates."),
        ("Fonts & Icons", "Self-Hosted Material Symbols Outlined", "Local .ttf font files serve vectors securely, bypassing CDN blocks."),
        ("Authentication", "Flask-Login & JWT Tokens", "Manages student session states and API authorization headers."),
        ("Enterprise Safety", "Flask-Limiter / Bcrypt / WTForms", "Halts brute-force attacks, hashes user passwords, and prevents CSRF.")
    ]
    
    for row_idx, data in enumerate(tech_stack, start=1):
        for col_idx, text in enumerate(data):
            cell = table.cell(row_idx, col_idx)
            cell.text = text
            cell.fill.solid()
            if row_idx % 2 == 0:
                cell.fill.fore_color.rgb = LIGHT_GRAY
            else:
                cell.fill.fore_color.rgb = WHITE
                
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(13)
                p.font.color.rgb = DARK_GRAY
                if col_idx < 2:
                    p.alignment = PP_ALIGN.CENTER
                    p.font.bold = (col_idx == 0)

    # ==========================================
    # SLIDE 14: Summary & Roadmap
    # ==========================================
    slide_14 = prs.slides.add_slide(blank_layout)
    set_white_background(slide_14)
    add_logo(slide_14, is_title_slide=True)
    
    title_box = slide_14.shapes.add_textbox(Inches(0.8), Inches(3.1), Inches(11.7), Inches(1.8))
    tf = title_box.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "Thank You!"
    p.font.name = "Arial"
    p.font.size = Pt(48)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.alignment = PP_ALIGN.CENTER
    p.space_after = Pt(10)
    
    p = tf.add_paragraph()
    p.text = "Student Hub: Streamlined, Secure, and Ready for Enterprise Enrollment."
    p.font.name = "Arial"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = GOLD
    p.alignment = PP_ALIGN.CENTER
    
    # Team reference in bottom card of slide 14
    pres_box = slide_14.shapes.add_textbox(Inches(0.8), Inches(5.4), Inches(11.7), Inches(1.5))
    tf_pres = pres_box.text_frame
    tf_pres.word_wrap = True
    p = tf_pres.paragraphs[0]
    p.text = f"Student Hub Development Team:  {members_text}"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.color.rgb = MUTED_GRAY
    p.alignment = PP_ALIGN.CENTER

    # Save presentation
    pptx_path = "Student_Registration_Presentation.pptx"
    prs.save(pptx_path)
    return pptx_path

if __name__ == "__main__":
    path = create_presentation()
    print(f"✅ PowerPoint presentation (14 slides) created successfully: {path}")
    print(f"📍 Location: {os.path.abspath(path)}")
