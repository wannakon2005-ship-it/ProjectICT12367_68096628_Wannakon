<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Laundry - Admin Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        :root { --primary-blue: #007bff; --light-bg: #f4f7f6; }
        body { background-color: var(--light-bg); font-family: 'Sarabun', sans-serif; }
        
        /* สไตล์การ์ดสถิติ */
        .stat-card { border: none; border-radius: 15px; transition: transform 0.3s; }
        .stat-card:hover { transform: translateY(-5px); }
        
        /* สไตล์ตาราง */
        .table-container { background: white; border-radius: 20px; padding: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
        .table thead { background-color: #f8f9fa; }
        .badge-status { padding: 8px 12px; border-radius: 50px; font-size: 0.85rem; }
        
        /* ปุ่มจัดการ */
        .btn-action { width: 35px; height: 35px; border-radius: 10px; display: inline-flex; align-items: center; justify-content: center; transition: 0.2s; }
    </style>
</head>
<body>

    
<div class="d-flex justify-content-between align-items-center mb-4">
    <div>
        <h3 class="fw-bold mb-0">Dashboard ผู้ดูแลระบบ</h3>
        <p class="text-muted">ยินดีต้อนรับกลับมา, คุณแอดมิน</p>
    </div>
    <div class="d-flex gap-3 align-items-center">
        <div class="input-group" style="width: 300px;">
            <span class="input-group-text bg-white border-end-0 rounded-pill-start">
                <i class="fa-solid fa-magnifying-glass text-muted"></i>
            </span>
            <input type="text" id="searchInput" class="form-control border-start-0 rounded-pill-end shadow-sm" 
                   placeholder="ค้นหาชื่อลูกค้า หรือ Order ID..." onkeyup="searchOrder()">
        </div>

        <a href="{% url 'logout' %}" class="btn btn-outline-danger shadow-sm rounded-pill px-4 fw-bold">
            <i class="fa-solid fa-right-from-bracket me-2"></i>ออกจากระบบ
        </a>
    </div>
</div>

    <div class="row g-3 mb-4">
    <div class="col-md-3">
        <div class="card shadow-sm p-3 border-start border-primary border-4">
            <small class="text-muted d-block">ออเดอร์วันนี้</small>
            <h4 class="fw-bold mb-0 text-primary">{{ today_count }} รายการ</h4>
        </div>
    </div>

    <div class="col-md-3">
        <div class="card shadow-sm p-3">
            <small class="text-muted d-block">ออเดอร์รวมทั้งหมด</small>
            <h4 class="fw-bold mb-0">{{ total_count }} รายการ</h4>
        </div>
    </div>

    <div class="col-md-2">
        <div class="card shadow-sm p-3">
            <small class="text-muted d-block text-warning">กำลังดำเนินการ</small>
            <h4 class="fw-bold mb-0">{{ washing_count }}</h4>
        </div>
    </div>

    <div class="col-md-2">
        <div class="card shadow-sm p-3">
            <small class="text-muted d-block text-info">เสร็จแล้ว</small>
            <h4 class="fw-bold mb-0">{{ finished_count }}</h4>
        </div>
    </div>

    <div class="col-md-2">
        <div class="card shadow-sm p-3">
            <small class="text-muted d-block text-success">ส่งมอบแล้ว</small>
            <h4 class="fw-bold mb-0">{{ returned_count }}</h4>
        </div>
    </div>

    <div class="col-md-6">
        <div class="card shadow-sm p-3 border-start border-success border-4">
            <small class="text-muted d-block text-success">รายได้วันนี้ (Daily Income)</small>
            <h3 class="fw-bold mb-0 text-success">{{ today_income }} ฿</h3>
        </div>
    </div>

    <div class="col-md-6">
        <div class="card shadow-sm p-3 border-start border-dark border-4 bg-light">
            <small class="text-muted d-block">รายได้รวมทั้งหมด (Total Revenue)</small>
            <h3 class="fw-bold mb-0">{{ total_income }} ฿</h3>
        </div>
    </div>
</div>

        <div class="table-responsive">
            <table class="table align-middle">
                <thead>
                    <tr>
                        <th class="border-0">Order ID</th>
                        <th class="border-0">ข้อมูลลูกค้า</th>
                        <th class="border-0 text-center">แต้มสะสม</th>
                        <th class="border-0 text-center">สถานะการทำงาน</th>
                        <th class="border-0">วัน/เวลานัดรับ</th>
                        <th class="border-0">ยอดชำระ</th>
                        <th class="border-0 text-center" style="width: 120px;">จัดการ</th>
                    </tr>
                </thead>
<tbody>
    {% for order in orders %}
    <tr>
        <td><span class="fw-bold text-primary">#{{ order.order_id }}</span></td>
        
        <td>
            <div class="fw-bold">{{ order.cus.cus_name }}</div> 
            <small class="text-muted">
                <i class="fa-solid fa-phone fa-xs"></i> {{ order.cus.telephone }}
            </small>
        </td>

        <td class="text-center">
            <div class="badge bg-light text-dark border rounded-pill px-3 py-2 shadow-sm">
                <i class="fa-solid fa-star text-warning me-1"></i>
                <span class="fw-bold">{{ order.cus.total_points|default:"0" }}</span> แต้ม
            </div>
        </td> 

        <td class="text-center">
    <select class="form-select status-dropdown" 
            onchange="updateOrderStatus('{{ order.order_id }}', this.value)">
        <option value="รับผ้าแล้ว" {% if order.order_status == 'รับผ้าแล้ว' %}selected{% endif %}>รับผ้าแล้ว</option>
        <option value="กำลังดำเนินการ" {% if order.order_status == 'กำลังดำเนินการ' %}selected{% endif %}>กำลังดำเนินการ</option>
        <option value="เสร็จแล้ว" {% if order.order_status == 'เสร็จแล้ว' %}selected{% endif %}>เสร็จแล้ว</option>
        <option value="ส่งมอบแล้ว" {% if order.order_status == 'ส่งมอบแล้ว' %}selected{% endif %}>ส่งมอบแล้ว</option>
    </select>
</td>

        <td>
            <span class="small">{{ order.pickup_date|date:"d/m/Y" }}</span><br>
            <span class="small text-muted">{{ order.pickup_date|time:"H:i" }}</span>
        </td>

        <td><span class="fw-bold">{{ order.total_amount }} ฿</span></td>

        <td class="text-center">
            <div class="d-flex justify-content-center gap-1">
                <button class="btn btn-sm btn-outline-info border-0" 
                        onclick="showOrderDetails('{{ order.order_id }}')" 
                        title="ดูรายการผ้า">
                    <i class="fa-solid fa-eye"></i>
                </button>

                <button class="btn btn-sm btn-outline-primary border-0" 
                        onclick="openEditCustomer('{{ order.cus.cus_id }}', '{{ order.cus.cus_name }}', '{{ order.cus.telephone }}')">
                    <i class="fa-solid fa-user-pen"></i>
                </button>

                <button class="btn btn-sm btn-outline-danger border-0" 
                        onclick="cancelOrder('{{ order.order_id }}')">
                    <i class="fa-solid fa-trash-can"></i>
                </button>
            </div>
        </td>
    </tr>
    {% endfor %}
</tbody>
            </table>
        </div>
    </div>
</div>

<div class="modal fade" id="customerModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow-lg rounded-4">
            <div class="modal-header border-0">
                <h5 class="fw-bold">แก้ไขข้อมูลลูกค้า</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body p-4">
                <input type="hidden" id="edit_cus_id">
                <div class="mb-3">
                    <label class="form-label small fw-bold">ชื่อ-นามสกุล</label>
                    <input type="text" class="form-control rounded-3" id="edit_cus_name">
                </div>
                <div class="mb-3">
                    <label class="form-label small fw-bold">เบอร์โทรศัพท์</label>
                    <input type="text" class="form-control rounded-3" id="edit_cus_phone">
                </div>
            </div>
            <div class="modal-footer border-0">
                <button type="button" class="btn btn-light rounded-pill px-4" data-bs-dismiss="modal">ยกเลิก</button>
                <button type="button" class="btn btn-primary rounded-pill px-4" onclick="saveCustomerData()">บันทึกการแก้ไข</button>
            </div>
        </div>
    </div>
</div>

<div class="modal fade" id="orderDetailModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow-lg rounded-4">
            <div class="modal-header border-0 bg-light">
                <h5 class="fw-bold mb-0">รายการซักผ้า ออเดอร์ <span id="display_order_id" class="text-primary"></span></h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body p-4">
                <div id="order_items_list">
                    <div class="text-center text-muted">กำลังโหลดข้อมูล...</div>
                </div>
                <hr>
                <div class="d-flex justify-content-between">
                    <span class="fw-bold">ยอดรวมสุทธิ:</span>
                    <span class="fw-bold text-success" id="display_total_amount">0 ฿</span>
                </div>
            </div>
        </div>
    </div>
</div>



<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

<script>
// ฟังก์ชันจัดการสถานะ (เชื่อมต่อ SQL)
function updateStatus(orderId, newStatus) {
    fetch('/update-status/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': '{{ csrf_token }}' },
        body: JSON.stringify({ 'order_id': orderId, 'status': newStatus })
    })
    .then(res => res.json())
    .then(data => {
        if(data.status === 'success') {
            console.log("อัปเดตเรียบร้อย");
        }
    });
}

// ฟังก์ชันเปิด Modal แก้ไขลูกค้า
function openEditCustomer(id, name, phone) {
    document.getElementById('edit_cus_id').value = id;
    document.getElementById('edit_cus_name').value = name;
    document.getElementById('edit_cus_phone').value = phone;
    new bootstrap.Modal(document.getElementById('customerModal')).show();
}

// ฟังก์ชันบันทึกข้อมูลลูกค้า (ส่งไป SQL)
function saveCustomerData() {
    const id = document.getElementById('edit_cus_id').value;
    const name = document.getElementById('edit_cus_name').value;
    const phone = document.getElementById('edit_cus_phone').value;
    
    // ตรงนี้พี่ต้องไปสร้าง Path /api/update-customer/ ใน urls.py ด้วยนะ
    fetch('/api/update-customer/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': '{{ csrf_token }}' },
        body: JSON.stringify({ 'cus_id': id, 'name': name, 'phone': phone })
    })
    .then(res => res.json())
    .then(data => {
        if(data.status === 'success') {
            location.reload(); // รีเฟรชหน้าเพื่อแสดงข้อมูลใหม่
        }
    });
}

