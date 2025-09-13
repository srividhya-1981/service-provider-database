from flask import Flask, request, render_template_string, redirect, url_for, jsonify
import psycopg2
from datetime import datetime
import os

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_NAME = os.environ.get("DB_NAME", "service_provider_db")
DB_USER = os.environ.get("DB_USER", "myuser")
DB_PASS = os.environ.get("DB_PASS", "mypassword")

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

@app.route('/')
def index():
    provider_id = request.args.get('provider_id')
    provider_data = None
    if provider_id:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM service_providers WHERE provider_id = %s", (provider_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row:
            # Adjust indices as per your DB schema
            provider_data = {
                'provider_id': row[0],
                'sub_zone': row[1],
                'area': row[2],
                'service_type': row[3],
                'provider_name': row[4],
                'address': row[5],
                'contact_mobile_1': row[6],
                'contact_mobile_2': row[7] or '',
                'delivery_available': 'Y' if row[8] else 'N',
                'immediate_delivery': 'Y' if row[9] else 'N',
                'delivery_charges': row[10] or '',
                'service_hours': row[11] or '',
                'field_visit_done': 'Y' if row[12] else 'N',
                'field_visit_remarks': row[13] or '',
                'last_verified_date': row[14].strftime('%d-%m-%Y') if row[14] else ''
            }
    with open('form.html', 'r') as f:
        form_html = f.read()
    return render_template_string(form_html, provider_data=provider_data)

@app.route('/submit', methods=['POST'])
def submit():
    provider_id = request.form.get('provider_id')
    sub_zone = request.form.get('sub_zone')
    area = request.form.get('area')

    # Use 'other' fields if "Others" is selected
    if sub_zone == "Others":
        sub_zone = request.form.get('sub_zone_other')
    if area == "Others" or sub_zone == "Others":
        area = request.form.get('area_other')

    service_type = request.form.get('service_type')
    provider_name = request.form.get('provider_name')
    address = request.form.get('address')
    contact_mobile_1 = request.form.get('contact_mobile 1')
    contact_mobile_2 = request.form.get('contact_mobile 2')
    delivery_available = request.form.get('delivery_available')
    immediate_delivery = request.form.get('immediate_delivery')
    delivery_charges = request.form.get('delivery_charges')
    service_hours = request.form.get('service_hours')
    field_visit_done = request.form.get('field_visit_done')
    field_visit_remarks = request.form.get('field_visit_remarks')
    last_verified_date = request.form.get('last_verified_date')

    last_verified_date_obj = datetime.strptime(last_verified_date, '%d-%m-%Y').date() if last_verified_date else None

    conn = get_connection()
    cur = conn.cursor()

    if provider_id:
        cur.execute("""
            UPDATE service_providers
            SET sub_zone = %s,
                area = %s,
                service_type = %s,
                provider_name = %s,
                address = %s,
                contact_mobile_1 = %s,
                contact_mobile_2 = %s,
                delivery_available = %s,
                immediate_delivery = %s,
                delivery_charges = %s,
                service_hours = %s,
                field_visit_done = %s,
                field_visit_remarks = %s,
                last_verified_date = %s,
                updated_at = %s
            WHERE provider_id = %s
        """, (
            sub_zone, area, service_type, provider_name, address,
            contact_mobile_1, contact_mobile_2, delivery_available,
            immediate_delivery, delivery_charges, service_hours,
            field_visit_done, field_visit_remarks, last_verified_date_obj,
            datetime.now(), provider_id
        ))
    else:
        cur.execute("""
            INSERT INTO service_providers (
                sub_zone, area, service_type, provider_name, address,
                contact_mobile_1, contact_mobile_2, delivery_available,
                immediate_delivery, delivery_charges, service_hours,
                field_visit_done, field_visit_remarks, last_verified_date
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            sub_zone, area, service_type, provider_name, address,
            contact_mobile_1, contact_mobile_2, delivery_available,
            immediate_delivery, delivery_charges, service_hours,
            field_visit_done, field_visit_remarks, last_verified_date_obj
        ))

    conn.commit()
    cur.close()
    conn.close()

    return "Submission successful!"

@app.route('/api/provider/<int:provider_id>')
def get_provider(provider_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM service_providers WHERE provider_id = %s", (provider_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        # Adjust indices as per your DB schema
        data = {
            "found": True,
            "provider_id": row[0],
            "sub_zone": row[1],
            "area": row[2],
            "service_type": row[3],
            "provider_name": row[4],
            "address": row[5],
            "contact_mobile_1": row[6],
            "contact_mobile_2": row[7],
            "delivery_available": row[8],
            "immediate_delivery": row[9],
            "delivery_charges": row[10],
            "service_hours": row[11],
            "field_visit_done": row[12],
            "field_visit_remarks": row[13],
            "last_verified_date": row[14].strftime('%d-%m-%Y') if row[14] else ''
        }
    else:
        data = {"found": False}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
