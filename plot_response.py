#!/usr/bin/env python

import os,sys
import numpy as np
from dipy.viz import actor, window, ui
from dipy.data import get_sphere
from dipy.reconst.csdeconv import AxSymShResponse
from xvfbwrapper import Xvfb
import json

def plot_response(response_src, out_png=False):

    # start virtual display
    print("starting Xvfb");
    vdisplay = Xvfb()
    vdisplay.start()

    response_src = np.loadtxt(src_txt)
    response_src = response_src[1]
    sphere = get_sphere('symmetric724')
    sh_resp = AxSymShResponse(0, response_src)
    sig_resp = sh_resp.on_sphere(sphere)
    sig_resp = sig_resp[None, None, None, :]

    ren = window.Renderer()
    #sphere_actor = actor.sphere(sig_resp, sphere)
    sphere_actor = actor.odf_slicer(sig_resp, sphere=sphere,colormap='blues')
    ren.add(sphere_actor)
    my_camera = ren.camera()
    my_camera.SetPosition(1.62, -9.19, 4.01)
    my_camera.SetFocalPoint(0.01, -0.46, -0.19)
    my_camera.SetViewUp(0.24, 0.46, 0.86)

    if out_png != False:
        window.record(ren, out_path=out_png, magnification=10, size=(60, 60))
    else:
        window.show(ren, reset_camera=False)
        print('Camera Settings')
        print('Position: ', '(%.2f, %.2f, %.2f)' % my_camera.GetPosition())
        print('Focal Point: ', '(%.2f, %.2f, %.2f)' % my_camera.GetFocalPoint())
        print('View Up: ', '(%.2f, %.2f, %.2f)' % my_camera.GetViewUp())

    vdisplay.stop()

# set paths
if not os.path.exists("images"):
    os.mkdir("images")

# read json file
with open('config.json') as config_json:
    config = json.load(config_json)

# set variables
src_txt = config['response']
out_png = "images/response.png"

# create png image
plot_response(src_txt,out_png)

