from collections import namedtuple
from datetime import datetime
from flask import Flask, request, redirect, abort, make_response, Response
import json
import logging
from logging.handlers import RotatingFileHandler
from mediawiki import MediaWiki
import os
import random
import requests
from threading import Thread
from help import search_wiki_payload, random_wiki_payload, today_wiki_payload, geosearch_wiki_payload, help_wiki_payload, invalid_command_payload
from utils import SignatureVerifier


app = Flask(__name__)
wikipedia = MediaWiki()
signature_verifier = SignatureVerifier(os.environ['SLACK_SIGNING_SECRET'])


@app.before_first_request
def before_first_request():
    handler = RotatingFileHandler('wikibot.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)


def parse_query(query):
    arguments = [arg.strip() for arg in query.split('--')]
    lat, lon, count = 0.0, 0.0, 1
    for arg in arguments[1:]:
        if arg.startswith('lat'):
            _, lat = arg.split('=')
        elif arg.startswith('lon'):
            _, lon = arg.split('=')
        elif arg.startswith('count'):
            _, count = arg.split('=')
    Arguments = namedtuple('Arguments', ['lat', 'lon', 'count'])
    return Arguments(float(lat), float(lon), int(count))


def search_wiki(query):
    if query.lower() == 'help':
        return search_wiki_payload
    payload = {'attachments': []}
    page = wikipedia.page(query)
    image_url = next((x for x in page.images if x.endswith(('.jpg', '.jpeg'))), None)
    page_summary = page.summary
    page_url = page.url
    payload['attachments'].append({
        "fallback": query,
        "color": "good",
        "title": query,
        "pretext": f'🔍 Results for *{query}*',
        "title_link": page_url,
        "text": f"{page_summary}",
        "image_url": image_url,
        "footer": query,
        "ts": "",
    })
    return payload


def random_wiki(query):
    if query.lower() == 'help':
        return random_wiki_payload
    page = wikipedia.random()
    payload = search_wiki(page)
    return payload


def today_wiki(query):
    if query.lower() == 'help':
        return today_wiki_payload
    today = datetime.now().strftime('%B %d')
    page = wikipedia.page(today)
    page_url = page.url
    sections = page.sections
    events = page.section('Events').split('\n')
    random.shuffle(events)
    events = '\n'.join(events[:10])
    payload = {
        'attachments': [{
            "fallback": query,
            "color": "good",
            "title": query,
            "pretext": f'🔍 Results for *{query}*',
            "title_link": page_url,
            "text": events,
            "footer": query,
            "ts": "",
        }]
    }
    return payload


def geosearch_wiki(query):
    if query.lower() == 'help':
        return geosearch_wiki_payload
    arguments = parse_query(query)
    lat = arguments.lat
    lon = arguments.lon
    pages = wikipedia.geosearch(lat, lon)
    page = random.choice(pages)
    payload = search_wiki(page)
    return payload


def background_worker(form):
    try:
        command = form['command']
        text = form['text'].strip()
        response_url = form['response_url']
        if command == '/searchwiki':
            payload = search_wiki(text)
        elif command == '/randomwiki':
            payload = random_wiki(text)
        elif command == '/todaywiki':
            payload = today_wiki(text)
        elif command == '/geosearchwiki':
            payload = geosearch_wiki(text)
        elif command == '/helpwiki':
            payload = help_wiki_payload
        else:
            payload = invalid_command_payload
        requests.post(response_url, data=json.dumps(payload))
    except mediawiki.DisambiguationError as e:
        app.logger.error(e)
        return make_response('An Error occured while connecting to Wikipedia. Please try again after some time.', 400)


@app.route('/')
def status():
    return "Bot is running"


@app.route('/auth')
def auth():
    code = request.args.get('code')
    if not code:
        return Response(status=401)
    
    client_id = os.environ.get('CLIENT_ID')
    client_secret = os.environ.get('CLIENT_SECRET')

    if not client_id:
        return make_response('Undefined Client ID')

    if not client_secret:
        return make_response('Undefined Client Secret')
    
    oauth_url = 'https://slack.com/api/oauth.v2.access'
    data = {
        'code': code, 
        'client_id': client_id, 
        'client_secret': client_secret
    }
    response = requests.post(oauth_url, data=data)
    if response.status_code != 200:
        return Response(status=400)

    access_token = response.json()['access_token']

    # Redirect the User to their Team's Slack
    team_info_url = 'https://slack.com/api/team.info'
    response = requests.post(team_info_url, data={'token': access_token})
    if response.status_code == 200:
        team_domain = response.json()['team']['domain']
        return redirect(f'https://{team_domain}.slack.com')
    else:
        return Response(status=200)


@app.route('/', methods=['POST'])
def home():
    # Verify the Signature
    if not signature_verifier.is_valid_request(request.get_data(), request.headers):
        return make_response('Invalid Request', 403)

    if 'user_id' not in request.form or 'text' not in request.form:
        abort(400)

    # Slack requires the bot to respond back within 3 seconds
    # Spawn a thread which does the heavy work in the background
    # Send 200 Response to notify Slack
    thr = Thread(target=background_worker, args=[request.form])
    thr.start()
    return Response(status=200)

