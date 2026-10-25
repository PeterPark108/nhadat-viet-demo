#!/usr/bin/env python3
"""Sinh toàn bộ site tĩnh NhàĐất Việt. Chạy: python3 tools/build.py  (từ thư mục gốc repo)"""
import os, sys, json, html, math, shutil
sys.path.insert(0, os.path.dirname(__file__))
from data import *
from parts import *
OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
import core; core.OUT = OUT

if __name__ == '__main__':
    for d in ['tin','du-an','tin-tuc','wiki','phan-tich','moi-gioi','doanh-nghiep']: shutil.rmtree(os.path.join(OUT,d), ignore_errors=True)
    for f in os.listdir(OUT):
        if f.endswith('.html'): os.remove(os.path.join(OUT,f))
    made = listing_pages(); detail_pages(); project_pages(); news_pages(); wiki_pages(); analytics_pages(); directory_pages(); misc_pages(); home()
    data_js(made); sitemap()
    print('pages:', len(PAGES))
