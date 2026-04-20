<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ยืนยันการจองสำเร็จ | ร้านซักรีด</title>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">

    <style>
        body {
            background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%);
            font-family: 'Prompt', sans-serif;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .confirm-card {
            background: rgba(255, 255, 255, 0.98);
            border-radius: 25px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            padding: 35px;
            max-width: 550px;
            width: 100%;
            text-align: center;
        }

        .success-icon {
            font-size: 4rem;
            color: #2ecc71; 
            margin-bottom: 10px;
            animation: popIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
        }

        @keyframes popIn {
            0% { transform: scale(0); opacity: 0; }
            100% { transform: scale(1); opacity: 1; }
        }

        .order-id {
            background: #eef2f7;
            color: #4facfe;
            font-weight: bold;
            padding: 8px 20px;
            border-radius: 50px;
            display: inline-block;
            margin-bottom: 25px;
            border: 1px dashed #4facfe;
        }

        .details-box {
            background: #ffffff;
            border-radius: 18px;
            padding: 22px;
            text-align: left;
            border: 1px solid #f1f3f5;
            box-shadow: 0 4px 6px rgba(0,0,0,0.02);
            margin-bottom: 20px;
        }

        .info-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }

        .info-item label {
            display: block;
            font-size: 0.8rem;
            color: #868e96;
            margin-bottom: 2px;
        }

        .info-item span {
            font-weight: 500;
            color: #343a40;
        }

        .total-row {
            font-size: 1.2rem;
            color: #4facfe;
            border-top: 2px dashed #e9ecef !important;
            padding-top: 15px !important;
            margin-top: 10px;
        }

        .btn-back {
            background: linear-gradient(to right, #4facfe 0%, #00f2fe 100%);
            border: none;
            border-radius: 12px;
            padding: 12px;
            font-weight: 500;
            transition: all 0.3s ease;
        }

        .btn-back:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(79, 172, 254, 0.3);
        }
    </style>
</head>
<body>

    <div class="confirm-card">
        <i class="fa-solid fa-circle-check success-icon"></i>
        <h3 class="fw-bold text-dark">บันทึกข้อมูลสำเร็จ</h3>
        <p class="text-muted">ขอบคุณที่ใช้บริการ Smart Laundry ค่ะ</p>

        <div class="order-id">
            <i class="fa-solid fa-receipt me-1"></i> หมายเลขรายการ: {{ order.order_id }}
        </div>

        <div class="details-box">
    <h6 class="fw-bold text-dark border-bottom pb-2 mb-3">
        <i class="fa-solid fa-file-invoice text-primary me-2"></i>ข้อมูลการทำรายการ
    </h6>
    <div class="info-grid">
        <div class="info-item">
            <label>ชื่อลูกค้า</label>
            <span>{{ customer.cus_name }}</span>
        </div>
        <div class="info-item text-end">
            <label>รหัสสมาชิก</label>
            <span class="text-primary fw-bold">{{ customer.cus_id }}</span>
        </div>

        <div class="info-item">
            <label>เบอร์โทรศัพท์</label>
            <span>{{ customer.telephone }}</span>
        </div>
        <div class="info-item text-end">
            <label>ชำระโดย</label>
            <span class="badge bg-light text-success border">{{ payment_method }}</span>
        </div>

        <div class="info-item">
            <label>วันที่ทำรายการ</label>
            <span class="text-muted small">{{ order.created_at|date:"d/m/Y" }}</span>
        </div>
        <div class="info-item text-end">
            <label>เวลาที่บันทึกออเดอร์</label>
            <span class="text-muted small">{{ order.created_at|date:"H:i" }} น.</span>
        </div>

        <div class="info-item mt-2 pt-2 border-top">
            <label class="text-primary">วันที่นัดรับผ้า</label>
            <span class="fw-bold">{{ order.pickup_date }}</span>
        </div>
        <div class="info-item text-end mt-2 pt-2 border-top">
            <label class="text-primary">เวลาที่นัด</label>
            <span class="fw-bold">{{ order.times }} น.</span>
        </div>
    </div>
</div>

        <div class="details-box">
            <h6 class="fw-bold text-dark border-bottom pb-2 mb-2">
                <i class="fa-solid fa-basket-shopping text-primary me-2"></i>สรุปค่าใช้จ่าย
            </h6>
            <ul class="list-group list-group-flush">
                {% for item in items_list %}
                <li class="list-group-item d-flex justify-content-between align-items-center px-0 border-0">
                    <div class="text-start">
                        <span class="fw-medium">{{ item.name }}</span>
                        <small class="d-block text-muted">จำนวน {{ item.qty }} ชิ้น</small>
                    </div>
                    <span class="fw-bold">{{ item.item_total }} ฿</span>
                </li>
                {% endfor %}

                {% if discount > 0 %}
                <li class="list-group-item d-flex justify-content-between align-items-center px-0 border-0 text-danger small">
                    <span>ส่วนลดจากการใช้แต้ม</span>
                    <span>-{{ discount }} ฿</span>
                </li>
                {% endif %}

                <li class="list-group-item d-flex justify-content-between align-items-center fw-bold total-row px-0">
                    ยอดรวมสุทธิ
                    <span class="fs-3">{{ final_total }} ฿</span>
                </li>
            </ul>
        </div>

        <div class="d-grid gap-2">
            <button onclick="window.print()" class="btn btn-outline-dark border-0 btn-sm mb-2 text-muted">
                <i class="fa-solid fa-print"></i> พิมพ์ใบเสร็จ
            </button>
            <a href="/servicesusers/" class="btn btn-back w-100 text-white">
                <i class="fa-solid fa-house me-1"></i> กลับสู่หน้าหลัก
            </a>
        </div>
    </div>
    
        
</body>
</html>