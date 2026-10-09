"""Genera un CV PDF público de hasta dos páginas sin dependencias externas."""

from pathlib import Path
import textwrap

PAGE_W, PAGE_H = 595.28, 841.89
MARGIN = 48
BOTTOM = 48
GREEN = (0.06, 0.42, 0.24)
DARK = (0.10, 0.12, 0.15)
GREY = (0.36, 0.40, 0.45)
pages = [[]]
ops = pages[0]
y = MARGIN


def new_page():
    global ops, y
    ops = []
    pages.append(ops)
    y = MARGIN


def emit(text, font="F1", size=8.7, color=DARK, gap=0):
    global y
    leading = size * 1.29
    if y + leading + gap > PAGE_H - BOTTOM:
        new_page()
    text = text.encode("cp1252", "replace").decode("cp1252")
    text = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    red, green, blue = color
    ops.append(
        f"BT /{font} {size:.1f} Tf {red:.3f} {green:.3f} {blue:.3f} rg "
        f"1 0 0 1 {MARGIN:.2f} {PAGE_H-y:.2f} Tm ({text}) Tj ET"
    )
    y += leading + gap


def paragraph(text, size=8.7, gap=3):
    width = int((PAGE_W - 2 * MARGIN) / (size * 0.50))
    for line in textwrap.wrap(text, width=width, break_long_words=False):
        emit(line, size=size)
    global y
    y += gap


def section(title):
    global y
    y += 4
    emit(title.upper(), "F2", 10, GREEN, 2)
    ops.append(
        f"0.06 0.42 0.24 RG 0.8 w {MARGIN} {PAGE_H-y+3:.2f} m "
        f"{PAGE_W-MARGIN} {PAGE_H-y+3:.2f} l S"
    )
    y += 5


def job(title, dates, detail):
    emit(f"{title} | {dates}", "F2", 9, DARK, 1)
    paragraph(detail, gap=3)


def pdf_bytes():
    objects = []

    def add(value):
        if isinstance(value, str):
            value = value.encode("cp1252", "replace")
        objects.append(value)
        return len(objects)

    regular = add(
        "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica "
        "/Encoding /WinAnsiEncoding >>"
    )
    bold = add(
        "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold "
        "/Encoding /WinAnsiEncoding >>"
    )
    content_ids = []
    for page_ops in pages:
        stream = "\n".join(page_ops).encode("cp1252", "replace")
        content_ids.append(
            add(f"<< /Length {len(stream)} >>\nstream\n".encode() + stream + b"\nendstream")
        )

    pages_id = add(b"")
    page_ids = []
    for content_id in content_ids:
        page_ids.append(
            add(
                f"<< /Type /Page /Parent {pages_id} 0 R /MediaBox [0 0 "
                f"{PAGE_W:.2f} {PAGE_H:.2f}] /Resources << /Font << "
                f"/F1 {regular} 0 R /F2 {bold} 0 R >> >> /Contents "
                f"{content_id} 0 R >>"
            )
        )
    kids = " ".join(f"{page_id} 0 R" for page_id in page_ids)
    objects[pages_id - 1] = (
        f"<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>"
    ).encode()
    catalog = add(f"<< /Type /Catalog /Pages {pages_id} 0 R >>")

    output = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for number, value in enumerate(objects, 1):
        offsets.append(len(output))
        output += f"{number} 0 obj\n".encode() + value + b"\nendobj\n"
    xref = len(output)
    output += f"xref\n0 {len(objects)+1}\n0000000000 65535 f \n".encode()
    for offset in offsets[1:]:
        output += f"{offset:010d} 00000 n \n".encode()
    output += (
        f"trailer\n<< /Size {len(objects)+1} /Root {catalog} 0 R >>\n"
        f"startxref\n{xref}\n%%EOF\n"
    ).encode()
    return output


emit("OSCAR CIMAS BRAVO", "F2", 21, DARK, 2)
emit("INGENIERO INFORMÁTICO · DESARROLLO DE SOFTWARE", "F1", 10.5, GREEN, 3)
emit("Valladolid, España · oscarcb@live.com · linkedin.com/in/oscar-cimas-bravo", "F1", 8.2, GREY, 2)
emit("github.com/J3np4y", "F1", 8.2, GREY, 2)

section("Perfil")
paragraph(
    "Ingeniero informático con cerca de 9 años de experiencia en desarrollo backend "
    "con Java y J2EE, principalmente en proyectos de la Administración Pública y "
    "telecomunicaciones. Experiencia en aplicaciones web, servicios, SQL, pruebas y "
    "mantenimiento evolutivo. Actualmente cursando un Máster de Desarrollo con IA."
)

