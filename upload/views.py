from __future__ import print_function
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *
from .forms import *

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required

import matplotlib.image as img
import matplotlib.pyplot as plt
from scipy.cluster.vq import whiten
from scipy.cluster.vq import kmeans
import pandas as pd
import os
import difflib
from base64 import b64encode

def index(request):
    dominant_colors = []
    if request.method == 'POST':
        amt_of_colors = request.POST.get('amt')
        img_data = request.FILES['imgfile']
        '''
        encoded = b64encode(img_data)
        encoded = encoded.decode('ascii')
        mime = "image/jpeg"
        uri = "data:%s;base64,%s" % (mime, encoded)
        
        colors = Color.objects.all()
        for color in colors:
            rgb = hex_to_rgb(color.hex_code)
            color.rgb_red = rgb[0]
            color.rgb_green = rgb[1]
            color.rgb_blue = rgb[2]
            color.save()
        '''

        read_img = img.imread(img_data)
        r = []
        g = []
        b = []
        try:
            for row in read_img:
                for temp_r, temp_g, temp_b, temp in row:
                    r.append(temp_r)
                    g.append(temp_g)
                    b.append(temp_b)
        except:
            for row in read_img:
                for temp_r, temp_g, temp_b in row:
                    r.append(temp_r)
                    g.append(temp_g)
                    b.append(temp_b)

        img_df = pd.DataFrame({'red' : r, 'green' : g, 'blue' : b})
        img_df['scaled_color_red'] = whiten(img_df['red'])
        img_df['scaled_color_green'] = whiten(img_df['green'])
        img_df['scaled_color_blue'] = whiten(img_df['blue'])
        cluster_centers, _ = kmeans(img_df[['scaled_color_red', 'scaled_color_green', 'scaled_color_blue']], int(amt_of_colors))
        red_std, green_std, blue_std = img_df[['red', 'green', 'blue']].std()

        for cluster_center in cluster_centers:
            red_scaled, green_scaled, blue_scaled = cluster_center
            rgb = get_closest_rgb(tuple(((red_scaled * red_std), (green_scaled * green_std), (blue_scaled * blue_std))))
            dominant_colors.append(
                Color.objects.get(id=rgb)
            )
        context = {'colors': Color.objects.all(), 'dominant_colors':dominant_colors}
        return render(request, 'main.html', context)
            
    context = {'colors': Color.objects.all(), 'dominant_colors':dominant_colors}
    return render(request, 'main.html', context)
    
from math import sqrt
COLORS = []
for c in Color.objects.all():
    COLORS.append(tuple((c.id, c.rgb_red, c.rgb_green, c.rgb_blue)))

def get_closest_rgb(rgb):
    r, g, b = rgb
    color_diffs = []
    for color in tuple(COLORS):
        c, cr, cg, cb = color
        color_diff = sqrt(abs(float(r) - float(cr))**2 + abs(float(g) - float(cg))**2 + abs(float(b) - float(cb))**2)
        color_diffs.append((color_diff, color))
    return min(color_diffs)[1][0]

import io, csv
@permission_required('staff_member_required')
def upload_color(request):
    template = "upload_color.html"

    prompt = {
        'order': 'DMC Code, DMC Name, R, G, B, HEX Color.'
    }

    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'This is not a csv file. Please try another file.')
    
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    errstr = ' '
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        #try:
        _, created = Color.objects.update_or_create(
            dmc_code=column[0],
            defaults={
                'dmc_name':column[1],
                'hex_code':column[3],
            }
        )    
        #except:
        #    errstr += 'error at dmc code: ' + column[0]
        context = {'error': errstr}
    return render(request, template, context)

def print_hex():
    h = input('Enter hex: ').lstrip('#')
    print('RGB =', tuple(int(h[i:i+2], 16) for i in (0, 2, 4)))