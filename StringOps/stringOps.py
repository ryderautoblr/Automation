import pyperclip

def copyStrToClipboard(text):
	pyperclip.copy(text)

def pasteStrFromClipboard(text):
	return pyperclip.paste()