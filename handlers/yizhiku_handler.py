from datetime import datetime, timedelta

def get_current_quarter_result():
    # 东八区时间
    now = datetime.utcnow() + timedelta(hours=8)
    minute = (now.minute // 15) * 15
    current_key = now.replace(minute=minute, second=0, microsecond=0).strftime("%H:%M:%S")
    next_key = (now + timedelta(minutes=15)).replace(minute=((now.minute // 15 + 1) % 4) * 15, second=0, microsecond=0).strftime("%H:%M:%S")

    # time table（你也可以分离出去）
    time_table = {
        "00:00:00": "东-9,南-0,西-1,北-9",
        "00:15:00": "东-9,南-0,西-1,北-0",
        "00:30:00": "东-9,南-0,西-1,北-1",
        "00:45:00": "东-9,南-0,西-1,北-2",
        "01:00:00": "东-9,南-0,西-1,北-3",
        "01:15:00": "东-9,南-0,西-1,北-4",
        "01:30:00": "东-9,南-0,西-1,北-4",
        "01:45:00": "东-9,南-0,西-1,北-4",
        "02:00:00": "东-9,南-0,西-1,北-4",
        "02:15:00": "东-9,南-0,西-1,北-4",
        "02:30:00": "东-9,南-0,西-1,北-4",
        "02:45:00": "东-9,南-0,西-1,北-4",
        "03:00:00": "东-9,南-0,西-1,北-3",
        "03:15:00": "东-9,南-0,西-1,北-2",
        "03:30:00": "东-9,南-0,西-1,北-1",
        "03:45:00": "东-9,南-0,西-1,北-0",
        "04:00:00": "东-9,南-0,西-1,北-9",
        "04:15:00": "东-9,南-0,西-1,北-8",
        "04:30:00": "东-9,南-0,西-1,北-7",
        "04:45:00": "东-9,南-0,西-1,北-6",
        "05:00:00": "南-0,西-1,北-4,东-0",
        "05:15:00": "南-0,西-1,北-4,东-1",
        "05:30:00": "南-0,西-1,北-4,东-2",
        "05:45:00": "南-0,西-1,北-4,东-3",
        "06:00:00": "南-0,西-1,北-4,东-4",
        "06:15:00": "南-0,西-1,北-4,东-5",
        "06:30:00": "南-0,西-1,北-4,东-6",
        "06:45:00": "南-0,西-1,北-4,东-7",
        "07:00:00": "南-0,西-1,北-4,东-8",
        "07:15:00": "南-0,西-1,北-4,东-9",
        "07:30:00": "南-0,西-1,北-4,东-9",
        "07:45:00": "南-0,西-1,北-4,东-9",
        "08:00:00": "南-0,西-1,北-4,东-9",
        "08:15:00": "南-0,西-1,北-4,东-9",
        "08:30:00": "南-0,西-1,北-4,东-9",
        "08:45:00": "南-0,西-1,北-4,东-9",
        "09:00:00": "南-0,西-1,北-4,东-8",
        "09:15:00": "南-0,西-1,北-4,东-7",
        "09:30:00": "南-0,西-1,北-4,东-6",
        "09:45:00": "南-0,西-1,北-4,东-5",
        "10:00:00": "南-0,西-1,北-4,东-4",
        "10:15:00": "南-0,西-1,北-4,东-3",
        "10:30:00": "南-0,西-1,北-4,东-2",
        "10:45:00": "南-0,西-1,北-4,东-1",
        "11:00:00": "东-9,西-1,北-4,南-1",
        "11:15:00": "东-9,西-1,北-4,南-2",
        "11:30:00": "东-9,西-1,北-4,南-3",
        "11:45:00": "东-9,西-1,北-4,南-4",
        "12:00:00": "东-9,西-1,北-4,南-5",
        "12:15:00": "东-9,西-1,北-4,南-6",
        "12:30:00": "东-9,西-1,北-4,南-7",
        "12:45:00": "东-9,西-1,北-4,南-8",
        "13:00:00": "东-9,西-1,北-4,南-0",
        "13:15:00": "东-9,西-1,北-4,南-0",
        "13:30:00": "东-9,西-1,北-4,南-0",
        "13:45:00": "东-9,西-1,北-4,南-0",
        "14:00:00": "东-9,西-1,北-4,南-0",
        "14:15:00": "东-9,西-1,北-4,南-0",
        "14:30:00": "东-9,西-1,北-4,南-0",
        "14:45:00": "东-9,西-1,北-4,南-0",
        "15:00:00": "东-9,西-1,北-4,南-9",
        "15:15:00": "东-9,西-1,北-4,南-8",
        "15:30:00": "东-9,西-1,北-4,南-7",
        "15:45:00": "东-9,西-1,北-4,南-6",
        "16:00:00": "东-9,西-1,北-4,南-5",
        "16:15:00": "东-9,西-1,北-4,南-4",
        "16:30:00": "东-9,西-1,北-4,南-3",
        "16:45:00": "东-9,西-1,北-4,南-2",
        "17:00:00": "东-9,南-0,北-4,西-2",
        "17:15:00": "东-9,南-0,北-4,西-3",
        "17:30:00": "东-9,南-0,北-4,西-4",
        "17:45:00": "东-9,南-0,北-4,西-5",
        "18:00:00": "东-9,南-0,北-4,西-6",
        "18:15:00": "东-9,南-0,北-4,西-7",
        "18:30:00": "东-9,南-0,北-4,西-8",
        "18:45:00": "东-9,南-0,北-4,西-9",
        "19:00:00": "东-9,南-0,北-4,西-1",
        "19:15:00": "东-9,南-0,北-4,西-1",
        "19:30:00": "东-9,南-0,北-4,西-1",
        "19:45:00": "东-9,南-0,北-4,西-1",
        "20:00:00": "东-9,南-0,北-4,西-1",
        "20:15:00": "东-9,南-0,北-4,西-1",
        "20:30:00": "东-9,南-0,北-4,西-1",
        "20:45:00": "东-9,南-0,北-4,西-1",
        "21:00:00": "东-9,南-0,北-4,西-0",
        "21:15:00": "东-9,南-0,北-4,西-9",
        "21:30:00": "东-9,南-0,北-4,西-8",
        "21:45:00": "东-9,南-0,北-4,西-7",
        "22:00:00": "东-9,南-0,北-4,西-6",
        "22:15:00": "东-9,南-0,北-4,西-5",
        "22:30:00": "东-9,南-0,北-4,西-4",
        "22:45:00": "东-9,南-0,北-4,西-3",
        "23:00:00": "东-9,南-0,西-1,北-5",
        "23:15:00": "东-9,南-0,西-1,北-6",
        "23:30:00": "东-9,南-0,西-1,北-7",
        "23:45:00": "东-9,南-0,西-1,北-8"
    }

    current_result = time_table.get(current_key, "无匹配结果")
    next_result = time_table.get(next_key, "无匹配结果")

    return {
        "content": (
            f"🕵️ 一之窟暗器解密助手\n"
            f"当前时间段（{current_key}）：{current_result}\n"
            f"下一个时间段（{next_key}）：{next_result}"
        )
    }
