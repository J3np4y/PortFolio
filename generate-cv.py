"""Genera un CV PDF de una página sin dependencias externas."""

from pathlib import Path
import textwrap

PAGE_W, PAGE_H = 595.28, 841.89
MARGIN = 52
GREEN = (0.06, 0.42, 0.24)
DARK = (0.10, 0.12, 0.15)
GREY = (0.36, 0.40, 0.45)
ops = []
y = MARGIN


def emit(text, font="F1", size=9.2, color=DARK, gap=0):
    global y
    text = text.encode("cp1252", "replace").decode("cp1252")
    text = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    red, green, blue = color
    ops.append(
        f"BT /{font} {size:.1f} Tf {red:.3f} {green:.3f} {blue:.3f} rg "
        f"1 0 0 1 {MARGIN:.2f} {PAGE_H-y:.2f} Tm ({text}) Tj ET"
    )
    y += size * 1.32 + gap


def paragraph(text, size=9.2, gap=4):
    width = int((PAGE_W - 2 * MARGIN) / (size * 0.51))
    for line in textwrap.wrap(text, width=width, break_long_words=False):
        emit(line, size=size)
    global y
    y += gap


def section(title):
    global y
    y += 5
    emit(title.upper(), "F2", 10.5, GREEN, 2)
    ops.append(
        f"0.06 0.42 0.24 RG 0.8 w {MARGIN} {PAGE_H-y+3:.2f} m "
        f"{PAGE_W-MARGIN} {PAGE_H-y+3:.2f} l S"
    )
    y += 7


def job(title, dates, detail):
    emit(f"{title} | {dates}", "F2", 9.6, DARK, 1)
    paragraph(detail, gap=5)


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
    stream = "\n".join(ops).encode("cp1252", "replace")
    content = add(
        f"<< /Length {len(stream)} >>\nstream\n".encode()
        + stream
        + b"\nendstream"
    )
    page = add(b"")
    pages = add(f"<< /Type /Pages /Kids [{page} 0 R] /Count 1 >>")
    objects[page - 1] = (
        f"<< /Type /Page /Parent {pages} 0 R /MediaBox [0 0 {PAGE_W:.2f} "
        f"{PAGE_H:.2f}] /Resources << /Font << /F1 {regular} 0 R "
        f"/F2 {bold} 0 R >> >> /Contents {content} 0 R >>"
    ).encode()
    catalog = add(f"<< /Type /Catalog /Pages {pages} 0 R >>")

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
emit("Ingeniero Informático · Desarrollador Senior", "F1", 11, GREEN, 3)
emit("Valladolid, España · oscarcb@live.com · linkedin.com/in/oscar-cimas-bravo", "F1", 8.5, GREY, 2)
emit("github.com/J3np4y", "F1", 8.5, GREY, 2)

section("Perfil")
paragraph(
    "Desarrollador senior con más de 8 años de experiencia desde 2017 en sistemas "
    "empresariales, aplicaciones Java y proyectos tecnológicos para la administración "
    "pública. Experiencia en desarrollo, mantenimiento, pruebas, evolución de "
    "aplicaciones y análisis de incidencias con equipos técnicos y funcionales."
)

section("Experiencia profesional")
job(
    "Programador Senior · ATK-TEKNEI",
    "2020 - Actualidad",
    "Desarrollo, mantenimiento, pruebas y evolución de aplicaciones empresariales "
    "para la administración pública. Trabajo diario con Java, J2EE, JSF, EJB y "
    "PrimeFaces sobre JBoss. Tecnologías: Java 1.7 / 1.8, Oracle, SonarQube, Jira.",
)
job(
    "Programador Senior · ATK-NAHITEK",
    "2018 - 2020",
    "Desarrollo de aplicaciones y evolutivos para la administración pública, con "
    "foco en calidad, mantenimiento y entrega coordinada. Tecnologías: JSF / EJB, "
    "AJAX, SQL Server, Confluence.",
)
job(
    "SD Analyst · Neoris España",
    "2017 - 2018",
    "Desarrollo de evolutivos y resolución de incidencias en proyectos de "
    "telecomunicaciones. Tecnologías: Java, PL/SQL, WebLogic, WSDL.",
)
job(
    "Becario programador · Iberdrola, Valladolid",
    "2011",
    "Consultas en bases de datos, creación de vistas e informes.",
)

section("Proyectos destacados")
job(
    "Buscaminas · Java, TeaVM, HTML / JavaScript",
    "Proyecto personal",
    "Lógica separada en modelo, controlador y API web; compilada a JavaScript para "
    "publicación estática. 12 pruebas JUnit y tres niveles de dificultad.",
)
job(
    "Editor y previsualizador de escenas WebGL",
    "TFG · Universidad de Valladolid",
    "Proyecto académico descrito como herramienta de apoyo para la asignatura de "
    "Programación de aplicaciones gráficas.",
)

section("Formación")
paragraph(
    "Ingeniería Informática, mención en Ingeniería de Software · Universidad de "
    "Valladolid (2011 - 2017)",
    gap=2,
)
paragraph(
    "Desarrollo de Aplicaciones, CFGS · Colegio La Salle (2009 - 2011)",
    gap=2,
)
paragraph("Spring Boot · Formación especializada en desarrollo web", gap=2)

section("Conocimientos técnicos")
paragraph(
    "Lenguajes: Java, JavaScript, SQL, PL/SQL, HTML / CSS. Frameworks y tecnologías: "
    "J2EE, JSF, EJB, PrimeFaces, AJAX, Spring Boot, WebGL, TeaVM. Datos e "
    "infraestructura: Oracle, SQL Server, JBoss, WebLogic, Linux. Herramientas: "
    "Git, Maven, SonarQube, Jira, Confluence."
)

if y > PAGE_H - 45:
    raise ValueError(f"El contenido excede una página: {y:.1f}/{PAGE_H:.1f}")

Path(__file__).with_name("CV-Oscar-Cimas-Bravo.pdf").write_bytes(pdf_bytes())
