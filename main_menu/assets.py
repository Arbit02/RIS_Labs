from flask_assets import Bundle, Environment
import glob

assets_env = Environment()
css_files = [
    'query_bp/static/css/index.css',
    'static/css/index.css',
    'auth_bp/static/css/index.css',
]

css_bundle = Bundle(*css_files, filters='cssmin', output='gen/packed.css')
assets_env.register('css_all', css_bundle)
