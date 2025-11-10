import requests
from typing import Optional, Dict, Any

API_URL = 'http://localhost:8000/api'

class APIClient:
    def __init__(self):
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
    
    def _get_headers(self) -> Dict[str, str]:
        headers = {'Content-Type': 'application/json'}
        if self.access_token:
            headers['Authorization'] = f'Bearer {self.access_token}'
        return headers
    
    def register(self, username: str, email: str, password: str) -> Dict[str, Any]:
        response = requests.post(
            f'{API_URL}/auth/register/',
            json={'username': username, 'email': email, 'password': password}
        )
        response.raise_for_status()
        return response.json()
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        response = requests.post(
            f'{API_URL}/auth/login/',
            json={'username': username, 'password': password}
        )
        response.raise_for_status()
        data = response.json()
        self.access_token = data['access']
        self.refresh_token = data['refresh']
        return data
    
    def get_datasets(self):
        response = requests.get(f'{API_URL}/datasets/', headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    def get_dataset(self, dataset_id: int):
        response = requests.get(f'{API_URL}/datasets/{dataset_id}/', headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    def get_summary(self, dataset_id: int):
        response = requests.get(f'{API_URL}/datasets/{dataset_id}/summary/', headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    def upload_dataset(self, file_path: str):
        with open(file_path, 'rb') as f:
            files = {'file': f}
            headers = {}
            if self.access_token:
                headers['Authorization'] = f'Bearer {self.access_token}'
            response = requests.post(f'{API_URL}/datasets/upload/', files=files, headers=headers)
            response.raise_for_status()
            return response.json()
    
    def download_pdf(self, dataset_id: int, save_path: str):
        response = requests.get(
            f'{API_URL}/datasets/{dataset_id}/download_pdf/',
            headers=self._get_headers(),
            stream=True
        )
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    
    def delete_dataset(self, dataset_id: int):
        response = requests.delete(f'{API_URL}/datasets/{dataset_id}/', headers=self._get_headers())
        response.raise_for_status()
