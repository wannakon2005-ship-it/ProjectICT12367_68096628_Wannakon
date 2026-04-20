from django.db import connection
import json
import random
from django.db.models import Sum, Count 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Customers, Orders, Employees
CustomerProfile = Customers
Order = Orders
from django.utils import timezone
from django.shortcuts import redirect
from .models import Orders, Customers
from .models import Orders, OrderDetails, Services

TRANSLATION_MAP = {
    'tshirt': 'เสื้อยืด',
    'white_shirt': 'เสื้อเชิ้ต',
    'coat': 'เสื้อโค้ท',
    'shorts': 'กางเกงขาสั้น',
    'jeans': 'กางเกงขายาว',
    'suit': 'ชุดสูท',
    'dress': 'ชุดเดรส',
    'curtain': 'ผ้าม่าน',
    'socks': 'ถุงเท้า',
}

def summarize_order_items(items_json):
    try:
        raw_items = json.loads(items_json)
    except Exception:
        return ''

    parts = []
    for key, item in (raw_items.items() if isinstance(raw_items, dict) else []):
        if not isinstance(item, dict):
            continue
        name = item.get('name', TRANSLATION_MAP.get(key, 'รายการทั่วไป'))
        try:
            total_qty = int(item.get('qty', item.get('wash_qty', 0) + item.get('iron_qty', 0)))
        except (TypeError, ValueError):
            total_qty = 0
        try:
            wash_qty = int(item.get('wash_qty', total_qty))
        except (TypeError, ValueError):
            wash_qty = 0
        try:
            iron_qty = int(item.get('iron_qty', 0))
        except (TypeError, ValueError):
            iron_qty = 0

        if wash_qty + iron_qty != total_qty:
            iron_qty = max(0, total_qty - wash_qty)

        details = []
        if wash_qty > 0:
            details.append(f'ซัก {wash_qty}')
        if iron_qty > 0:
            details.append(f'ซักรีด {iron_qty}')
        detail_text = ' / '.join(details) if details else 'ไม่มีรายการ'
        parts.append(f'{name} ({detail_text})')

    return ', '.join(parts)

# --- ส่วนตรวจสอบสิทธิ์ Admin ---
def is_admin(user):
    return user.is_authenticated and user.is_staff and user.is_superuser

# 0. หน้า Landing page
def index_view(request):
    return render(request, 'index.html')

# 1. หน้า เข้าสู่ระบบ
def login_view(request):
    if request.method == 'POST':
        uname = request.POST.get('username')  
        pwd = request.POST.get('password')    
        user = authenticate(request, username=uname, password=pwd)

        if user is not None:
            login(request, user)
            if user.is_staff or user.is_superuser:
                return redirect('/admin-dashboard/')
            else:
                return redirect('/servicesusers/')

        try:
            customer = Customers.objects.get(cus_name=uname, telephone=pwd)
            
            # เก็บข้อมูลลง Session เพื่อใช้ระบุตัวตนในหน้าอื่นๆ
            request.session['customer_id'] = customer.cus_id
            request.session['customer_name'] = customer.cus_name
            request.session['is_customer'] = True
            
            messages.success(request, f'ยินดีต้อนรับคุณ {customer.cus_name} เข้าสู่ระบบค่ะ')
            return redirect('/servicesusers/')
            
        except Customers.DoesNotExist:
            messages.error(request, 'ชื่อผู้ใช้ หรือ เบอร์โทรศัพท์ ไม่ถูกต้อง!')
            
    return render(request, 'login.html')

# 1.5. หน้า Logout
def logout_view(request):
    logout(request)
    return redirect('index')

