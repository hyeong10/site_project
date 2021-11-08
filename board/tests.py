from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Board
from datetime import datetime
# Create your tests here.

class BoardAPITest(APITestCase):
    def _check_board(self, data):
        board = Board.objects.get(id=data.get("id"))

        for key in data.keys():
            if key in ["created_at", "updated_at"]:
                self.assertEqual(data.get(key),datetime.strftime(getattr(board, key),"%Y-%m-%dT%H:%M:%S.%f"))
            elif key in ["id", "comments"]:
                continue
            else:
                self.assertEqual(data.get(key), getattr(board, key))

    def create_board(self, board):
        res = self.client.post("/api/board/",data=board)
        return res

    def retrieve_board(self, board_id):
        res = self.client.get(f"/api/board/{board_id}/")
        return res
    
    def list_board(self):
        res = self.client.get("/api/board/")
        return res

    def update_board(self, board_id, data, password):
        header = {
            "HTTP_PASSWORD" : password
        }
        res = self.client.patch(f"/api/board/{board_id}/", data=data, **header)
        return res
    
    def delete_board(self, board_id, password):
        header = {
            "HTTP_PASSWORD" : password
        }
        res = self.client.delete(f"/api/board/{board_id}/", **header)
        return res

    def test_create_board(self):
        self.password = "1234"
        data = {
            "password": self.password,
            "title" : "Test1",
            "content": "Content Test"
        }
        res = self.create_board(board=data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self._check_board(res.data)
        self.board_id = res.data["id"]
        
    def test_retrieve_board(self):
        self.test_create_board()
        res = self.retrieve_board(board_id=self.board_id)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self._check_board(res.data)
    
    def test_retrieve_board_error(self):
        self.test_create_board()
        res = self.retrieve_board(board_id=self.board_id+1)
        self.assertEqual(res.status_code, 404)

    def test_list_board(self):
        self.test_create_board()
        res = self.list_board()
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_board(self):
        self.test_create_board()
        data = {
            "title": "Test2",
            "content": "Update Test"
        }
        res = self.update_board(board_id=self.board_id, data=data, password=self.password)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self._check_board(res.data)
    
    def test_update_board_error1(self):
        # Wrong id
        self.test_create_board()
        data = {
            "title": "Test2"
        }
        res = self.update_board(board_id=self.board_id+1, data=data, password=self.password)
        self.assertEqual(res.status_code, 400)
    
    def test_update_board_error2(self):
        # Wrong Password
        self.test_create_board()
        data = {
            "title": "Test2"
        }
        res = self.update_board(board_id=self.board_id, data=data, password=self.password+"WRONG")
        self.assertEqual(res.status_code, 400)
    
    def test_delete_board(self):
        self.test_create_board()
        res = self.delete_board(board_id=self.board_id, password=self.password)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Board.objects.filter(id=self.board_id).exists(), False)
    
    def test_delete_board_error1(self):
        # Wrong id
        self.test_create_board()
        res = self.delete_board(board_id=self.board_id+1, password=self.password)
        self.assertEqual(res.status_code, 400)
    
    def test_delete_board_error2(self):
        # Wrong Password
        self.test_create_board()
        res = self.delete_board(board_id=self.board_id, password=self.password+"WRONG")
        self.assertEqual(res.status_code, 400)