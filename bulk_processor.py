"""
Bulk Processing Utility for Scholarship Eligibility Filter
Handles Excel/PDF file uploads and generates eligibility results
"""

import pandas as pd
import PyPDF2
import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime
import json

class BulkProcessor:
    def __init__(self, rules_engine):
        self.rules_engine = rules_engine
        
    def read_excel_file(self, file_path):
        """Read student data from Excel file"""
        try:
            df = pd.read_excel(file_path)
            return self.process_dataframe(df)
        except Exception as e:
            raise Exception(f"Error reading Excel file: {str(e)}")
    
    def read_pdf_file(self, file_path):
        """Extract text from PDF and attempt to parse student data"""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
            
            # Simple parsing - assumes tabular data in PDF
            lines = text.split('\n')
            data = []
            headers = None
            
            for line in lines:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 6:  # Minimum required fields
                        if not headers:
                            headers = parts
                        else:
                            data.append(parts)
            
            if headers and data:
                df = pd.DataFrame(data, columns=headers[:len(data[0])])
                return self.process_dataframe(df)
            else:
                raise Exception("Could not parse student data from PDF")
                
        except Exception as e:
            raise Exception(f"Error reading PDF file: {str(e)}")
    
    def process_dataframe(self, df):
        """Process DataFrame and standardize column names"""
        # Map common column variations to standard names
        column_mapping = {
            'name': ['name', 'student_name', 'full_name', 'Name', 'Student Name'],
            'email': ['email', 'email_address', 'Email', 'Email Address'],
            'course': ['course', 'program', 'Course', 'Program'],
            'year_of_study': ['year', 'year_of_study', 'Year', 'Year of Study'],
            'marks_percentage': ['marks', 'percentage', 'marks_percentage', 'Marks', 'Percentage'],
            'family_income': ['income', 'family_income', 'Income', 'Family Income'],
            'category': ['category', 'caste', 'Category', 'Caste'],
            'has_backlogs': ['backlogs', 'has_backlogs', 'Backlogs'],
            'is_full_time': ['full_time', 'is_full_time', 'Full Time']
        }
        
        # Rename columns to standard format
        for standard_name, variations in column_mapping.items():
            for col in df.columns:
                if col in variations:
                    df = df.rename(columns={col: standard_name})
                    break
        
        # Convert data types
        if 'marks_percentage' in df.columns:
            df['marks_percentage'] = pd.to_numeric(df['marks_percentage'], errors='coerce')
        if 'family_income' in df.columns:
            df['family_income'] = pd.to_numeric(df['family_income'], errors='coerce')
        if 'year_of_study' in df.columns:
            df['year_of_study'] = pd.to_numeric(df['year_of_study'], errors='coerce')
        
        # Handle boolean fields
        if 'has_backlogs' in df.columns:
            df['has_backlogs'] = df['has_backlogs'].map({'Yes': True, 'No': False, 'TRUE': True, 'FALSE': False, True: True, False: False})
        if 'is_full_time' in df.columns:
            df['is_full_time'] = df['is_full_time'].map({'Yes': True, 'No': False, 'TRUE': True, 'FALSE': False, True: True, False: False})
        
        return df
    
    def check_bulk_eligibility(self, df, scholarships):
        """Check eligibility for all students in DataFrame"""
        results = []
        
        for index, row in df.iterrows():
            student_data = {
                'name': row.get('name', f'Student {index + 1}'),
                'email': row.get('email', f'student{index + 1}@example.com'),
                'course': row.get('course', 'Unknown'),
                'year_of_study': int(row.get('year_of_study', 1)),
                'marks_percentage': float(row.get('marks_percentage', 0)),
                'family_income': float(row.get('family_income', 0)),
                'category': row.get('category', 'General'),
                'has_backlogs': bool(row.get('has_backlogs', False)),
                'is_full_time': bool(row.get('is_full_time', True))
            }
            
            # Create a mock student object
            class MockStudent:
                def __init__(self, data):
                    for key, value in data.items():
                        setattr(self, key, value)
            
            student = MockStudent(student_data)
            
            # Check eligibility for each scholarship
            student_results = {
                'student_data': student_data,
                'scholarships': []
            }
            
            for scholarship in scholarships:
                result = self.rules_engine.check_eligibility(student, scholarship)
                student_results['scholarships'].append(result)
            
            results.append(student_results)
        
        return results
    
    def generate_excel_report(self, results, output_path):
        """Generate Excel report with eligibility results and detailed reasons"""
        data = []
        
        for student_result in results:
            student = student_result['student_data']
            base_row = {
                'Name': student['name'],
                'Email': student['email'],
                'Course': student['course'],
                'Year': student['year_of_study'],
                'Marks (%)': student['marks_percentage'],
                'Family Income': student['family_income'],
                'Category': student['category'],
                'Has Backlogs': 'Yes' if student['has_backlogs'] else 'No',
                'Full Time': 'Yes' if student['is_full_time'] else 'No'
            }
            
            for scholarship in student_result['scholarships']:
                row = base_row.copy()
                
                # Enhanced eligibility reasons
                if scholarship['eligible']:
                    eligibility_status = 'ELIGIBLE'
                    reasons = '; '.join(scholarship.get('acceptance_reasons', ['All criteria met']))
                else:
                    eligibility_status = 'NOT ELIGIBLE'
                    reasons = '; '.join(scholarship.get('rejection_reasons', ['Criteria not met']))
                
                row.update({
                    'Scholarship': scholarship['scholarship_name'],
                    'Amount': scholarship['scholarship_amount'],
                    'Eligibility Status': eligibility_status,
                    'Priority Score': scholarship['priority_score'],
                    'Detailed Reasons': reasons,
                    'Summary': f"{eligibility_status} - {reasons[:100]}{'...' if len(reasons) > 100 else ''}"
                })
                data.append(row)
        
        df = pd.DataFrame(data)
        
        # Reorder columns for better readability
        column_order = [
            'Name', 'Email', 'Course', 'Year', 'Marks (%)', 'Family Income', 'Category',
            'Has Backlogs', 'Full Time', 'Scholarship', 'Amount', 'Eligibility Status',
            'Priority Score', 'Detailed Reasons', 'Summary'
        ]
        
        df = df[column_order]
        df.to_excel(output_path, index=False)
        return output_path
    
    def generate_pdf_report(self, results, output_path):
        """Generate PDF report with eligibility results"""
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        elements.append(Paragraph("Scholarship Eligibility Report", title_style))
        elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # Summary
        total_students = len(results)
        eligible_count = sum(1 for r in results if any(s['eligible'] for s in r['scholarships']))
        
        summary_data = [
            ['Total Students Processed', str(total_students)],
            ['Students with Eligible Scholarships', str(eligible_count)],
            ['Students with No Eligible Scholarships', str(total_students - eligible_count)]
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 1*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(Paragraph("Summary", styles['Heading2']))
        elements.append(summary_table)
        elements.append(Spacer(1, 20))
        
        # Detailed Results
        elements.append(Paragraph("Detailed Results with Eligibility Reasons", styles['Heading2']))
        
        for i, student_result in enumerate(results):
            student = student_result['student_data']
            
            # Student header
            elements.append(Paragraph(f"Student {i+1}: {student['name']}", styles['Heading3']))
            
            # Student details
            student_info = [
                ['Email', student['email']],
                ['Course', f"{student['course']} (Year {student['year_of_study']})"],
                ['Marks', f"{student['marks_percentage']}%"],
                ['Family Income', f"₹{student['family_income']:,.0f}"],
                ['Category', student['category']],
                ['Backlogs', 'Yes' if student['has_backlogs'] else 'No'],
                ['Full Time', 'Yes' if student['is_full_time'] else 'No']
            ]
            
            student_table = Table(student_info, colWidths=[1.5*inch, 3*inch])
            student_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(student_table)
            elements.append(Spacer(1, 10))
            
            # Scholarship results
            scholarship_data = [['Scholarship', 'Amount', 'Status', 'Score', 'Eligibility Reasons']]
            
            for scholarship in student_result['scholarships']:
                if scholarship['eligible']:
                    status = '✓ ELIGIBLE'
                    reasons = '; '.join(scholarship.get('acceptance_reasons', ['All criteria met'])[:2])
                else:
                    status = '✗ NOT ELIGIBLE'
                    reasons = '; '.join(scholarship.get('rejection_reasons', ['Criteria not met'])[:2])
                
                scholarship_data.append([
                    scholarship['scholarship_name'],
                    f"₹{scholarship['scholarship_amount']:,.0f}",
                    status,
                    str(scholarship['priority_score']),
                    reasons
                ])
            
            scholarship_table = Table(scholarship_data, colWidths=[1.5*inch, 0.8*inch, 0.8*inch, 0.5*inch, 2.4*inch])
            scholarship_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                # Color eligible rows green
                ('TEXTCOLOR', (2, 1), (2, -1), colors.green),
                # Color ineligible rows red  
                ('TEXTCOLOR', (2, 1), (2, -1), colors.red)
            ]))
            
            elements.append(scholarship_table)
            elements.append(Spacer(1, 20))
        
        doc.build(elements)
        return output_path

# Global instance
bulk_processor = None

def get_bulk_processor(rules_engine):
    global bulk_processor
    if bulk_processor is None:
        bulk_processor = BulkProcessor(rules_engine)
    return bulk_processor