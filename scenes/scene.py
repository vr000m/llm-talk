from abc import abstractmethod
import threading
from PIL import Image
import os

class Scene:
	def __init__(self, **kwargs):
		# call this last in your scene subclass inits. It will
		# handle all the threading and data storage for you.
		# Your prepare and perform methods can pass data through
		# the scene_data dictionary
		
		# each subclass should use its prepare method to prep
		# an audio thread and image thread. You can join either
		# of those threads in the prepare method to block
		# starting this scene until they're ready, and/or join
		# them in the perform method before you call super().perform()
		# or just leave it alone to do one or both async 
		self.orchestrator = kwargs.get('orchestrator', None)
		self.scene_data = {}
		# everybody needs a grandma now and then
		script_dir = os.path.dirname(__file__)
		listening_path = "../grandma-listening.png"
		writing_path = "../grandma-writing.png"
		listening_path = os.path.join(script_dir, listening_path)
		writing_path = os.path.join(script_dir, writing_path)
		self.grandma_listening = Image.open(listening_path)
		self.grandma_writing = Image.open(writing_path)

		self.prepare_thread = threading.Thread(target=self.prepare)
		self.prepare_thread.start()
		
		self.image_thread = None
		self.audio_thread = None
		pass

	# Speak the sentence. Returns None
	@abstractmethod
	def prepare(self):
		pass
		
	def play_image(self):
		if self.image_thread:
			self.image_thread.join()
		if self.scene_data.get('image', None):
			print("🖼️ setting image")
			self.orchestrator.display_image(self.scene_data['image'])
		
	def play_audio(self):
		if self.audio_thread:
			self.audio_thread.join()
		if self.scene_data.get('audio', None):
			print("🖼️ playing audio")
			self.orchestrator.handle_audio(self.scene_data['audio'])

	def perform(self):
		self.prepare_thread.join()
		print("🖼️ in parent perform, past prepare join")
		img = threading.Thread(target=self.play_image)
		img.start()
		aud = threading.Thread(target=self.play_audio)
		aud.start()
		# Don't join the image thread, so we can skip
		# images that arrive too late
		# img.join()
		aud.join()



