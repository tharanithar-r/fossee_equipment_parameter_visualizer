from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import os


def generate_pdf_report(dataset):
    """Generate a PDF report for a dataset"""
    
    # Create reports directory
    reports_dir = 'media/reports'
    os.makedirs(reports_dir, exist_ok=True)
    
    # Generate filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    pdf_filename = f"{reports_dir}/report_{dataset.id}_{timestamp}.pdf"
    
    # Create PDF
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    story.append(Paragraph("Chemical Equipment Analysis Report", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Dataset Info
    info_style = styles['Normal']
    story.append(Paragraph(f"<b>Dataset:</b> {dataset.name}", info_style))
    story.append(Paragraph(f"<b>Upload Date:</b> {dataset.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}", info_style))
    story.append(Paragraph(f"<b>Total Equipment:</b> {dataset.total_count}", info_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Summary Statistics
    story.append(Paragraph("<b>Summary Statistics</b>", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    stats_data = [
        ['Parameter', 'Average', 'Minimum', 'Maximum'],
        ['Flowrate', f'{dataset.avg_flowrate:.2f}', f'{dataset.min_flowrate:.2f}', f'{dataset.max_flowrate:.2f}'],
        ['Pressure', f'{dataset.avg_pressure:.2f}', f'{dataset.min_pressure:.2f}', f'{dataset.max_pressure:.2f}'],
        ['Temperature', f'{dataset.avg_temperature:.2f}', f'{dataset.min_temperature:.2f}', f'{dataset.max_temperature:.2f}'],
    ]
    
    stats_table = Table(stats_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(stats_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Equipment Type Distribution
    story.append(Paragraph("<b>Equipment Type Distribution</b>", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    type_counts = {}
    for equipment in dataset.equipment.all():
        type_counts[equipment.equipment_type] = type_counts.get(equipment.equipment_type, 0) + 1
    
    type_data = [['Equipment Type', 'Count', 'Percentage']]
    for eq_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / dataset.total_count) * 100
        type_data.append([eq_type, str(count), f'{percentage:.1f}%'])
    
    type_table = Table(type_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
    type_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(type_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Equipment Details (first 50 items)
    story.append(Paragraph("<b>Equipment Details (First 50 Items)</b>", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    equipment_data = [['Name', 'Type', 'Flowrate', 'Pressure', 'Temp']]
    for equipment in dataset.equipment.all()[:50]:
        equipment_data.append([
            equipment.equipment_name[:20],
            equipment.equipment_type[:15],
            f'{equipment.flowrate:.1f}',
            f'{equipment.pressure:.1f}',
            f'{equipment.temperature:.1f}'
        ])
    
    equipment_table = Table(equipment_data, colWidths=[2*inch, 1.5*inch, 1*inch, 1*inch, 1*inch])
    equipment_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(equipment_table)
    
    # Build PDF
    doc.build(story)
    return pdf_filename
