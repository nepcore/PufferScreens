#!/usr/bin/python

import argparse
from getpass import getpass
import os
import time
import shutil
import sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

parser = argparse.ArgumentParser()
parser.add_argument('-U', '--url',      help = 'The instances base URL (default: http://localhost:8080/)', default = 'http://localhost:8080/')
parser.add_argument('-e', '--email',    help = 'The email to log in with', required = True)
parser.add_argument('-s', '--server',   help = 'The server to take screenshots of', nargs = '?')
parser.add_argument('-n', '--node',     help = 'The node to take screenshots of', nargs = '?')
parser.add_argument('-u', '--user',     help = 'The user to take screenshots of', nargs = '?')
parser.add_argument('-t', '--template', help = 'The template to take screenshots of', nargs = '?')
parser.add_argument('-o', '--output',   help = 'Where to store the generated screenshots (default: out)', default = 'out')
parser.add_argument('-H', '--head',     help = 'Run in headful mode and render browser windows', action = 'store_true')
parser.add_argument('-d', '--delay',    help = 'The time to wait after page load to take a screenshot in seconds (default: 0.75)', default = 0.75, type = float)
parser.add_argument('-x', '--width',    help = 'The width of the browser window (default: 1920)', default = 1920, type = int)
parser.add_argument('-y', '--height',   help = 'The height of the browser window (default: 1080)', default = 1080, type = int)
args = parser.parse_args()

url = args.url
email = args.email
server_id = args.server
node_id = args.node
user_id = args.user
template_id = args.template
out_dir = args.output
password = getpass()

def prepareOutDir(base):
  for theme in ['light', 'dark']:
    # clean up existing screenshots
    if os.path.exists(f'{base}/{theme}'):
      shutil.rmtree(f'{base}/{theme}')

    # servers
    os.makedirs(f'{base}/{theme}/servers')
    os.makedirs(f'{base}/{theme}/servers/create')
    if server_id is not None:
      os.makedirs(f'{base}/{theme}/servers/view')

    # nodes
    os.makedirs(f'{base}/{theme}/nodes')
    if node_id is not None:
      os.makedirs(f'{base}/{theme}/nodes/deploy')

    # users
    os.makedirs(f'{base}/{theme}/users')

    # templates
    os.makedirs(f'{base}/{theme}/templates')
    os.makedirs(f'{base}/{theme}/templates/create')
    if template_id is not None:
      os.makedirs(f'{base}/{theme}/templates/view')

def makeFirefox(mode):
  options = Options()
  options.headless = not args.head
  options.set_preference("layout.css.prefers-color-scheme.content-override", 0 if mode == "dark" else 1)
  return webdriver.Firefox(options = options)

def screen(browser, path, file):
  browser.get(url + path)
  if '#' in path:
    # reload to force ui update
    browser.refresh()
  time.sleep(args.delay)
  browser.save_screenshot(file)

def scrape(mode, out):
  print(f'Taking screenshots of {mode} mode')
  browser = makeFirefox(mode)
  browser.set_window_size(args.width, args.height)

  # unauthed
  print('Unauthed screens')
  screen(browser, 'auth/register', f'{out}/{mode}/register.png')
  screen(browser, 'auth/login', f'{out}/{mode}/login.png')

  for elem in browser.find_elements(By.TAG_NAME, 'input'):
    if elem.get_attribute('type') == 'email':
      elem.send_keys(email)
    if elem.get_attribute('type') == 'password':
      elem.send_keys(password)

  # servers
  print('Server screens')
  browser.find_element(By.TAG_NAME, 'button').click()
  time.sleep(args.delay)
  browser.save_screenshot(f'out/{mode}/servers/list.png')

  screen(browser, 'servers/new', f'{out}/{mode}/servers/create/templates.png')

  browser.find_elements(By.CLASS_NAME, 'template')[0].click()
  browser.save_screenshot(f'{out}/{mode}/servers/create/confirm-template.png')

  for elem in browser.find_elements(By.TAG_NAME, 'button'):
    if elem.text == 'Use this template':
      elem.click()
      browser.save_screenshot(f'{out}/{mode}/servers/create/env.png')
      break

  for elem in browser.find_elements(By.TAG_NAME, 'input'):
    if elem.get_attribute('placeholder') == 'Server Name':
      elem.send_keys('My Server')
      break

  for elem in browser.find_elements(By.TAG_NAME, 'button'):
    if elem.text == 'Next':
      elem.click()
      browser.save_screenshot(f'{out}/{mode}/servers/create/users.png')
      break

  for elem in browser.find_elements(By.TAG_NAME, 'button'):
    if elem.text == 'Next':
      elem.click()
      browser.save_screenshot(f'{out}/{mode}/servers/create/settings.png')
      break

  if server_id is not None:
    for tab in ['console', 'stats', 'files', 'settings', 'users', 'sftp', 'api', 'admin']:
      screen(browser, f'servers/view/{server_id}#{tab}', f'{out}/{mode}/servers/view/{tab}.png')

  # nodes
  print('Node screens')
  screen(browser, 'nodes', f'{out}/{mode}/nodes/list.png')
  screen(browser, 'nodes/new', f'{out}/{mode}/nodes/create.png')
  if node_id is not None:
    screen(browser, f'nodes/view/{node_id}?created=true', f'{out}/{mode}/nodes/deploy/1.png')

    for i in [2, 3, 4, 5]:
      for elem in browser.find_elements(By.TAG_NAME, 'button'):
        if elem.text == 'Next':
          elem.click()
          browser.save_screenshot(f'out/{mode}/nodes/deploy/{i}.png')
          break

    screen(browser, f'nodes/view/{node_id}', f'{out}/{mode}/nodes/view.png')

  # users
  print('User screens')
  screen(browser, 'users', f'{out}/{mode}/users/list.png')
  screen(browser, 'users/new', f'{out}/{mode}/users/create.png')
  if user_id is not None:
    screen(browser, f'users/view/{user_id}', f'{out}/{mode}/users/view.png')

  # templates
  print('Template screens')
  screen(browser, 'templates', f'{out}/{mode}/templates/list.png')

  for tab in ['general', 'variables', 'install', 'run', 'hooks', 'environment', 'json']:
    screen(browser, f'templates/new#{tab}', f'{out}/{mode}/templates/create/{tab}.png')

  if template_id is not None:
    for tab in ['general', 'variables', 'install', 'run', 'hooks', 'environment', 'json']:
      screen(browser, f'templates/view/local/{template_id}#{tab}', f'{out}/{mode}/templates/view/{tab}.png')

  # settings
  print('Settings screens')
  screen(browser, 'settings', f'{out}/{mode}/settings.png')

  browser.quit()
  print(f'Done with {mode} mode')

prepareOutDir(out_dir)
scrape('light', out_dir)
scrape('dark', out_dir)
