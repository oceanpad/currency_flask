# -*- coding: utf-8 -*-
import pytest
from currency import currency

@pytest.fixture
def client():
  currency.app.config['TESTING'] = True
  client = currency.app.test_client()
  return client

def test_urls(client):
  r = client.get('/')
  assert r.status_code == 200

def test_currency(client):
  r = client.get('/currency')
  assert r.status_code == 200
