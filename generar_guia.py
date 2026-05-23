from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.platypus.flowables import Flowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── Colores ──────────────────────────────────────────────────────────────────
DARK_BG    = colors.HexColor("#1e1e2e")   # fondo encabezados
ACCENT     = colors.HexColor("#89b4fa")   # azul suave (acento)
CODE_BG    = colors.HexColor("#1a1a2e")   # fondo bloques de código
CODE_FG    = colors.HexColor("#cdd6f4")   # texto código
STEP_BG    = colors.HexColor("#313244")   # fondo número de paso
TEXT_DARK  = colors.HexColor("#11111b")
WHITE      = colors.white
LIGHT_GRAY = colors.HexColor("#f5f5f5")
BORDER     = colors.HexColor("#cba6f7")   # morado suave para bordes
GREEN      = colors.HexColor("#a6e3a1")
YELLOW     = colors.HexColor("#f9e2af")
RED        = colors.HexColor("#f38ba8")

OUTPUT = "Guia_NestJS_Backend.pdf"

# ── Documento ────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=letter,
    rightMargin=0.75*inch, leftMargin=0.75*inch,
    topMargin=0.75*inch,   bottomMargin=0.75*inch,
    title="Guia NestJS Backend",
    author="OCSO Project"
)

styles = getSampleStyleSheet()

# ── Estilos personalizados ───────────────────────────────────────────────────
def make_style(name, **kwargs):
    return ParagraphStyle(name, **kwargs)

S = {
    "cover_title": make_style("cover_title",
        fontSize=34, textColor=WHITE, alignment=TA_CENTER,
        leading=42, fontName="Helvetica-Bold"),

    "cover_sub": make_style("cover_sub",
        fontSize=14, textColor=ACCENT, alignment=TA_CENTER,
        leading=20, fontName="Helvetica"),

    "cover_note": make_style("cover_note",
        fontSize=10, textColor=colors.HexColor("#a6adc8"),
        alignment=TA_CENTER, leading=14, fontName="Helvetica"),

    "h1": make_style("h1",
        fontSize=20, textColor=WHITE, leading=26,
        fontName="Helvetica-Bold", spaceBefore=8, spaceAfter=6),

    "h2": make_style("h2",
        fontSize=14, textColor=ACCENT, leading=20,
        fontName="Helvetica-Bold", spaceBefore=10, spaceAfter=4),

    "h3": make_style("h3",
        fontSize=11, textColor=colors.HexColor("#cba6f7"), leading=16,
        fontName="Helvetica-Bold", spaceBefore=8, spaceAfter=3),

    "body": make_style("body",
        fontSize=10, textColor=TEXT_DARK, leading=15,
        fontName="Helvetica", alignment=TA_JUSTIFY,
        spaceBefore=3, spaceAfter=3),

    "bullet": make_style("bullet",
        fontSize=10, textColor=TEXT_DARK, leading=15,
        fontName="Helvetica", leftIndent=16,
        spaceBefore=2, spaceAfter=2),

    "code": make_style("code",
        fontSize=8.5, textColor=CODE_FG, leading=13,
        fontName="Courier", leftIndent=8, rightIndent=8,
        spaceBefore=2, spaceAfter=2),

    "code_label": make_style("code_label",
        fontSize=8, textColor=ACCENT, leading=12,
        fontName="Courier-Bold", leftIndent=8),

    "step_text": make_style("step_text",
        fontSize=13, textColor=WHITE, leading=18,
        fontName="Helvetica-Bold"),

    "step_desc": make_style("step_desc",
        fontSize=10, textColor=TEXT_DARK, leading=15,
        fontName="Helvetica", spaceBefore=2),

    "tip": make_style("tip",
        fontSize=9.5, textColor=TEXT_DARK, leading=14,
        fontName="Helvetica", leftIndent=8),

    "toc_item": make_style("toc_item",
        fontSize=11, textColor=TEXT_DARK, leading=18,
        fontName="Helvetica"),

    "toc_num": make_style("toc_num",
        fontSize=11, textColor=ACCENT, leading=18,
        fontName="Helvetica-Bold"),
}

# ── Helpers ──────────────────────────────────────────────────────────────────
def section_header(num, title, subtitle=""):
    """Encabezado de sección con fondo oscuro."""
    inner = []
    inner.append(Paragraph(f"0{num}  {title}", S["h1"]))
    if subtitle:
        inner.append(Paragraph(subtitle, S["cover_sub"]))

    data = [[inner]]
    t = Table(data, colWidths=[6.9*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), DARK_BG),
        ("ROUNDEDCORNERS", [6]),
        ("TOPPADDING",    (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("LEFTPADDING",   (0,0), (-1,-1), 16),
        ("RIGHTPADDING",  (0,0), (-1,-1), 16),
    ]))
    return t

def code_block(label, code_lines):
    """Bloque de código con etiqueta y fondo oscuro."""
    items = []
    if label:
        items.append(Paragraph(f"▸ {label}", S["code_label"]))
    for line in code_lines:
        safe = (line
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;"))
        items.append(Paragraph(safe, S["code"]))

    data = [[items]]
    t = Table(data, colWidths=[6.9*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), CODE_BG),
        ("ROUNDEDCORNERS", [4]),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("RIGHTPADDING",  (0,0), (-1,-1), 6),
    ]))
    return t

def info_box(text, color=LIGHT_GRAY, border_color=ACCENT):
    data = [[Paragraph(text, S["tip"])]]
    t = Table(data, colWidths=[6.9*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,-1), color),
        ("LEFTBORDER",  (0,0), (0,-1), 4, border_color),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 12),
        ("RIGHTPADDING",  (0,0), (-1,-1), 12),
        ("LINEAFTER",  (0,0), (0,-1), 0, border_color),
        ("LINEBEFORE", (0,0), (0,-1), 3, border_color),
    ]))
    return t

def step_box(num, title, description):
    """Caja de paso numerado."""
    num_cell  = [Paragraph(str(num), S["step_text"])]
    text_cell = [
        Paragraph(title, S["h2"]),
        Paragraph(description, S["step_desc"]),
    ]
    data = [[num_cell, text_cell]]
    t = Table(data, colWidths=[0.55*inch, 6.3*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (0,-1), STEP_BG),
        ("BACKGROUND",    (1,0), (-1,-1), colors.HexColor("#eff1f5")),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("ALIGN",         (0,0), (0,-1), "CENTER"),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (0,-1), 6),
        ("RIGHTPADDING",  (1,0), (-1,-1), 12),
        ("LEFTPADDING",   (1,0), (-1,-1), 12),
        ("ROUNDEDCORNERS", [5]),
    ]))
    return t

