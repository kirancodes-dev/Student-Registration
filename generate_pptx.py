#!/usr/bin/env python3
"""
Generate a professional 16:9 PowerPoint Presentation (.pptx) for Student Hub
Features:
- Sapthagiri University logo on the top right of all pages (matching background)
- Names and SRNs of all 3 members on all slides
- Clean, premium Navy & Gold themed slide layout
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
    # SLIDE 2: What is Student Hub?
    # ==========================================
    slide_2 = add_content_slide("What is Student Hub?")
    
    # Left Content Box
    left_box = slide_2.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(7.5), Inches(4.8))
    tf_left = left_box.text_frame
    tf_left.word_wrap = True
    tf_left.margin_left = tf_left.margin_top = tf_left.margin_bottom = tf_left.margin_right = 0
    
    p = tf_left.paragraphs[0]
    p.text = "A modern, highly secure online student registration platform designed to eliminate offline paperwork and streamline the enrollment process."
    p.font.name = "Arial"
    p.font.size = Pt(18)
    p.font.color.rgb = DARK_GRAY
    p.space_after = Pt(20)
    
    bullet_points = [
        "⚡ Fast & Intuitive: Replaces complex admission forms with a 4-step wizard.",
        "📱 Responsive Architecture: Works flawlessly across mobiles, tablets, and desktops.",
        "🔒 Local Asset Security: Self-hosts all font and icons vectors to comply with local CSP restrictions.",
        "💼 Institutional Readiness: Designed to match university style systems with dedicated student & admin controls."
    ]
    
    for pt in bullet_points:
        p = tf_left.add_paragraph()
        p.text = pt
        p.font.name = "Arial"
        p.font.size = Pt(15)
        p.font.color.rgb = DARK_GRAY
        p.space_before = Pt(12)
        
    # Right Visual Block (Highlights card)
    right_card = slide_2.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(1.8), Inches(3.7), Inches(4.4)
    )
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = LIGHT_GRAY
    right_card.line.color.rgb = GOLD
    right_card.line.width = Pt(1.5)
    
    rc_text = slide_2.shapes.add_textbox(Inches(9.1), Inches(2.1), Inches(3.1), Inches(3.8))
    tf_rc = rc_text.text_frame
    tf_rc.word_wrap = True
    
    p = tf_rc.paragraphs[0]
    p.text = "CORE METRICS"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(14)
    
    metrics = [
        ("3 mins", "Average student registration time"),
        ("100%", "Paperless online workflow"),
        ("Instant", "ID generation (e.g. STU-2026-XXXX)"),
        ("Bank-Grade", "Bcrypt hashing & JWT protection")
    ]
    for num, desc in metrics:
        p = tf_rc.add_paragraph()
        p.text = f"• {num}"
        p.font.name = "Arial"
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = GOLD
        p.space_before = Pt(8)
        
        p = tf_rc.add_paragraph()
        p.text = desc
        p.font.name = "Arial"
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_GRAY
        p.space_after = Pt(4)

    # ==========================================
    # SLIDE 3: Key Features
    # ==========================================
    slide_3 = add_content_slide("Key Features")
    
    features = [
        ("⚡ 4-Step Registration Wizard", "Personal, Address, Academic, and Account creation screens featuring dynamic validations.", Inches(0.8), Inches(1.6)),
        ("👤 Dynamic Student Dashboard", "Allows students to view profile completion metrics, deadlines, course information, and manage details.", Inches(6.8), Inches(1.6)),
        ("🔐 Enterprise Security System", "Features bcrypt password hashing, CSRF token validation, rate-limiting, and detailed request audit logging.", Inches(0.8), Inches(4.1)),
        ("📊 Admin Analytics Dashboard", "Provides real-time student search, sorting, details editors, and major enrollment analytics using Chart.js.", Inches(6.8), Inches(4.1))
    ]
    
    for title, desc, left, top in features:
        card = slide_3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.7), Inches(2.2))
        card.fill.solid()
        card.fill.fore_color.rgb = LIGHT_GRAY
        card.line.color.rgb = LIGHT_GRAY
        
        tb = slide_3.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), Inches(5.3), Inches(1.8))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(17)
        p.font.bold = True
        p.font.color.rgb = NAVY
        p.space_after = Pt(8)
        
        p = tf.add_paragraph()
        p.text = desc
        p.font.name = "Arial"
        p.font.size = Pt(13)
        p.font.color.rgb = DARK_GRAY

    # ==========================================
    # SLIDE 4: Interactive Registration Form
    # ==========================================
    slide_4 = add_content_slide("The Student Registration Process")
    
    steps = [
        ("1", "Personal Info", "Full name, DOB, email, and phone validation."),
        ("2", "Address Details", "Mailing address, state, city, and ZIP validations."),
        ("3", "Academic Profile", "Select high school, graduation year, major, and course schedule."),
        ("4", "Account Settings", "Set up password with strength meter, and review terms.")
    ]
    
    for i, (num, title, desc) in enumerate(steps):
        left = Inches(0.8 + i * 2.95)
        top = Inches(2.0)
        
        # Circle for step number
        circle = slide_4.shapes.add_shape(MSO_SHAPE.OVAL, left + Inches(0.9), top, Inches(1.15), Inches(1.15))
        circle.fill.solid()
        circle.fill.fore_color.rgb = NAVY
        circle.line.color.rgb = GOLD
        circle.line.width = Pt(2)
        
        p = circle.text_frame.paragraphs[0]
        p.text = num
        p.font.name = "Arial"
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = GOLD
        p.alignment = PP_ALIGN.CENTER
        
        # Description Card
        card = slide_4.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top + Inches(1.4), Inches(2.95), Inches(3.0))
        card.fill.solid()
        card.fill.fore_color.rgb = LIGHT_GRAY
        card.line.color.rgb = LIGHT_GRAY
        
        tb = slide_4.shapes.add_textbox(left + Inches(0.1), top + Inches(1.5), Inches(2.75), Inches(2.8))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = NAVY
        p.alignment = PP_ALIGN.CENTER
        p.space_after = Pt(10)
        
        p = tf.add_paragraph()
        p.text = desc
        p.font.name = "Arial"
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_GRAY
        p.alignment = PP_ALIGN.CENTER

    # ==========================================
    # SLIDE 5: Admin Panel & Data Control
    # ==========================================
    slide_5 = add_content_slide("Admin Panel & Data Control")
    
    left_box = slide_5.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(7.5), Inches(4.8))
    tf_left = left_box.text_frame
    tf_left.word_wrap = True
    tf_left.margin_left = tf_left.margin_top = tf_left.margin_bottom = tf_left.margin_right = 0
    
    p = tf_left.paragraphs[0]
    p.text = "The Admin Console (/admin) provides university administrators with total authority over candidate files, enrollment figures, and system settings."
    p.font.name = "Arial"
    p.font.size = Pt(18)
    p.font.color.rgb = DARK_GRAY
    p.space_after = Pt(20)
    
    admin_pts = [
        "👥 Integrated Search & Sort: Locate candidates instantly by Name, ID, or Major.",
        "📊 KPI Analysis Cards: Visual cards showing total enrollments, active courses, and status.",
        "📈 Analytics Graphs: Chart.js rendering breakdown percentages of academic majors.",
        "✏️ Profile Editor: Update course schedules, academic records, and statuses."
    ]
    for pt in admin_pts:
        p = tf_left.add_paragraph()
        p.text = pt
        p.font.name = "Arial"
        p.font.size = Pt(15)
        p.font.color.rgb = DARK_GRAY
        p.space_before = Pt(12)

    # Right Card: Access Details
    right_card = slide_5.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(1.8), Inches(3.7), Inches(4.4)
    )
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = LIGHT_GRAY
    right_card.line.color.rgb = NAVY
    right_card.line.width = Pt(1.5)
    
    rc_text = slide_5.shapes.add_textbox(Inches(9.1), Inches(2.1), Inches(3.1), Inches(3.8))
    tf_rc = rc_text.text_frame
    tf_rc.word_wrap = True
    
    p = tf_rc.paragraphs[0]
    p.text = "PORTAL ACCESS"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = GOLD
    p.space_after = Pt(20)
    
    p = tf_rc.add_paragraph()
    p.text = "🔒 Admin URL:"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY
    
    p = tf_rc.add_paragraph()
    p.text = "https://f0e3e2dbe03207.lhr.life/admin"
    p.font.name = "Courier New"
    p.font.size = Pt(11)
    p.font.color.rgb = DARK_GRAY
    p.space_after = Pt(10)
    
    p = tf_rc.add_paragraph()
    p.text = "📧 Email login:"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY
    
    p = tf_rc.add_paragraph()
    p.text = "admin@school.com"
    p.font.name = "Courier New"
    p.font.size = Pt(12)
    p.font.color.rgb = DARK_GRAY
    p.space_after = Pt(10)
    
    p = tf_rc.add_paragraph()
    p.text = "🔑 Password:"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY
    
    p = tf_rc.add_paragraph()
    p.text = "Admin123!"
    p.font.name = "Courier New"
    p.font.size = Pt(12)
    p.font.color.rgb = DARK_GRAY

    # ==========================================
    # SLIDE 6: Production Security Architecture
    # ==========================================
    slide_6 = add_content_slide("Production Security Architecture")
    
    sec_pillars = [
        ("🛡️ Content Security Policy", "Strict HTTP headers restricting script origins to self and approved CDN domains. Self-hosted Material Symbols font file avoids cross-site tracking/loading blockers.", Inches(0.8), Inches(1.8)),
        ("🔐 Cryptographic Safety", "Sensitive user passwords are encrypted using Bcrypt (cost factor 12) before storage. Separate Flask-Login and JWT authorization protect endpoint controllers.", Inches(6.8), Inches(1.8)),
        ("📊 Request Audit Logging", "Every HTTP request and response payload is recorded securely inside a logging system to track user sessions, deactivations, and configuration changes.", Inches(0.8), Inches(4.3)),
        ("🛑 Rate Limiting", "Flask-Limiter intercepts login and registration routes to lock out automated brute force actions (e.g. max 5 login attempts / 15 mins).", Inches(6.8), Inches(4.3))
    ]
    
    for title, desc, left, top in sec_pillars:
        card = slide_6.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, Inches(5.7), Inches(2.1))
        card.fill.solid()
        card.fill.fore_color.rgb = LIGHT_GRAY
        card.line.color.rgb = LIGHT_GRAY
        
        tb = slide_6.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), Inches(5.3), Inches(1.8))
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
    # SLIDE 7: Technical Stack
    # ==========================================
    slide_7 = add_content_slide("Technical Stack")
    
    # Table data
    rows = 7
    cols = 3
    table_shape = slide_7.shapes.add_table(rows, cols, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.5))
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
        ("Backend Framework", "Python / Flask 3.0", "Handles HTTP endpoints, controllers, and routes lifecycle."),
        ("Database / ORM", "SQLAlchemy 2.0 / SQLite & MySQL", "Relational database maps schemas dynamically; Dev default uses SQLite."),
        ("Frontend Styles", "CSS3 / Custom Variable Design", "Apple-inspired styling, glassmorphism filters, and Dark/Light styles."),
        ("Font & Vectors", "Self-Hosted Material Symbols Outlined", "Local .ttf font files serve UI vectors securely without CDN redirects."),
        ("Authentication", "Flask-Login & JWT Tokens", "Manages user state sessions and API authorization controllers."),
        ("Security Helpers", "Flask-Limiter / Bcrypt / WTForms CSRF", "Halts brute-force attacks, hashes user passwords, and stops CSRF injections.")
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
    # SLIDE 8: Thank You / Summary
    # ==========================================
    slide_8 = prs.slides.add_slide(blank_layout)
    set_white_background(slide_8)
    add_logo(slide_8, is_title_slide=True)
    
    title_box = slide_8.shapes.add_textbox(Inches(0.8), Inches(3.2), Inches(11.7), Inches(1.8))
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
    p.text = "Questions? We are ready to present the live application demo."
    p.font.name = "Arial"
    p.font.size = Pt(18)
    p.font.color.rgb = GOLD
    p.alignment = PP_ALIGN.CENTER
    
    # Team reference in bottom card of slide 8
    pres_box = slide_8.shapes.add_textbox(Inches(0.8), Inches(5.4), Inches(11.7), Inches(1.5))
    tf_pres = pres_box.text_frame
    tf_pres.word_wrap = True
    p = tf_pres.paragraphs[0]
    p.text = f"Student Hub Team:  {members_text}"
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
    print(f"✅ PowerPoint presentation created successfully: {path}")
    print(f"📍 Location: {os.path.abspath(path)}")