function submitAdminOrder() {
    const form = document.getElementById('combinedOrderForm');
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    // ตรวจสอบว่าอยู่ Tab ไหน (ลูกค้าเก่า หรือ สมัครใหม่)
    const activeTab = document.querySelector('#orderTab .active').innerText;
    data.mode = (activeTab === 'ลูกค้าเก่า') ? 'existing' : 'new';

    fetch('/api/admin-add-order/', { 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(data => {
        if(data.status === 'success') {
            alert('บันทึกรายการเรียบร้อยค่ะ!');
            location.reload();
        } else {
            alert('พังตรงนี้ค่ะพี่: ' + data.message);
        }
    });
}

function showOrderDetails(orderId) {
    // 1. ลบ # ออกเพื่อให้เหลือแค่ O034
    let cleanId = orderId.replace('#', '');
    
    // 2. แสดง Modal
    var myModal = new bootstrap.Modal(document.getElementById('orderDetailModal'));
    document.getElementById('display_order_id').innerText = '#' + cleanId;
    myModal.show();

    // 3. ดึงข้อมูล (ลบ / ตัวสุดท้ายออกเพื่อให้ตรงกับ urls.py ของพี่ค่ะ)
    fetch(`/get-order-details/${cleanId}`) 
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            let html = '<ul class="list-group list-group-flush">';
            
            // เช็คว่ามีรายการ items ส่งมาไหม
            if (data.items && data.items.length > 0) {
                data.items.forEach(item => {
                    html += `
                        <li class="list-group-item d-flex justify-content-between align-items-center px-0">
                            <div>
                                <span class="fw-bold">${item.service_name}</span> 
                                <small class="text-muted d-block">จำนวน ${parseInt(item.quantity)} ชิ้น</small>
                            </div>
                            <span class="text-dark">${parseFloat(item.subtotal).toLocaleString()} ฿</span>
                        </li>`;
                });
            } else {
                html += '<li class="list-group-item text-center">ไม่พบรายการผ้าในออเดอร์นี้</li>';
            }

            html += '</ul>';
            document.getElementById('order_items_list').innerHTML = html;
            document.getElementById('display_total_amount').innerText = data.total + ' ฿';
        })
        .catch(err => {
            console.error('Fetch Error:', err);
            document.getElementById('order_items_list').innerHTML = '<p class="text-danger text-center">โหลดข้อมูลไม่สำเร็จ</p>';
        });
}

