import sys, tempfile, os, datetime
from subprocess import call

from cryptography.fernet import Fernet
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown

from src.redditor import Redditor


class Notebook:

	def __init__(self):

		self.EDITOR = os.environ.get('EDITOR', 'nano')
		self.encrypt_key = os.environ.get('NOTE_KEY', None)
		self.today = datetime.datetime.today().strftime("%Y-%m-%d")
		self.reddit_bot = Redditor()
		self.encoding = 'utf-8'
		self.rich_console = Console()


	def create_note(self, title='Untitled', tags='None'):
		with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
			call([self.EDITOR, tf.name])

			save_flag = input('Do you want to save the note? (y/n): ')
			if not save_flag:
				save_flag = 'y'

			if save_flag == 'y':
				tf.seek(0)
				edited_message = tf.read()

				# handle encryption and string conversion of note
				encrypted_message = self._encrypt_text(edited_message)
				string_message = encrypted_message.decode(self.encoding)

				# handle encryption and string conversion of title
				string_tags = ";".join(tags)
				front_matter = f'{title} | {self.today} | {string_tags}'

				encrypted_front_matter = self._encrypt_text(bytes(front_matter, self.encoding))
				string_front_matter = encrypted_front_matter.decode(self.encoding)
				
				self.reddit_bot.post_submission(string_front_matter, string_message)

		return 200


	def list_notes(self):
		notes_metadata = self.reddit_bot.list_submissions()
		table = Table(show_header=True, header_style="bold royal_blue1")
		table.add_column('Date', style="dim")
		table.add_column('Title')
		table.add_column('Tags')
		table.add_column('ID')

		for note in notes_metadata:
			byte_front_matter = self._decrypt_text(bytes(note['title'], self.encoding))
			string_front_matter = byte_front_matter.decode(self.encoding)

			title, date, tags = string_front_matter.split(' | ')
			note_link = note['url']
			note_id = note['id']

			hyperlinked_note_id = f'[link={note_link}]{note_id}[/link]'

			table.add_row(date, title, tags, hyperlinked_note_id)


		self.rich_console.print(table)

		return 200


	def get_note(self, id):
		encrypted_note_text = self.reddit_bot.read_submission(id)
		decrypted_note_text = self._decrypt_text(bytes(encrypted_note_text, self.encoding))

		note_text = decrypted_note_text.decode(self.encoding)
		markdown_converted = Markdown(note_text)

		self.rich_console.print(markdown_converted)


		return 200


	def _encrypt_text(self, plain_text):
		cipher_suite = Fernet(self.encrypt_key)
		cipher_text = cipher_suite.encrypt(plain_text)

		return cipher_text


	def _decrypt_text(self, cipher_text):
		cipher_suite = Fernet(self.encrypt_key)
		plain_text = cipher_suite.decrypt(cipher_text)

		return plain_text


	def _make_encrypt_key(self):
		key = Fernet.generate_key()
		print(key)

		return key
