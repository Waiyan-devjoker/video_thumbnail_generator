{
    'name': 'Video Thumbnail Generator',
    'version': '16.0.1.0.0',
    'summary': 'Video Thumbnail Generator',
    'description': 'Video Thumbnail Generator',
    'category': 'Extra Tools',
    'author': 'WaiYan-DEVJ@K3R, FourLeafHouse',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'view/channel_video_view.xml'
    ],
    'external_dependencies': {'python': ['opencv-python']},
    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False
}