def mini_table(headers, rows, col_widths=None):
    """Tabla simple de referencia."""
    if col_widths is None:
        w = 6.9*inch / len(headers)
        col_widths = [w]*len(headers)

    data = [headers] + rows
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), DARK_BG),
        ("TEXTCOLOR",     (0,0), (-1,0), ACCENT),
        ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 9),
        ("FONTNAME",      (0,1), (-1,-1), "Helvetica"),
        ("TEXTCOLOR",     (0,1), (-1,-1), TEXT_DARK),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, LIGHT_GRAY]),
        ("GRID",          (0,0), (-1,-1), 0.4, colors.HexColor("#cdd6f4")),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("RIGHTPADDING",  (0,0), (-1,-1), 8),
        ("ALIGN",         (0,0), (-1,-1), "LEFT"),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))
    return t

def sp(n=6):
    return Spacer(1, n)

def hr():
    return HRFlowable(width="100%", thickness=0.5,
                      color=colors.HexColor("#45475a"), spaceAfter=6, spaceBefore=6)

# ════════════════════════════════════════════════════════════════════════════
# CONTENIDO
# ════════════════════════════════════════════════════════════════════════════
story = []

# ── PORTADA ──────────────────────────────────────────────────────────────────
cover_data = [[
    Paragraph("GUÍA DE DESARROLLO", S["cover_note"]),
    Spacer(1, 10),
    Paragraph("NestJS Backend", S["cover_title"]),
    Spacer(1, 8),
    Paragraph("TypeScript · TypeORM · PostgreSQL · JWT · Swagger", S["cover_sub"]),
    Spacer(1, 30),
    HRFlowable(width="60%", thickness=1, color=ACCENT, hAlign="CENTER"),
    Spacer(1, 20),
    Paragraph(
        "Guía paso a paso basada en el proyecto OCSO.<br/>"
        "Cubre cada tecnología en el orden exacto en que se aplica<br/>"
        "al construir una API REST profesional desde cero.",
        S["cover_note"]),
    Spacer(1, 40),
    Paragraph("Stack utilizado en este proyecto", S["cover_note"]),
    Spacer(1, 10),
]]
cover_table = Table([[cover_data]], colWidths=[7.5*inch])
cover_table.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,-1), DARK_BG),
    ("TOPPADDING",    (0,0), (-1,-1), 80),
    ("BOTTOMPADDING", (0,0), (-1,-1), 40),
    ("LEFTPADDING",   (0,0), (-1,-1), 40),
    ("RIGHTPADDING",  (0,0), (-1,-1), 40),
    ("ALIGN",         (0,0), (-1,-1), "CENTER"),
    ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
]))
story.append(cover_table)

# Stack badges en portada
badge_items = [
    ["TypeScript", "Lenguaje base"],
    ["NestJS",     "Framework"],
    ["TypeORM",    "ORM"],
    ["PostgreSQL", "Base de datos"],
    ["JWT",        "Autenticación"],
    ["bcrypt",     "Seguridad"],
    ["Swagger",    "Documentación"],
    ["Multer",     "Archivos"],
]
badge_rows = []
row = []
for i, (name, desc) in enumerate(badge_items):
    cell = [
        Paragraph(f"<b>{name}</b>", make_style(f"b{i}",
            fontSize=9, textColor=ACCENT, fontName="Helvetica-Bold",
            alignment=TA_CENTER, leading=13)),
        Paragraph(desc, make_style(f"d{i}",
            fontSize=7.5, textColor=colors.HexColor("#a6adc8"),
            fontName="Helvetica", alignment=TA_CENTER, leading=11)),
    ]
    row.append(cell)
    if len(row) == 4:
        badge_rows.append(row)
        row = []
if row:
    while len(row) < 4:
        row.append([""])
    badge_rows.append(row)

badge_table = Table(badge_rows, colWidths=[1.87*inch]*4)
badge_table.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,-1), colors.HexColor("#313244")),
    ("TOPPADDING",    (0,0), (-1,-1), 8),
    ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    ("LEFTPADDING",   (0,0), (-1,-1), 4),
    ("RIGHTPADDING",  (0,0), (-1,-1), 4),
    ("GRID",          (0,0), (-1,-1), 0.3, colors.HexColor("#45475a")),
    ("ALIGN",         (0,0), (-1,-1), "CENTER"),
    ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
]))

badge_wrapper = Table([[badge_table]], colWidths=[7.5*inch])
badge_wrapper.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,-1), DARK_BG),
    ("BOTTOMPADDING", (0,0), (-1,-1), 60),
    ("TOPPADDING",    (0,0), (-1,-1), 0),
    ("LEFTPADDING",   (0,0), (-1,-1), 10),
    ("RIGHTPADDING",  (0,0), (-1,-1), 10),
    ("ALIGN",         (0,0), (-1,-1), "CENTER"),
]))
story.append(badge_wrapper)
story.append(PageBreak())

# ── ÍNDICE ───────────────────────────────────────────────────────────────────
story.append(section_header("", "Índice de Contenidos"))
story.append(sp(12))

toc = [
    ("01", "TypeScript — Fundamentos base"),
    ("02", "NestJS — Arquitectura y estructura"),
    ("03", "TypeORM — Base de datos con PostgreSQL"),
    ("04", "@nestjs/config — Variables de entorno"),
    ("05", "class-validator — Validación de DTOs"),
    ("06", "bcrypt — Hasheo de contraseñas"),
    ("07", "JWT — Autenticación con tokens"),
    ("08", "Guards — Protección de rutas"),
    ("09", "Decoradores personalizados"),
    ("10", "Pipes — Transformación de parámetros"),
    ("11", "Swagger — Documentación automática"),
    ("12", "Multer — Carga de archivos"),
    ("  ", "Orden paso a paso para nuevos proyectos"),
]
toc_data = []
for num, title in toc:
    toc_data.append([
        Paragraph(num, S["toc_num"]),
        Paragraph(title, S["toc_item"]),
    ])

toc_table = Table(toc_data, colWidths=[0.5*inch, 6.4*inch])
toc_table.setStyle(TableStyle([
    ("ROWBACKGROUNDS", (0,0), (-1,-1), [WHITE, LIGHT_GRAY]),
    ("TOPPADDING",    (0,0), (-1,-1), 7),
    ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ("LEFTPADDING",   (0,0), (-1,-1), 10),
    ("RIGHTPADDING",  (0,0), (-1,-1), 10),
    ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ("LINEABOVE",     (0,0), (-1,0), 1, ACCENT),
    ("LINEBELOW",     (0,-1), (-1,-1), 1, ACCENT),
]))
story.append(toc_table)
story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 01 — TypeScript
# ════════════════════════════════════════════════════════════════════════════
story.append(section_header(1, "TypeScript", "El lenguaje base del proyecto"))
story.append(sp(10))

story.append(Paragraph("¿Qué es?", S["h2"]))
story.append(Paragraph(
    "TypeScript es un superset de JavaScript que agrega tipado estático. "
    "Todo el código de NestJS se escribe en TypeScript. Antes de ejecutarse, "
    "se compila a JavaScript plano.", S["body"]))
story.append(sp(8))

story.append(Paragraph("Conceptos clave usados en este proyecto", S["h2"]))
story.append(sp(4))

