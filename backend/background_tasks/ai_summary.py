from tasks import celery
from helpers.ai import summarize_audio, summarize_docx, summarize_pdf, summarize_text
import os
import mimetypes
from repos.summaries import update_summary, get_summary
from constants.summary import StatusEnum
import traceback
from helpers.db import model_to_dict


SUPPORTED_AUDIO_MIME_TYPES = {
    'audio/mpeg',
    'audio/mp4',
    'audio/x-m4a',
    'video/mp4',
    'audio/wav',
    'audio/x-wav',
    'audio/webm',
    'video/webm',
    'audio/mpeg',
}


@celery.task
def generate_ai_summary(summary_id, temp_path, text_to_summarize=None):
    try:
        mime_type, encoding = mimetypes.guess_type(temp_path)
        if mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            summary_result = summarize_docx(temp_path)
        elif mime_type == 'application/pdf':
            summary_result = summarize_pdf(temp_path)
        elif mime_type in SUPPORTED_AUDIO_MIME_TYPES:
            summary_result = summarize_audio(temp_path)
        elif text_to_summarize:
            summary_result = summarize_text(text_to_summarize)

        summary = get_summary(summary_id)
        new_args = {
            'user_id': summary.user_id,
            'file_path': summary.file_path,
            'text_to_summarize': summary.text_to_summarize,
            'summary_id': summary_id,
            'summary_result': summary_result,
            'status': StatusEnum.COMPLETE.value,

        }
        update_summary(**new_args)
        os.remove(temp_path)
    except:
        traceback.print_exc()
        summary = get_summary(summary_id)
        new_args = {
            'user_id': summary.user_id,
            'file_path': summary.file_path,
            'text_to_summarize': summary.text_to_summarize,
            'summary_id': summary_id,
            'status': StatusEnum.ERROR.value,
        }
        update_summary(**new_args)
