from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import F
from django.template import loader
from django.http import Http404
from .models import Voucher



def _get_context(message='', error_message='', inline_error_message=''):
    """return default context"""
    available_vouchers= Voucher.objects.filter(usage_number__lt=F('max_usage'))
    context={
        'available_vouchers': available_vouchers,
        'message': message,
        'error_message': error_message,
        'inline_error_message': inline_error_message
    }

    return context

def index(request):
    template = loader.get_template('home/index.html')
    return render(request, 'home/index.html', _get_context())

def success(request, voucher_code):
    """success page if everything is fine, redirect here to avoid send request on refresh"""
    print(voucher_code)
    code= get_object_or_404(Voucher, voucher_code= voucher_code)
    context= _get_context(message=f'congratulation you got {code.discount_value}{code.discount_type} off on your purchase')
    return render(request, 'home/index.html', context)

def error(request, error_code):
    """error page if voucher is exceed the number of usage, redirect here to avoid send request on refresh"""
    errors={
        1:{'error':'this voucher exceed the allowed usage number!', 'type':'inline'},
        2:{'error':'this voucher is invalid!', 'type':'block'}
    }
    print(error_code)
    context=None
    errorInfo=errors.get(error_code, None)
    print(errorInfo)
    if (errorInfo==None):
        raise Http404()
    
    if errorInfo['type']=='inline':
        context= _get_context(inline_error_message=errorInfo['error'])
    else:
        context= _get_context(error_message=errorInfo['error'])
    
    return render(request, 'home/index.html', context)


def consume(request):
    voucher_code= request.POST['voucher_code']
    code=None
    try:
        code=Voucher.objects.get(voucher_code= voucher_code)
    except:
        return redirect('error/2')

    if (code.usage_number >=code.max_usage ):
        return redirect('/error/1')

    code.usage_number+=1
    code.save()

    return redirect(f'/success/{code.voucher_code}')

# Create your views here.