ts_table = mini_table(
    ["Concepto", "Para qué sirve", "Dónde aparece en el proyecto"],
    [
        ["enum", "Define un conjunto de valores con nombre", "ROLES (Admin, Manager, Employee)"],
        ["class", "Estructura base de entidades y DTOs", "Employee, User, CreateEmployeeDto"],
        ["interface", "Define la forma de un objeto", "Tipos de retorno y parámetros"],
        ["declare", "Re-declara propiedad heredada", "DTOs que extienden la entidad"],
        ["async/await", "Maneja operaciones asíncronas", "Todos los métodos de servicio"],
        ["generics T", "Tipos reutilizables (Repository&lt;T&gt;)", "Repository&lt;Employee&gt;, Repository&lt;User&gt;"],
    ],
    [1.5*inch, 2.5*inch, 2.9*inch]
)
story.append(ts_table)
story.append(sp(10))

story.append(Paragraph("Ejemplo: enum de roles", S["h3"]))
story.append(code_block("src/auth/constants/roles.constants.ts", [
    "export enum ROLES {",
    "    ADMIN    = 'Admin',",
    "    MANAGER  = 'Manager',",
    "    EMPLOYEE = 'Employee'",
    "}",
]))
story.append(sp(8))

story.append(Paragraph("Ejemplo: declare en un DTO", S["h3"]))
story.append(Paragraph(
    "Los DTOs extienden la entidad para heredar sus propiedades, "
    "pero usan <b>declare</b> para re-tiparlo con validaciones sin crear "
    "una nueva propiedad en memoria:", S["body"]))
story.append(sp(4))
story.append(code_block("src/employees/dto/create-employee.dto.ts", [
    "export class CreateEmployeeDto extends Employee {",
    "    @IsString()",
    "    @MaxLength(30)",
    "    declare employeeName: string;  // 'declare' = solo tipo, sin nueva propiedad",
    "",
    "    @IsEmail()",
    "    declare employeeEmail: string;",
    "}",
]))
story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 02 — NestJS
# ════════════════════════════════════════════════════════════════════════════
story.append(section_header(2, "NestJS", "Framework principal — Módulos, Controladores y Servicios"))
story.append(sp(10))

story.append(Paragraph("¿Qué es?", S["h2"]))
story.append(Paragraph(
    "NestJS es un framework de Node.js construido sobre Express. Organiza el código "
    "en <b>módulos</b>, siguiendo el patrón MVC adaptado a APIs. Usa decoradores de "
    "TypeScript para declarar rutas, inyectar dependencias y configurar comportamientos.", S["body"]))
story.append(sp(8))

story.append(Paragraph("El patrón fundamental: Module → Controller → Service", S["h2"]))
story.append(sp(4))

flow_data = [
    [Paragraph("Request HTTP", make_style("fc", fontSize=9, textColor=WHITE,
               fontName="Helvetica-Bold", alignment=TA_CENTER, leading=13))],
    [Paragraph("▼", make_style("ar", fontSize=14, textColor=ACCENT,
               fontName="Helvetica-Bold", alignment=TA_CENTER, leading=16))],
    [Paragraph("Controller\nRecibe la request, extrae @Body, @Param, @Query",
               make_style("fc2", fontSize=9, textColor=TEXT_DARK,
               fontName="Helvetica", alignment=TA_CENTER, leading=13))],
    [Paragraph("▼", make_style("ar2", fontSize=14, textColor=ACCENT,
               fontName="Helvetica-Bold", alignment=TA_CENTER, leading=16))],
    [Paragraph("Service\nContiene la lógica de negocio",
               make_style("fc3", fontSize=9, textColor=TEXT_DARK,
               fontName="Helvetica", alignment=TA_CENTER, leading=13))],
    [Paragraph("▼", make_style("ar3", fontSize=14, textColor=ACCENT,
               fontName="Helvetica-Bold", alignment=TA_CENTER, leading=16))],
    [Paragraph("Repository (TypeORM)\nHabla con la base de datos",
               make_style("fc4", fontSize=9, textColor=TEXT_DARK,
               fontName="Helvetica", alignment=TA_CENTER, leading=13))],
]
flow_table = Table(flow_data, colWidths=[6.9*inch])
flow_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (0,0), DARK_BG),
    ("BACKGROUND", (0,2), (0,2), colors.HexColor("#dce0f0")),
    ("BACKGROUND", (0,4), (0,4), colors.HexColor("#dce0f0")),
    ("BACKGROUND", (0,6), (0,6), colors.HexColor("#dce0f0")),
    ("ALIGN",      (0,0), (-1,-1), "CENTER"),
    ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING",    (0,0), (-1,-1), 8),
    ("BOTTOMPADDING", (0,0), (-1,-1), 8),
]))
story.append(flow_table)
story.append(sp(10))

story.append(Paragraph("Decoradores del Controller", S["h2"]))
story.append(mini_table(
    ["Decorador", "Nivel", "Para qué"],
    [
        ["@Controller('ruta')", "Clase", "Define el prefijo de todas las rutas del controlador"],
        ["@Get()", "@Post()", "Método", "Define el verbo HTTP y la sub-ruta"],
        ["@Body()", "Parámetro", "Extrae el cuerpo JSON del request"],
        ["@Param('nombre')", "Parámetro", "Extrae un segmento de la URL  /ruta/:id"],
        ["@Query('nombre')", "Parámetro", "Extrae un query param  /ruta?pagina=1"],
        ["@UploadedFile()", "Parámetro", "Extrae el archivo subido (con Multer)"],
    ],
    [2.2*inch, 1.2*inch, 3.5*inch]
))
story.append(sp(10))

story.append(Paragraph("Ejemplo completo de un módulo", S["h3"]))
story.append(code_block("src/employees/employees.module.ts", [
    "import { Module } from '@nestjs/common';",
    "import { TypeOrmModule } from '@nestjs/typeorm';",
    "import { EmployeesService }    from './employees.service';",
    "import { EmployeesController } from './employees.controller';",
    "import { Employee }            from './entities/employee.entity';",
    "",
    "@Module({",
    "  imports:     [TypeOrmModule.forFeature([Employee])], // registra la entidad",
    "  controllers: [EmployeesController],",
    "  providers:   [EmployeesService],",
    "})",
    "export class EmployeesModule {}",
]))
story.append(sp(8))

story.append(Paragraph("Ejemplo de Controller con rutas", S["h3"]))
story.append(code_block("src/employees/employees.controller.ts (simplificado)", [
    "@Controller('employees')",
    "export class EmployeesController {",
    "  constructor(private readonly employeesService: EmployeesService) {}",
    "",
    "  @Post()                                      // POST /employees",
    "  create(@Body() dto: CreateEmployeeDto) {",
    "    return this.employeesService.create(dto);",
    "  }",
    "",
    "  @Get()                                       // GET /employees",
    "  findAll() {",
    "    return this.employeesService.findAll();",
    "  }",
    "",
    "  @Get(':id')                                  // GET /employees/:id",
    "  findOne(@Param('id') id: string) {",
    "    return this.employeesService.findOne(id);",
    "  }",
    "",
    "  @Patch(':id')                                // PATCH /employees/:id",
    "  update(@Param('id') id: string, @Body() dto: UpdateEmployeeDto) {",
    "    return this.employeesService.update(id, dto);",
    "  }",
    "",
    "  @Delete(':id')                               // DELETE /employees/:id",
    "  remove(@Param('id') id: string) {",
    "    return this.employeesService.remove(id);",
    "  }",
    "}",
]))
story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 03 — TypeORM
# ════════════════════════════════════════════════════════════════════════════
story.append(section_header(3, "TypeORM", "Mapeo de objetos a tablas de PostgreSQL"))
story.append(sp(10))

