# 🔧 Troubleshooting Guide - Ghibli Cake Video Generator

## المشاكل الشائعة وحلولها

### ❌ المشكلة: الفيديو لا يتحمل / لا يتم إنشاء الفيديو

#### الحل 1: استخدم جودة منخفضة للاختبار
```bash
python main.py low
```
هذا سيقلل من الموارد المطلوبة بشكل كبير.

#### الحل 2: تحقق من المتطلبات
```bash
pip install --upgrade moviepy scipy numpy opencv-python Pillow
```

#### الحل 3: تأكد من تثبيت FFmpeg
- **Linux (Ubuntu/Debian):**
  ```bash
  sudo apt-get install ffmpeg
  ```
- **macOS:**
  ```bash
  brew install ffmpeg
  ```
- **Windows:**
  - استخدم [FFmpeg Official](https://ffmpeg.org/download.html)
  - أو عبر Chocolatey: `choco install ffmpeg`

---

### ❌ المشكلة: خطأ "No such file or directory"

**السبب:** ملفات الإطارات لم تُنشأ بشكل صحيح

**الحل:**
```bash
rm -rf output/
python main.py low
```

---

### ❌ المشكلة: استهلاك عالي للذاكرة

**الحل:**
1. استخدم جودة منخفضة:
   ```bash
   python main.py low
   ```

2. أغلق التطبيقات الأخرى

3. تحقق من المساحة الحرة على القرص (يجب أن تكون على الأقل 2GB)

---

### ❌ المشكلة: "KeyError" أو "ImportError"

**السبب:** مشكلة في المتطلبات

**الحل:**
```bash
pip install -r requirements.txt --force-reinstall
python main.py low
```

---

### ❌ المشكلة: الصوت غير موجود في الفيديو

**الحل:**
1. تأكد من أن `scipy` مثبت:
   ```bash
   pip install --upgrade scipy
   ```

2. حاول من جديد:
   ```bash
   python main.py
   ```

---

## 🎯 نصائح الأداء

| الخيار | السرعة | جودة | حجم الملف | ذاكرة |
|--------|--------|-------|---------|-------|
| `low` | ⚡⚡⚡ | ⭐⭐ | ~100MB | منخفض |
| `medium` | ⚡⚡ | ⭐⭐⭐ | ~200MB | متوسط |
| `high` | ⚡ | ⭐⭐⭐⭐ | ~400MB | عالي |

---

## 📊 الخطوات التفصيلية

### خطوة 1: تحضير البيئة
```bash
# تثبيت المتطلبات
pip install -r requirements.txt

# تحقق من FFmpeg
ffmpeg -version
```

### خطوة 2: تشغيل البرنامج
```bash
# أول محاولة (جودة منخفضة للاختبار)
python main.py low

# إذا نجح، جرب جودة متوسطة
python main.py medium

# للجودة العالية (قد يستغرق وقت طويل)
python main.py high
```

### خطوة 3: تحقق من النتيجة
```bash
# الملف سيكون موجود في:
output/ghibli_chocolate_cake.mp4
```

---

## 🐛 تصحيح الأخطاء

إذا واجهت خطأ، تحقق من المعلومات التالية:

```python
# أضف هذا في main.py لترى معلومات النظام
import platform
import sys

print(f"Python Version: {sys.version}")
print(f"Platform: {platform.system()} {platform.release()}")
print(f"Processor: {platform.processor()}")
```

---

## 📞 احصل على المساعدة

1. **تحقق من رسالة الخطأ** - اقرأ الرسالة الحمراء بعناية
2. **جرب جودة منخفضة** - `python main.py low`
3. **أعد تثبيت المتطلبات** - `pip install -r requirements.txt --force-reinstall`
4. **افسح مساحة على القرص** - تأكد من وجود 2GB متاح
5. **أعد تشغيل الكمبيوتر** - قد يساعد في تحرير الموارد

---

## ✅ علامات النجاح

عندما يعمل كل شيء بشكل صحيح، يجب أن ترى:

```
✓ Intro frame created
✓ crack_eggs frame created
✓ add_sugar frame created
✓ pour_liquids frame created
✓ sift_dry frame created
✓ whisk_batter frame created
✓ pour_batter frame created
✓ oven frame created
✓ outro frame created
✓ ASMR audio track created
✓ Video created successfully!
📁 Output: output/ghibli_chocolate_cake.mp4
```

---

**أخر تحديث:** September 2026
