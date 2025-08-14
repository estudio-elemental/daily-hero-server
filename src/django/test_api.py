#!/usr/bin/env python3
"""
Script de teste simples para a API Daily Hero
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_register():
    """Testa o endpoint de registro"""
    url = f"{BASE_URL}/api/auth/register/"
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "password2": "testpass123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Registro: {response.status_code}")
        if response.status_code == 201:
            print("✅ Usuário registrado com sucesso!")
            return response.json()
        else:
            print(f"❌ Erro: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return None

def test_login(username, password):
    """Testa o endpoint de login"""
    url = f"{BASE_URL}/api/auth/login/"
    data = {
        "username": username,
        "password": password
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Login: {response.status_code}")
        if response.status_code == 200:
            print("✅ Login realizado com sucesso!")
            return response.json()
        else:
            print(f"❌ Erro: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return None

def test_profile(access_token):
    """Testa o endpoint de perfil"""
    url = f"{BASE_URL}/api/auth/profile/"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Perfil: {response.status_code}")
        if response.status_code == 200:
            print("✅ Perfil obtido com sucesso!")
            return response.json()
        else:
            print(f"❌ Erro: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
            return None

def test_logout(access_token, refresh_token):
    """Testa o endpoint de logout"""
    url = f"{BASE_URL}/api/auth/logout/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "refresh": refresh_token
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"Logout: {response.status_code}")
        if response.status_code == 200:
            print("✅ Logout realizado com sucesso!")
            return True
        else:
            print(f"❌ Erro: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("🚀 Iniciando testes da API Daily Hero...\n")
    
    # Teste 1: Registro
    print("1️⃣ Testando registro...")
    user_data = test_register()
    if not user_data:
        print("❌ Falha no registro. Abortando testes.")
        return
    
    # Teste 2: Login
    print("\n2️⃣ Testando login...")
    login_data = test_login("testuser", "testpass123")
    if not login_data:
        print("❌ Falha no login. Abortando testes.")
        return
    
    access_token = login_data.get('access')
    refresh_token = login_data.get('refresh')
    
    # Teste 3: Perfil
    print("\n3️⃣ Testando perfil...")
    profile_data = test_profile(access_token)
    if not profile_data:
        print("❌ Falha ao obter perfil.")
    
    # Teste 4: Logout
    print("\n4️⃣ Testando logout...")
    logout_success = test_logout(access_token, refresh_token)
    if not logout_success:
        print("❌ Falha no logout.")
    
    print("\n🎉 Testes concluídos!")

if __name__ == "__main__":
    main()