story.append(Paragraph("¿Qué es?", S["h2"]))
story.append(Paragraph(
    "TypeORM es un ORM (Object-Relational Mapper) que permite definir las tablas "
    "de la base de datos como clases TypeScript, y hacer operaciones CRUD sin "
    "escribir SQL directamente.", S["body"]))
story.append(sp(8))

story.append(Paragraph("3.1  Configuración global en AppModule", S["h2"]))
story.append(code_block("src/app.module.ts", [
    "TypeOrmModule.forRoot({",
    "  type:            'postgres',",
    "  host:            process.env.host,",
    "  port:            +(process.env.port || '5432'),",
    "  username:        'postgres',",
    "  password:        process.env.pass,",
    "  database:        process.env.name,",
    "  autoLoadEntities: true,   // carga entidades registradas con forFeature()",
    "  synchronize:      true,   // crea/modifica tablas automáticamente (solo dev)",
    "})",
]))
story.append(sp(4))
story.append(info_box(
    "⚠  synchronize: true es solo para desarrollo. En producción debe ser false "
    "y se usan migraciones para no perder datos.",
    color=colors.HexColor("#fff9e6"), border_color=YELLOW))
story.append(sp(10))

story.append(Paragraph("3.2  Decoradores de columnas más usados", S["h2"]))
story.append(mini_table(
    ["Decorador", "Para qué"],
    [
        ["@Entity()", "Marca la clase como tabla en la BD"],
        ["@PrimaryGeneratedColumn('uuid')", "ID único auto-generado tipo UUID"],
        ["@PrimaryGeneratedColumn('increment')", "ID numérico auto-incremental (1, 2, 3...)"],
        ["@Column('text')", "Columna de texto"],
        ["@Column('float')", "Columna numérica decimal"],
        ["@Column('simple-array')", "Guarda un array como texto separado por comas"],
        ["@Column({ unique: true })", "Valor único, no puede repetirse"],
        ["@Column({ nullable: true })", "La columna puede estar vacía (null)"],
        ["@Column({ default: 'valor' })", "Valor por defecto si no se envía"],
    ],
    [3.2*inch, 3.7*inch]
))
story.append(sp(10))

story.append(Paragraph("3.3  Relaciones entre entidades", S["h2"]))
story.append(Paragraph(
    "Las relaciones definen cómo se conectan las tablas entre sí. "
    "Siempre se declaran en ambas entidades y el lado que tiene "
    "<b>@JoinColumn</b> es el que guarda la clave foránea (FK).", S["body"]))
story.append(sp(6))

story.append(mini_table(
    ["Decorador", "Relación", "Ejemplo en el proyecto"],
    [
        ["@OneToOne", "1 registro ↔ 1 registro", "User ↔ Manager, User ↔ Employee"],
        ["@ManyToOne", "Muchos registros → 1 registro", "Employee → Location (muchos employees en una location)"],
        ["@OneToMany", "1 registro → Muchos registros", "Location → Employee[] (una location tiene muchos employees)"],
        ["@JoinColumn", "Define cuál lado tiene la FK", "Va en el lado 'dueño' de la relación"],
    ],
    [1.6*inch, 2.1*inch, 3.2*inch]
))
story.append(sp(8))

story.append(Paragraph("Ejemplo de relaciones en la entidad Employee", S["h3"]))
story.append(code_block("src/employees/entities/employee.entity.ts", [
    "@Entity()",
    "export class Employee {",
    "    @PrimaryGeneratedColumn('uuid')",
    "    employeeId: string;",
    "",
    "    @Column('text')",
    "    employeeName: string;",
    "",
    "    @Column({ type: 'text', nullable: true })",
    "    employeePhoto: string;",
    "",
    "    // Muchos employees pertenecen a una Location",
    "    @ManyToOne(() =&gt; Location, (location) =&gt; location.employees)",
    "    @JoinColumn({ name: 'locationId' })  // FK en esta tabla",
    "    location: Location;",
    "",
    "    // Un employee tiene un User (login)",
    "    @OneToOne(() =&gt; User)",
    "    @JoinColumn({ name: 'userId' })",
    "    user: User;",
    "}",
]))
story.append(sp(10))

story.append(Paragraph("3.4  Métodos del Repository", S["h2"]))
story.append(mini_table(
    ["Método", "Para qué", "Retorna"],
    [
        [".find()", "Trae todos los registros", "Entity[]"],
        [".findOne({ where: {...} })", "Busca uno por condición", "Entity | null"],
        [".findOneBy({ campo: valor })", "Busca por campo directo", "Entity | null"],
        [".findBy({ campo: valor })", "Trae varios por campo", "Entity[]"],
        [".create(dto)", "Crea instancia en memoria (sin guardar)", "Entity"],
        [".save(entidad)", "Guarda o actualiza en la BD", "Entity"],
        [".preload({ id, ...datos })", "Carga registro + mezcla nuevos datos (para update)", "Entity | undefined"],
        [".delete({ campo: valor })", "Elimina por campo", "DeleteResult"],
    ],
    [2.5*inch, 2.6*inch, 1.8*inch]
))
story.append(sp(8))

story.append(Paragraph("Ejemplo: Service con operaciones CRUD", S["h3"]))
story.append(code_block("src/employees/employees.service.ts", [
    "@Injectable()",
    "export class EmployeesService {",
    "  constructor(",
    "    @InjectRepository(Employee)",
    "    private employeeRepository: Repository&lt;Employee&gt;",
    "  ) {}",
    "",
    "  async create(dto: CreateEmployeeDto) {",
    "    const employee = this.employeeRepository.create(dto); // instancia en memoria",
    "    return await this.employeeRepository.save(employee);  // guarda en BD",
    "  }",
    "",
    "  findAll() {",
    "    return this.employeeRepository.find();",
    "  }",
    "",
    "  async update(id: string, dto: UpdateEmployeeDto) {",
    "    const employee = await this.employeeRepository.preload({ employeeId: id, ...dto });",
    "    if (!employee) throw new NotFoundException();",
    "    return this.employeeRepository.save(employee);",
    "  }",
    "",
    "  remove(id: string) {",
    "    this.employeeRepository.delete({ employeeId: id });",
    "    return { message: 'employee deleted' };",
    "  }",
    "}",
]))
story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 04 — Config
# ════════════════════════════════════════════════════════════════════════════
story.append(section_header(4, "@nestjs/config", "Variables de entorno con archivo .env"))
story.append(sp(10))

