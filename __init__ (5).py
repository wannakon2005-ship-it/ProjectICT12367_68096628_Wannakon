<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ร้านสะดวกซักรีด - บริการซักผ้าออนไลน์</title>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">

    <style>
        body {
            background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%);
            font-family: 'Prompt', sans-serif;
            min-height: 100vh;
            margin: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            overflow: hidden;
        }
        .background-layer {
            position: absolute;
            inset: 0;
            pointer-events: none;
            z-index: 0;
            background: radial-gradient(circle at 15% 10%, rgba(255,255,255,0.35), transparent 18%),
                        radial-gradient(circle at 80% 18%, rgba(255,255,255,0.25), transparent 22%),
                        radial-gradient(circle at 50% 70%, rgba(255,255,255,0.18), transparent 24%);
            animation: swayBackground 14s ease-in-out infinite;
        }
        .bg-icon {
            position: absolute;
            font-size: 2rem;
            opacity: 0.25;
            animation: floatIcon 12s ease-in-out infinite;
        }
        .bg-icon:nth-child(1) { top: 14%; left: 10%; animation-delay: 0s; }
        .bg-icon:nth-child(2) { top: 20%; right: 14%; animation-delay: 1.5s; }
        .bg-icon:nth-child(3) { bottom: 26%; left: 14%; animation-delay: 3s; }
        .bg-icon:nth-child(4) { bottom: 22%; right: 20%; animation-delay: 4.5s; }
        .bg-icon:nth-child(5) { top: 52%; left: 54%; animation-delay: 6s; }
        .bg-icon:nth-child(6) { top: 40%; right: 36%; animation-delay: 7.5s; }
        @keyframes floatIcon {
            0%, 100% { transform: translateY(0) rotate(0deg); opacity: 0.18; }
            50% { transform: translateY(-10px) rotate(6deg); opacity: 0.32; }
        }
        .trail-dot {
            position: absolute;
            pointer-events: none;
            width: 10px;
            height: 10px;
            background: rgba(255, 255, 255, 0.9);
            border-radius: 50%;
            opacity: 1;
            transform: translate(-50%, -50%) scale(1);
            animation: fadeTrail 0.85s ease-out forwards;
            filter: blur(0.4px);
        }
        @keyframes fadeTrail {
            to { opacity: 0; transform: translate(-50%, -50%) scale(1.6); }
        }
        @keyframes swayBackground {
            0%, 100% { transform: translateX(0) rotate(0deg); }
            50% { transform: translateX(8px) rotate(0.35deg); }
        }
        .welcome-container {
            position: relative;
            z-index: 1;
            text-align: center;
            max-width: 600px;
            padding: 40px;
        }
        .welcome-title {
            color: #4facfe;
            font-weight: 600;
            font-size: 2.5rem;
            margin-bottom: 20px;
        }
        .welcome-subtitle {
            color: #495057;
            font-size: 1.2rem;
            margin-bottom: 40px;
            line-height: 1.6;
        }
        .btn-start {
            background: linear-gradient(to right, #4facfe 0%, #00f2fe 100%);
            border: none;
            border-radius: 15px;
            padding: 20px 40px;
            font-size: 1.5rem;
            font-weight: 600;
            color: white;
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s ease;
            box-shadow: 0 8px 25px rgba(79, 172, 254, 0.3);
        }
        .btn-start:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 35px rgba(79, 172, 254, 0.5);
            color: white;
            text-decoration: none;
        }
        .btn-start i {
            margin-right: 10px;
        }
    </style>
</head>
<body>
    <div class="background-layer">
        <span class="bg-icon">🧺</span>
        <span class="bg-icon">👕</span>
        <span class="bg-icon">🧦</span>
        <span class="bg-icon">👗</span>
        <span class="bg-icon">🛏️</span>
        <span class="bg-icon">👚</span>
    </div>
    <div class="welcome-container">
        <h1 class="welcome-title">
            <i class="fa-solid fa-washing-machine"></i><br>
            ร้านสะดวกซักรีด
        </h1>
        <p class="welcome-subtitle">
            บริการซักผ้าออนไลน์ที่สะดวก รวดเร็ว และปลอดภัย<br>
            จองคิวซักผ้าได้ง่ายๆ เพียงไม่กี่คลิก
        </p>
        <a href="/login/" class="btn-start">
            <i class="fa-solid fa-plus-circle"></i>
            เริ่มใช้งาน
        </a>
    </div>

    <script>
        const trailDelay = 100;
        let lastTrail = 0;
        document.addEventListener('mousemove', function(e) {
            const now = Date.now();
            if (now - lastTrail < trailDelay) return;
            lastTrail = now;
            const dot = document.createElement('span');
            dot.className = 'trail-dot';
            dot.style.left = e.clientX + 'px';
            dot.style.top = e.clientY + 'px';
            document.body.appendChild(dot);
            setTimeout(() => {
                if (dot.parentNode) dot.parentNode.removeChild(dot);
            }, 850);
        });
    </script>
</body>
</html>