function searchOrder() {
    // ดึงค่าจากช่องค้นหา
    const input = document.getElementById("searchInput");
    const filter = input.value.toLowerCase();
    const table = document.querySelector(".table");
    const tr = table.getElementsByTagName("tr");

    // วนลูปเช็คทุกแถวในตาราง (ยกเว้นหัวตาราง)
    for (let i = 1; i < tr.length; i++) {
        const orderIdCell = tr[i].getElementsByTagName("td")[0]; // คอลัมน์ Order ID
        const customerCell = tr[i].getElementsByTagName("td")[1]; // คอลัมน์ ชื่อลูกค้า
        
        if (orderIdCell || customerCell) {
            const orderText = orderIdCell.textContent || orderIdCell.innerText;
            const customerText = customerCell.textContent || customerCell.innerText;
            
            // ถ้าคำที่พิมพ์ตรงกับ Order ID หรือ ชื่อลูกค้า ให้แสดงแถวนั้น
            if (orderText.toLowerCase().indexOf(filter) > -1 || 
                customerText.toLowerCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none"; // ถ้าไม่ตรงให้ซ่อนแถวนั้น
            }
        }
    }
}

function updateOrderStatus(orderId, newStatus) {
    // ลบ # ออกเพื่อให้เหลือแค่ O016 ตรงตาม SQL
    let cleanId = orderId.replace('#', '').trim();
    
    // บรรทัดนี้จะช่วยให้พี่เห็นใน Console (F12) ว่าเลขที่ส่งไปคืออะไร
    console.log("กำลังอัปเดตออเดอร์:", cleanId, "เป็นสถานะ:", newStatus);

    fetch('/update-status/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // ใช้ฟังก์ชัน getCookie ที่พี่มีอยู่แล้ว
        },
        body: JSON.stringify({
            order_id: cleanId, 
            status: newStatus
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert(data.message || 'บันทึกสถานะและแต้มลง SQL เรียบร้อย!');
            location.reload(); 
        } else {
            alert('พังเพราะ: ' + data.message);
        }
    })
    .catch(err => alert('เชื่อมต่อ Server ไม่ได้: ' + err));
}

// ฟังก์ชันสำหรับดึง CSRF Token (จำเป็นสำหรับ Django POST)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
</script>


</body>
</html>
