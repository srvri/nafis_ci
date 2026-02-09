// تابع تبدیل تاریخ شمسی به میلادی
function jalaliToGregorian(jy, jm, jd) {
    jy = parseInt(jy);
    jm = parseInt(jm);
    jd = parseInt(jd);
    
    let gy, gm, gd;
    
    jy += 1595;
    let days = 365 * jy + Math.floor(jy / 33) * 8 + Math.floor((jy % 33 + 3) / 4) + jd;
    
    if (jm < 7) {
        days += (jm - 1) * 31;
    } else {
        days += (jm - 7) * 30 + 186;
    }
    
    gy = 400 * Math.floor(days / 146097);
    days %= 146097;
    
    if (days >= 36525) {
        days--;
        gy += 100 * Math.floor(days / 36524);
        days %= 36524;
        
        if (days >= 365) {
            days++;
        }
    }
    
    gy += 4 * Math.floor(days / 1461);
    days %= 1461;
    
    if (days >= 366) {
        days--;
        gy += Math.floor(days / 365);
        days = days % 365;
    }
    
    gm = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334].findIndex((el, i) => {
        return i > 0 && el <= days;
    });
    
    if (gy % 400 === 0 || (gy % 100 !== 0 && gy % 4 === 0)) {
        [0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335].forEach((el, i) => {
            if (i > 0 && el <= days) gm = i;
        });
    }
    
    gd = days - [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334][gm] + 1;
    
    if (gm > 2) gd--;
    
    return [gy, gm, gd];
}

// تابع فرمت‌کردن تاریخ
function formatDate(year, month, day) {
    return year + '-' + String(month).padStart(2, '0') + '-' + String(day).padStart(2, '0');
}

// تابع جاری‌سازی هنگام تغییر input
function updateHiddenDate() {
    const year = document.getElementById('birth_year').value;
    const month = document.getElementById('birth_month').value;
    const day = document.getElementById('birth_day').value;
    
    if (year && month && day) {
        if (year.length === 4 && month.length <= 2 && day.length <= 2) {
            const [gy, gm, gd] = jalaliToGregorian(year, month, day);
            document.getElementById('birth_date_hidden').value = formatDate(gy, gm, gd);
        }
    }
}

// رویدادهای تغییر input
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('birth_year').addEventListener('input', updateHiddenDate);
    document.getElementById('birth_month').addEventListener('input', updateHiddenDate);
    document.getElementById('birth_day').addEventListener('input', updateHiddenDate);
});
