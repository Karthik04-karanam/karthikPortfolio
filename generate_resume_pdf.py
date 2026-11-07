import os

def create_resume_pdf(output_path):
    # A4 dimensions in points: 595.28 x 841.89
    # We will build a clean, professional vector PDF with Helvetica and Helvetica-Bold
    
    stream_lines = []
    
    # Helper to add text
    def text(x, y, font, size, s, color=(0.12, 0.16, 0.23)):
        # Escaping parentheses and backslashes in PDF strings
        escaped = s.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
        stream_lines.append(f"{color[0]} {color[1]} {color[2]} rg")
        stream_lines.append("BT")
        stream_lines.append(f"/{font} {size} Tf")
        stream_lines.append(f"{x:.2f} {y:.2f} Td")
        stream_lines.append(f"({escaped}) Tj")
        stream_lines.append("ET")
        
    def line(x1, y1, x2, y2, color=(0.85, 0.90, 0.95), width=1.0):
        stream_lines.append(f"{color[0]} {color[1]} {color[2]} RG")
        stream_lines.append(f"{width} w")
        stream_lines.append(f"{x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S")

    def rect(x, y, w, h, fill_color=(0.93, 0.96, 1.0)):
        stream_lines.append(f"{fill_color[0]} {fill_color[1]} {fill_color[2]} rg")
        stream_lines.append(f"{x:.2f} {y:.2f} {w:.2f} {h:.2f} re f")

    # Header section
    curr_y = 800
    
    # Accent top border
    line(40, 815, 555, 815, color=(0.0, 0.78, 0.95), width=3.5)
    
    text(40, curr_y - 20, "F2", 18, "Karthik Venkata Jaya Karthik", color=(0.06, 0.09, 0.16))
    text(40, curr_y - 36, "F2", 10.5, "Aspiring Software Developer  |  Python  |  Web Development  |  AI", color=(0.0, 0.65, 0.85))
    
    # Contact strip
    curr_y -= 54
    text(40, curr_y, "F1", 8.5, "Location: Rajahmundry, Andhra Pradesh, India   |   Email: karanamvenkatjaykarthik@gmail.com", color=(0.28, 0.35, 0.44))
    curr_y -= 13
    text(40, curr_y, "F1", 8.5, "GitHub: github.com/Karthik04-karanam   |   LinkedIn: linkedin.com/in/venkat-jay-karthik-karanam-098800404", color=(0.28, 0.35, 0.44))
    curr_y -= 13
    text(40, curr_y, "F1", 8.5, "CodeChef: codechef.com/users/holy_care_25", color=(0.28, 0.35, 0.44))
    
    line(40, curr_y - 8, 555, curr_y - 8, color=(0.88, 0.91, 0.94), width=0.8)
    curr_y -= 22

    # Section Helper
    def draw_section_header(title, y):
        rect(40, y - 2, 4, 12, fill_color=(0.0, 0.78, 0.95))
        text(48, y, "F2", 10.5, title.upper(), color=(0.06, 0.09, 0.16))
        line(48 + len(title)*7.5, y + 4, 555, y + 4, color=(0.90, 0.92, 0.95), width=0.8)
        return y - 16

    # 1. PROFILE SUMMARY
    curr_y = draw_section_header("Profile Summary", curr_y)
    p1 = "Final-year Diploma student in Computer Science Engineering (CGPA: 9.72/10) with strong technical"
    p2 = "proficiency in full-stack Python development, REST API engineering, modern web technologies, and database"
    p3 = "architecture. Hands-on experience building practical applications including meteorological platforms, AI-powered"
    p4 = "productivity workspaces, and commercial booking systems. Disciplined problem solver eager to contribute to"
    p5 = "innovative software engineering teams."
    for p in [p1, p2, p3, p4, p5]:
        text(40, curr_y, "F1", 8.8, p, color=(0.20, 0.25, 0.33))
        curr_y -= 12.5
    curr_y -= 6

    # 2. TECHNICAL SKILLS
    curr_y = draw_section_header("Technical Skills", curr_y)
    skills = [
        ("Programming Languages:", "Python, Java, C, JavaScript (ES6+)"),
        ("Web Development:", "HTML5, CSS3, Bootstrap 5, jQuery, Responsive Web Design"),
        ("Backend & APIs:", "FastAPI, RESTful APIs, Python Architecture"),
        ("Databases:", "MySQL, Relational Database Modeling"),
        ("Libraries & Data:", "NumPy, Pandas"),
        ("Tools & Platforms:", "Git, GitHub, VS Code"),
        ("AI & Productivity Tools:", "Google Gemini, ChatGPT, GitHub Copilot"),
    ]
    for cat, val in skills:
        text(40, curr_y, "F2", 8.5, cat, color=(0.10, 0.15, 0.22))
        text(175, curr_y, "F1", 8.5, val, color=(0.28, 0.35, 0.44))
        curr_y -= 12
    curr_y -= 6

    # 3. FEATURED PROJECTS
    curr_y = draw_section_header("Featured Projects", curr_y)
    
    # Project 1: AURA AI
    text(40, curr_y, "F2", 9.5, "AURA AI - AI Productivity Workspace", color=(0.06, 0.09, 0.16))
    text(330, curr_y, "F1", 8.2, "Python, FastAPI, HTML5, CSS3, JS, AI APIs", color=(0.0, 0.65, 0.85))
    curr_y -= 12
    text(48, curr_y, "F1", 8.5, "- Engineered a unified productivity workspace combining AI chat, prompt repository, and developer tools.", color=(0.25, 0.30, 0.38))
    curr_y -= 11
    text(48, curr_y, "F1", 8.5, "- Built high-throughput backend endpoints with FastAPI, request schema validation, and asynchronous handlers.", color=(0.25, 0.30, 0.38))
    curr_y -= 11
    text(48, curr_y, "F1", 8.5, "- Designed an intuitive modern dark UI with streaming token rendering and responsive state management.", color=(0.25, 0.30, 0.38))
    curr_y -= 15

    # Project 2: Weather Application
    text(40, curr_y, "F2", 9.5, "Weather Application", color=(0.06, 0.09, 0.16))
    text(330, curr_y, "F1", 8.2, "Python, Weather API, HTML5, CSS3, JavaScript, Bootstrap", color=(0.0, 0.65, 0.85))
    curr_y -= 12
    text(48, curr_y, "F1", 8.5, "- Developed a responsive real-time weather application consuming meteorological RESTful APIs.", color=(0.25, 0.30, 0.38))
    curr_y -= 11
    text(48, curr_y, "F1", 8.5, "- Implemented live telemetry cards (temperature, humidity, wind speed) with resilient error states for invalid queries.", color=(0.25, 0.30, 0.38))
    curr_y -= 15

    # Project 3: Beauty Parlour Management
    text(40, curr_y, "F2", 9.5, "Beauty Parlour Management & Booking Website", color=(0.06, 0.09, 0.16))
    text(330, curr_y, "F1", 8.2, "HTML5, CSS3, Bootstrap 5, JavaScript, jQuery", color=(0.0, 0.65, 0.85))
    curr_y -= 12
    text(48, curr_y, "F1", 8.5, "- Created an interactive business portal featuring service catalogs, tiered pricing schedules, and client reviews.", color=(0.25, 0.30, 0.38))
    curr_y -= 11
    text(48, curr_y, "F1", 8.5, "- Implemented responsive appointment reservation workflows and dynamic modal interactions using jQuery.", color=(0.25, 0.30, 0.38))
    curr_y -= 16

    # 4. EDUCATION
    curr_y = draw_section_header("Education", curr_y)
    text(40, curr_y, "F2", 9.5, "Diploma in Computer Science Engineering (Final Year)", color=(0.06, 0.09, 0.16))
    text(480, curr_y, "F2", 9.0, "CGPA: 9.72 / 10", color=(0.0, 0.65, 0.85))
    curr_y -= 12
    text(40, curr_y, "F1", 8.5, "Aditya Polytechnic College   |   2024 - 2027", color=(0.28, 0.35, 0.44))
    curr_y -= 11
    text(40, curr_y, "F1", 8.2, "Key Coursework: Data Structures, Algorithms, Python Programming, Database Management, Web Engineering", color=(0.40, 0.45, 0.52))
    curr_y -= 15

    text(40, curr_y, "F2", 9.5, "Secondary School Certificate (SSC)", color=(0.06, 0.09, 0.16))
    text(495, curr_y, "F2", 9.0, "Score: 91.0%", color=(0.0, 0.65, 0.85))
    curr_y -= 12
    text(40, curr_y, "F1", 8.5, "Chunilal Jajoo Rotary Municipal High School   |   Passing Year: 2024", color=(0.28, 0.35, 0.44))
    curr_y -= 16

    # 5. CERTIFICATIONS
    curr_y = draw_section_header("Certifications & Credentials", curr_y)
    text(40, curr_y, "F2", 9.0, "Full Stack Python Development", color=(0.06, 0.09, 0.16))
    text(250, curr_y, "F1", 8.5, "- Anurag IT Solutions (2026)", color=(0.28, 0.35, 0.44))
    curr_y -= 12
    text(40, curr_y, "F2", 9.0, "Computer Fundamentals & Office Automation", color=(0.06, 0.09, 0.16))
    text(285, curr_y, "F1", 8.5, "- Rama Krishna Math (2025)", color=(0.28, 0.35, 0.44))
    curr_y -= 16

    # 6. COMPETITIVE CODING & ACHIEVEMENTS
    curr_y = draw_section_header("Competitive Coding & Achievements", curr_y)
    text(40, curr_y, "F1", 8.5, "- CodeChef (holy_care_25): Active participant practicing algorithmic problem solving and logic building.", color=(0.25, 0.30, 0.38))
    curr_y -= 11
    text(40, curr_y, "F1", 8.5, "- Academic Standing: Consistently ranked in top academic tier at Aditya Polytechnic College with 9.72 CGPA.", color=(0.25, 0.30, 0.38))

    # Assemble PDF stream
    content_stream = "\n".join(stream_lines).encode('latin-1')
    
    objects = []
    # 1: Catalog
    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    # 2: Pages
    objects.append(b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
    # 3: Page
    objects.append(b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595.28 841.89] /Contents 4 0 R /Resources << /Font << /F1 5 0 R /F2 6 0 R >> >> >>")
    # 4: Contents
    objects.append(b"<< /Length " + str(len(content_stream)).encode('ascii') + b" >>\nstream\n" + content_stream + b"\nendstream")
    # 5: Font Regular
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    # 6: Font Bold
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")

    pdf_bytes = bytearray(b"%PDF-1.4\n")
    xref_offsets = [0]
    
    for i, obj in enumerate(objects, 1):
        xref_offsets.append(len(pdf_bytes))
        pdf_bytes.extend(f"{i} 0 obj\n".encode('ascii'))
        pdf_bytes.extend(obj)
        pdf_bytes.extend(b"\nendobj\n")
        
    startxref = len(pdf_bytes)
    pdf_bytes.extend(f"xref\n0 {len(objects) + 1}\n".encode('ascii'))
    pdf_bytes.extend(b"0000000000 65535 f \n")
    for offset in xref_offsets[1:]:
        pdf_bytes.extend(f"{offset:010d} 00000 n \n".encode('ascii'))
        
    pdf_bytes.extend(f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{startxref}\n%%EOF\n".encode('ascii'))

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, 'wb') as f:
        f.write(pdf_bytes)
    print(f"Generated {output_path} ({len(pdf_bytes)} bytes)")

if __name__ == '__main__':
    create_resume_pdf('assets/resume.pdf')
