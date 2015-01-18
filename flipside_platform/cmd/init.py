'''
flipside init
'''
import os
import shutil

import yaml

from .. import config

# Set from commandline params
EXTRA_CONTEXT = {}


def _set_extra_context(ctx):
    global EXTRA_CONTEXT
    if ctx:
        EXTRA_CONTEXT.update(ctx)


def _render_to_file(template, path, context=None, force=False):
    if not force and os.path.exists(path):
        raise ValueError(
            u'File {} exists. Flipside is already inited'.format(path)
        )
    env = config.get_jinja_environment()
    content = env.get_template(template).render(context or {}).encode('utf8')
    with open(path, 'wb+') as f:
        f.write(content)


def _make_template_context(app_name, app_template):
    '''App context for rendering app template.'''
    extra = {'app_name': app_name}
    extra.update(EXTRA_CONTEXT)
    return {'app_name': app_name, 'template': app_template,
            'extra': extra}


def _write_flipfile(app_name, app_template, force=False):
    path = config.get_flipfile_path()
    base_dir = os.path.dirname(path)
    if not os.path.isdir(base_dir):
        os.makedirs(base_dir)
    ctx = _make_template_context(app_name, app_template)
    _render_to_file('app_templates/{}/flipfile.yaml'.format(app_template),
                    path, context=ctx, force=force)


def _write_saltstack(app_name, app_template, force=False):
    dst_base_dir = config.get_app_salt_path()

    ctx = _make_template_context(app_name, app_template)
    env = config.get_jinja_environment()
    src_tpl_dir = 'app_templates/{}/salt'.format(app_template)
    for tpl in env.list_templates(filter_func=lambda n: n.startswith(src_tpl_dir)):
        dst_path = os.path.join(dst_base_dir,
                                os.path.relpath(tpl, src_tpl_dir))
        dst_dir = os.path.dirname(dst_path)
        if not os.path.isdir(dst_dir):
            os.makedirs(dst_dir)
        _render_to_file(tpl, dst_path, context=ctx, force=force)


def _write_vagrantfile(force=False):
    src_path = config.get_flipside_vagrantfile()
    dst_path = config.get_app_vagrantfile()
    if not force and os.path.exists(dst_path):
        raise ValueError('Vagrantfile exists: can\'t overwrite')
    shutil.copyfile(src_path, dst_path)


def do_init(app_name, app_template, force=False, extra_context=None):
    _set_extra_context(extra_context)
    _write_flipfile(app_name, app_template, force=force)
    _write_saltstack(app_name, app_template, force=force)
    _write_vagrantfile(force=force)


def main():
    import argparse
    parser = argparse.ArgumentParser()

    # First stage parse. only to get the app_template
    parser.add_argument('app_name')
    parser.add_argument('template')
    parser.add_argument('--force', action='store_true')
    args, _ = parser.parse_known_args()

    # Second stage. Get specific extra context from the app_template
    app_meta = config.get_app_template_meta(args.template)
    extra_context = app_meta.get('extra_context', {})
    if extra_context:
        if not isinstance(extra_context, dict):
            parser.error('bad extra_context in app template meta')
        for key, val in extra_context.items():
            parser.add_argument('--{}'.format(key), help=val,
                                required=True)
        more_args = parser.parse_args()
        extra_context = {k: getattr(more_args, k)
                         for k, v in extra_context.items()}
    do_init(args.app_name, args.template, force=args.force,
            extra_context=extra_context)

if __name__ == '__main__':
    main()