story.append(Paragraph("¿Qué es?", S["h2"]))
story.append(Paragraph(
    "Permite leer un archivo <b>.env</b> y exponer sus valores como "
    "<b>process.env.VARIABLE</b>. Así los datos sensibles (contraseñas, "
    "claves, URLs) no se escriben directamente en el código.", S["body"]))
story.append(sp(8))

story.append(Paragraph("Configuración (solo una vez en AppModule)", S["h2"]))
story.append(code_block("src/app.module.ts", [
    "import { ConfigModule } from '@nestjs/config';",
    "",
    "@Module({",
    "  imports: [",
    "    ConfigModule.forRoot(),  // lee el archivo .env automáticamente",
    "    // ... resto de módulos",
    "  ],",
    "})",
    "export class AppModule {}",
]))
story.append(sp(8))

story.append(Paragraph("Archivo .env", S["h2"]))
story.append(code_block(".env (en la raíz del proyecto, NO se sube al repositorio)", [
    "host=localhost",
    "port=5432",
    "pass=mi_password_segura",
    "name=ocso_db",
]))
story.append(sp(8))

story.append(Paragraph("Uso en cualquier parte del código", S["h2"]))
story.append(code_block("src/app.module.ts", [
    "TypeOrmModule.forRoot({",
    "  host:     process.env.host,",
    "  port:     +(process.env.port || '5432'),",
    "  password: process.env.pass,",
    "  database: process.env.name,",
    "})",
]))
story.append(sp(6))
story.append(info_box(
    "Regla de oro: nunca hardcodear contraseñas o claves en el código. "
    "Siempre usar variables de entorno. Agrega .env al archivo .gitignore "
    "para que no se suba al repositorio.",
    color=colors.HexColor("#e8f5e9"), border_color=GREEN))
story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 05 — class-validator
# ════════════════════════════════════════════════════════════════════════════
story.append(section_header(5, "class-validator + class-transformer", "Validación automática de datos entrantes"))
story.append(sp(10))

story.append(Paragraph("¿Qué es?", S["h2"]))
story.append(Paragraph(
    "class-validator verifica que los datos que llegan en el @Body() cumplan "
    "con las reglas definidas en el DTO. Si algo no cumple, NestJS "
    "responde automáticamente con un error 400 Bad Request.", S["body"]))
story.append(sp(8))

story.append(Paragraph("Activación global en main.ts", S["h2"]))
story.append(code_block("src/main.ts", [
    "app.useGlobalPipes(new ValidationPipe({",
    "    whitelist:           true,   // ignora campos no declarados en el DTO",
    "    forbidNonWhitelisted: true,  // error 400 si llegan campos extra",
    "    transform:           true,   // convierte tipos automáticamente (string -&gt; number)",
    "}))",
]))
story.append(sp(10))

story.append(Paragraph("Decoradores de validación más usados", S["h2"]))
story.append(mini_table(
    ["Decorador", "Valida que..."],
    [
        ["@IsString()", "El valor sea una cadena de texto"],
        ["@IsEmail()", "El valor tenga formato de correo electrónico"],
        ["@IsNumber()", "El valor sea un número"],
        ["@IsBoolean()", "El valor sea true o false"],
        ["@MinLength(n)", "El texto tenga al menos n caracteres"],
        ["@MaxLength(n)", "El texto tenga máximo n caracteres"],
        ["@IsOptional()", "El campo puede no venir en el request"],
        ["@IsIn(['a','b'])", "El valor sea uno de los permitidos"],
        ["@IsObject()", "El valor sea un objeto"],
        ["@IsArray()", "El valor sea un array"],
    ],
    [2.5*inch, 4.4*inch]
))
story.append(sp(10))

story.append(Paragraph("Ejemplo: DTO del usuario", S["h3"]))
story.append(code_block("src/auth/dto/create-user.dto.ts", [
    "import { IsEmail, IsIn, IsOptional, IsString, MinLength } from 'class-validator';",
    "",
    "export class CreateUserDto extends User {",
    "    @IsEmail()",
    "    declare userEmail: string;",
    "",
    "    @IsString()",
    "    @MinLength(8)                    // mínimo 8 caracteres",
    "    declare userPassword: string;",
    "",
    "    @IsOptional()                    // si no viene, toma el default de la entidad",
    "    @IsIn(['Admin', 'Employee', 'Manager'])  // solo estos valores son válidos",
    "    declare userRoles: string[];",
    "}",
]))
story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 06 — bcrypt
# ════════════════════════════════════════════════════════════════════════════
story.append(section_header(6, "bcrypt", "Hasheo seguro de contraseñas"))
story.append(sp(10))

story.append(Paragraph("¿Qué es?", S["h2"]))
story.append(Paragraph(
    "bcrypt convierte una contraseña en texto plano a un hash irreversible. "
    "Aunque alguien robe la base de datos, no podrá obtener la contraseña original. "
    "Para verificar si una contraseña es correcta, se compara con el hash guardado.", S["body"]))
story.append(sp(8))

story.append(Paragraph("Las dos operaciones esenciales", S["h2"]))
story.append(code_block("src/auth/auth.service.ts", [
    "import * as bcrypt from 'bcrypt';",
    "",
    "// Al REGISTRAR un usuario: hashear la contraseña antes de guardar",
    "registerUser(createUserDto: CreateUserDto) {",
    "    createUserDto.userPassword = bcrypt.hashSync(",
    "        createUserDto.userPassword,",
    "        5  // salt rounds: cuántas veces se aplica el algoritmo (más = más seguro)",
    "    );",
    "    return this.userRepository.save(createUserDto);",
    "}",
    "",
    "// Al HACER LOGIN: comparar contraseña ingresada con el hash guardado",
    "async loginUser(loginUserDto: LoginUserDto) {",
    "    const user = await this.userRepository.findOne({",
    "        where: { userEmail: loginUserDto.userEmail }",
    "    });",
    "    if (!user) throw new UnauthorizedException('Credenciales incorrectas');",
    "",
    "    const match = await bcrypt.compare(",
    "        loginUserDto.userPassword,  // texto plano ingresado",
    "        user.userPassword           // hash guardado en BD",
    "    );",
    "    if (!match) throw new UnauthorizedException('No estás autorizado');",
    "    // ... generar token",
    "}",
]))
story.append(sp(8))
story.append(info_box(
    "Nunca se puede 'desencriptar' un hash de bcrypt. Para verificar, "
    "bcrypt aplica el mismo proceso a la contraseña ingresada y compara "
    "los resultados. Por eso se usa bcrypt.compare() y no una comparación directa.",
    color=colors.HexColor("#fce4ec"), border_color=RED))
story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 07 — JWT
# ════════════════════════════════════════════════════════════════════════════
story.append(section_header(7, "JWT — JSON Web Tokens", "Autenticación sin estado con tokens"))
story.append(sp(10))

