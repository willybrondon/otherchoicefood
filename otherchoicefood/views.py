from django.http import HttpResponse
from django.shortcuts import render
from vendor.models import Vendor
from django.db.models import Q
from django.contrib.gis.geos import GEOSGeometry
#from django.contrib.gis.mesure import D # D is the shortcut of distance
#from django.contrib.gis.db.models.function import Distance


def get_or_set_current_location(request):
    if 'lat' in request.session: 
        lat = request.session['lat']
        lng = request.session['lng']
        return lng, lat
    elif 'lat' in request.GET:
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')
        request.session['lat'] = lat
        request.session['lng'] = lng
        return lng, lat
    else : 
        return None

def home(request):
    if  get_or_set_current_location(request) is not  None: 
        # lat = request.GET.get('lat')
        # lng = request.GET.get('lat')
        pnt = GEOSGeometry('POINT(% %)' % (get_or_set_current_location(request)))
        vendors = Vendor.objects.filter(user_profile__distance_Ite=(pnt, D(km=1000))).annotate(distance=Distance('user_profile__location', pnt)).order_by('distance')
    
        for v in vendors :
            v.kms = round(v.distance.km)
    else:
        vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]
    
    context = {
        'vendors' : vendors,
    }
    return render(request, 'home.html', context)