import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
pt = 1
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

PDF_PATH = r"c:\Users\Dhruv's Dell\Desktop\Remo\LaunchCV_AI_SPI_Project_Report.pdf"

# Register standard TrueType fonts available on Windows
pdfmetrics.registerFont(TTFont('ProFont', r'C:\Windows\Fonts\times.ttf'))
pdfmetrics.registerFont(TTFont('ProFont-Bold', r'C:\Windows\Fonts\timesbd.ttf'))
pdfmetrics.registerFont(TTFont('ProFont-Italic', r'C:\Windows\Fonts\timesi.ttf'))
pdfmetrics.registerFont(TTFont('ProFont-BoldItalic', r'C:\Windows\Fonts\timesbi.ttf'))

pdfmetrics.registerFont(TTFont('HeadFont', r'C:\Windows\Fonts\arial.ttf'))
pdfmetrics.registerFont(TTFont('HeadFont-Bold', r'C:\Windows\Fonts\arialbd.ttf'))

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations()
            super().showPage()
        super().save()

    def draw_decorations(self):
        self.saveState()
        border_x = 24 * pt
        border_y = 20 * pt
        w, h = A4

        # Outer Frame Border
        self.setStrokeColor(colors.HexColor("#000000"))
        self.setLineWidth(1.2 * pt)
        self.rect(border_x, border_y, w - 2 * border_x, h - 2 * border_y)

        # Running Footer Divider & Metadata
        self.setStrokeColor(colors.HexColor("#94a3b8"))
        self.setLineWidth(0.6 * pt)
        self.line(border_x + 8 * pt, border_y + 18 * pt, w - border_x - 8 * pt, border_y + 18 * pt)

        self.setFont("HeadFont", 8.5 * pt)
        self.setFillColor(colors.HexColor("#000000"))
        footer_text = "MSBTE 5TH SEM (K-SCHEME) SPI PROJECT REPORT | DEPT. OF COMPUTER ENGINEERING"
        self.drawString(border_x + 10 * pt, border_y + 6.5 * pt, footer_text)
        self.drawRightString(w - border_x - 10 * pt, border_y + 6.5 * pt, f"Page {self._pageNumber}")

        self.restoreState()

def create_placeholder_box(title, subtitle="", height_pt=180):
    """Creates a clean drop-zone container for screenshot insertion."""
    content = [
        Paragraph(f"<font size=11 color='#0284c7'><b>[ 🖼️ {title} ]</b></font>", ParagraphStyle('PH1', fontName='HeadFont-Bold', alignment=TA_CENTER, leading=14)),
        Paragraph(f"<font size=9 color='#64748b'><i>{subtitle if subtitle else 'Reserved Drop Zone — Drop verified application output screenshot / architectural diagram here'}</i></font>", ParagraphStyle('PH2', fontName='ProFont-Italic', alignment=TA_CENTER, leading=12, spaceBefore=4))
    ]
    tbl = Table([[content]], colWidths=[525 * pt], rowHeights=[height_pt * pt])
    tbl.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1.5 * pt, colors.HexColor("#94a3b8")),
        ('TOPPADDING', (0,0), (-1,-1), 8 * pt),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8 * pt),
    ]))
    return tbl

def create_callout_box(title, text_content):
    """Creates an executive takeaway callout box with accent left border."""
    content = [
        Paragraph(f"<b><font color='#0284c7'>{title}</font></b>", ParagraphStyle('CalloutT', fontName='HeadFont-Bold', fontSize=10, leading=13, spaceAfter=3)),
        Paragraph(text_content, ParagraphStyle('CalloutB', fontName='ProFont', fontSize=9.5, leading=13.5, alignment=TA_JUSTIFY))
    ]
    tbl = Table([[content]], colWidths=[525 * pt])
    tbl.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 0.5 * pt, colors.HexColor("#e2e8f0")),
        ('LINEBEFORE', (0,0), (0,0), 3.5 * pt, colors.HexColor("#0284c7")),
        ('TOPPADDING', (0,0), (-1,-1), 6 * pt),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6 * pt),
        ('LEFTPADDING', (0,0), (-1,-1), 10 * pt),
        ('RIGHTPADDING', (0,0), (-1,-1), 10 * pt),
    ]))
    return tbl