story.append(Paragraph("¿Qué es?", S["h2"]))
story.append(Paragraph(
    "JWT es un estándar para crear tokens de autenticación. El servidor genera "
    "un token firmado con datos del usuario (payload). El cliente lo guarda y "
    "lo envía en cada request para identificarse, sin que el servidor guarde "
    "sesiones en memoria.", S["body"]))
story.append(sp(8))

story.append(Paragraph("Flujo completo de autenticación", S["h2"]))
story.append(sp(4))

flow2_data = [
    ["1", "Cliente envía email + password a POST /auth/login"],
    ["2", "Backend verifica credenciales con bcrypt"],
    ["3", "Backend genera un token JWT con el payload del usuario"],
    ["4", "Cliente guarda el token (localStorage o memoria)"],
    ["5", "En cada request protegida: Authorization: Bearer &lt;token&gt;"],
    ["6", "AuthGuard verifica el token y permite o rechaza el acceso"],
]
flow2_table = Table(flow2_data, colWidths=[0.4*inch, 6.5*inch])
flow2_table.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (0,-1), DARK_BG),
    ("TEXTCOLOR",     (0,0), (0,-1), ACCENT),
    ("FONTNAME",      (0,0), (0,-1), "Helvetica-Bold"),
    ("FONTSIZE",      (0,0), (-1,-1), 9.5),
    ("FONTNAME",      (1,0), (1,-1), "Helvetica"),
    ("TEXTCOLOR",     (1,0), (1,-1), TEXT_DARK),
    ("ROWBACKGROUNDS",(1,0), (1,-1), [WHITE, LIGHT_GRAY]),
    ("ALIGN",         (0,0), (0,-1), "CENTER"),
    ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING",    (0,0), (-1,-1), 8),
    ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    ("LEFTPADDING",   (1,0), (1,-1), 12),
    ("GRID",          (0,0), (-1,-1), 0.3, colors.HexColor("#cdd6f4")),
]))
story.append(flow2_table)
story.append(sp(10))

story.append(Paragraph("Configuración del módulo JWT", S["h2"]))
story.append(code_block("src/auth/auth.module.ts", [
    "JwtModule.register({",
    "    secret:      JWT_KEY,        // clave secreta para firmar los tokens",
    "    signOptions: { expiresIn: EXPIRES_IN },  // tiempo de expiración: '120s', '1h', '7d'",
    "    global:      true            // disponible en toda la app sin re-importar",
    "})",
]))
story.append(sp(8))

story.append(Paragraph("src/auth/constants/jwt.constants.ts", S["h3"]))
story.append(code_block("src/auth/constants/jwt.constants.ts", [
    "export const JWT_KEY   = 'ADSWFSDAWDA12312'  // en producción: process.env.JWT_SECRET",
    "export const EXPIRES_IN = '120s'              // el token expira en 2 minutos",
]))
story.append(sp(8))

story.append(Paragraph("Generación del token en el Service", S["h2"]))
story.append(code_block("src/auth/auth.service.ts", [
    "constructor(",
    "    @InjectRepository(User) private userRepository: Repository&lt;User&gt;,",
    "    private jwtService: JwtService,  // inyectado del JwtModule global",
    ") {}",
    "",
    "async loginUser(loginUserDto: LoginUserDto) {",
    "    // ... verificación con bcrypt ...",
    "",
    "    const payload = {",
    "        userEmail:    user.userEmail,",
    "        userPassword: user.userPassword,",
    "        userRoles:    user.userRoles,   // roles incluidos en el token",
    "    };",
    "    const token = this.jwtService.sign(payload);",
    "    return token;  // el cliente guarda este token",
    "}",
]))
story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 08 — Guards
# ════════════════════════════════════════════════════════════════════════════
story.append(section_header(8, "Guards", "Protección de rutas — AuthGuard y RolesGuard"))
story.append(sp(10))

story.append(Paragraph("¿Qué son?", S["h2"]))
story.append(Paragraph(
    "Los Guards son clases que implementan <b>CanActivate</b> e interceptan "
    "cada request antes de que llegue al controlador. Retornan <b>true</b> "
    "para permitir el acceso o lanzan una excepción para rechazarlo.", S["body"]))
story.append(sp(8))

story.append(Paragraph("Orden de ejecución", S["h2"]))
story.append(code_block("Flujo de una request protegida", [
    "Request",
    "   ↓",
    "AuthGuard    — ¿El token existe y es válido? Si no: 401 Unauthorized",
    "   ↓            Si sí: guarda el payload en request.user",
    "RolesGuard   — ¿El usuario tiene el rol requerido? Si no: 403 Forbidden",
    "   ↓",
    "Controller   — Procesa la request normalmente",
]))
story.append(sp(10))

story.append(Paragraph("AuthGuard — Verifica el token JWT", S["h2"]))
story.append(code_block("src/auth/guards/auth.guards.ts", [
    "@Injectable()",
    "export class AuthGuard implements CanActivate {",
    "    constructor(private jwtService: JwtService) {}",
    "",
    "    private extractTokenFromHeader(request: Request): string | undefined {",
    "        const [type, token] = request.headers.authorization?.split(' ') ?? [];",
    "        return type === 'Bearer' ? token : undefined;",
    "    }",
    "",
    "    async canActivate(context: ExecutionContext): Promise&lt;boolean&gt; {",
    "        const request = context.switchToHttp().getRequest();",
    "        const token = this.extractTokenFromHeader(request);",
    "        if (!token) throw new UnauthorizedException();",
    "",
    "        const payload = await this.jwtService.verifyAsync(token, { secret: JWT_KEY });",
    "        request['user'] = payload;  // guarda los datos del usuario en la request",
    "        return true;",
    "    }",
    "}",
]))
story.append(sp(10))

story.append(Paragraph("RolesGuard — Verifica el rol del usuario", S["h2"]))
story.append(code_block("src/auth/guards/roles.guards.ts", [
    "@Injectable()",
    "export class RolesGuard implements CanActivate {",
    "    constructor(private reflector: Reflector) {}",
    "",
    "    canActivate(context: ExecutionContext): boolean {",
    "        // Lee los roles requeridos del decorador @Roles en el handler",
    "        const roles = this.reflector.get(Roles, context.getHandler());",
    "        if (!roles) return true;  // si no hay @Roles, permite el acceso",
    "",
    "        const request = context.switchToHttp().getRequest();",
    "        const user: User = request.user;  // viene del AuthGuard",
    "        return this.matchRoles(roles, user.userRoles);",
    "    }",
    "",
    "    matchRoles(roles: string[], userRoles: string[]): boolean {",
    "        return userRoles.some(role =&gt; roles.includes(role));",
    "    }",
    "}",
]))
story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 09 — Decoradores personalizados
# ════════════════════════════════════════════════════════════════════════════
story.append(section_header(9, "Decoradores Personalizados", "Simplificando el código del controlador"))
story.append(sp(10))

