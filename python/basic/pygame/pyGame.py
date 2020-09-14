# -*- coding:utf-8 -*-
# file: pyGame.py
#
import sys 
import pygame
import threading
import random
class Game:										# ������Ϸ��
	def __init__(self):
		pygame.init()								# pygame��ʼ��
		self.screen = pygame.display.set_mode((800,600))			# ������ʾģʽ
		pygame.display.set_caption('Python Game')				# ���ô��ڱ���
		self.image = []								# ͼƬ�б�
		self.imagerect = []							# ͼƬ��С�б�
		self.vs = pygame.image.load('image/vs.gif')				# ����ͼƬ
		self.o = pygame.image.load('image/o.gif')
		self.p = pygame.image.load('image/p.gif')
		self.u = pygame.image.load('image/u.gif')
		self.title = pygame.image.load('image/title.gif')
		self.start = pygame.image.load('image/start.gif')
		self.exit = pygame.image.load('image/exit.gif')
		for i in range(3):
			gif = pygame.image.load('image/' + str(i) + '.gif')
			self.image.append(gif)
		for i in range(3):							# ����ͼƬ��������
			image = self.image[i]
			rect = image.get_rect()
			rect.left = 200 * (i+1) + rect.left
			rect.top = 400
			self.imagerect.append(rect)
	def Start(self):								# ������Ϸ��ʼ����
		self.screen.blit(self.title, (200,100,400,140))				# ������Ϸ����
		self.screen.blit(self.start, (350,300,100,50))				# ���ƿ�ʼ��ť
		self.screen.blit(self.exit, (350, 400,100,50))				# �����˳���ť
		pygame.display.flip()							# ˢ����Ļ
		start = 1
		while start:								# ������Ϣѭ��
			for event in pygame.event.get():				# ������Ϣ
				if event.type == pygame.QUIT:
					sys.exit()
				elif event.type == pygame.MOUSEBUTTONDOWN:		# �����������Ϣ
					if self.isStart() == 0:
						start = 0
					elif self.isStart() == 1:
						sys.exit()
					else:
						pass
				else:
					pass
		self.run()								# ��ʼ��Ϸ
	def run(self):									# ��ʼ��Ϸ
		self.screen.fill((0,0,0))
		for i in range(3):							# ����ͼƬ
			self.screen.blit(self.image[i], self.imagerect[i])
		pygame.display.flip()							# ˢ����Ļ������Ϣѭ��
		while True:
			for event in pygame.event.get():				# ������Ϣ
				if event.type == pygame.QUIT:
					sys.exit()
				elif event.type == pygame.MOUSEBUTTONDOWN:		# �����������Ϣ
					self.OnMouseButDown()
				else:
					pass
	def isStart(self):								# �ж�������İ�ť
		pos = pygame.mouse.get_pos()
		if pos[0] > 350 and pos[0] < 450:
			if pos[1] > 300 and pos[1] < 350:
				return 0
			elif pos[1] > 400 and pos[1] < 450:
				return 1
			else:
				return 2
		else:
			return 2
	def OnMouseButDown(self):							# �����������Ϣ
		self.screen.blit(self.vs, (300, 150, 140, 140))				# ����ͼƬ
		pos = pygame.mouse.get_pos()						# ��ȡ���λ��
		if pos[1] > 400 and pos[1] < 540:					# �ж����λ�û�����ӦͼƬ
			if pos[0] > 200 and pos[0] < 340:
				self.screen.blit(self.image[0], 
						(150 ,150, 140,140))
				self.isWin(0)
			elif pos[0] > 400 and pos[0] < 540:
				self.screen.blit(self.image[1], 
						(150 ,150, 140,140))
				self.isWin(1)
			elif pos[0] > 600 and pos[0] < 740:
				self.screen.blit(self.image[2], 
						(150 ,150, 140,140))
				self.isWin(2)
			else:
				pass
	def isWin(self, value):								# �ж�˭Ӯ
		num = random.randint(0, 2)						# ���������
		self.screen.blit(self.image[num], 					# ������ӦͼƬ
				(450 ,150, 590,240))
		pygame.display.flip()							# ˢ����Ļ
		if num == value:							# �ж�˭Ӯ
			self.screen.blit(self.o, 
					(220, 10, 140, 70))
			pygame.display.flip()
		elif num < value:
			if num == 0:
				if value == 2:
					self.screen.blit(self.u, 
						(220, 10, 140, 70))
				else:
					self.screen.blit(self.p, 
						(220, 10, 140, 70))
				pygame.display.flip()
			else:
				self.screen.blit(self.u, 
						(220, 10, 140, 70))
				pygame.display.flip()
		else:
			if num == 2:
				if value == 1:
					self.screen.blit(self.u, 
						(220, 10, 140, 70))
				else:
					self.screen.blit(self.p, 
						(220, 10, 140, 70))
				pygame.display.flip()
			else:
				self.screen.blit(self.u, 
						(220, 10, 140, 70))
				pygame.display.flip()
game = Game()
game.Start()