def generate_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=A4,
        leftMargin=30 * pt,
        rightMargin=30 * pt,
        topMargin=26 * pt,
        bottomMargin=28 * pt
    )

    # Typography styles tailored for MSBTE Technical Documentation
    title_cover = ParagraphStyle('CoverTitle', fontName='HeadFont-Bold', fontSize=24, leading=28, alignment=TA_CENTER, textColor=colors.HexColor("#000000"), spaceAfter=4)
    subtitle_cover = ParagraphStyle('CoverSub', fontName='ProFont-Italic', fontSize=12, leading=15, alignment=TA_CENTER, textColor=colors.HexColor("#1f2937"), spaceAfter=12)
    center_bold_13 = ParagraphStyle('CBold13', fontName='HeadFont-Bold', fontSize=13, leading=16, alignment=TA_CENTER, textColor=colors.HexColor("#000000"))
    center_bold_12 = ParagraphStyle('CBold12', fontName='HeadFont-Bold', fontSize=11.5, leading=15, alignment=TA_CENTER, textColor=colors.HexColor("#000000"))
    center_bold_11 = ParagraphStyle('CBold11', fontName='HeadFont-Bold', fontSize=10.5, leading=14, alignment=TA_CENTER, textColor=colors.HexColor("#000000"))
    center_reg_12 = ParagraphStyle('CReg12', fontName='ProFont', fontSize=11.5, leading=15, alignment=TA_CENTER, textColor=colors.HexColor("#000000"))
    center_reg_11 = ParagraphStyle('CReg11', fontName='ProFont', fontSize=10.5, leading=14, alignment=TA_CENTER, textColor=colors.HexColor("#000000"))
    
    chapter_h1 = ParagraphStyle('ChapH1', fontName='HeadFont-Bold', fontSize=13.5, leading=16.5, alignment=TA_CENTER, spaceBefore=0, spaceAfter=2, textColor=colors.HexColor("#000000"))
    chapter_h2 = ParagraphStyle('ChapH2', fontName='HeadFont-Bold', fontSize=10.5, leading=13.5, alignment=TA_CENTER, spaceAfter=7, textColor=colors.HexColor("#000000"))
    
    body = ParagraphStyle('ProBody', fontName='ProFont', fontSize=10, leading=14.5, alignment=TA_JUSTIFY, spaceAfter=7, textColor=colors.HexColor("#000000"))
    bullet = ParagraphStyle('ProBullet', fontName='ProFont', fontSize=9.5, leading=13.8, alignment=TA_JUSTIFY, leftIndent=14, firstLineIndent=-8, spaceAfter=4, textColor=colors.HexColor("#000000"))
    subhead = ParagraphStyle('ProSubhead', fontName='HeadFont-Bold', fontSize=10.8, leading=14.5, alignment=TA_LEFT, spaceBefore=6, spaceAfter=2, textColor=colors.HexColor("#000000"))
    fig_cap = ParagraphStyle('FigCap', fontName='HeadFont-Bold', fontSize=8.5, leading=11, alignment=TA_CENTER, textColor=colors.HexColor("#334155"))

    table_heading_style = ParagraphStyle('TblHdr', fontName='HeadFont-Bold', fontSize=8.5, leading=11, alignment=TA_CENTER, textColor=colors.black)
    table_cell_style = ParagraphStyle('TblCell', fontName='ProFont', fontSize=8.5, leading=11.5, alignment=TA_LEFT, textColor=colors.black)
    table_center_style = ParagraphStyle('TblCenter', fontName='ProFont', fontSize=8.5, leading=11.5, alignment=TA_CENTER, textColor=colors.black)

    story = []

    # ==========================================
    # PAGE 1: COVER PAGE
    # ==========================================
    story.append(Spacer(1, 10 * pt))
    story.append(Paragraph("A Technical Project Report on<br/><b>SOFTWARE PROJECT IMPLEMENTATION (SPI)</b><br/>Submitted in Partial Fulfillment of the Requirements for the<br/><b>DIPLOMA IN COMPUTER ENGINEERING</b><br/>(Maharashtra State Board of Technical Education – MSBTE, 'K' Scheme)", center_reg_11))
    story.append(Spacer(1, 18 * pt))
    story.append(Paragraph("LAUNCHCV AI", title_cover))
    story.append(Paragraph("An End-to-End AI-Driven Career Intelligence, Dynamic Resume Studio &amp; Multi-Tenant Portfolio Suite", subtitle_cover))
    story.append(Spacer(1, 10 * pt))
    story.append(Paragraph("Submitted By", center_reg_12))
    story.append(Spacer(1, 3 * pt))
    story.append(Paragraph("<b>Dhruv R. Dubey</b><br/>Enrollment No: 25112400240 | Class: TYCO - B (Semester V)", center_bold_13))
    story.append(Spacer(1, 14 * pt))
    story.append(Paragraph("Under the Guidance of", center_reg_12))
    story.append(Spacer(1, 4 * pt))
    
    mentor_box_data = [
        [Paragraph("<b>Project Guide</b><br/>Ms. Mansi Patil<br/><font size=8.5 color='#4b5563'>Lecturer, Dept. of Computer Engg.</font>", center_bold_11),
         Paragraph("<b>Head of Department</b><br/>Prof. Ashwini Save<br/><font size=8.5 color='#4b5563'>HOD, Dept. of Computer Engg.</font>", center_bold_11)]
    ]
    mentor_tbl = Table(mentor_box_data, colWidths=[255 * pt, 255 * pt])
    mentor_tbl.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOX', (0,0), (-1,-1), 1.2 * pt, colors.HexColor("#0f2b5c")),
        ('INNERGRID', (0,0), (-1,-1), 0.6 * pt, colors.HexColor("#cbd5e1")),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('TOPPADDING', (0,0), (-1,-1), 6 * pt),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6 * pt),
    ]))
    story.append(mentor_tbl)
    story.append(Spacer(1, 18 * pt))

    viva_badge_data = [
        [Paragraph("<font size=8.5 color='#b91c1c'><b>VISHNU WAMAN THAKUR CHARITABLE TRUST'S</b></font>", center_bold_11)],
        [Paragraph("<font size=22 color='#b91c1c'><b>VIVA</b></font>", center_bold_13)],
        [Paragraph("<font size=8.5 color='#0f2b5c'><b>INSTITUTE OF TECHNOLOGY / POLYTECHNIC</b></font>", center_bold_11)]
    ]
    viva_badge_tbl = Table(viva_badge_data, colWidths=[260 * pt])
    viva_badge_tbl.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOX', (0,0), (-1,-1), 1.5 * pt, colors.HexColor("#b91c1c")),
        ('INNERGRID', (0,0), (-1,-1), 0.5 * pt, colors.HexColor("#e5e7eb")),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#ffffff")),
        ('TOPPADDING', (0,0), (-1,-1), 5 * pt),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5 * pt),
    ]))
    story.append(viva_badge_tbl)
    story.append(Spacer(1, 14 * pt))

    story.append(Paragraph("DEPARTMENT OF COMPUTER ENGINEERING", center_bold_12))
    story.append(Spacer(1, 2 * pt))
    story.append(Paragraph("VIVA INSTITUTE OF TECHNOLOGY", center_bold_13))
    story.append(Spacer(1, 2 * pt))
    story.append(Paragraph("Shirgaon, Virar (East), Dist. Palghar, Maharashtra – 401305", center_reg_11))
    story.append(Spacer(1, 3 * pt))
    story.append(Paragraph("Academic Year: 2026-2027", center_bold_12))

    # ==========================================
    # PAGE 2: CERTIFICATE OF APPROVAL
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("<u>MAHARASHTRA STATE BOARD OF TECHNICAL EDUCATION</u>", chapter_h1))
    story.append(Paragraph("<b>VIVA INSTITUTE OF TECHNOLOGY, VIRAR (EAST)</b><br/>DEPARTMENT OF COMPUTER ENGINEERING", center_bold_11))
    story.append(Spacer(1, 14 * pt))
    
    cert_title = ParagraphStyle('CertT', fontName='HeadFont-Bold', fontSize=18, leading=22, alignment=TA_CENTER, textColor=colors.HexColor("#0f2b5c"))
    story.append(Paragraph("<u>CERTIFICATE</u>", cert_title))
    story.append(Spacer(1, 14 * pt))
    
    story.append(Paragraph(
        "This is to certify that the project entitled <b>\"LAUNCHCV AI: An End-to-End AI-Driven Career Intelligence, Dynamic Resume Studio &amp; Multi-Tenant Portfolio Suite\"</b> is a bona fide work carried out by <b>Dhruv R. Dubey</b> (Enrollment No: <b>25112400240</b>), student of Fifth Semester Diploma in Computer Engineering (TYCO - B) at <b>VIVA Institute of Technology, Virar</b>, in partial fulfillment of the requirements for the award of Diploma in Computer Engineering under the <b>Maharashtra State Board of Technical Education (MSBTE)</b> for the academic year 2026–2027.",
        body
    ))
    story.append(Spacer(1, 8 * pt))
    story.append(Paragraph(
        "The project work has been completed under my supervision and guidance and complies with all academic and engineering guidelines prescribed for the <b>Software Project Implementation (SPI - 5th Semester 'K' Scheme)</b> curriculum.",
        body
    ))
    story.append(Spacer(1, 45 * pt))

    sig_data = [
        [Paragraph("<b>Ms. Mansi Patil</b><br/>Project Guide<br/>Dept. of Computer Engg.", center_bold_11),
         Paragraph("<b>Prof. Ashwini Save</b><br/>Head of Department<br/>Dept. of Computer Engg.", center_bold_11),
         Paragraph("<b>Dr. Arun Kumar</b><br/>Principal<br/>VIVA Institute of Technology", center_bold_11)]
    ]
    sig_tbl = Table(sig_data, colWidths=[175 * pt, 175 * pt, 175 * pt])
    sig_tbl.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
        ('TOPPADDING', (0,0), (-1,-1), 10 * pt),
    ]))
    story.append(sig_tbl)
    story.append(Spacer(1, 40 * pt))

    eval_data = [
        [Paragraph("<b>Internal Examiner</b><br/>Signature: __________________<br/>Date: ____ / ____ / 2026", center_reg_11),
         Paragraph("<b>External Examiner</b><br/>Signature: __________________<br/>Date: ____ / ____ / 2026", center_reg_11)]
    ]
    eval_tbl = Table(eval_data, colWidths=[260 * pt, 260 * pt])
    eval_tbl.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
        ('BOX', (0,0), (-1,-1), 1 * pt, colors.HexColor("#94a3b8")),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('TOPPADDING', (0,0), (-1,-1), 8 * pt),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8 * pt),
    ]))
    story.append(eval_tbl)

    # ==========================================
    # PAGE 3: DECLARATION & ACKNOWLEDGEMENT
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("<u>CANDIDATE'S DECLARATION</u>", chapter_h1))
    story.append(Spacer(1, 6 * pt))
    story.append(Paragraph(
        "I hereby declare that the project report entitled <b>\"LAUNCHCV AI\"</b> submitted by me to the Department of Computer Engineering, <b>VIVA Institute of Technology, Virar</b>, in partial fulfillment of the requirements for the award of Diploma in Computer Engineering from <b>MSBTE</b>, is an authentic record of my original work completed under the guidance of <b>Ms. Mansi Patil</b>.",
        body
    ))
    story.append(Paragraph(
        "I confirm that this project report has not formed the basis for the award of any other degree, diploma, fellowship, or associate-ship from any other university or board.",
        body
    ))
    story.append(Spacer(1, 16 * pt))
    
    decl_data = [
        [Paragraph("<b>Place:</b> Virar, Maharashtra<br/><b>Date:</b> ____ / ____ / 2026", ParagraphStyle('DecL', fontName='ProFont', fontSize=10, leading=14)),
         Paragraph("<b>Dhruv R. Dubey</b><br/>Enrollment No: 25112400240<br/>Third Year Computer Engineering (TYCO-B)", ParagraphStyle('DecR', fontName='ProFont-Bold', fontSize=10, leading=14, alignment=TA_RIGHT))]
    ]
    decl_tbl = Table(decl_data, colWidths=[260 * pt, 265 * pt])
    decl_tbl.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(decl_tbl)
    
    story.append(Spacer(1, 16 * pt))
    story.append(Paragraph("<u>ACKNOWLEDGEMENT</u>", chapter_h1))
    story.append(Spacer(1, 6 * pt))
    story.append(Paragraph(
        "I express my deepest sense of gratitude and sincere thanks to my project guide, <b>Ms. Mansi Patil</b>, Lecturer in the Department of Computer Engineering, for her invaluable guidance, constructive criticism, and constant encouragement throughout the development of <b>LaunchCV AI</b>.",
        body
    ))
    story.append(Paragraph(
        "I am profoundly grateful to <b>Prof. Ashwini Save</b>, Head of the Department of Computer Engineering, and <b>Dr. Arun Kumar</b>, Principal of VIVA Institute of Technology, for providing the necessary institutional facilities, computing labs, and academic atmosphere required to successfully complete this project.",
        body
    ))
    story.append(Paragraph(
        "I also thank all the faculty members of the Computer Engineering department, lab assistants, and my peers for their valuable suggestions, peer-testing feedback, and continuous moral support during the execution of this Software Project Implementation.",
        body
    ))

    # ==========================================
    # PAGE 4: ABSTRACT & EXECUTIVE SUMMARY
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("<u>ABSTRACT</u>", chapter_h1))
    story.append(Spacer(1, 6 * pt))
    story.append(Paragraph(
        "In the contemporary competitive technology employment ecosystem, candidates face severe friction across multiple stages of career advancement: unoptimized resumes filtered out by automated <b>Applicant Tracking Systems (ATS)</b>, generic outreach messages ignored by hiring managers, and the technical complexity of publishing fast, standalone developer portfolios. Traditional resume editors operate as static formatters with no semantic intelligence or real-time alignment scoring against target job descriptions.",
        body
    ))
    story.append(Paragraph(
        "To solve these challenges, <b>LaunchCV AI</b> is architected as an end-to-end, high-throughput full-stack career intelligence and personal branding suite. Developed under the MSBTE 5th Semester 'K' Scheme Computer Engineering curriculum, LaunchCV AI integrates six specialized sub-suites under a decoupled client-server architecture:",
        body
    ))
    story.append(Paragraph("• <b>Remo AI (Smart Resume Builder):</b> Form-driven resume composer featuring real-time AI bullet refinement via Groq LPU (Llama 3 / Qwen 2.5) and a coordinate-based PDFKit vector compilation engine guaranteeing print-perfect A4 pagination.", bullet))
    story.append(Paragraph("• <b>Folio AI (Web Portfolio Publisher):</b> Instant generator with four responsive themes (Bento Grid, Cyber Terminal, Modern Executive, Clean Glassmorphism) and client-side zero-dependency HTML/CSS/JS export in ZIP format via JSZip.", bullet))
    story.append(Paragraph("• <b>Talo AI (ATS Alignment Auditor):</b> Real-time comparative semantic matcher analyzing resumes against target job descriptions, computing keyword match scores, and suggesting instant bullet rewrites.", bullet))
    story.append(Paragraph("• <b>Covo AI (Recruiter Outreach Studio):</b> Generator for tailored cover letters with instant PDF compilation, cold emails, and recruiter pitch messaging.", bullet))
    story.append(Paragraph("• <b>Liko AI (LinkedIn Architect):</b> Milestone-to-social post converter with dynamic hook styles and LinkedIn profile About bio optimizer.", bullet))
    story.append(Paragraph("• <b>Mali AI (Email Campaign Studio):</b> Visual rich-text HTML email composer with 12 Google fonts, 7 theme palettes, and an automated background scheduling worker via Zoho SMTP.", bullet))
    story.append(Spacer(1, 4 * pt))
    story.append(create_callout_box(
        "Executive Summary",
        "LaunchCV AI delivers a unified SaaS workflow reducing resume tailoring and outreach preparation time by over 80% while ensuring strict deterministic formatting, multi-tenant JWT security, and 10 dynamic Apple-smooth visual themes."
    ))

    # ==========================================
    # PAGE 5: TABLE OF CONTENTS & LIST OF TABLES/FIGURES
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("<u>TABLE OF CONTENTS</u>", chapter_h1))
    story.append(Spacer(1, 5 * pt))

    toc_data = [
        [Paragraph("<b>Sr. No.</b>", center_bold_11), Paragraph("<b>Chapter / Topic Title</b>", center_bold_11), Paragraph("<b>Page No.</b>", center_bold_11)],
        [Paragraph("1", center_reg_11), Paragraph("Certificate of Approval &amp; Candidate Declaration", body), Paragraph("2–3", center_reg_11)],
        [Paragraph("2", center_reg_11), Paragraph("Abstract &amp; Executive Summary", body), Paragraph("4", center_reg_11)],
        [Paragraph("3", center_reg_11), Paragraph("Chapter 1: Introduction, Problem Statement &amp; Objectives", body), Paragraph("6", center_reg_11)],
        [Paragraph("4", center_reg_11), Paragraph("Chapter 2: Literature Survey, Market Analysis &amp; Feasibility Study", body), Paragraph("7", center_reg_11)],
        [Paragraph("5", center_reg_11), Paragraph("Chapter 3: Software Requirement Specification (SRS) &amp; Environment", body), Paragraph("8", center_reg_11)],
        [Paragraph("6", center_reg_11), Paragraph("Chapter 4: System Architecture, Data Flow &amp; Database Design", body), Paragraph("9–10", center_reg_11)],
        [Paragraph("7", center_reg_11), Paragraph("Chapter 5: Methodology &amp; Implementation of 6 AI Sub-Suites", body), Paragraph("11–13", center_reg_11)],
        [Paragraph("8", center_reg_11), Paragraph("Chapter 6: Software Testing, Test Cases &amp; Quality Assurance", body), Paragraph("14", center_reg_11)],
        [Paragraph("9", center_reg_11), Paragraph("Chapter 7: Results, System Output Screens &amp; Performance Analysis", body), Paragraph("15–16", center_reg_11)],
        [Paragraph("10", center_reg_11), Paragraph("Chapter 8: Conclusion, MSBTE CO/PO Alignment &amp; Future Scope", body), Paragraph("17", center_reg_11)],
        [Paragraph("11", center_reg_11), Paragraph("Chapter 9: References, Technical Standards &amp; Bibliography", body), Paragraph("18", center_reg_11)]
    ]

    toc_tbl = Table(toc_data, colWidths=[42 * pt, 436 * pt, 52 * pt])
    toc_tbl.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1.2 * pt, colors.HexColor("#000000")),
        ('INNERGRID', (0,0), (-1,-1), 0.6 * pt, colors.HexColor("#000000")),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (2,0), (2,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3.5 * pt),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5 * pt),
        ('LEFTPADDING', (1,0), (1,-1), 6 * pt),
    ]))
    story.append(toc_tbl)
    story.append(Spacer(1, 10 * pt))

    story.append(Paragraph("<u>LIST OF FIGURES &amp; TABLES</u>", chapter_h1))
    story.append(Spacer(1, 4 * pt))
    lot_data = [
        [Paragraph("<b>Figure / Table</b>", center_bold_11), Paragraph("<b>Description / Title</b>", center_bold_11), Paragraph("<b>Page No.</b>", center_bold_11)],
        [Paragraph("Figure 4.1", center_reg_11), Paragraph("LaunchCV AI Decoupled Client-Server &amp; Groq LPU System Architecture", body), Paragraph("9", center_reg_11)],
        [Paragraph("Figure 4.2", center_reg_11), Paragraph("Data Flow Diagram (DFD Level 0 &amp; Level 1) for Profile &amp; AI Refinement", body), Paragraph("9", center_reg_11)],
        [Paragraph("Table 3.1", center_reg_11), Paragraph("Hardware &amp; Software Environment Specifications", body), Paragraph("8", center_reg_11)],
        [Paragraph("Table 4.1", center_reg_11), Paragraph("Supabase PostgreSQL &amp; JSONB Data Schema Entity Definition", body), Paragraph("10", center_reg_11)],
        [Paragraph("Table 6.1", center_reg_11), Paragraph("Software Test Cases &amp; Validation Matrix (Pass/Fail Results)", body), Paragraph("14", center_reg_11)],
        [Paragraph("Figure 7.1–7.4", center_reg_11), Paragraph("System Output Screens: Auth, Remo AI Editor, Folio Themes, Mali Campaign Studio", body), Paragraph("15–16", center_reg_11)]
    ]
    lot_tbl = Table(lot_data, colWidths=[80 * pt, 398 * pt, 52 * pt])
    lot_tbl.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1.2 * pt, colors.HexColor("#000000")),
        ('INNERGRID', (0,0), (-1,-1), 0.6 * pt, colors.HexColor("#000000")),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (2,0), (2,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3 * pt),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3 * pt),
        ('LEFTPADDING', (1,0), (1,-1), 6 * pt),
    ]))
    story.append(lot_tbl)

    # ==========================================
    # PAGE 6: CHAPTER 1 - INTRODUCTION & PROBLEM STATEMENT
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("CHAPTER 1", chapter_h1))
    story.append(Paragraph("INTRODUCTION, PROBLEM DEFINITION &amp; PROJECT OBJECTIVES", chapter_h2))
    
    story.append(Paragraph("1.1 Background &amp; Motivation", subhead))
    story.append(Paragraph(
        "In the modern technology job market, the transition from college graduation to industry employment requires a multi-faceted digital presence. Candidates must prepare ATS-compliant resumes, publish responsive portfolio websites, craft customized cover letters, and maintain engaging professional outreach on platforms like LinkedIn and email. However, existing tools operate in silos: resume builders lack semantic alignment feedback, portfolio site generators require complex hosting configurations, and outreach drafting remains a tedious manual effort.",
        body
    ))
    story.append(Paragraph("1.2 Problem Statement", subhead))
    story.append(Paragraph(
        "Current career preparation platforms suffer from three critical engineering limitations:",
        body
    ))
    story.append(Paragraph("1. <b>Inflexible Formatting &amp; Layout Shift:</b> Web-based PDF generators relying on standard browser printing (`window.print()`) often break page boundaries, clip margins, and fail strict A4 standard sizing.", bullet))
    story.append(Paragraph("2. <b>Lack of Intelligent ATS Gap Analysis:</b> Candidates submit generic resumes without knowing if their keyword density matches target Job Descriptions (JDs), leading to high automated rejection rates.", bullet))
    story.append(Paragraph("3. <b>Fragmented Tooling Ecosystem:</b> Users must juggle separate tools for resume writing, portfolio hosting, cover letter generation, and cold emailing, resulting in disjointed candidate profiles.", bullet))

    story.append(Paragraph("1.3 Objectives of the Project", subhead))
    story.append(Paragraph("• To design and implement a unified full-stack career platform connecting candidate profiling with 6 specialized generative AI sub-suites.", bullet))
    story.append(Paragraph("• To develop a server-side vector PDF generation engine using PDFKit with mathematical coordinate pagination on exact A4 dimensions.", bullet))
    story.append(Paragraph("• To integrate high-speed Large Language Models (Groq LPU inference) for real-time resume bullet refinement and ATS alignment scoring under 800ms.", bullet))
    story.append(Paragraph("• To implement client-side zero-dependency static portfolio bundling via JSZip and an automated background email queue scheduler using Zoho SMTP.", bullet))
    story.append(Paragraph("• To engineer a multi-theme responsive interface with Apple-smooth cubic-bezier transitions and multi-device cybersecurity audit tracking.", bullet))

    # ==========================================
    # PAGE 7: CHAPTER 2 - LITERATURE SURVEY & FEASIBILITY STUDY
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("CHAPTER 2", chapter_h1))
    story.append(Paragraph("LITERATURE SURVEY, MARKET ANALYSIS &amp; FEASIBILITY STUDY", chapter_h2))
    
    story.append(Paragraph("2.1 Literature Survey &amp; Existing System Comparison", subhead))
    story.append(Paragraph(
        "A detailed comparative analysis was conducted between popular existing commercial solutions and the proposed LaunchCV AI system architecture:",
        body
    ))

    comp_data = [
        [Paragraph("<b>Platform Feature</b>", table_heading_style), Paragraph("<b>Canva / Novoresume</b>", table_heading_style), Paragraph("<b>LinkedIn / Standard Sites</b>", table_heading_style), Paragraph("<b>LaunchCV AI (Proposed)</b>", table_heading_style)],
        [Paragraph("Resume Generation", table_cell_style), Paragraph("Static canvas / HTML print", table_cell_style), Paragraph("Basic text export", table_cell_style), Paragraph("PDFKit Vector A4 coordinate math (105+ layouts)", table_cell_style)],
        [Paragraph("AI Bullet Refinement", table_cell_style), Paragraph("Paid add-on / Generic", table_cell_style), Paragraph("Limited premium rewrite", table_cell_style), Paragraph("Groq LPU Sub-second LLM inference (Llama 3/Qwen)", table_cell_style)],
        [Paragraph("ATS Match Scoring", table_cell_style), Paragraph("Not available / Basic", table_cell_style), Paragraph("Keyword alerts only", table_cell_style), Paragraph("Talo AI: % match, keyword gap, targeted rewrites", table_cell_style)],
        [Paragraph("Portfolio Publishing", table_cell_style), Paragraph("Hosted link only", table_cell_style), Paragraph("Profile URL only", table_cell_style), Paragraph("Folio AI: Standalone zero-dep ZIP package + Live URL", table_cell_style)],
        [Paragraph("Outreach &amp; Emailing", table_cell_style), Paragraph("None", table_cell_style), Paragraph("Manual InMail messaging", table_cell_style), Paragraph("Covo &amp; Mali AI: HTML composer + background queue", table_cell_style)]
    ]
    comp_tbl = Table(comp_data, colWidths=[95 * pt, 135 * pt, 135 * pt, 160 * pt])
    comp_tbl.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1 * pt, colors.HexColor("#000000")),
        ('INNERGRID', (0,0), (-1,-1), 0.5 * pt, colors.HexColor("#cbd5e1")),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3.5 * pt),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5 * pt),
    ]))
    story.append(comp_tbl)
    story.append(Spacer(1, 6 * pt))

    story.append(Paragraph("2.2 Feasibility Analysis", subhead))
    story.append(Paragraph(
        "<b>1. Technical Feasibility:</b> Built upon proven open-source industry stacks (React 18, Node.js, Express, Supabase PostgreSQL). Groq SDK provides ultra-fast inference speeds (500+ tokens/sec), ensuring responsive user interactions without heavy local GPU dependencies.",
        body
    ))
    story.append(Paragraph(
        "<b>2. Economic Feasibility:</b> Leverages free-tier cloud resources (Supabase, Groq API, Zoho SMTP) and open-source npm packages, resulting in near-zero software licensing and deployment costs.",
        body
    ))
    story.append(Paragraph(
        "<b>3. Operational Feasibility:</b> Designed with an intuitive Single-Page Application (SPA) workflow, accessible to students, job-seekers, and professionals without requiring coding skills.",
        body
    ))

    # ==========================================
    # PAGE 8: CHAPTER 3 - SOFTWARE REQUIREMENT SPECIFICATION (SRS)
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("CHAPTER 3", chapter_h1))
    story.append(Paragraph("SOFTWARE REQUIREMENT SPECIFICATION (SRS) &amp; SYSTEM ENVIRONMENT", chapter_h2))
    
    story.append(Paragraph("3.1 Functional Requirements", subhead))
    story.append(Paragraph("• <b>Authentication &amp; User Security:</b> 6-digit OTP email verification via Zoho SMTP, JWT token issuance, and multi-device access security tracking.", bullet))
    story.append(Paragraph("• <b>Centralized Profile Management:</b> Dynamic CRUD operations storing JSONB candidate profile parameters (skills, experience, projects, education, social links).", bullet))
    story.append(Paragraph("• <b>Remo AI Engine:</b> Dynamic resume configuration supporting 105+ layout permutations and backend PDFKit vector generation with exact page breaking.", bullet))
    story.append(Paragraph("• <b>Folio AI Engine:</b> Live multi-theme web portfolio renderer with zero-dependency standalone ZIP archive bundling via JSZip.", bullet))
    story.append(Paragraph("• <b>Talo AI Engine:</b> Job description parsing, comparative keyword scoring algorithm, and ATS optimization suggestions.", bullet))
    story.append(Paragraph("• <b>Mali AI Engine:</b> Visual rich-text HTML email editor with 12 Google fonts, 7 theme palettes, and automated background queue worker (emailScheduler.js).", bullet))

    story.append(Paragraph("3.2 Non-Functional Requirements", subhead))
    story.append(Paragraph("• <b>Performance:</b> AI refinement latency &lt; 1000ms; PDF rendering time &lt; 1500ms; page load speed &lt; 2 seconds.", bullet))
    story.append(Paragraph("• <b>Security:</b> Enforced JWT bearer token validation on protected API routes; sanitization of LLM responses against prompt injection.", bullet))
    story.append(Paragraph("• <b>Reliability &amp; Availability:</b> Graceful fallback to local JSON database and mock LLM pipelines during network or third-party outages.", bullet))

    story.append(Paragraph("3.3 Hardware &amp; Software Environment Specifications", subhead))
    env_data = [
        [Paragraph("<b>Category</b>", table_heading_style), Paragraph("<b>Minimum Requirements</b>", table_heading_style), Paragraph("<b>Development / Recommended Setup</b>", table_heading_style)],
        [Paragraph("Processor", table_cell_style), Paragraph("Dual-Core 2.0 GHz Intel / AMD", table_cell_style), Paragraph("Intel Core i5 / AMD Ryzen 5 or higher", table_cell_style)],
        [Paragraph("System RAM", table_cell_style), Paragraph("4 GB RAM", table_cell_style), Paragraph("8 GB / 16 GB DDR4 RAM", table_cell_style)],
        [Paragraph("Storage", table_cell_style), Paragraph("500 MB free disk space", table_cell_style), Paragraph("SSD NVMe Storage (1 GB+ free)", table_cell_style)],
        [Paragraph("Operating System", table_cell_style), Paragraph("Windows 10 / 11 / Linux / macOS", table_cell_style), Paragraph("Windows 11 64-bit with PowerShell / Bash", table_cell_style)],
        [Paragraph("Frontend Toolchain", table_cell_style), Paragraph("Modern Web Browser (Chrome / Edge)", table_cell_style), Paragraph("React 18.2, Vite 5, Tailwind CSS v3, PostCSS", table_cell_style)],
        [Paragraph("Backend &amp; Database", table_cell_style), Paragraph("Node.js v18 LTS, npm v9+", table_cell_style), Paragraph("Express.js, Supabase PostgreSQL, Groq SDK, PDFKit", table_cell_style)]
    ]
    env_tbl = Table(env_data, colWidths=[110 * pt, 185 * pt, 230 * pt])
    env_tbl.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1 * pt, colors.HexColor("#000000")),
        ('INNERGRID', (0,0), (-1,-1), 0.5 * pt, colors.HexColor("#cbd5e1")),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('TOPPADDING', (0,0), (-1,-1), 3 * pt),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3 * pt),
    ]))
    story.append(env_tbl)

    # ==========================================
    # PAGE 9: CHAPTER 4 - SYSTEM ARCHITECTURE & DESIGN (PART 1)
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("CHAPTER 4", chapter_h1))
    story.append(Paragraph("SYSTEM ARCHITECTURE, DATA FLOW &amp; DESIGN MODELLING", chapter_h2))
    
    story.append(Paragraph("4.1 Decoupled Client-Server System Architecture", subhead))
    story.append(Paragraph(
        "LaunchCV AI implements a modern decoupled 3-tier cloud architecture. The presentation layer (React 18 Single Page Application) communicates asynchronously with the application tier (Node.js &amp; Express REST APIs) over secure JSON endpoints. The service tier interfaces with Supabase PostgreSQL for persistent data, Groq LPU for sub-second AI inference, and Nodemailer/Zoho for SMTP routing:",
        body
    ))

    story.append(create_placeholder_box(
        "Figure 4.1: LaunchCV AI High-Throughput Decoupled Cloud Architecture Diagram",
        "React 18 SPA <-> Express REST APIs <-> Groq LPU Inference (Llama 3/Qwen) <-> Supabase Database & Zoho SMTP",
        height_pt=180
    ))
    story.append(Spacer(1, 3 * pt))
    story.append(Paragraph("<b>Figure 4.1:</b> LaunchCV AI High-Throughput Decoupled Cloud Architecture Diagram", fig_cap))
    story.append(Spacer(1, 5 * pt))

    story.append(Paragraph("4.2 Data Flow Diagram (DFD Level 0 &amp; Level 1)", subhead))
    story.append(Paragraph(
        "<b>DFD Level 0 (Context Level):</b> The user inputs profile bio, job descriptions, and template choices. The system processes credentials, triggers AI LLM completion, calculates A4 vector coordinates, and returns compiled PDF resumes, standalone portfolio ZIP packages, and ATS audit scores.",
        body
    ))
    story.append(Paragraph(
        "<b>DFD Level 1 (Decomposed Processes):</b> (1.0) Auth Handler &amp; OTP Verifier, (2.0) Central Profile Manager, (3.0) Groq AI Prompt Controller, (4.0) PDFKit Dynamic Coordinate Rendering Engine, (5.0) JSZip Client Bundler, and (6.0) Mali Background Email Queue Dispatcher.",
        body
    ))

    # ==========================================
    # PAGE 10: CHAPTER 4 - DATABASE DESIGN & JSON SCHEMA (PART 2)
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("CHAPTER 4 (CONTINUED)", chapter_h1))
    story.append(Paragraph("DATABASE DESIGN, SUPABASE POSTGRESQL &amp; STATE MANAGEMENT", chapter_h2))
    
    story.append(Paragraph("4.3 Database Schema &amp; Data Entity Design", subhead))
    story.append(Paragraph(
        "The application utilizes Supabase PostgreSQL with flexible JSONB structures to support candidate profiles with dynamic array parameters (experiences, skill hierarchies, bullet points) without schema lock:",
        body
    ))

    schema_data = [
        [Paragraph("<b>Table Name</b>", table_heading_style), Paragraph("<b>Field Name</b>", table_heading_style), Paragraph("<b>Data Type</b>", table_heading_style), Paragraph("<b>Constraints / Purpose</b>", table_heading_style)],
        [Paragraph("<b>otps</b>", table_cell_style), Paragraph("id<br/>email<br/>otp<br/>expires_at", table_cell_style), Paragraph("UUID<br/>TEXT<br/>TEXT<br/>TIMESTAMP", table_cell_style), Paragraph("PRIMARY KEY (DEFAULT gen_random_uuid())<br/>User email identifier<br/>6-digit cryptographically generated OTP<br/>Verification expiry (10 min TTL)", table_cell_style)],
        [Paragraph("<b>profiles</b>", table_cell_style), Paragraph("id<br/>user_id<br/>name, profession<br/>skills, achievements<br/>values (JSONB)<br/>updated_at", table_cell_style), Paragraph("UUID<br/>UUID<br/>TEXT<br/>JSONB<br/>JSONB<br/>TIMESTAMP", table_cell_style), Paragraph("PRIMARY KEY<br/>FOREIGN KEY -> auth.users(id)<br/>Candidate personal details<br/>Structured skill arrays<br/>Packed full profile state (experience, education, links)<br/>Last modified audit timestamp", table_cell_style)],
        [Paragraph("<b>login_history</b>", table_cell_style), Paragraph("id<br/>user_id<br/>ip_address<br/>user_agent<br/>created_at", table_cell_style), Paragraph("UUID<br/>UUID<br/>TEXT<br/>TEXT<br/>TIMESTAMP", table_cell_style), Paragraph("PRIMARY KEY<br/>FOREIGN KEY -> auth.users(id)<br/>Client IP address for anomaly detection<br/>Browser/Device signature string<br/>Login access timestamp", table_cell_style)]
    ]
    schema_tbl = Table(schema_data, colWidths=[85 * pt, 110 * pt, 85 * pt, 245 * pt])
    schema_tbl.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1 * pt, colors.HexColor("#000000")),
        ('INNERGRID', (0,0), (-1,-1), 0.5 * pt, colors.HexColor("#cbd5e1")),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3 * pt),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3 * pt),
    ]))
    story.append(schema_tbl)
    story.append(Spacer(1, 6 * pt))

    story.append(Paragraph("4.4 Hybrid Fallback Storage Architecture", subhead))
    story.append(Paragraph(
        "To ensure continuous offline resilience, LaunchCV AI implements a dual-mode persistence layer. If cloud database credentials or remote network connections are unavailable, the backend automatically transitions to a localized atomic JSON file store (`backend/localStore.js`) without degrading application performance or user workflow.",
        body
    ))

    # ==========================================
    # PAGE 11: CHAPTER 5 - METHODOLOGY & IMPLEMENTATION (PART 1)
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("CHAPTER 5", chapter_h1))
    story.append(Paragraph("METHODOLOGY &amp; IMPLEMENTATION — REMO AI &amp; FOLIO AI", chapter_h2))
    
    story.append(Paragraph("5.1 Remo AI: Smart Resume Builder &amp; PDFKit Dynamic Vector Engine", subhead))
    story.append(Paragraph(
        "<b>Remo AI</b> is designed to eliminate formatting breakage and content fluff in technical resumes. Key implementation highlights include:",
        body
    ))
    story.append(Paragraph("• <b>Dynamic Split-Screen Live Synchronization:</b> A dual-pane interface built in React 18 where user input edits in the left pane trigger debounced updates to the right-hand canvas preview.", bullet))
    story.append(Paragraph("• <b>Mathematical Coordinate Math in PDFKit:</b> Unlike browser HTML-to-PDF converters that generate rasterized images with blurred fonts, our backend `pdfGenerator.js` calculates exact A4 point coordinates (595.28 x 841.89 pt). Line wraps, section headings, and margin offsets are computed dynamically using `doc.heightOfString()` to enforce clean multi-page boundary splits.", bullet))
    story.append(Paragraph("• <b>105+ Visual Layout Permutations:</b> Supports 7 font families, 5 header color styles, 3 layout columns (Modern, Clean, Compact), and custom section reordering.", bullet))
    story.append(Paragraph("• <b>AI Bullet Point Refinement:</b> Connects to Groq LPU API (Llama 3 70B) with custom sliders for creativity, length, and industry action verbs to strengthen accomplishment impact.", bullet))

    story.append(Paragraph("5.2 Folio AI: Web Portfolio Publisher &amp; Zero-Dependency JSZip Packaging", subhead))
    story.append(Paragraph(
        "<b>Folio AI</b> empowers students and engineers to generate and publish responsive portfolio websites in seconds:",
        body
    ))
    story.append(Paragraph("• <b>4 Curated Visual Themes:</b> Bento Grid (modern modular cards), Cyber Terminal (developer monospace aesthetic), Modern Executive (clean corporate minimalism), and Clean Glassmorphism (translucent frosted panels).", bullet))
    story.append(Paragraph("• <b>Zero-Dependency Client-Side ZIP Packaging:</b> Utilizes client-side `JSZip` to compile full standalone `index.html`, `style.css`, and `script.js` assets directly in the browser. Users can download and deploy their complete portfolio onto GitHub Pages, Netlify, or Vercel with zero external runtime dependencies.", bullet))
    story.append(Paragraph("• <b>Open Profile Switcher:</b> Allows immediate live preview switching across multiple candidate profiles on the fly.", bullet))

    # ==========================================
    # PAGE 12: CHAPTER 5 - METHODOLOGY & IMPLEMENTATION (PART 2)
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("CHAPTER 5 (CONTINUED)", chapter_h1))
    story.append(Paragraph("METHODOLOGY &amp; IMPLEMENTATION — TALO AI &amp; COVO AI", chapter_h2))
    
    story.append(Paragraph("5.3 Talo AI: ATS Alignment Auditor &amp; Keyword Gap Engine", subhead))
    story.append(Paragraph(
        "<b>Talo AI</b> addresses the leading cause of candidate rejection: failing automated Applicant Tracking System keyword thresholds. The module implements a multi-step semantic evaluation pipeline:",
        body
    ))
    story.append(Paragraph("1. <b>Job Description Ingestion &amp; Entity Extraction:</b> Parses unstructured recruiter job postings into core competencies (Hard Skills, Frameworks, Experience Levels, Domain Certifications).", bullet))
    story.append(Paragraph("2. <b>Comparative Cosine Similarity &amp; Scoring Matrix:</b> Compares candidate profile JSON with target JD requirements, computing an overall alignment percentage (0–100%).", bullet))
    story.append(Paragraph("3. <b>Keyword Gap Detection:</b> Flags critical missing technical keywords categorized by priority (Essential, Recommended, Bonus).", bullet))
    story.append(Paragraph("4. <b>Targeted Bullet Rewriting:</b> Generates contextual sentence recommendations integrating missing keywords naturally into existing experience descriptions without fabricated data.", bullet))

    story.append(Paragraph("5.4 Covo AI: Recruiter Outreach Studio &amp; Dynamic Cover Letters", subhead))
    story.append(Paragraph(
        "<b>Covo AI</b> automates the creation of high-impact professional outreach materials tailored to specific company profiles:",
        body
    ))
    story.append(Paragraph("• <b>Dynamic Cover Letter PDF Generation:</b> Renders formatted 1-page A4 corporate cover letters matching the styling and typography of the candidate's resume.", bullet))
    story.append(Paragraph("• <b>Recruiter Pitch &amp; Cold Email Generator:</b> Produces customized email pitches highlighting key candidate achievements relevant to the target company's business domain.", bullet))
    story.append(Paragraph("• <b>LinkedIn Connection Requests:</b> Drafts concise, 300-character networking notes optimized for high response rates.", bullet))

    # ==========================================
    # PAGE 13: CHAPTER 5 - METHODOLOGY & IMPLEMENTATION (PART 3)
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("CHAPTER 5 (CONTINUED)", chapter_h1))
    story.append(Paragraph("METHODOLOGY &amp; IMPLEMENTATION — LIKO, MALI &amp; SECURITY SYSTEM", chapter_h2))
    
    story.append(Paragraph("5.5 Liko AI: LinkedIn Personal Branding Architect", subhead))
    story.append(Paragraph(
        "<b>Liko AI</b> transforms project milestones and hackathon wins into viral, formatted LinkedIn posts with customizable hook structures (Curiosity, Direct Value, Storytelling), relevant hashtags, and profile 'About' section optimization.",
        body
    ))

    story.append(Paragraph("5.6 Mali AI: Email Campaign Studio &amp; Background Queue Worker", subhead))
    story.append(Paragraph(
        "<b>Mali AI</b> is a complete automated email dispatch suite featuring:",
        body
    ))
    story.append(Paragraph("• <b>Visual Rich-Text HTML Composer:</b> Interactive WYSIWYG editor supporting custom typography (12 Google fonts), colors, alignments, hyperlinks, and simulated browser live preview.", bullet))
    story.append(Paragraph("• <b>Dual Time Pickers:</b> Inline React calendar picker and 12-Hour (AM/PM) / 24-Hour time toggles.", bullet))
    story.append(Paragraph("• <b>Asynchronous Background Queue Scheduler (`emailScheduler.js`):</b> An event-driven background polling service that monitors scheduled campaign timestamps, dispatches emails via Zoho SMTP, and audits delivery status (Pending, Sent, Failed) without blocking the Express event loop.", bullet))

    story.append(Paragraph("5.7 10-Theme Apple-Smooth UI &amp; Cybersecurity Monitoring", subhead))
    story.append(Paragraph(
        "• <b>10 Premium Visual Themes:</b> Luna, Moon, Solara Gold, Aurora Emerald, Nebula Crimson, Cyber Neon, Glacier Blue, Vulcan Orange, Forest Olive, Monochrome Silver, featuring Apple-style `cubic-bezier(0.16, 1, 0.3, 1)` snapping curves.", bullet
    ))
    story.append(Paragraph(
        "• <b>Multi-Device Security Alerts:</b> Audits client IP addresses and User-Agent headers (`loginHistory.js`), triggering automated security alert emails if logins occur across 3+ distinct devices.", bullet
    ))

    # ==========================================
    # PAGE 14: CHAPTER 6 - SOFTWARE TESTING & QUALITY ASSURANCE
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("CHAPTER 6", chapter_h1))
    story.append(Paragraph("SOFTWARE TESTING, TEST CASES &amp; QUALITY ASSURANCE", chapter_h2))
    
    story.append(Paragraph("6.1 Testing Methodology", subhead))
    story.append(Paragraph(
        "To verify system robustness, comprehensive testing was conducted across all layers: <b>Unit Testing</b> (individual API routes, OTP generation math), <b>Integration Testing</b> (Groq LLM streaming, Supabase JSONB serialization), <b>System Testing</b> (end-to-end PDF downloads, ZIP exports), and <b>Security Testing</b> (JWT token expiration, multi-device login alerts).",
        body
    ))

    story.append(Paragraph("6.2 Test Cases &amp; Validation Results Matrix", subhead))
    test_data = [
        [Paragraph("<b>Test ID</b>", table_heading_style), Paragraph("<b>Test Scenario / Description</b>", table_heading_style), Paragraph("<b>Expected Output</b>", table_heading_style), Paragraph("<b>Actual Output</b>", table_heading_style), Paragraph("<b>Status</b>", table_heading_style)],
        [Paragraph("TC-01", table_center_style), Paragraph("User OTP Signup with valid email", table_cell_style), Paragraph("6-digit OTP dispatched via Zoho SMTP", table_cell_style), Paragraph("OTP received in inbox within 3s", table_cell_style), Paragraph("<font color='green'><b>PASS</b></font>", table_center_style)],
        [Paragraph("TC-02", table_center_style), Paragraph("Invalid OTP entry verification", table_cell_style), Paragraph("HTTP 400 'Invalid or Expired OTP'", table_cell_style), Paragraph("Error toast displayed, login blocked", table_cell_style), Paragraph("<font color='green'><b>PASS</b></font>", table_center_style)],
        [Paragraph("TC-03", table_center_style), Paragraph("Remo AI Resume PDF vector rendering", table_cell_style), Paragraph("Clean A4 PDF download with exact margins", table_cell_style), Paragraph("PDFKit coordinates match A4 page grid", table_cell_style), Paragraph("<font color='green'><b>PASS</b></font>", table_center_style)],
        [Paragraph("TC-04", table_center_style), Paragraph("Folio AI Standalone ZIP Portfolio export", table_cell_style), Paragraph("ZIP contains index.html, style.css, script.js", table_cell_style), Paragraph("Unpacked file opens standalone locally", table_cell_style), Paragraph("<font color='green'><b>PASS</b></font>", table_center_style)],
        [Paragraph("TC-05", table_center_style), Paragraph("Talo AI ATS Match vs target JD", table_cell_style), Paragraph("Computes score % and missing keywords", table_cell_style), Paragraph("Returns JSON score & keyword array", table_cell_style), Paragraph("<font color='green'><b>PASS</b></font>", table_center_style)],
        [Paragraph("TC-06", table_center_style), Paragraph("Mali AI Background email queue dispatch", table_cell_style), Paragraph("Scheduler sends email at target timestamp", table_cell_style), Paragraph("Email dispatched successfully on schedule", table_cell_style), Paragraph("<font color='green'><b>PASS</b></font>", table_center_style)],
        [Paragraph("TC-07", table_center_style), Paragraph("Multi-Device Login Detection (3+ devices)", table_cell_style), Paragraph("Dispatches automated security alert email", table_cell_style), Paragraph("Alert email triggered with IP & device info", table_cell_style), Paragraph("<font color='green'><b>PASS</b></font>", table_center_style)]
    ]
    test_tbl = Table(test_data, colWidths=[40 * pt, 140 * pt, 150 * pt, 145 * pt, 50 * pt])
    test_tbl.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1 * pt, colors.HexColor("#000000")),
        ('INNERGRID', (0,0), (-1,-1), 0.5 * pt, colors.HexColor("#cbd5e1")),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3 * pt),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3 * pt),
    ]))
    story.append(test_tbl)
    story.append(Spacer(1, 4 * pt))
    story.append(create_callout_box(
        "QA Assessment Conclusion",
        "100% of the core functional and security test cases passed successfully, confirming high software reliability, deterministic PDF layout rendering, and sub-second API execution speeds."
    ))

    # ==========================================
    # PAGE 15: CHAPTER 7 - RESULTS & OUTPUT SCREENS (PART 1)
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("CHAPTER 7", chapter_h1))
    story.append(Paragraph("RESULTS, SYSTEM OUTPUT SCREENS &amp; INTERFACE SHOWCASE", chapter_h2))
    
    story.append(Paragraph("7.1 Authentication &amp; Profile Hub Interface", subhead))
    story.append(Paragraph(
        "The authentication interface features a minimalist dark theme supporting OTP-based passwordless entry and secure JWT credential validation:",
        body
    ))
    story.append(create_placeholder_box(
        "Figure 7.1: LaunchCV AI Authentication Screen & Central Candidate Profile Hub",
        "Drop screenshot of Auth.jsx login screen (One Text Box / OTP) and central Profile Management Hub",
        height_pt=175
    ))
    story.append(Spacer(1, 3 * pt))
    story.append(Paragraph("<b>Figure 7.1:</b> LaunchCV AI Authentication Screen &amp; Central Profile Hub", fig_cap))
    story.append(Spacer(1, 6 * pt))

    story.append(Paragraph("7.2 Remo AI: Interactive Resume Studio &amp; Live Vector Preview", subhead))
    story.append(Paragraph(
        "Split-screen editing environment with dynamic text synchronization, font/color selectors, AI refinement sliders, and live A4 PDF page rendering:",
        body
    ))
    story.append(create_placeholder_box(
        "Figure 7.2: Remo AI Resume Studio — Live Editor & PDFKit Dynamic Vector Preview",
        "Drop screenshot of Remo AI editor showing form controls, AI refine sliders, and dynamic A4 PDF preview",
        height_pt=175
    ))
    story.append(Spacer(1, 3 * pt))
    story.append(Paragraph("<b>Figure 7.2:</b> Remo AI Resume Studio — Interactive Split Screen Editor &amp; Vector Preview", fig_cap))

    # ==========================================
    # PAGE 16: CHAPTER 7 - RESULTS & OUTPUT SCREENS (PART 2)
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("CHAPTER 7 (CONTINUED)", chapter_h1))
    story.append(Paragraph("RESULTS, SYSTEM OUTPUT SCREENS &amp; CAMPAIGN DASHBOARD", chapter_h2))
    
    story.append(Paragraph("7.3 Folio AI: Multi-Theme Portfolio Generator &amp; Template Picker", subhead))
    story.append(Paragraph(
        "Visual theme gallery allowing users to select Bento Grid, Cyber Terminal, Executive, or Glassmorphism templates and download zero-dependency ZIP packages:",
        body
    ))
    story.append(create_placeholder_box(
        "Figure 7.3: Folio AI Portfolio Studio — Multi-Theme Visual Showcase & ZIP Exporter",
        "Drop screenshot of Folio AI template selection cards and exported standalone web portfolio preview",
        height_pt=175
    ))
    story.append(Spacer(1, 3 * pt))
    story.append(Paragraph("<b>Figure 7.3:</b> Folio AI Portfolio Studio — Multi-Theme Visual Showcase &amp; ZIP Exporter", fig_cap))
    story.append(Spacer(1, 6 * pt))

    story.append(Paragraph("7.4 Mali AI: HTML Email Campaign Studio &amp; Scheduled Queue", subhead))
    story.append(Paragraph(
        "Visual rich-text email composer with Google typography picker, theme presets, simulated browser sandbox, and scheduled background queue monitor:",
        body
    ))
    story.append(create_placeholder_box(
        "Figure 7.4: Mali AI & Covo AI — Visual HTML Composer & Scheduled Queue Manager",
        "Drop screenshot of Mali AI email composer, typography settings, and scheduled campaign queue list",
        height_pt=175
    ))
    story.append(Spacer(1, 3 * pt))
    story.append(Paragraph("<b>Figure 7.4:</b> Mali AI &amp; Covo AI — Visual HTML Email Composer &amp; Scheduled Queue Dashboard", fig_cap))

    # ==========================================
    # PAGE 17: CHAPTER 8 - CONCLUSION & FUTURE SCOPE
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("CHAPTER 8", chapter_h1))
    story.append(Paragraph("CONCLUSION, MSBTE CURRICULUM OUTCOMES &amp; FUTURE SCOPE", chapter_h2))
    
    story.append(Paragraph("8.1 Project Conclusion", subhead))
    story.append(Paragraph(
        "The development of <b>LaunchCV AI</b> represents a comprehensive, production-grade implementation of full-stack software engineering, generative AI orchestration, and deterministic document compilation. Developed under the <b>MSBTE 5th Semester 'K' Scheme Computer Engineering</b> curriculum for <b>Software Project Implementation (SPI)</b>, the project successfully resolves real-world challenges in resume tailoring, ATS optimization, web portfolio generation, and recruiter outreach.",
        body
    ))
    story.append(Paragraph(
        "By integrating React 18, Node.js, Express, Supabase PostgreSQL, Groq LPU sub-second inference, and PDFKit mathematical coordinate rendering, LaunchCV AI delivers a unified SaaS workflow that operates reliably across both cloud-connected and offline environments.",
        body
    ))

    story.append(Paragraph("8.2 Alignment with MSBTE Course Outcomes (COs) &amp; Program Outcomes (POs)", subhead))
    story.append(Paragraph("• <b>CO-1 (Requirements &amp; Analysis):</b> Formulated structured Software Requirement Specifications (SRS) and conducted comparative literature reviews.", bullet))
    story.append(Paragraph("• <b>CO-2 (System Design &amp; Modeling):</b> Designed decoupled client-server architectures, Data Flow Diagrams (DFDs), and relational/JSONB database schemas.", bullet))
    story.append(Paragraph("• <b>CO-3 (Software Implementation):</b> Mastered modern JavaScript ES6+, React component hierarchies, RESTful Express APIs, and third-party AI integrations.", bullet))
    story.append(Paragraph("• <b>CO-4 (Testing &amp; Quality Assurance):</b> Executed comprehensive unit, integration, and security test cases with 100% validation success.", bullet))

    story.append(Paragraph("8.3 Future Enhancements &amp; Scope", subhead))
    story.append(Paragraph("• <b>Multi-Language Resume Translation:</b> Automated translation of resumes and outreach pitches into major Indian and international languages.", bullet))
    story.append(Paragraph("• <b>AI Voice Mock Interviews:</b> Real-time interactive voice simulation conducting behavioral and technical interviews tailored to specific JDs.", bullet))
    story.append(Paragraph("• <b>Institutional Placement Portals:</b> Multi-tenant administrative dashboards for polytechnic colleges and universities to monitor student placement progress.", bullet))

    # ==========================================
    # PAGE 18: CHAPTER 9 - REFERENCES & BIBLIOGRAPHY
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("CHAPTER 9", chapter_h1))
    story.append(Paragraph("REFERENCES, TECHNICAL STANDARDS &amp; BIBLIOGRAPHY", chapter_h2))
    
    story.append(Paragraph("9.1 Technical References &amp; Official Documentation", subhead))
    story.append(Paragraph("1. React 18 Core Documentation &amp; Component Lifecycle: <u>https://react.dev/</u>", bullet))
    story.append(Paragraph("2. Vite Frontend Tooling &amp; HMR Build Guide: <u>https://vitejs.dev/</u>", bullet))
    story.append(Paragraph("3. Node.js Event-Driven Runtime Architecture &amp; RESTful Express: <u>https://nodejs.org/</u>", bullet))
    story.append(Paragraph("4. Groq SDK &amp; LPU High-Speed Inference Documentation: <u>https://console.groq.com/docs</u>", bullet))
    story.append(Paragraph("5. PDFKit Vector Document Coordinate Generation Engine: <u>https://pdfkit.org/docs/</u>", bullet))
    story.append(Paragraph("6. Supabase Cloud PostgreSQL &amp; Row-Level Security: <u>https://supabase.com/docs</u>", bullet))
    story.append(Paragraph("7. Nodemailer SMTP Transport Client &amp; Zoho Integration: <u>https://nodemailer.com/</u>", bullet))
    story.append(Paragraph("8. JSZip Client-Side Zip Archive Compression Library: <u>https://stuk.github.io/jszip/</u>", bullet))
    story.append(Paragraph("9. Tailwind CSS Utility-First Framework Documentation: <u>https://tailwindcss.com/docs</u>", bullet))

    story.append(Paragraph("9.2 Academic References &amp; Textbooks", subhead))
    story.append(Paragraph("10. <i>Software Engineering: A Practitioner's Approach</i> – Roger S. Pressman, McGraw-Hill Education.", bullet))
    story.append(Paragraph("11. <i>JavaScript: The Definitive Guide (7th Edition)</i> – David Flanagan, O'Reilly Media.", bullet))
    story.append(Paragraph("12. <i>Learning React: Modern Patterns for Developing React Apps</i> – Alex Banks &amp; Eve Porcello.", bullet))
    story.append(Paragraph("13. MSBTE Curriculum Guidelines for 5th Semester 'K' Scheme Computer Engineering Group (Course: Software Project Implementation / Capstone Project).", bullet))
    
    story.append(Spacer(1, 14 * pt))
    inst_box_data = [
        [Paragraph("<b>INSTITUTE DETAILS:</b><br/><b>VIVA Institute of Technology / Polytechnic</b><br/><font size=8.5 color='#4b5563'>Approved by AICTE, New Delhi &amp; DTE Maharashtra | Affiliated to MSBTE, Mumbai<br/>Shirgaon, Virar (East), Dist. Palghar, Maharashtra – 401305</font>", center_bold_11)]
    ]
    inst_box_tbl = Table(inst_box_data, colWidths=[480 * pt])
    inst_box_tbl.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOX', (0,0), (-1,-1), 1.2 * pt, colors.HexColor("#0f2b5c")),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('TOPPADDING', (0,0), (-1,-1), 8 * pt),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8 * pt),
    ]))
    story.append(inst_box_tbl)

    doc.build(story, canvasmaker=NumberedCanvas)
    print("18-Page LaunchCV AI MSBTE 5th Sem (K-Scheme) SPI Project Report PDF successfully generated.")

if __name__ == "__main__":
    generate_pdf()