# 2. หน้า สมัครสมาชิก
def register_view(request):
    from .models import Customers # นำเข้าชื่อรุ่นให้ถูก (มี s)
    
    if request.method == 'POST':
        uname = request.POST.get('username')
        pwd = request.POST.get('password')
        cpwd = request.POST.get('confirm_password')
        phone = request.POST.get('telephone')

        if pwd != cpwd:
            messages.error(request, 'รหัสผ่านและการยืนยันรหัสผ่านไม่ตรงกัน!')
            return render(request, 'register.html')
            
        if len(pwd) < 6:
            messages.error(request, 'รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร!')
            return render(request, 'register.html')

        if User.objects.filter(username=uname).exists():
            messages.error(request, 'ชื่อผู้ใช้นี้ถูกใช้งานแล้ว!')
            return render(request, 'register.html')

        try:
            # 1. สร้าง User หลักของ Django
            user = User.objects.create_user(username=uname, password=pwd)
            user.save()

            random_id = str(random.randint(10000, 99999))

            # 2. บันทึกข้อมูลลงตาราง Customers ใน SQL Server 
            # สำคัญ: ในโมเดลพี่ไม่มีช่อง 'user' ให้ใส่แค่ชื่อลูกค้าไปก่อนค่ะ
            Customers.objects.create(
                cus_id=random_id,       # ส่ง ID ที่สุ่มมา (Primary Key)
                cus_name=uname,         # ใช้ username เป็นชื่อลูกค้า
                room_id='000',          # ใส่ค่าเริ่มต้น (เพราะห้ามว่าง)
                telephone=phone,          # ใส่ค่าเริ่มต้น
                regist_date=timezone.now().date(), # ส่งวันที่สมัคร (DateField)
                total_points=0          # เริ่มต้นที่ 0 แต้ม
            )

            messages.success(request, 'สมัครสมาชิกสำเร็จ! กรุณาเข้าสู่ระบบ')
            return redirect('login') # หรือเปลี่ยนเป็นชื่อ URL หน้า login ของพี่
        except Exception as e:
            if 'user' in locals():
                user.delete()
            messages.error(request, f'เกิดข้อผิดพลาด: {str(e)}')
            
    return render(request, 'register.html')

# 3. หน้า เลือกบริการซักผ้า (ลูกค้าสั่งออเดอร์)
def users_view(request):
    from .models import Customers # หรือชื่อ Model ที่เก็บข้อมูลลูกค้า
    customers = Customers.objects.all()
    
    cus_id = request.session.get('customer_id')
    if not cus_id:
        messages.error(request, 'กรุณาเข้าสู่ระบบก่อนใช้บริการค่ะ')
        return redirect('login') 

    try:
        current_customer = Customers.objects.get(cus_id=cus_id)
    except Customers.DoesNotExist:
        return redirect('login')

    if request.method == 'POST':
        # ดึงค่าจากฟอร์ม
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        pickup_date = request.POST.get('pickup_date')
        times = request.POST.get('times')
        cart_data_str = request.POST.get('cart_data')
        used_points = int(request.POST.get('used_points', 0))
        
        payment_method_raw = request.POST.get('payment_method')
        payment_th = "เงินสด (ชำระหน้าร้าน)" if payment_method_raw == 'cash' else "โอนเงิน / สแกน QR"

        try:
            cart_data = json.loads(cart_data_str)
        except:
            cart_data = {}

        total_price = 0
        items_list = []
        
        # คำนวณราคา
        for key, item in cart_data.items():
            qty = int(item.get('qty', 0))
            if qty > 0:
                # 1. ต้องกำหนดค่าตัวแปรพวกนี้ "ก่อน" สั่ง append ค่ะ
                price = int(item.get('price', 0))
                
                # ดึงค่าจาก item หรือถ้าไม่มีให้ใช้ค่าเริ่มต้น
                wash_qty = int(item.get('wash_qty', qty)) 
                iron_qty = int(item.get('iron_qty', 0))
                wash_price = int(item.get('wash_price', price))
                
                # 2. คำนวณราคารายการนี้
                item_total = (wash_qty * wash_price) + (iron_qty * int(item.get('iron_price', 0)))
                total_price += item_total
                
                # 3. สั่ง append หลังจากมีค่าตัวแปรครบแล้ว
                items_list.append({
                    'name': item.get('name', key),
                    'qty': qty,
                    'wash_qty': wash_qty,
                    'iron_qty': iron_qty,
                    'wash_price': wash_price,
                    'item_total': item_total,
                })

        # คำนวณส่วนลดจากแต้ม
        discount = used_points // 50 
        final_total = max(total_price - discount, 0)

        # บันทึกแต้มใหม่ลงในตาราง Customers
        current_customer.total_points = max(current_customer.total_points - (discount * 100), 0)
        current_customer.save()

        # ส่งข้อมูลไปหน้ายืนยัน (Confirm/Receipt)
        context = {
            'customer': current_customer,
            'items_list': items_list,
            'total_price': total_price,
            'discount': discount,
            'final_total': final_total,
            'payment_method': payment_th,
            
            # --- จุดที่ต้องเพิ่มเพื่อให้ข้อมูล "วันที่/เวลานัด" และ "เวลาออเดอร์" แสดงผล ---
            'order': {
                'order_id': random.randint(10000, 99999),
                'pickup_date': pickup_date,
                'times': times,
                'created_at': timezone.now(), # บันทึกเวลาปัจจุบันที่สั่งออเดอร์สำเร็จ
            },
        }
        return render(request, 'confirm.html', context)

    # --- ส่วนที่ 4: ถ้าเป็นการเข้าหน้าเว็บปกติ (GET) ---
    context = {
        'customer': current_customer, # ส่งข้อมูลลูกค้าคนนี้ไปโชว์ชื่อ/แต้ม
        'user_points': current_customer.total_points,
    }
    return render(request, 'servicesusers.html', context)

