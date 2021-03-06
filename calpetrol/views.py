from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
#from .forms import UserRegistrationForm
from django import forms
from .models import *
from django.contrib.auth.models import User
k_source = ''
k_destination = ''
k_car_type = ''
k_cost_petrol = ''
k_cost = ''
#save variable
save_source = ''
save_destination = ''
save_car_type = ''
save_cost_petrol = ''
save_cost = ''
def home_page(request):
    global save_source
    global save_destination
    global save_car_type
    global save_cost_petrol
    global save_cost
    save_source = ''
    save_destination = ''
    save_car_type = ''
    save_cost_petrol = ''
    save_cost = ''
    return render(request,"calpetrol/home1.html")

def calculate(request):
    username = 'User'
    if request.user.is_authenticated():
        username = request.user.username
    # declare initial variables.
    get_source = ''
    get_destination = ''
    get_car_type = ''
    get_cost_petrol = ''
    d_selected = ''
    cost = ''
    use =''
    
    province = ['ชัยภูมิ','เลย','หนองบัวลำภู','หนองคาย']#,'อุดรธานี'],'ขอนแก่น','มหาสารคาม','ร้อยเอ็ด','กาฬสินธุ์','สกลนคร','นครพนม','มุกดาหาร','อำนาจเจริญ','ยโสธร','อุบลราชธานี','ศรีสะเกษ','สุรินทร์','บุรีรัมย์','นครราชสีมา','สระบุรี','แม่ฮ่องสอน','เชียงใหม่','ลำพูน','เชียงราย','พะเยา','น่าน','แพร่','ลำปาง','ตาก','กำแพงเพชร','สุโขทัย','อุตรดิตถ์','พิษณุโลก','พิจิตร','นครสวรรค์','เพชรบูรณ์','กรุงเทพฯ','นนทบุรี','ปทุมธานี','อยุธยา','อ่างทอง','สิงห์บุรี','ชัยนาท','อุทัยธานี','สุพรรณบุรี','นครสวรรค์','สระบุรี','ลพบุรี','นครนายก','ปราจีนบุรี','สระแก้ว','สมุทรปราการ','ฉะเชิงเทรา','ชลบุรี','ระยอง','จันทบุรี','ตราด','นครปฐม','กาญจนบุรี','ราชบุรี','สมุทรสาคร','สมุทรสงคราม','เพชรบุรี','ประจวบคีรีขันธ์','ชุมพร','ระนอง','สุราษฎร์ธานี','พังงา','ภูเก็ต','กระบี่','ตรัง','นครศรีธรรมราช','พัทลุง','สงขลา','ปัตตานี','ยะลา','นราธิวาส','สตูล']
    if 'cal_btn' in request.POST:
        # get input data from web app. 
        get_source = request.POST.get("source","")
        get_destination = request.POST.get("destination","")
        get_car_type = request.POST.get("car_type","")
        get_cost_petrol = request.POST.get("cost_petrol","")
        # query input data into database. 
        # by first use filter() because this query get many data. 
        d_selected = Distance.objects.values_list('distance', flat=True).filter(source_text=get_source)
        # but second has only one data ,so use get()==>get use with only one data.
        d_selected = d_selected.get(destination_text=get_destination)
        use = Car.objects.values_list('car_use', flat=True).get(car_type=get_car_type)
        cost = round((d_selected * float(get_cost_petrol))/use,2)
        k_source = get_source
        k_destination = get_destination
        k_car_type = get_car_type
        k_cost_petrol = get_cost_petrol
        k_cost = cost
        
    elif 'save_btn' in request.POST:
        global k_source
        global k_destination
        global k_car_type
        global k_cost_petrol
        global k_cost
        if k_source != '' :
             get_username = request.user.username
             username = User.objects.get(username=get_username)
             car = Car.objects.get(car_type=k_car_type)
             source_destination  = Distance.objects.get(destination_text=k_destination,source_text=k_source)

             keep_user_data = User_data.objects.create(user=username,source_destination=source_destination,car=car,petrol_cost=k_cost_petrol,cost= k_cost)
             keep_user_data.save()
	
    elif 'memo_btn' in request.POST:
        global k_source
        global save_source
        save_source = k_source
        global k_destination
        global save_destination
        save_destination = k_destination
        global k_car_type
        global save_car_type
        save_car_type = k_car_type
        global k_cost_petrol
        global save_cost_petrol
        save_cost_petrol = k_cost_petrol
        global k_cost
        global save_cost
        save_cost = k_cost

        #reset value in keep variables.
        k_source = ''
        k_destination = ''
        k_car_type = ''
        k_cost_petrol = ''
        k_cost = ''
    
    return render(request,"calpetrol/index.html",{'pro':province,'obj':Car.objects.all(),'get_source':get_source,'get_destination':get_destination,'get_car_type':get_car_type,
'get_cost_petrol':get_cost_petrol,'cost':cost,'save_source':save_source,'save_destination':save_destination,'save_car_type':save_car_type,
'save_cost_petrol':save_cost_petrol,'save_cost':save_cost,'username':username})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return render(request,"calpetrol/home1.html")
    else:
        form = UserCreationForm()
    return render(request, 'calpetrol/signup.html', {'form': form})

def userdata(request):
    username = request.user.username
    latest_data = User_data.objects.filter(user=request.user)
    #.order_by('-date')[:5]
    
    return render(request, 'calpetrol/userdata.html',{'username': username,'d':latest_data})