section("Experiencia profesional")
job(
    "Programador Senior · ATK-Bilbomatica",
    "Mayo 2021 - Octubre 2026",
    "Análisis, desarrollo, mantenimiento evolutivo, pruebas y asistencia técnica de "
    "aplicaciones web de gestión para los departamentos de Alimentación, Desarrollo "
    "Rural, Agricultura y Pesca, Sanidad y Medio Ambiente. Proyectos: aplicación "
    "presupuestaria W85, Ingurunet y Estadísticas de Pesca AD44B. Stack: Java, Spring "
    "MVC, JDBC/SQL, HTML, JavaScript, jQuery, AJAX, XML, JSP/JSTL y Maven; frameworks "
    "corporativos RUP y UDA (EJIE).",
)
job(
    "Programador Senior · ATK-TEKNEI",
    "Diciembre 2020 - Mayo 2021",
    "Desarrollo, mantenimiento evolutivo y pruebas para la Administración Pública. "
    "Proyectos SAREA y Udalekuak, con frameworks ATOM y BIDE. Java/J2EE, JSF, EJB, "
    "PrimeFaces, AJAX, JavaScript, jQuery, JBoss, Oracle, SQL Server 2017, SVN y Jira.",
)
job(
    "Programador Junior · ATK-NAHITEK",
    "Octubre 2018 - Mayo 2020",
    "Desarrollo de evolutivos, mantenimiento y pruebas en equipos Java para la "
    "Administración Pública. Frameworks ATOM y BIDE; Java/J2EE, JSF, EJB, PrimeFaces, "
    "AJAX, JavaScript, jQuery, JBoss, Oracle, SQL Server 2017, SVN y Jira.",
)
job(
    "SD Analyst · Neoris España",
    "Junio 2017 - Septiembre 2018",
    "Mantenimiento evolutivo y resolución de incidencias en CRM Vodafone. Framework "
    "SMART; Java, PL/SQL, XML, WSDL, WebLogic, PVCS, Eclipse, IntelliJ IDEA, SQL "
    "Developer y SoapUI.",
)

section("Proyectos")
job(
    "Nexora · SaaS de documentación empresarial con IA",
    "Proyecto educativo en desarrollo",
    "Aplicación web para colaborar sobre documentación y obtener respuestas en "
    "lenguaje natural con citas a las fuentes. Frontend Next.js/TypeScript con proxy "
    "same-origin; API FastAPI/Python; PostgreSQL, SQLAlchemy, Alembic y pgvector; "
    "RAG con OpenAI. Incluye organizaciones y roles, sesiones revocables, gestión "
    "de documentos, búsqueda y citas. Repositorio: github.com/J3np4y/SaaS-Documentacion-IA. "
    "Prototipo educativo, no preparado para producción.",
)
job(
    "Editor y previsualizador de contenido WebGL",
    "Proyecto fin de grado · Universidad de Valladolid",
    "Editor de escritorio desarrollado en Java con navegador Chromium integrado "
    "para previsualizar páginas HTML/JavaScript y gráficos 3D WebGL.",
)

section("Formación")
paragraph(
    "Máster de Desarrollo con IA · BIG school / Universidad Isabel I · En curso",
    gap=2,
)
paragraph(
    "Grado en Ingeniería Informática, mención Ingeniería del Software · Universidad "
    "de Valladolid (2011 - 2017)",
    gap=2,
)
paragraph(
    "Técnico Superior en Desarrollo de Aplicaciones Informáticas · Colegio La Salle "
    "(2009 - 2011)",
    gap=2,
)
paragraph(
    "Cursos: Iniciación a la IA y desarrollo con IA · BIG school. Python · Mouredev, "
    "en curso.",
    gap=2,
)

section("Conocimientos e idiomas")
paragraph(
    "Lenguajes: Java, SQL, PL/SQL, JavaScript, Python (básico), TypeScript, HTML, "
    "JSP, XML y CSS. Backend: Spring MVC, JDBC, J2EE, JSF, EJB y FastAPI. Datos: "
    "Oracle, SQL Server y PostgreSQL. Herramientas: Maven, JBoss, WebLogic, Git, "
    "SVN, Jira, SonarQube, SoapUI, Eclipse, IntelliJ IDEA y Docker Compose."
)
paragraph("Español: nativo · Inglés: B1")

if len(pages) > 2:
    raise ValueError(f"El CV supera las dos páginas: {len(pages)}")

Path(__file__).with_name("CV-Oscar-Cimas-Bravo.pdf").write_bytes(pdf_bytes())
