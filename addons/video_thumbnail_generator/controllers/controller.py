from odoo import http
from odoo.http import request, Response
import base64

class VideoThumbnailController(http.Controller):

    @http.route('/api/upload_video', type='http', auth='public', methods=['POST'], csrf=False)
    def upload_video(self, **kwargs):
        video_file = kwargs.get('video_file')
        video_file_name = kwargs.get('video_file_name')

        # Validate input
        if not video_file or not video_file_name:
            return {'status': 'error', 'message': 'Missing video file or name'}

        # Create a new channel video record
        record = request.env['channel.video'].create({
            'name': video_file_name,
            'video_file': base64.b64encode(video_file.read()).decode('utf-8'),
            'video_file_name': video_file_name,
        })

        # Generate video properties
        record.action_generate_video_properties()

        return "Success"