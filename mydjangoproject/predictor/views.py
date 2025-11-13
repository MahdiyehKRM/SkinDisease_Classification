from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
from django.contrib.auth.decorators import login_required

MODEL = tf.keras.models.load_model("my_model_resnet_final_c.keras")
CLASS_NAMES = [
    '1.Eczema',
    '2.Melanoma',
    '4.Basel Cell Carcinoma(BCC)',
    '5.Melanocytic Nevi(NV)',
    '7.Psoriasis pictures Lichen Planus and related diseases'
]

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image

@csrf_exempt
@login_required
def predict(request):
    context = {}  
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        image = read_file_as_image(file.read())
        img_batch = np.expand_dims(image, 0)

        predictions = MODEL.predict(img_batch)
        confidence = np.max(predictions[0])
        predicted_class = CLASS_NAMES[np.argmax(predictions[0])]

      
        if confidence < 0.6:
            message = 'ما نمی‌توانیم بیماری را پیش‌بینی کنیم یا تصویر بارگذاری شده یک تصویر پوستی نیست.'
        elif 'Eczema' in predicted_class:
            message = 'شما دچار عارضه‌ی پوستی اگزما هستید. برای مدیریت این بیماری، توصیه می‌شود از مرطوب‌کننده‌های بدون عطر استفاده کرده و پوست خود را همواره مرطوب نگه دارید. از صابون‌ها و مواد شوینده ملایم و بدون عطر بهره ببرید و از تماس با مواد محرک مانند مواد شیمیایی قوی پرهیز کنید. همچنین، مدیریت استرس و خودداری از خاراندن پوست نیز می‌تواند مؤثر باشد. بهتر است برای مشاوره و درمان تخصصی، به پزشک مراجعه کنید.'
        elif 'Melanoma' in predicted_class:
            message = 'شما دچار عارضه‌ی پوستی ملانوما هستید. برای مدیریت این بیماری، از مواجهه با نور مستقیم خورشید خودداری کرده و حتماً از ضدآفتاب با فاکتور حفاظتی بالا استفاده کنید. به تغییرات ظاهری خال‌ها و لکه‌های پوستی خود دقت کنید و هر گونه تغییر مشکوک را به پزشک گزارش دهید. از برنزه کردن با دستگاه‌های سولاریوم نیز پرهیز کنید. بهتر است برای تشخیص دقیق و درمان تخصصی، به پزشک مراجعه کنید.'
        elif 'Basel Cell Carcinoma(BCC)' in predicted_class:
            message = 'شما دچار عارضه‌ی پوستی کارسینوم سلول پایه‌ای هستید. برای مدیریت این بیماری، از قرار گرفتن در معرض نور خورشید به‌ویژه در ساعات اوج خودداری کرده و همیشه از ضدآفتاب مناسب استفاده کنید. همچنین، در صورت مشاهده هرگونه زخم، لکه، یا ناهنجاری پوستی که بهبود نمی‌یابد، به پزشک اطلاع دهید. از برنزه کردن مصنوعی و استفاده از سولاریوم نیز خودداری کنید. بهتر است برای تشخیص و درمان مناسب، به پزشک مراجعه کنید'
        elif 'Melanocytic Nevi(NV)' in predicted_class:
            message = 'شما دارای خال ملانوسیتی هستید. برای مراقبت از این خال، از قرار گرفتن طولانی‌مدت در معرض نور مستقیم خورشید خودداری کرده و همیشه از ضدآفتاب مناسب استفاده کنید. به تغییرات رنگ، شکل، یا اندازه خال خود توجه داشته باشید و در صورت مشاهده هرگونه تغییر غیرعادی، آن را به پزشک اطلاع دهید. بهتر است برای اطمینان از سلامت پوست و بررسی‌های دوره‌ای، به پزشک مراجعه کنید'
        elif 'Psoriasis pictures Lichen Planus and related diseases' in predicted_class:
            message = 'شما دچار عارضه‌ی پوستی پسوریازیس هستید. برای مدیریت این بیماری، بهتر است پوست خود را مرطوب نگه دارید و از مرطوب‌کننده‌های مناسب استفاده کنید. از تحریک‌کننده‌هایی مانند صابون‌های قوی و مواد شیمیایی اجتناب کنید و استرس را تا حد ممکن کاهش دهید، زیرا استرس می‌تواند باعث تشدید علائم شود. همچنین، پرهیز از خاراندن پوست و قرار گرفتن در معرض نور مستقیم خورشید می‌تواند مفید باشد. برای درمان و مدیریت بهتر این بیماری، توصیه می‌شود به پزشک مراجعه کنید'
        else:
            message = 'نتیجه خاصی یافت نشد.'

        context['prediction'] = {
            'class': predicted_class,
            'confidence': float(confidence),
            'message': message
        }

    return render(request, 'upload.html', context)
