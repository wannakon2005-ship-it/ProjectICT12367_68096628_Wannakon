from django.urls import path
from . import views # ใช้ . แทนชื่อแอปเพื่อให้ยืดหยุ่นและลดโอกาส Error

urlpatterns = [
    path('api/loyalty/', views.get_loyalty_data_api, name='loyalty_api'),
    path('api/order-history/', views.get_order_history_api, name='order_history_api'),
    path('api/dashboard-stats/', views.get_dashboard_stats, name='dashboard_stats'),

    # 0. หน้าแรก Landing page - http://127.0.0.1:8000/
    path('', views.index_view, name='index'), 

    # 1. หน้าเข้าสู่ระบบ - http://127.0.0.1:8000/login/
    path('login/', views.login_view, name='login'), 
    path('logout/', views.logout_view, name='logout'),
    
    # 2. หน้าสมัครสมาชิก - http://127.0.0.1:8000/register/
    path('register/', views.register_view, name='register'), 
    
    # 3. หน้าเลือกบริการซักผ้า (สำหรับลูกค้า) - http://127.0.0.1:8000/servicesusers/
    path('servicesusers/', views.users_view, name='servicesusers'), 
    
    # 4. หน้ายืนยันการจอง - http://127.0.0.1:8000/confirm/
    path('confirm/', views.confirm_view, name='confirm'),

    # 5. หน้าแอดมินแดชบอร์ด (สำหรับแอดมิน) - http://127.0.0.1:8000/admin-dashboard/
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('api/submit-order/', views.submit_order_ajax, name='submit_order_ajax'),
    path('api/customer-points/', views.customer_points_api, name='customer_points_api'),
    path('api/orders/', views.get_orders_api, name='get_orders_api'),
    path('api/current-points/', views.current_points_api, name='current_points_api'),
    path('api/clear-history/', views.clear_history, name='clear_history'),

    # 6. ช่องทางส่งข้อมูลอัปเดตสถานะ (API) - สำหรับปุ่มกดในหน้า Admin
    # เส้นทางนี้สำคัญมาก ห้ามลบ! เพราะใช้ซิงค์สถานะลงฐานข้อมูล
    path('update-status/', views.update_order_status, name='update_status'),
    path('cancel-order/', views.cancel_order, name='cancel_order'),
    path('get-order-details/<str:order_id>/', views.get_order_details, name='get_order_details'),
]