from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import F
from django.template import loader
from .models import Voucher

def get_context(message='', error_message=''):
    available_vouchers= Voucher.objects.filter(usage_number__lt=F('max_usage'))
    context={
        'available_vouchers': available_vouchers,
        'message': message,
        'error_message': error_message,
    }

    return context
    
def success(request, voucher_code):
    print(voucher_code)
    code= get_object_or_404(Voucher, voucher_code= voucher_code)
    context= get_context(f'congratulation you got {code.discount_value}{code.discount_type} off on your purchase')
    return render(request, 'home/index.html', context)

def error(request):
    context= get_context('',"this voucher exceed the allowed usage number!")
    return render(request, 'home/index.html', context)

def index(request):
    template = loader.get_template('home/index.html')
    
    return render(request, 'home/index.html', get_context())

def consume(request):
    voucher_code= request.POST['voucher_code']
    
    code= get_object_or_404(Voucher, voucher_code= voucher_code)

    if (code.usage_number >=code.max_usage ):
        return redirect('/error')

    code.usage_number+=1
    code.save()

    return redirect(f'/success/{code.voucher_code}')

# Create your views here.
