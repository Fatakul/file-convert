import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from docx import Document
from aspose.pdf import Document as PdfDocument

# Token API dari BotFather
TOKEN = '7554220392:AAE4LH0F4WIM66r2-kgDAUGaqiT4OQON99g'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! Send me a DOCX or PDF file to convert.')

def handle_file(update: Update, context: CallbackContext) -> None:
    file = update.message.document
    file_path = file.file_name
    file_type = file.mime_type

    if file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        new_file_path = convert_docx_to_pdf(file_path)
        update.message.reply_document(document=open(new_file_path, 'rb'))
    elif file_type == 'application/pdf':
        new_file_path = convert_pdf_to_docx(file_path)
        update.message.reply_document(document=open(new_file_path, 'rb'))
    else:
        update.message.reply_text('Unsupported file type!')

def convert_docx_to_pdf(file_path: str) -> str:
    doc = Document(file_path)
    pdf_path = file_path.replace('.docx', '.pdf')
    doc.save(pdf_path)
    return pdf_path

def convert_pdf_to_docx(file_path: str) -> str:
    pdf = PdfDocument(file_path)
    docx_path = file_path.replace('.pdf', '.docx')
    pdf.save(docx_path, 'docx')
    return docx_path

def main() -> None:
    updater = Updater(7554220392:AAE4LH0F4WIM66r2-kgDAUGaqiT4OQON99g)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.document.mime_type("application/vnd.openxmlformats-officedocument.wordprocessingml.document") | Filters.document.mime_type("application/pdf"), handle_file))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