# 4. API สร้างออเดอร์แบบ AJAX เพื่อให้หน้าเว็บไม่รีเฟรช
import json
from django.http import JsonResponse
from django.utils import timezone
from .models import Orders

# ในไฟล์ views.py
import json
from django.http import JsonResponse
from django.db.models import Max
from django.utils import timezone
from .models import Orders, Customers, Employees
from django.db import transaction

def submit_order_ajax(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid method'})

    try:
        data = json.loads(request.body)
        items = data.get('items', [])

        # 1. รัน Order ID (O001...)
        max_id = Orders.objects.all().aggregate(Max('order_id'))['order_id__max']
        if max_id:
            new_number = int(max_id[1:]) + 1
        else:
            new_number = 1
        o_id = 'O' + str(new_number).zfill(3)

        # 2. ดึงข้อมูลลูกค้า และพนักงาน (E001)
        try:
            customer_obj = Customers.objects.get(cus_id=request.user.username)
            # พี่ต้องมั่นใจว่าในตาราง Employees มีรหัส E001 อยู่จริงนะคะ
            employee_obj = Employees.objects.get(emp_id='E001') 
        except Exception:
            return JsonResponse({'status': 'error', 'message': 'ไม่พบข้อมูลลูกค้าหรือพนักงานในระบบ'})

        # 3. เริ่มบันทึกแบบ Transaction (ถ้าพัง ให้ยกเลิกทั้งหมด)
        with transaction.atomic():
            # บันทึกหัวออเดอร์ (Orders)
            new_order = Orders.objects.create(
                order_id=o_id,
                cus=customer_obj,
                order_date=timezone.now(),
                pickup_date=data.get('pickup_date'), # ส่งวันที่จาก JS เข้า DateTimeField ตรงๆ
                is_express=data.get('is_express', 'ปกติ'),
                total_amount=data.get('total_price'),
                order_status='รับผ้าแล้ว',
                emp=employee_obj,
                discount_amount=0
            )

            # บันทึกรายละเอียดผ้า (OrderDetails)
            for item in items:
                service_obj = Services.objects.get(service_id=item['service_id'])
                
                OrderDetails.objects.create(
                    order=new_order,
                    service=service_obj,
                    quantity=item['quantity'],
                    unit_price=service_obj.price, # ต้องใส่! เพราะ Model พี่บังคับ
                    sub_total=item['subtotal']    # ต้องใส่! เพราะ Model พี่บังคับ
                )

        return JsonResponse({'status': 'success', 'order_id': o_id})

    except Exception as e:
        # ถ้ายังพังอีก ให้มันบอกชื่อฟิลด์ที่พังออกมาเลยค่ะ
        return JsonResponse({'status': 'error', 'message': f'SQL Error: {str(e)}'})

# 5. API ให้ข้อมูลคะแนนลูกค้าปัจจุบัน
def customer_points_api(request):
    all_customers = Customers.objects.all()
    items = []
    for c in all_customers:
        items.append({
            'id': c.cus_id,         
            'name': c.cus_name,     
            'points': c.total_points 
        })
    return JsonResponse({'status': 'success', 'customers': items})

def current_points_api(request):
    if request.user.is_authenticated:
        profile, _ = CustomerProfile.objects.get_or_create(user=request.user)
        return JsonResponse({'status': 'success', 'points': profile.points})
    return JsonResponse({'status': 'success', 'points': 0})

# 7. API ให้ข้อมูลออเดอร์ปัจจุบันสำหรับ real-time updates
def get_orders_api(request):
    from .models import Orders as Order
    orders = Order.objects.all().order_by('-order_date')

    orders_data = []
    for order in orders:
        orders_data.append({
            'order_id': order.order_id,
            'customer_name': order.cus.cus_name if order.cus else '-',
            # ดึงเบอร์จากตาราง Customers ผ่านความสัมพันธ์ cus
            'phone': order.cus.telephone if order.cus else '-', 
            'pickup_date': order.order_date.strftime('%d/%m/%Y %H:%M') if order.order_date else '-',
            
            # แสดงสถานะตามที่พิมพ์ใน SQL เป๊ะๆ
            'status': order.order_status,          
            'status_display': order.order_status, 
            
            'total_price': f"{order.total_amount:,.2f}",
            'item_summary': 'ซักพับ/ซักรีด', 
        })
    return JsonResponse({'status': 'success', 'orders': orders_data})

# 6. หน้า Admin Dashboard
@user_passes_test(is_admin)
def admin_dashboard(request):
    # 1. ดึงข้อมูลพื้นฐาน (ใช้ชื่อรุ่นที่พี่ตั้งไว้คือ Order และ CustomerProfile)
    all_orders = Order.objects.select_related('cus').all().order_by('-order_id')
    today = timezone.now().date()
    
    # 2. คำนวณรายได้ (Sum) - ใช้ฟิลด์ total_amount ตาม Model พี่เป๊ะๆ
    # รวมรายได้ทั้งหมด
    total_income_data = all_orders.aggregate(total=Sum('total_amount'))
    total_income = total_income_data['total'] or 0
    
    # รวมรายได้เฉพาะวันนี้ (กรองจาก order_date)
    today_income_data = all_orders.filter(order_date__date=today).aggregate(total=Sum('total_amount'))
    today_income = today_income_data['total'] or 0

    # 3. จัดชุดข้อมูลลง Context (ใช้ชื่อตัวแปรที่ HTML ของพี่รอรับอยู่)
    context = {
        'orders': all_orders,
        'all_customers': CustomerProfile.objects.all(),
        
        # ตัวเลขจำนวนออเดอร์
        'today_count': all_orders.filter(order_date__date=today).count(),
        'total_count': all_orders.count(),
        
        # สถานะ (สะกดตามที่พี่บอกว่ามีใน SQL: รับผ้าแล้ว, กำลังดำเนินการ, เสร็จแล้ว, ส่งมอบแล้ว)
        'washing_count': all_orders.filter(order_status='กำลังดำเนินการ').count(),
        'finished_count': all_orders.filter(order_status='เสร็จแล้ว').count(),
        'returned_count': all_orders.filter(order_status='ส่งมอบแล้ว').count(),
        
        # ยอดรายได้
        'today_income': today_income,
        'total_income': total_income,
    }
    
    # เช็ค DEBUG ในจอดำตอนรัน server ว่ายอดรวมขึ้นไหม
    print(f"DEBUG: รายได้รวมที่คำนวณได้ = {total_income}")
    
    return render(request, 'admin_dashboard.html', context)

# 5. API อัปเดตสถานะ 
@csrf_exempt
def update_order_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # รับ order_id มาจาก JS (เช่น O016)
            order_pk = data.get('order_id')
            new_status = data.get('status')

            # 1. ค้นหาออเดอร์ (ใช้ order_id= ตาม models.py บรรทัด 47)
            order = Orders.objects.get(order_id=order_pk)
            
            # เก็บสถานะเดิมไว้เพื่อเช็คก่อนเพิ่มแต้ม
            previous_status = order.order_status
            
            # 2. อัปเดตสถานะใหม่ลง SQL (ใช้ order_status ตาม models.py บรรทัด 54)
            order.order_status = new_status
            order.save() 

            response_data = {'status': 'success'}

            # --- 🟢 ส่วนเก็บแต้ม: ทำงานเมื่อเปลี่ยนเป็น 'ส่งมอบแล้ว' 🟢 ---
            # เช็คคำว่า "ส่งมอบแล้ว" ให้ตรงกับหน้าเว็บพี่
            if new_status == 'ส่งมอบแล้ว' and previous_status != 'ส่งมอบแล้ว':
                # เข้าถึงลูกค้าผ่าน ForeignKey 'cus' (ตาม models.py บรรทัด 48)
                customer = order.cus 
                if customer:
                    # เพิ่มแต้มใน 'total_points' (ตาม models.py บรรทัด 24)
                    # ใช้ยอด 'total_amount' (ตาม models.py บรรทัด 51)
                    added_points = int(order.total_amount)
                    customer.total_points += added_points
                    customer.save()
                    
                    response_data['message'] = f'อัปเดตสถานะและเพิ่ม {added_points} แต้มแล้ว'
            else:
                response_data['message'] = 'อัปเดตสถานะใน SQL เรียบร้อย'

            return JsonResponse(response_data)

        except Orders.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': f'ไม่พบออเดอร์ {order_pk}'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

# Cancel Order
@csrf_exempt
def cancel_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order_pk = data.get('id')
            order = Order.objects.get(id=order_pk)
            
            if order.status == 'cancelled':
                return JsonResponse({'status': 'error', 'message': 'รายการนี้ถูกยกเลิกแล้ว'})
            
            if order.status == 'delivered':
                return JsonResponse({'status': 'error', 'message': 'ไม่สามารถยกเลิกรายการที่ส่งแล้ว'})         
            order.status = 'cancelled'
            order.save()
            return JsonResponse({'status': 'success', 'message': 'ยกเลิกรายการสำเร็จ'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

@csrf_exempt
def clear_history(request):
    if request.method == 'POST':
        try:
            deleted, _ = Order.objects.filter(status='delivered').delete()
            return JsonResponse({'status': 'success', 'deleted_count': deleted})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def confirm_view(request):
    from .models import Customers, Order # มั่นใจว่า import มาครบ
    import json

    order_id = request.GET.get('order_id')
    payment_method = request.GET.get('payment_method', 'เงินสด (ชำระหน้าร้าน)')
    
    if not order_id:
        return redirect('/servicesusers/')

    # 1. ดึงข้อมูลออเดอร์
    order = get_object_or_404(Order, order_id=order_id)

    # 2. ดึงข้อมูลลูกค้า (จุดที่เพิ่มเข้ามา!)
    # เราใช้ cus_id จากตัว order มาค้นหาในตาราง Customers
    try:
        current_customer = Customers.objects.get(cus_id=order.cus_id)
    except Customers.DoesNotExist:
        current_customer = None

    # 3. จัดการรายการผ้า (Logic เดิมของพี่)
    items_list = []
    try:
        raw_items = json.loads(order.items_json)
        for key, item in raw_items.items():
            if not isinstance(item, dict): continue
            
            total_qty = int(item.get('qty', 0))
            wash_qty = int(item.get('wash_qty', total_qty))
            iron_qty = int(item.get('iron_qty', 0))
            wash_price = int(item.get('wash_price', 0))
            iron_price = int(item.get('iron_price', 0))
            
            item_total = (wash_qty * wash_price) + (iron_qty * iron_price)
            items_list.append({
                'name': item.get('name', key),
                'total_qty': total_qty,
                'item_total': item_total,
                # พี่สามารถเพิ่มรายละเอียดอื่นๆ ได้ตามต้องการค่ะ
            })
    except:
        items_list = []

    # 4. ส่งค่าไปที่หน้าเว็บ (ต้องมีคำว่า 'customer'!)
    context = {
        'order': order,
        'order_time': order.created_at, # ดึงเวลาที่บันทึกจาก Model Order
        'customer': current_customer,
        'payment_method': payment_method,
        'items_list': items_list,
        'final_total': order.total_amount,
        'discount': 0,
    }
    return render(request, 'confirm.html', context)


from .models import VOrderstatus, VDailyrevenue

def get_dashboard_stats(request):
    from .models import Orders as Order
    from django.utils import timezone
    
    # 1. งานใหม่วันนี้
    new_orders = Order.objects.filter(order_date__date=timezone.now().date()).count()
    
    # 2. กำลังดำเนินการ (ต้องสะกดให้ตรงกับในตาราง SQL ของคุณเป๊ะๆ)
    # สมมติใน SQL ของคุณใช้คำว่า 'กำลังดำเนินการ'
    processing = Order.objects.filter(order_status='กำลังดำเนินการ').count()
    
    # 3. รอรับผ้าคืน (สมมติใน SQL ใช้คำว่า 'เสร็จแล้ว')
    ready_to_pickup = Order.objects.filter(order_status='เสร็จแล้ว').count()
    
    # 4. รายรับทั้งหมด
    total_revenue = Order.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    return JsonResponse({
        'status': 'success',
        'new_orders': new_orders,
        'processing': processing,
        'ready_to_pickup': ready_to_pickup,
        'total_revenue': float(total_revenue)
    })

def get_order_history_api(request):
    from .models import Orders as Order
    from django.http import JsonResponse
    
    # ดึงเฉพาะรายการที่สถานะคือ 'ส่งมอบแล้ว'
    history_orders = Order.objects.filter(order_status='ส่งมอบแล้ว').order_by('-order_date')

    data = []
    for order in history_orders:
        data.append({
            'order_id': order.order_id,
            'cus_name': order.cus.cus_name if order.cus else '-',
            'order_date': order.order_date.strftime('%d/%m/%Y') if order.order_date else '-',
            'pickup_date': order.actual_pickup_date.strftime('%d/%m/%Y') if order.actual_pickup_date else '-',
            'total_price': f"{order.total_amount:,.2f}",
            'status': order.order_status,
        })
    return JsonResponse({'status': 'success', 'history': data})

def get_loyalty_data_api(request):
    from django.db import connection
    try:
        with connection.cursor() as cursor:
            # เช็กตรงนี้: ถ้าใน SQL ชื่อ Customer (ไม่มี s) ต้องเขียนแบบนี้เป๊ะๆ
            cursor.execute("SELECT Cus_name, Telephone, Total_Points FROM dbo.Customers")
            rows = cursor.fetchall()

        data = []
        for row in rows:
            data.append({
                'name': str(row[0]),
                'phone': str(row[1]) if row[1] else '-',
                'points': int(row[2]) if row[2] is not None else 0
            })
        return JsonResponse({'status': 'success', 'customers': data})

    except Exception as e:
        print(f"SQL Error: {e}") 
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    from django.http import JsonResponse
from django.db import connection # สำหรับ SQL โดยตรง

# ใน views.py
def save_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # --- 🟢 จุดที่พี่ต้องแก้ 🟢 ---
            # เดิมพี่อาจจะใช้ request.user.username 
            # ให้เปลี่ยนมาใช้ ID ของลูกค้าที่ล็อกอินอยู่จริงๆ ผ่าน Django Session ค่ะ
            
            if request.user.is_authenticated:
                # บังคับดึง Username ของคนที่ล็อกอิน ณ ตอนนั้น (เช่น Earth)
                customer_id = request.user.username 
            else:
                # ถ้าไม่ได้ล็อกอิน (เช่น แอดมินคีย์ให้) ให้ดึงจากข้อมูลที่ส่งมา
                customer_id = data.get('cus_id', 'C032')

            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Orders (Order_ID, Cus_ID, Order_Status, Order_Date, Total_Amount)
                    VALUES (%s, %s, %s, GETDATE(), %s)
                """, [
                    data['order_id'], 
                    customer_id,      # บันทึกด้วย ID ที่เราเช็คแล้วว่าคือคนสั่งจริง
                    'รับผ้าแล้ว', 
                    data['total']
                ])
                
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    def admin_add_order(request):
      if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # ตรวจสอบว่าต้องสร้างลูกค้าใหม่ไหม
            if data.get('new_cus_name'):
                customer = Customers.objects.create(
                    cus_name=data['new_cus_name'],
                    phone=data['new_cus_phone']
                )
            else:
                customer = Customers.objects.get(id=data['cus_id'])

            # บันทึกออเดอร์ (ระวังเรื่องชื่อ field ให้ตรงกับใน SQL นะคะ)
            new_order = Order.objects.create(
                customer=customer,
                total_price=data['total_price'],
                status='รับผ้าแล้ว'
            )
            return JsonResponse({'status': 'success', 'id': new_order.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

from django.http import JsonResponse
from .models import OrderDetails, Orders

def get_order_details(request, order_id):
    # ลบ # ออกให้เหลือ O034
    clean_id = order_id.replace('#', '')
    
    try:
        # 1. ดึงข้อมูลออเดอร์หลักเพื่อเอายอดรวม (อันนี้พี่ทำผ่านแล้ว ยอดเลยขึ้น 48)
        order_main = Orders.objects.get(order_id=clean_id)
        
        # 2. ดึงรายละเอียดผ้า (ต้องระวังชื่อฟิลด์ 'order_id' ใน filter)
        # พี่ใช้ OrderDetails (มี s) ตามที่ส่งมานะคะ
        items = OrderDetails.objects.filter(order_id=clean_id)
        
        order_list = []
        for item in items:
            # ดึงชื่อรายการจากตาราง Services ผ่านความสัมพันธ์
            # ใช้ item.service.item_name ตามชื่อคอลัมน์ใน SQL
            order_list.append({
                'service_name': item.service.item_name, 
                'quantity': int(item.quantity),
                'subtotal': float(item.sub_total) 
            })

        return JsonResponse({
            'items': order_list, 
            'total': float(order_main.total_amount)
        })

    except Exception as e:
        # ถ้าพังตรงไหน ให้มันฟ้องออกมาเลยค่ะ
        return JsonResponse({'error': str(e)}, status=404)