story.append(Paragraph("¿Para qué?", S["h2"]))
story.append(Paragraph(
    "Los decoradores personalizados agrupan lógica repetida en un solo "
    "decorador reutilizable. Así el controlador queda limpio y legible.", S["body"]))
story.append(sp(8))

story.append(Paragraph("@Roles — Guarda metadata de roles requeridos", S["h2"]))
story.append(code_block("src/auth/decorators/roles.decorator.ts", [
    "import { Reflector } from '@nestjs/core';",
    "",
    "// Crea un decorador que guarda metadata (los roles requeridos)",
    "// en el handler del controlador para que RolesGuard lo lea",
    "export const Roles = Reflector.createDecorator&lt;string[]&gt;();",
]))
story.append(sp(8))

story.append(Paragraph("@Auth — Combina Guards y Roles en uno", S["h2"]))
story.append(code_block("src/auth/decorators/auth.decorator.ts", [
    "import { applyDecorators, UseGuards } from '@nestjs/common';",
    "",
    "// En lugar de escribir @Roles + @UseGuards en cada endpoint,",
    "// se usa solo @Auth(ROLES.MANAGER)",
    "export const Auth = (...roles: ROLES[]) =&gt; {",
    "    roles.push(ROLES.ADMIN);  // Admin siempre tiene acceso",
    "    return applyDecorators(",
    "        Roles(roles),",
    "        UseGuards(AuthGuard, RolesGuard)",
    "    );",
    "};",
]))
story.append(sp(8))

story.append(Paragraph("@UserData — Extrae el usuario de la request", S["h2"]))
story.append(code_block("src/auth/decorators/user.decorator.ts", [
    "import { createParamDecorator, ExecutionContext } from '@nestjs/common';",
    "",
    "// Crea un decorador de parámetro personalizado",
    "// que extrae el usuario que guardó AuthGuard en request.user",
    "export const UserData = createParamDecorator(",
    "    (data: unknown, ctx: ExecutionContext) =&gt; {",
    "        const request = ctx.switchToHttp().getRequest();",
    "        return request.user;",
    "    }",
    ");",
    "",
    "// Uso en el controlador:",
    "// @Get('profile')",
    "// getProfile(@UserData() user: User) { return user; }",
]))
story.append(sp(8))

story.append(Paragraph("Uso final en el controlador", S["h2"]))
story.append(code_block("src/employees/employees.controller.ts", [
    "// Sin decoradores personalizados (código repetitivo):",
    "// @Roles([ROLES.MANAGER, ROLES.ADMIN])",
    "// @UseGuards(AuthGuard, RolesGuard)",
    "// @Post()",
    "",
    "// Con @Auth (limpio y reutilizable):",
    "@Auth(ROLES.MANAGER)    // solo Manager y Admin pueden crear employees",
    "@Post()",
    "create(@Body() dto: CreateEmployeeDto) {",
    "    return this.employeesService.create(dto);",
    "}",
    "",
    "@Auth(ROLES.ADMIN)      // solo Admin puede eliminar",
    "@Delete(':id')",
    "remove(@Param('id') id: string) {",
    "    return this.employeesService.remove(id);",
    "}",
]))
story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 10 — Pipes
# ════════════════════════════════════════════════════════════════════════════
story.append(section_header(10, "Pipes", "Transformación y validación de parámetros"))
story.append(sp(10))

story.append(Paragraph("¿Qué son?", S["h2"]))
story.append(Paragraph(
    "Los Pipes transforman o validan datos antes de que lleguen al método "
    "del controlador. NestJS incluye pipes predefinidos para los casos más comunes.", S["body"]))
story.append(sp(8))

story.append(Paragraph("Los dos pipes usados en este proyecto", S["h2"]))
story.append(mini_table(
    ["Pipe", "Dónde", "Para qué"],
    [
        ["ValidationPipe", "Global en main.ts", "Valida el @Body() contra el DTO con class-validator"],
        ["ParseUUIDPipe", "Por parámetro en el controller", "Valida que @Param('id') sea un UUID válido"],
    ],
    [2*inch, 2.2*inch, 2.7*inch]
))
story.append(sp(10))

story.append(Paragraph("ValidationPipe — Validación global", S["h2"]))
story.append(code_block("src/main.ts", [
    "app.useGlobalPipes(new ValidationPipe({",
    "    whitelist:            true,",
    "    forbidNonWhitelisted: true,",
    "    transform:            true,",
    "}))",
    "",
    "// Resultado: si el @Body() no cumple las reglas del DTO,",
    "// NestJS responde 400 automáticamente sin llegar al controlador",
]))
story.append(sp(10))

story.append(Paragraph("ParseUUIDPipe — Validación de parámetros de ruta", S["h2"]))
story.append(code_block("src/employees/employees.controller.ts", [
    "@Get(':id')",
    "findOne(",
    "    @Param('id', new ParseUUIDPipe({ version: '4' })) id: string",
    "    //            ↑ valida que ':id' sea un UUID v4 válido",
    "    //            Si no es válido: responde 400 automáticamente",
    ") {",
    "    return this.employeesService.findOne(id);",
    "}",
]))
story.append(sp(8))
story.append(info_box(
    "Sin ParseUUIDPipe, si alguien envía un ID inválido como /employees/hola, "
    "TypeORM lanzaría un error interno 500. Con el pipe, NestJS lo rechaza "
    "antes con un 400 Bad Request descriptivo.",
    color=colors.HexColor("#e3f2fd"), border_color=ACCENT))
story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 11 — Swagger
# ════════════════════════════════════════════════════════════════════════════
story.append(section_header(11, "Swagger", "Documentación automática e interactiva"))
story.append(sp(10))

story.append(Paragraph("¿Qué es?", S["h2"]))
story.append(Paragraph(
    "Swagger genera automáticamente una interfaz web en <b>/api</b> que "
    "muestra todos los endpoints, permite probarlos y sirve como documentación "
    "para el equipo frontend. Basta con agregar decoradores al código.", S["body"]))
story.append(sp(8))

story.append(Paragraph("Configuración en main.ts", S["h2"]))
story.append(code_block("src/main.ts", [
    "const config = new DocumentBuilder()",
    "    .setTitle('Ocso API')",
    "    .setDescription('Api for ocso management')",
    "    .setVersion('0.9')",
    "    .addBearerAuth()   // agrega campo de token JWT en la UI",
    "    .build();",
    "",
    "const document = SwaggerModule.createDocument(app, config);",
    "SwaggerModule.setup('api', app, document);",
    "// UI disponible en: http://localhost:3000/api",
]))
story.append(sp(10))

story.append(Paragraph("Decoradores de Swagger", S["h2"]))
story.append(mini_table(
    ["Decorador", "Para qué"],
    [
        ["@ApiTags('nombre')", "Agrupa endpoints bajo una etiqueta en la UI"],
        ["@ApiProperty()", "Documenta una propiedad del DTO (la muestra en el schema)"],
        ["@ApiResponse({ status, description })", "Documenta un posible tipo de respuesta"],
        ["applyDecorators(ApiResponse(...))", "Agrupa respuestas comunes en un decorador reutilizable"],
    ],
    [3.2*inch, 3.7*inch]
))
story.append(sp(10))

