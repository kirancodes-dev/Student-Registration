#!/usr/bin/env python3
"""
Generate a professional 16:9 PowerPoint Presentation (.pptx) with 19 slides based on the guidelines:
- Logo on the top right of all pages matching the background
- Names and SRNs of all 3 members on all slides
- Custom Navy & Gold design matching the project system
- Content sections matching the requested outline (Introduction, Problem Definition, Database Design,
  Tables/Relationships, SQL Queries/CRUD, Frontend, Innovation, Output/Reports, Advantages/Limitations,
  Conclusion, Future Scope, References)
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
WARNING_RED = RGBColor(239, 68, 68) # #EF4444

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

    # =========================================================================
    # SLIDE 1: Title Slide (Introduction Slide 1/2)
    # =========================================================================
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
    p2.text = "Online Student Registration System"
    p2.font.name = "Arial"
    p2.font.size = Pt(22)
    p2.font.bold = True
    p2.font.color.rgb = GOLD
    p2.alignment = PP_ALIGN.CENTER
    p2.space_before = Pt(8)

    # Department and CSE label
    dept_box = slide_1.shapes.add_textbox(Inches(0.8), Inches(4.7), Inches(11.7), Inches(0.4))
    tf_dept = dept_box.text_frame
    tf_dept.word_wrap = True
    p_dept = tf_dept.paragraphs[0]
    p_dept.text = "Department of Computer Science & Engineering (Dept. of CSE)"
    p_dept.font.name = "Arial"
    p_dept.font.size = Pt(12)
    p_dept.font.italic = True
    p_dept.font.color.rgb = NAVY
    p_dept.alignment = PP_ALIGN.CENTER

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
        p_member.font.size = Pt(13)
        p_member.font.bold = True
        p_member.font.color.rgb = DARK_GRAY
        p_member.alignment = PP_ALIGN.CENTER
        p_member.space_before = Pt(4)

    # =========================================================================
    # SLIDE 2: Introduction & Overview (Introduction Slide 2/2)
    # =========================================================================
    slide_2 = add_content_slide("Introduction & Overview")
    
    left_box = slide_2.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(7.5), Inches(4.8))
    tf_left = left_box.text_frame
    tf_left.word_wrap = True
    tf_left.margin_left = tf_left.margin_top = tf_left.margin_bottom = tf_left.margin_right = 0
    
    p = tf_left.paragraphs[0]
    p.text = "Student Hub is a full-stack digital enrollment environment built to modernize the traditional, paper-intensive college registration routines."
    p.font.name = "Arial"
    p.font.size = Pt(18)
    p.font.color.rgb = DARK_GRAY
    p.space_after = Pt(20)
    
    intro_bullets = [
        "🌐 Digitalization Target: Transforms slow manual registration steps into a fast, 3-minute paperless flow.",
        "📱 Access & Control: Offers interactive interfaces for student profiles, course checks, and admin analytics.",
        "⚡ Modular Structure: Standardized MVC design system connecting Flask controllers, SQLAlchemy models, and variable CSS.",
        "⚙️ Database Adaptability: Uses local SQLite files for fast testing and scales easily to enterprise MySQL instances."
    ]
    for pt in intro_bullets:
        p = tf_left.add_paragraph()
        p.text = pt
        p.font.name = "Arial"
        p.font.size = Pt(15)
        p.font.color.rgb = DARK_GRAY
        p.space_before = Pt(12)

    # Right Card: Project Pillars
    right_card = slide_2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(1.8), Inches(3.7), Inches(4.4))
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = LIGHT_GRAY
    right_card.line.color.rgb = GOLD
    right_card.line.width = Pt(1.5)
    
    rc_text = slide_2.shapes.add_textbox(Inches(9.1), Inches(2.1), Inches(3.1), Inches(3.8))
    tf_rc = rc_text.text_frame
    tf_rc.word_wrap = True
    p = tf_rc.paragraphs[0]
    p.text = "CORE PILLARS"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(20)
    
    pillars = [
        ("Automated Roster", "Instantly generates identifiers and registers students in real-time."),
        ("Design Harmony", "Apple-inspired variable CSS with dynamic Dark/Light modes."),
        ("Offline Security", "Local assets (Material Symbols Outlined) bypasses CSP problems.")
    ]
    for title, desc in pillars:
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
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_GRAY

    # =========================================================================
    # SLIDE 3: Problem Definition (Problem Definition Slide 1/1)
    # =========================================================================
    slide_3 = add_content_slide("Problem Definition")
    
    problems = [
        ("📁 Administrative Overload", "Handling manual paperwork results in huge processing queues, candidate dropouts, and catalog errors.", Inches(0.8), Inches(1.8)),
        ("🔑 Credential & Session Risks", "Legacy forms lack security defenses like CSRF verification, rate limiting, and password strength checks.", Inches(6.8), Inches(1.8)),
        ("⚡ High User Friction", "Single-page layouts containing hundreds of unorganized inputs confuse candidates, leading to incomplete applications.", Inches(0.8), Inches(4.3)),
        ("🔌 Third-Party Asset Dependency", "Depending on remote CDNs to fetch fonts and icons violates strict local CSP rules and causes page rendering failures.", Inches(6.8), Inches(4.3))
    ]
    
    for title, desc, left, top in problems:
        card = slide_3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.7), Inches(2.1))
        card.fill.solid()
        card.fill.fore_color.rgb = LIGHT_GRAY
        card.line.color.rgb = WARNING_RED
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

    # =========================================================================
    # SLIDE 4: Database Design: ER Concepts (Database Design Slide 1/2)
    # =========================================================================
    slide_4 = add_content_slide("Database Design: ER Model concepts")
    
    left_box = slide_4.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(7.5), Inches(4.8))
    tf_left = left_box.text_frame
    tf_left.word_wrap = True
    tf_left.margin_left = tf_left.margin_top = tf_left.margin_bottom = tf_left.margin_right = 0
    
    p = tf_left.paragraphs[0]
    p.text = "The Entity-Relationship (ER) model organizes candidates, administrative settings, and course records within an integrated structure."
    p.font.name = "Arial"
    p.font.size = Pt(18)
    p.font.color.rgb = DARK_GRAY
    p.space_after = Pt(20)
    
    db_concepts = [
        "👤 Students Entity: Represents the applicant profile, storing personal, address, academic, and security fields.",
        "🛡️ Admins Entity: Represents the staff credentials, holding unique keys and authorization hashes.",
        "📊 Relational Constraints: Enforces uniqueness constraints on fields like email and student_id.",
        "📑 Indices Mapping: Indexes email and student_id keys on database level to speed up search lookups."
    ]
    for pt in db_concepts:
        p = tf_left.add_paragraph()
        p.text = pt
        p.font.name = "Arial"
        p.font.size = Pt(15)
        p.font.color.rgb = DARK_GRAY
        p.space_before = Pt(12)

    # Right Card: Concept Relationships
    right_card = slide_4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(1.8), Inches(3.7), Inches(4.4))
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = LIGHT_GRAY
    right_card.line.color.rgb = GOLD
    right_card.line.width = Pt(1.5)
    
    rc_text = slide_4.shapes.add_textbox(Inches(9.1), Inches(2.1), Inches(3.1), Inches(3.8))
    tf_rc = rc_text.text_frame
    tf_rc.word_wrap = True
    p = tf_rc.paragraphs[0]
    p.text = "DATABASE ENTITIES"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(16)
    
    entities = [
        ("Students", "1-to-1 mapping with accounts. Stores all validation records."),
        ("Admins", "Central controls. Authorization checks protect administrative queries."),
        ("Index Rules", "Speed-optimizes index lookups on email & student_id.")
    ]
    for title, desc in entities:
        p = tf_rc.add_paragraph()
        p.text = f"• {title}"
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

    # =========================================================================
    # SLIDE 5: Database Schema Architecture (Database Design Slide 2/2)
    # =========================================================================
    slide_5 = add_content_slide("Database Schema Architecture")
    
    left_box = slide_5.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(6.5), Inches(4.8))
    tf_left = left_box.text_frame
    tf_left.word_wrap = True
    tf_left.margin_left = tf_left.margin_top = tf_left.margin_bottom = tf_left.margin_right = 0
    
    p = tf_left.paragraphs[0]
    p.text = "The schema implementation maps objects dynamically using Python's SQLAlchemy ORM, ensuring database engine independence."
    p.font.name = "Arial"
    p.font.size = Pt(18)
    p.font.color.rgb = DARK_GRAY
    p.space_after = Pt(14)
    
    schema_details = [
        "🗄️ Dev Database: Runs on SQLite locally via `student_hub.db` file for fast zero-configuration testing.",
        "🌐 Prod Database: Connects to MySQL 8+ for enterprise workloads with transactions.",
        "📊 Index Optimization: Adds database B-Tree index constraints: `idx_email` and `idx_student_id` for fast administrative lookup queries.",
        "⚡ DB Engines: Utilizes MySQL InnoDB engine to ensure foreign key integrity and transactional stability."
    ]
    for pt in schema_details:
        p = tf_left.add_paragraph()
        p.text = pt
        p.font.name = "Arial"
        p.font.size = Pt(14.5)
        p.font.color.rgb = DARK_GRAY
        p.space_before = Pt(12)

    # Right Card: Schema SQL creation script snippet
    right_card = slide_5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.8), Inches(1.8), Inches(4.7), Inches(4.4))
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = DARK_GRAY
    right_card.line.color.rgb = GOLD
    right_card.line.width = Pt(1)
    
    rc_text = slide_5.shapes.add_textbox(Inches(7.95), Inches(2.0), Inches(4.4), Inches(4.0))
    tf_rc = rc_text.text_frame
    tf_rc.word_wrap = True
    p = tf_rc.paragraphs[0]
    p.text = "RAW SCHEMA SQL SNIPPET"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = GOLD
    p.space_after = Pt(12)
    
    sql_snippet = (
        "CREATE DATABASE IF NOT EXISTS student_registration;\n"
        "USE student_registration;\n\n"
        "CREATE TABLE students (\n"
        "  id INT AUTO_INCREMENT PRIMARY KEY,\n"
        "  student_id VARCHAR(20) NOT NULL UNIQUE,\n"
        "  email VARCHAR(120) NOT NULL UNIQUE,\n"
        "  major VARCHAR(100) NOT NULL,\n"
        "  password_hash VARCHAR(255) NOT NULL,\n"
        "  INDEX idx_email (email),\n"
        "  INDEX idx_student_id (student_id)\n"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"
    )
    p = tf_rc.add_paragraph()
    p.text = sql_snippet
    p.font.name = "Courier New"
    p.font.size = Pt(9.5)
    p.font.color.rgb = SUCCESS_GREEN
    p.line_spacing = 1.15

    # =========================================================================
    # SLIDE 6: Tables & Relationships: Students (Tables/Relationships Slide 1/2)
    # =========================================================================
    slide_6 = add_content_slide("Tables & Relationships: Students Table")
    
    # Table of columns for students
    rows = 7
    cols = 3
    table_shape = slide_6.shapes.add_table(rows, cols, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.5))
    table = table_shape.table
    
    table.columns[0].width = Inches(2.5)
    table.columns[1].width = Inches(2.8)
    table.columns[2].width = Inches(6.4)
    
    headers = ["Column Name", "Data Type & Constraints", "Description / Constraints"]
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
            
    cols_data = [
        ("id", "INT AUTO_INCREMENT PRIMARY KEY", "Unique auto-incremented database key."),
        ("student_id", "VARCHAR(20) NOT NULL UNIQUE", "Unique generated registration ID key (STU-YYYY-XXXX)."),
        ("email", "VARCHAR(120) NOT NULL UNIQUE", "Candidate email address (indexes speed up sign-in lookup)."),
        ("major", "VARCHAR(100) NOT NULL", "Selected major (e.g. Computer Science, Data Science, etc.)."),
        ("password_hash", "VARCHAR(255) NOT NULL", "Encrypted password string computed via Bcrypt algorithm."),
        ("registration_date", "DATETIME NOT NULL", "Candidate creation timestamp (Defaults to CURRENT_TIMESTAMP).")
    ]
    
    for row_idx, data in enumerate(cols_data, start=1):
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

    # =========================================================================
    # SLIDE 7: Tables & Relationships: System Tables (Tables/Relationships Slide 2/2)
    # =========================================================================
    slide_7 = add_content_slide("Tables & Relationships: System Tables")
    
    # Left table: admins
    tb_left_title = slide_7.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(5.6), Inches(0.4))
    tb_left_title.text_frame.paragraphs[0].text = "Admins Table Schema"
    tb_left_title.text_frame.paragraphs[0].font.size = Pt(18)
    tb_left_title.text_frame.paragraphs[0].font.bold = True
    tb_left_title.text_frame.paragraphs[0].font.color.rgb = NAVY
    
    table_shape_l = slide_7.shapes.add_table(5, 3, Inches(0.8), Inches(2.1), Inches(5.6), Inches(2.8))
    tl = table_shape_l.table
    tl.columns[0].width = Inches(1.5)
    tl.columns[1].width = Inches(1.8)
    tl.columns[2].width = Inches(2.3)
    
    headers_l = ["Column", "Type", "Details"]
    for i, h in enumerate(headers_l):
        cell = tl.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        cell.text_frame.paragraphs[0].font.color.rgb = GOLD
        cell.text_frame.paragraphs[0].font.bold = True
        cell.text_frame.paragraphs[0].font.size = Pt(13)
        cell.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        
    admin_cols = [
        ("id", "INT PRIMARY KEY", "PK auto-key"),
        ("username", "VARCHAR(80) UNIQUE", "Unique login ID"),
        ("email", "VARCHAR(120) UNIQUE", "Unique contact"),
        ("password_hash", "VARCHAR(255)", "Bcrypt signature")
    ]
    for row_idx, data in enumerate(admin_cols, start=1):
        for col_idx, text in enumerate(data):
            cell = tl.cell(row_idx, col_idx)
            cell.text = text
            cell.fill.solid()
            cell.fill.fore_color.rgb = LIGHT_GRAY if row_idx % 2 == 0 else WHITE
            cell.text_frame.paragraphs[0].font.size = Pt(11)
            cell.text_frame.paragraphs[0].font.color.rgb = DARK_GRAY

    # Right table: audit_logs / configuration details
    tb_right_title = slide_7.shapes.add_textbox(Inches(6.9), Inches(1.6), Inches(5.6), Inches(0.4))
    tb_right_title.text_frame.paragraphs[0].text = "System Relationships Overview"
    tb_right_title.text_frame.paragraphs[0].font.size = Pt(18)
    tb_right_title.text_frame.paragraphs[0].font.bold = True
    tb_right_title.text_frame.paragraphs[0].font.color.rgb = NAVY
    
    table_shape_r = slide_7.shapes.add_table(5, 3, Inches(6.9), Inches(2.1), Inches(5.6), Inches(2.8))
    tr = table_shape_r.table
    tr.columns[0].width = Inches(1.6)
    tr.columns[1].width = Inches(1.7)
    tr.columns[2].width = Inches(2.3)
    
    headers_r = ["Concept", "Security Level", "Description"]
    for i, h in enumerate(headers_r):
        cell = tr.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        cell.text_frame.paragraphs[0].font.color.rgb = GOLD
        cell.text_frame.paragraphs[0].font.bold = True
        cell.text_frame.paragraphs[0].font.size = Pt(13)
        cell.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        
    rel_rows = [
        ("Student -> Session", "Student Cookies", "Isolated cookies protect student credentials."),
        ("Admin -> Session", "Admin Cookie check", "Enforces access blocks on endpoints."),
        ("Audit -> Operations", "Backend log file", "Records administrative changes."),
        ("JWT -> API Stats", "Crypto signature", "Secures analytics lookups.")
    ]
    for row_idx, data in enumerate(rel_rows, start=1):
        for col_idx, text in enumerate(data):
            cell = tr.cell(row_idx, col_idx)
            cell.text = text
            cell.fill.solid()
            cell.fill.fore_color.rgb = LIGHT_GRAY if row_idx % 2 == 0 else WHITE
            cell.text_frame.paragraphs[0].font.size = Pt(11)
            cell.text_frame.paragraphs[0].font.color.rgb = DARK_GRAY

    # Descriptive text below
    desc_box = slide_7.shapes.add_textbox(Inches(0.8), Inches(5.1), Inches(11.7), Inches(1.5))
    tf_desc = desc_box.text_frame
    tf_desc.word_wrap = True
    tf_desc.margin_left = tf_desc.margin_top = tf_desc.margin_bottom = tf_desc.margin_right = 0
    p = tf_desc.paragraphs[0]
    p.text = "💡 **Schema Integrity Rules:**"
    p.font.name = "Arial"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = NAVY
    p.space_after = Pt(4)
    
    p = tf_desc.add_paragraph()
    p.text = "• Unique constraints are evaluated by Flask validators before DB operations are attempted.\n• Administrator credentials and regular student credentials are kept separated via dedicated Flask session identifiers, preventing privilege escalation."
    p.font.name = "Arial"
    p.font.size = Pt(13.5)
    p.font.color.rgb = DARK_GRAY

    # =========================================================================
    # SLIDE 8: SQL Queries: Write Operations (SQL Queries/CRUD Slide 1/2)
    # =========================================================================
    slide_8 = add_content_slide("SQL CRUD Operations: Write Actions")
    
    left_box = slide_8.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(6.0), Inches(4.8))
    tf_left = left_box.text_frame
    tf_left.word_wrap = True
    tf_left.margin_left = tf_left.margin_top = tf_left.margin_bottom = tf_left.margin_right = 0
    
    p = tf_left.paragraphs[0]
    p.text = "The registration pipeline validates inputs and runs SQL write commands (inserts/updates) through SQLAlchemy transactions."
    p.font.name = "Arial"
    p.font.size = Pt(18)
    p.font.color.rgb = DARK_GRAY
    p.space_after = Pt(14)
    
    write_pts = [
        "📥 Candidate Registration: Generates a unique index ID and writes full personal, address, and academic records.",
        "🔒 Encrypted Write: Computes secure password hashes using Blowfish-based Bcrypt and stores the signature.",
        "📝 Candidate Edits: Translates form changes into dynamic SQL update queries."
    ]
    for pt in write_pts:
        p = tf_left.add_paragraph()
        p.text = pt
        p.font.name = "Arial"
        p.font.size = Pt(14.5)
        p.font.color.rgb = DARK_GRAY
        p.space_before = Pt(12)

    # Right Box: SQL Code Insert Sample
    right_card = slide_8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.2), Inches(1.8), Inches(5.3), Inches(4.4))
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = DARK_GRAY
    right_card.line.color.rgb = GOLD
    right_card.line.width = Pt(1)
    
    rc_text = slide_8.shapes.add_textbox(Inches(7.35), Inches(2.0), Inches(5.0), Inches(4.0))
    tf_rc = rc_text.text_frame
    tf_rc.word_wrap = True
    p = tf_rc.paragraphs[0]
    p.text = "SQL WRITE STATEMENT SAMPLES"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = GOLD
    p.space_after = Pt(12)
    
    sql_write = (
        "-- Insert a new student record\n"
        "INSERT INTO students (\n"
        "  student_id, first_name, last_name, email, \n"
        "  major, enrollment_type, password_hash\n"
        ") VALUES (\n"
        "  'STU-2026-A3F9', 'John', 'Doe', 'john.doe@email.com',\n"
        "  'Computer Science', 'Full-Time', '$2b$12$R9...'\n"
        ");\n\n"
        "-- Update student record\n"
        "UPDATE students SET \n"
        "  phone = '+1 555-0199',\n"
        "  street = '456 Oak Road'\n"
        "WHERE student_id = 'STU-2026-A3F9';"
    )
    p = tf_rc.add_paragraph()
    p.text = sql_write
    p.font.name = "Courier New"
    p.font.size = Pt(9.5)
    p.font.color.rgb = SUCCESS_GREEN
    p.line_spacing = 1.15

    # =========================================================================
    # SLIDE 9: SQL Queries: Read & Analytics (SQL Queries/CRUD Slide 2/2)
    # =========================================================================
    slide_9 = add_content_slide("SQL CRUD Operations: Read & Analytics")
    
    left_box = slide_9.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(6.0), Inches(4.8))
    tf_left = left_box.text_frame
    tf_left.word_wrap = True
    tf_left.margin_left = tf_left.margin_top = tf_left.margin_bottom = tf_left.margin_right = 0
    
    p = tf_left.paragraphs[0]
    p.text = "Administrative pages run SQL queries to search records, filter results, and generate analytics."
    p.font.name = "Arial"
    p.font.size = Pt(18)
    p.font.color.rgb = DARK_GRAY
    p.space_after = Pt(14)
    
    read_pts = [
        "🔍 Roster Search Query: Matches search queries against candidate names, email formats, and unique IDs.",
        "📊 Dynamic Aggregations: Computes enrollment totals and groups records by academic major.",
        "🔐 Token Credentials Verification: Validates account passwords and matches Bcrypt hashes during login."
    ]
    for pt in read_pts:
        p = tf_left.add_paragraph()
        p.text = pt
        p.font.name = "Arial"
        p.font.size = Pt(14.5)
        p.font.color.rgb = DARK_GRAY
        p.space_before = Pt(12)

    # Right Box: SQL Code Read Sample
    right_card = slide_9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.2), Inches(1.8), Inches(5.3), Inches(4.4))
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = DARK_GRAY
    right_card.line.color.rgb = GOLD
    right_card.line.width = Pt(1)
    
    rc_text = slide_9.shapes.add_textbox(Inches(7.35), Inches(2.0), Inches(5.0), Inches(4.0))
    tf_rc = rc_text.text_frame
    tf_rc.word_wrap = True
    p = tf_rc.paragraphs[0]
    p.text = "SQL READ & ANALYTICS SAMPLES"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = GOLD
    p.space_after = Pt(12)
    
    sql_read = (
        "-- Administrative dynamic search & sort\n"
        "SELECT * FROM students \n"
        "WHERE (first_name LIKE '%John%' \n"
        "   OR email LIKE '%John%'\n"
        "   OR student_id = 'John')\n"
        "ORDER BY registration_date DESC;\n\n"
        "-- Major breakdown aggregation query\n"
        "SELECT major, COUNT(*) AS enrollments \n"
        "FROM students \n"
        "GROUP BY major;\n"
    )
    p = tf_rc.add_paragraph()
    p.text = sql_read
    p.font.name = "Courier New"
    p.font.size = Pt(9.5)
    p.font.color.rgb = SUCCESS_GREEN
    p.line_spacing = 1.15

    # =========================================================================
    # SLIDE 10: Frontend Design System (Frontend Slide 1/2)
    # =========================================================================
    slide_10 = add_content_slide("Frontend Design System")
    
    left_box = slide_10.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(7.5), Inches(4.8))
    tf_left = left_box.text_frame
    tf_left.word_wrap = True
    tf_left.margin_left = tf_left.margin_top = tf_left.margin_bottom = tf_left.margin_right = 0
    
    p = tf_left.paragraphs[0]
    p.text = "The design system uses CSS variables to ensure brand consistency across light and dark modes."
    p.font.name = "Arial"
    p.font.size = Pt(18)
    p.font.color.rgb = DARK_GRAY
    p.space_after = Pt(14)
    
    design_pts = [
        "🎨 Primary Branded Colorways: Navy Blue (`#00317e`) representing security and Gold (`#D4AF37`) representing academic achievement.",
        "🌓 System-wide Dark Mode: Changes styles dynamically using `[data-theme='dark']` settings and saves user choice.",
        "🖥️ Layout Elements: Premium glassmorphism cards, blur navigation bars, and rounded pill containers.",
        "📱 Variable Fonts Scales: System fonts (Inter, Public Sans) scale dynamically for clean readability."
    ]
    for pt in design_pts:
        p = tf_left.add_paragraph()
        p.text = pt
        p.font.name = "Arial"
        p.font.size = Pt(14.5)
        p.font.color.rgb = DARK_GRAY
        p.space_before = Pt(10)
        
    # Right Box: CSS Variables
    right_card = slide_10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(1.8), Inches(3.7), Inches(4.4))
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = LIGHT_GRAY
    right_card.line.color.rgb = GOLD
    right_card.line.width = Pt(1.5)
    
    rc_text = slide_10.shapes.add_textbox(Inches(9.1), Inches(2.1), Inches(3.1), Inches(3.8))
    tf_rc = rc_text.text_frame
    tf_rc.word_wrap = True
    p = tf_rc.paragraphs[0]
    p.text = "CSS VARIABLE TOKENS"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(14)
    
    tokens = [
        ("--navy", "#00317e (Brand primary)"),
        ("--gold", "#D4AF37 (Brand accent)"),
        ("--card-bg", "rgba(255,255,255,0.65)"),
        ("--card-border", "rgba(255,255,255,0.45)"),
        ("--radius-xl", "24px (Soft pill buttons)")
    ]
    for t_name, t_val in tokens:
        p = tf_rc.add_paragraph()
        p.text = t_name
        p.font.name = "Courier New"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = GOLD
        
        p = tf_rc.add_paragraph()
        p.text = t_val
        p.font.name = "Arial"
        p.font.size = Pt(11.5)
        p.font.color.rgb = DARK_GRAY
        p.space_after = Pt(4)

    # =========================================================================
    # SLIDE 11: Interface Wizard Screens (Frontend Slide 2/2)
    # =========================================================================
    slide_11 = add_content_slide("The Interface Wizard Screens")
    
    steps = [
        ("Step 1: Identity", "Personal details inputs featuring regex email checks and phone formatting.", Inches(0.8)),
        ("Step 2: Location", "Collects mailing coordinates and postal address details.", Inches(3.8)),
        ("Step 3: Program", "Academic selection mapping candidates to specific program majors.", Inches(6.8)),
        ("Step 4: Account", "Password meter validation and dynamic registration code generation.", Inches(9.8))
    ]
    
    for title, desc, left in steps:
        card = slide_11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.8), Inches(2.75), Inches(3.6))
        card.fill.solid()
        card.fill.fore_color.rgb = LIGHT_GRAY
        card.line.color.rgb = NAVY
        card.line.width = Pt(1)
        
        tb = slide_11.shapes.add_textbox(left + Inches(0.1), Inches(2.0), Inches(2.55), Inches(3.2))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = NAVY
        p.alignment = PP_ALIGN.CENTER
        p.space_after = Pt(12)
        
        p = tf.add_paragraph()
        p.text = desc
        p.font.name = "Arial"
        p.font.size = Pt(13)
        p.font.color.rgb = DARK_GRAY
        p.alignment = PP_ALIGN.CENTER

    # Additional text at bottom
    tb_bottom = slide_11.shapes.add_textbox(Inches(0.8), Inches(5.6), Inches(11.7), Inches(1.2))
    tf_bot = tb_bottom.text_frame
    tf_bot.word_wrap = True
    tf_bot.margin_left = tf_bot.margin_top = tf_bot.margin_bottom = tf_bot.margin_right = 0
    p = tf_bot.paragraphs[0]
    p.text = "💡 **User Experience Features:**"
    p.font.name = "Arial"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = NAVY
    p.space_after = Pt(4)
    
    p = tf_bot.add_paragraph()
    p.text = "• Seamless Navigation: Next/Previous controls maintain filled states, reducing user input frustration.\n• Form Validation Feedback: Immediate visual alerts are triggered before form submission to ensure database clean writes."
    p.font.name = "Arial"
    p.font.size = Pt(13.5)
    p.font.color.rgb = DARK_GRAY

    # =========================================================================
    # SLIDE 12: Innovation: Local Asset Self-Hosting (Innovation Slide 1/2)
    # =========================================================================
    slide_12 = add_content_slide("Innovation: Local Asset Self-Hosting")
    
    left_box = slide_12.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(7.5), Inches(4.8))
    tf_left = left_box.text_frame
    tf_left.word_wrap = True
    tf_left.margin_left = tf_left.margin_top = tf_left.margin_bottom = tf_left.margin_right = 0
    
    p = tf_left.paragraphs[0]
    p.text = "A core security innovation in Student Hub is the elimination of external content delivery networks (CDNs) for key UI icons."
    p.font.name = "Arial"
    p.font.size = Pt(18)
    p.font.color.rgb = DARK_GRAY
    p.space_after = Pt(20)
    
    asset_pts = [
        "🔒 Asset Isolation: Serves the Material Symbols font file (`.ttf`) directly from local `/static/fonts` folders.",
        "🛡️ Content Security Policy compliance: Prevents security blocks on external CDN domains by referencing assets from `'self'`.",
        "🔌 Network Independence: The application loads fast in offline local dev, removing the risk of CDN outages.",
        "🧩 Dynamic Font Rendering: Retains variable axis settings (optical sizes, fill axis, weights) through pure local CSS rules."
    ]
    for pt in asset_pts:
        p = tf_left.add_paragraph()
        p.text = pt
        p.font.name = "Arial"
        p.font.size = Pt(15)
        p.font.color.rgb = DARK_GRAY
        p.space_before = Pt(12)

    # Right Card: Asset details
    right_card = slide_12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(1.8), Inches(3.7), Inches(4.4))
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = LIGHT_GRAY
    right_card.line.color.rgb = GOLD
    right_card.line.width = Pt(1.5)
    
    rc_text = slide_12.shapes.add_textbox(Inches(9.1), Inches(2.1), Inches(3.1), Inches(3.8))
    tf_rc = rc_text.text_frame
    tf_rc.word_wrap = True
    p = tf_rc.paragraphs[0]
    p.text = "LOCAL ASSET SETUP"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(16)
    
    setup_steps = [
        ("Download Binary", "Pulled Google's official variable font file to project disk folders."),
        ("CSS Mapping", "Added @font-face rules mapping families to '/static/fonts/' urls."),
        ("Strict CSP settings", "Wiped out external font-src domains, whitelisting 'self' only.")
    ]
    for step_title, step_desc in setup_steps:
        p = tf_rc.add_paragraph()
        p.text = f"✔ {step_title}"
        p.font.name = "Arial"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = GOLD
        p.space_before = Pt(8)
        
        p = tf_rc.add_paragraph()
        p.text = step_desc
        p.font.name = "Arial"
        p.font.size = Pt(11.5)
        p.font.color.rgb = DARK_GRAY

    # =========================================================================
    # SLIDE 13: Innovation: Session Controls & Logging (Innovation Slide 2/2)
    # =========================================================================
    slide_13 = add_content_slide("Innovation: Session Protection & Audit Logs")
    
    left_box = slide_13.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(7.5), Inches(4.8))
    tf_left = left_box.text_frame
    tf_left.word_wrap = True
    tf_left.margin_left = tf_left.margin_top = tf_left.margin_bottom = tf_left.margin_right = 0
    
    p = tf_left.paragraphs[0]
    p.text = "Student Hub implements strict backend audit tracking to secure administrative actions and session states."
    p.font.name = "Arial"
    p.font.size = Pt(18)
    p.font.color.rgb = DARK_GRAY
    p.space_after = Pt(20)
    
    log_pts = [
        "🛡️ Separated Session Managers: Employs different authentication flows for Students and Admins, preventing privilege escalation.",
        "📜 Operational Audit Logging: Writes JSON logs (`audit.py`) tracking actions, user context, client IP, and target candidate IDs.",
        "🧹 Input Sanitizer Middleware: Cleans inbound inputs before they reach the DB to block SQL injections and XSS attempts.",
        "🔑 Endpoint Token Protections: Protects backend APIs with JWT verification decorators (`@token_required`)."
    ]
    for pt in log_pts:
        p = tf_left.add_paragraph()
        p.text = pt
        p.font.name = "Arial"
        p.font.size = Pt(15)
        p.font.color.rgb = DARK_GRAY
        p.space_before = Pt(12)

    # Right Card: Log Format
    right_card = slide_13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(1.8), Inches(3.7), Inches(4.4))
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = DARK_GRAY
    right_card.line.color.rgb = GOLD
    right_card.line.width = Pt(1.5)
    
    rc_text = slide_13.shapes.add_textbox(Inches(9.0), Inches(2.0), Inches(3.3), Inches(4.0))
    tf_rc = rc_text.text_frame
    tf_rc.word_wrap = True
    p = tf_rc.paragraphs[0]
    p.text = "AUDIT LOGGER LOG SAMPLE"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = GOLD
    p.space_after = Pt(12)
    
    log_sample = (
        "2026-05-24 10:45:01 [INFO]\n"
        "AuditLog: {\n"
        '  "request_id": "8a32-9b2f",\n'
        '  "user_id": 14,\n'
        '  "action": "UPDATE_PROFILE",\n'
        '  "ip": "127.0.0.1",\n'
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
    p.line_spacing = 1.15

    # =========================================================================
    # SLIDE 14: Output Screens: Student (Output Screens Slide 1/2)
    # =========================================================================
    slide_14 = add_content_slide("Output Screens: Student Experience")
    
    outputs_s = [
        ("✨ Hero Canvas Particle Effects", "The index landing page features a custom floating canvas particle background that animates smoothly.", Inches(0.8), Inches(1.8)),
        ("⭕ Circular Progress Indicator", "The student dashboard features a dynamic SVG completion ring that updates based on profile fields filled.", Inches(6.8), Inches(1.8)),
        ("🎉 Confetti Overlay Celebration", "When registration finishes, the confirmation screen triggers a confetti celebration to welcome the user.", Inches(0.8), Inches(4.3)),
        ("🌓 Dark & Light Modes Visuals", "Responsive navigation and card templates change theme immediately without page reloads.", Inches(6.8), Inches(4.3))
    ]
    
    for title, desc, left, top in outputs_s:
        card = slide_14.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, Inches(5.7), Inches(2.1))
        card.fill.solid()
        card.fill.fore_color.rgb = LIGHT_GRAY
        card.line.color.rgb = LIGHT_GRAY
        
        tb = slide_14.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), Inches(5.3), Inches(1.8))
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

    # =========================================================================
    # SLIDE 15: Output Screens: Admin & KPI Charts (Output Screens Slide 2/2)
    # =========================================================================
    slide_15 = add_content_slide("Output Screens: Admin Console & KPI Charts")
    
    left_box = slide_15.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(7.5), Inches(4.8))
    tf_left = left_box.text_frame
    tf_left.word_wrap = True
    tf_left.margin_left = tf_left.margin_top = tf_left.margin_bottom = tf_left.margin_right = 0
    
    p = tf_left.paragraphs[0]
    p.text = "The Admin Console displays key performance metrics and enrollment breakdown visualizations."
    p.font.name = "Arial"
    p.font.size = Pt(18)
    p.font.color.rgb = DARK_GRAY
    p.space_after = Pt(14)
    
    outputs_a = [
        "📊 KPI Overview Panels: Quick-view cards display totals, course catalogs, and registration types.",
        "📈 Visual Major Charts: Rendered dynamically via Chart.js from real-time database counts.",
        "👥 Searchable Candidate Table: Sorts, filters, and searches entries by Name, ID, or Major.",
        "📥 Dynamic CSV Downloader: One-click export download of the student roster."
    ]
    for pt in outputs_a:
        p = tf_left.add_paragraph()
        p.text = pt
        p.font.name = "Arial"
        p.font.size = Pt(15)
        p.font.color.rgb = DARK_GRAY
        p.space_before = Pt(10)

    # Right Card: stats JSON representation
    right_card = slide_15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(1.8), Inches(3.7), Inches(4.4))
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = LIGHT_GRAY
    right_card.line.color.rgb = GOLD
    right_card.line.width = Pt(1.5)
    
    rc_text = slide_15.shapes.add_textbox(Inches(9.1), Inches(2.1), Inches(3.1), Inches(3.8))
    tf_rc = rc_text.text_frame
    tf_rc.word_wrap = True
    
    p = tf_rc.paragraphs[0]
    p.text = "ADMIN VIEWS"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(16)
    
    admin_views = [
        ("Enrollment Stats", "Real-time count of total students enrolled and majors breakdown."),
        ("Search / Sort Table", "Tabular display with multi-column sorting and filtering options."),
        ("CSV Directory Export", "Generates and triggers download of student records in CSV format.")
    ]
    for view_title, view_desc in admin_views:
        p = tf_rc.add_paragraph()
        p.text = f"✔ {view_title}"
        p.font.name = "Arial"
        p.font.size = Pt(14.5)
        p.font.bold = True
        p.font.color.rgb = GOLD
        p.space_before = Pt(8)
        
        p = tf_rc.add_paragraph()
        p.text = view_desc
        p.font.name = "Arial"
        p.font.size = Pt(11.5)
        p.font.color.rgb = DARK_GRAY

    # =========================================================================
    # SLIDE 16: Advantages & Limitations (Advantages/Limitations Slide 1/1)
    # =========================================================================
    slide_16 = add_content_slide("Advantages & Limitations")
    
    # Left Card: Advantages
    card_adv = slide_16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.4))
    card_adv.fill.solid()
    card_adv.fill.fore_color.rgb = LIGHT_GRAY
    card_adv.line.color.rgb = SUCCESS_GREEN
    card_adv.line.width = Pt(1.5)
    
    tb_adv = slide_16.shapes.add_textbox(Inches(1.0), Inches(2.1), Inches(5.2), Inches(4.0))
    tf_adv = tb_adv.text_frame
    tf_adv.word_wrap = True
    p = tf_adv.paragraphs[0]
    p.text = "ADVANTAGES"
    p.font.name = "Arial"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(14)
    
    advs = [
        "⭐ Clean User Interface: Multi-step layout reduces user input cognitive fatigue.",
        "⭐ Local Resource Assets: Bypassing external CDN calls improves speed and CSP safety.",
        "⭐ Comprehensive Security: Integrates Bcrypt, CSRF tokens, rate limiters, and CSP.",
        "⭐ Centralized Roster Controls: Allows easy student directory updates and CSV exports."
    ]
    for pt in advs:
        p = tf_adv.add_paragraph()
        p.text = pt
        p.font.name = "Arial"
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_GRAY
        p.space_before = Pt(10)

    # Right Card: Limitations
    card_lim = slide_16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.8), Inches(5.6), Inches(4.4))
    card_lim.fill.solid()
    card_lim.fill.fore_color.rgb = LIGHT_GRAY
    card_lim.line.color.rgb = WARNING_RED
    card_lim.line.width = Pt(1.5)
    
    tb_lim = slide_16.shapes.add_textbox(Inches(7.1), Inches(2.1), Inches(5.2), Inches(4.0))
    tf_lim = tb_lim.text_frame
    tf_lim.word_wrap = True
    p = tf_lim.paragraphs[0]
    p.text = "LIMITATIONS"
    p.font.name = "Arial"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(14)
    
    lims = [
        "⚠️ Session Cookies: Relies on HTTP-only session cookies; session state is lost on browser logout.",
        "⚠️ JS Dependent: Visual animations and transitions require JavaScript support to render properly.",
        "⚠️ Local Server Testing: SQLite configurations are designed for local developer environments.",
        "⚠️ Administrative Authority: Lacks advanced multi-tier admin role permission trees."
    ]
    for pt in lims:
        p = tf_lim.add_paragraph()
        p.text = pt
        p.font.name = "Arial"
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_GRAY
        p.space_before = Pt(10)

    # =========================================================================
    # SLIDE 17: Conclusion (Conclusion Slide 1/1)
    # =========================================================================
    slide_17 = add_content_slide("Conclusion")
    
    left_box = slide_17.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(7.5), Inches(4.8))
    tf_left = left_box.text_frame
    tf_left.word_wrap = True
    tf_left.margin_left = tf_left.margin_top = tf_left.margin_bottom = tf_left.margin_right = 0
    
    p = tf_left.paragraphs[0]
    p.text = "Student Hub successfully digitizes university admission processes, delivering a fast, highly secure, and user-friendly experience."
    p.font.name = "Arial"
    p.font.size = Pt(18)
    p.font.color.rgb = DARK_GRAY
    p.space_after = Pt(20)
    
    conc_bullets = [
        "🏆 Automated Registration: Speeds up file compilation and enrollment tracking.",
        "🔒 Secure Design: Implements rigid headers (CSP/HSTS) and password encryption hashes (Bcrypt).",
        "🎨 Interface Aesthetics: Clean Navy/Gold design system optimized for mobile viewports.",
        "⚙️ Robust Architecture: Successfully tested with local SQLite and staging MySQL environments."
    ]
    for pt in conc_bullets:
        p = tf_left.add_paragraph()
        p.text = pt
        p.font.name = "Arial"
        p.font.size = Pt(15)
        p.font.color.rgb = DARK_GRAY
        p.space_before = Pt(12)

    # Right Card: Takeaways
    right_card = slide_17.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(1.8), Inches(3.7), Inches(4.4))
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = LIGHT_GRAY
    right_card.line.color.rgb = GOLD
    right_card.line.width = Pt(1.5)
    
    rc_text = slide_17.shapes.add_textbox(Inches(9.1), Inches(2.1), Inches(3.1), Inches(3.8))
    tf_rc = rc_text.text_frame
    tf_rc.word_wrap = True
    p = tf_rc.paragraphs[0]
    p.text = "KEY TAKEAWAYS"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(20)
    
    takeaways = [
        ("Easy Deploy", "Containerizable code structure ready for production server setups."),
        ("Self-Hosted", "Local assets remove CDN risks and keep pages fully secure."),
        ("Compliance Logs", "Requests tracking helps audit operations and sessions.")
    ]
    for t_title, t_desc in takeaways:
        p = tf_rc.add_paragraph()
        p.text = f"✔ {t_title}"
        p.font.name = "Arial"
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = GOLD
        p.space_before = Pt(8)
        
        p = tf_rc.add_paragraph()
        p.text = t_desc
        p.font.name = "Arial"
        p.font.size = Pt(11.5)
        p.font.color.rgb = DARK_GRAY

    # =========================================================================
    # SLIDE 18: Future Scope (Future Scope Slide 1/1)
    # =========================================================================
    slide_18 = add_content_slide("Future Scope")
    
    left_box = slide_18.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(7.5), Inches(4.8))
    tf_left = left_box.text_frame
    tf_left.word_wrap = True
    tf_left.margin_left = tf_left.margin_top = tf_left.margin_bottom = tf_left.margin_right = 0
    
    p = tf_left.paragraphs[0]
    p.text = "While Student Hub delivers a solid foundation, several extensions are planned for future iterations."
    p.font.name = "Arial"
    p.font.size = Pt(18)
    p.font.color.rgb = DARK_GRAY
    p.space_after = Pt(20)
    
    future_pts = [
        "💳 Integrated Payment Portals: Connects payment gateways (Razorpay, Stripe) to collect registration and library fees.",
        "✉️ Automated Notifications: Triggers SMS updates and email dispatches for status changes.",
        "🔐 Advanced Authentication: Adds two-factor verification (2FA) and multi-tier admin roles.",
        "📱 Mobile App Wrappers: Packages the layout as a native Android/iOS application."
    ]
    for pt in future_pts:
        p = tf_left.add_paragraph()
        p.text = pt
        p.font.name = "Arial"
        p.font.size = Pt(15)
        p.font.color.rgb = DARK_GRAY
        p.space_before = Pt(12)

    # Right Card: Roadmap
    right_card = slide_18.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(1.8), Inches(3.7), Inches(4.4))
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = LIGHT_GRAY
    right_card.line.color.rgb = GOLD
    right_card.line.width = Pt(1.5)
    
    rc_text = slide_18.shapes.add_textbox(Inches(9.1), Inches(2.1), Inches(3.1), Inches(3.8))
    tf_rc = rc_text.text_frame
    tf_rc.word_wrap = True
    p = tf_rc.paragraphs[0]
    p.text = "ROADMAP MILESTONES"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(20)
    
    milestones = [
        ("Phase 1: Gateway", "Integrate online fee payment API checkout routines."),
        ("Phase 2: Alert System", "Build notification triggers for confirmations."),
        ("Phase 3: Native Wrapper", "Publish Android/iOS application wrapper containers.")
    ]
    for m_title, m_desc in milestones:
        p = tf_rc.add_paragraph()
        p.text = f"• {m_title}"
        p.font.name = "Arial"
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = GOLD
        p.space_before = Pt(8)
        
        p = tf_rc.add_paragraph()
        p.text = m_desc
        p.font.name = "Arial"
        p.font.size = Pt(11.5)
        p.font.color.rgb = DARK_GRAY

    # =========================================================================
    # SLIDE 19: References (References Slide 1/1)
    # =========================================================================
    slide_19 = add_content_slide("References")
    
    left_box = slide_19.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(4.8))
    tf_left = left_box.text_frame
    tf_left.word_wrap = True
    tf_left.margin_left = tf_left.margin_top = tf_left.margin_bottom = tf_left.margin_right = 0
    
    p = tf_left.paragraphs[0]
    p.text = "The development and security compliance of Student Hub references the following standards and frameworks:"
    p.font.name = "Arial"
    p.font.size = Pt(18)
    p.font.color.rgb = DARK_GRAY
    p.space_after = Pt(20)
    
    refs = [
        "📚 **Flask 3.0 Documentation**: [https://flask.palletsprojects.com](https://flask.palletsprojects.com)",
        "🗄️ **SQLAlchemy 2.0 Specifications**: [https://www.sqlalchemy.org](https://www.sqlalchemy.org)",
        "🎨 **Apple Human Interface Guidelines (HIG)**: [https://developer.apple.com/design/human-interface-guidelines](https://developer.apple.com/design/human-interface-guidelines)",
        "🎨 **Google Material Design 3 Documentation**: [https://m3.material.io](https://m3.material.io)",
        "🛡️ **OWASP Top 10 Security Risks & Controls**: [https://owasp.org/www-project-top-ten](https://owasp.org/www-project-top-ten)",
        "💻 **Werkzeug WSGI Web Utilities**: [https://werkzeug.palletsprojects.com](https://werkzeug.palletsprojects.com)"
    ]
    for ref in refs:
        p = tf_left.add_paragraph()
        p.text = ref
        p.font.name = "Arial"
        p.font.size = Pt(15.5)
        p.font.color.rgb = DARK_GRAY
        p.space_before = Pt(12)

    # Save presentation
    pptx_path = "Student_Registration_Presentation.pptx"
    prs.save(pptx_path)
    return pptx_path

if __name__ == "__main__":
    path = create_presentation()
    print(f"✅ PowerPoint presentation (19 slides) created successfully: {path}")
    print(f"📍 Location: {os.path.abspath(path)}")