story.append(Paragraph("@ApiAuth — Decorador reutilizable con respuestas comunes", S["h3"]))
story.append(code_block("src/auth/decorators/api.decorator.ts", [
    "export const ApiAuth = () =&gt; {",
    "    return applyDecorators(",
    "        ApiResponse({ status: 401, description: 'Missing or invalid token' }),",
    "        ApiResponse({ status: 403, description: 'Missing role' }),",
    "        ApiResponse({ status: 500, description: 'Server error' }),",
    "    );",
    "};",
    "",
    "// Uso en el controlador:",
    "@ApiAuth()           // documenta las respuestas 401, 403 y 500 de todos los endpoints",
    "@ApiTags('Auth')",
    "@Controller('auth')",
    "export class AuthController { ... }",
]))
story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 12 — Multer
# ════════════════════════════════════════════════════════════════════════════
story.append(section_header(12, "Multer — File Upload", "Recepción de archivos en los endpoints"))
story.append(sp(10))

story.append(Paragraph("¿Qué es?", S["h2"]))
story.append(Paragraph(
    "Multer es un middleware para manejar <b>multipart/form-data</b>, "
    "el formato que se usa para subir archivos. NestJS lo integra "
    "a través de <b>FileInterceptor</b>.", S["body"]))
story.append(sp(8))

story.append(Paragraph("Uso en el Controller", S["h2"]))
story.append(code_block("src/employees/employees.controller.ts", [
    "import { FileInterceptor } from '@nestjs/platform-express';",
    "import { UseInterceptors, UploadedFile } from '@nestjs/common';",
    "",
    "@Post('upload')",
    "@UseInterceptors(FileInterceptor('file'))  // 'file' = nombre del campo en el formulario",
    "uploadPhoto(@UploadedFile() file: Express.Multer.File) {",
    "    console.log(file.originalname);  // nombre del archivo",
    "    console.log(file.mimetype);      // tipo: image/jpeg, application/pdf...",
    "    console.log(file.size);          // tamaño en bytes",
    "    console.log(file.buffer);        // contenido del archivo en memoria",
    "    return 'archivo recibido';",
    "}",
]))
story.append(sp(8))
story.append(info_box(
    "FileInterceptor('file') lee el campo 'file' del form-data. "
    "El nombre debe coincidir exactamente con el campo que envía el cliente. "
    "Para guardar el archivo en disco, se configura diskStorage en las opciones de Multer.",
    color=colors.HexColor("#f3e5f5"), border_color=colors.HexColor("#cba6f7")))
story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════════════
# ORDEN PASO A PASO
# ════════════════════════════════════════════════════════════════════════════
story.append(section_header("", "Orden Paso a Paso para Nuevos Proyectos",
             "Guía de referencia rápida"))
story.append(sp(12))

pasos = [
    ("1", "Crear el proyecto", "nest new nombre-proyecto"),
    ("2", "Instalar dependencias",
     "npm install @nestjs/typeorm typeorm pg @nestjs/config "
     "class-validator class-transformer @nestjs/jwt bcrypt @nestjs/swagger uuid"),
    ("3", "Crear el archivo .env",
     "host, port, pass, name (datos de conexión a PostgreSQL)"),
    ("4", "Configurar AppModule",
     "ConfigModule.forRoot() + TypeOrmModule.forRoot() con datos del .env"),
    ("5", "Crear recursos base",
     "nest g resource nombre — genera module, controller, service y DTOs"),
    ("6", "Definir la Entidad",
     "Decoradores @Entity, @Column, relaciones @OneToOne/@ManyToOne/@OneToMany"),
    ("7", "Completar los DTOs",
     "Agregar decoradores de class-validator a cada propiedad"),
    ("8", "Registrar la entidad en el módulo",
     "TypeOrmModule.forFeature([Entidad]) en el imports del módulo"),
    ("9", "Completar el Service",
     "CRUD con el Repository: create/save, find, preload/save, delete"),
    ("10", "Completar el Controller",
     "Rutas @Get/@Post/@Patch/@Delete con @Body, @Param, @ParseUUIDPipe"),
    ("11", "Implementar Auth",
     "Entidad User + bcrypt al registrar + JwtModule + generar token en login"),
    ("12", "Crear AuthGuard",
     "Verifica el token JWT en el header y guarda el payload en request.user"),
    ("13", "Crear RolesGuard",
     "Lee los roles del @Roles decorator y verifica contra user.userRoles"),
    ("14", "Crear decoradores personalizados",
     "@Roles (Reflector.createDecorator) + @Auth (applyDecorators) + @UserData"),
    ("15", "Aplicar @Auth() en controladores",
     "@Auth(ROLES.MANAGER) sobre los métodos o toda la clase"),
    ("16", "Configurar Swagger",
     "DocumentBuilder + SwaggerModule.setup en main.ts. Agregar @ApiTags, @ApiProperty"),
    ("17", "Configurar ValidationPipe global",
     "app.useGlobalPipes(new ValidationPipe({ whitelist, forbidNonWhitelisted, transform }))"),
    ("18", "Probar la API",
     "Abrir http://localhost:3000/api y probar cada endpoint con Swagger UI"),
]

for num, title, desc in pasos:
    story.append(step_box(num, title, desc))
    story.append(sp(6))

story.append(PageBreak())

# ── RESUMEN FINAL ─────────────────────────────────────────────────────────
story.append(section_header("", "Resumen del Stack", "Tecnologías y su rol"))
story.append(sp(10))
story.append(mini_table(
    ["Tecnología", "Rol en el proyecto", "Cuándo se aplica"],
    [
        ["TypeScript", "Lenguaje base con tipado estático", "Siempre — es la base de todo"],
        ["NestJS", "Framework: módulos, rutas, DI", "Desde el inicio"],
        ["TypeORM", "ORM para PostgreSQL", "Al definir entidades y hacer CRUD"],
        ["@nestjs/config", "Variables de entorno (.env)", "Antes de conectar la BD"],
        ["class-validator", "Validar datos entrantes (DTOs)", "Al definir los DTOs"],
        ["bcrypt", "Hashear contraseñas", "Al implementar registro/login"],
        ["JWT", "Autenticación con tokens", "Al implementar login y rutas protegidas"],
        ["Guards", "Proteger rutas con lógica", "Después de implementar JWT"],
        ["Decoradores custom", "Simplificar el controlador", "Después de tener Guards"],
        ["Pipes", "Validar parámetros de ruta", "Al definir rutas con @Param"],
        ["Swagger", "Documentación interactiva", "Al finalizar los endpoints"],
        ["Multer", "Recibir archivos", "Cuando se necesita upload de archivos"],
    ],
    [1.6*inch, 2.8*inch, 2.5*inch]
))

# ── BUILD ────────────────────────────────────────────────────────────────────
doc.build(story)
print(f"PDF generado: {OUTPUT}")
